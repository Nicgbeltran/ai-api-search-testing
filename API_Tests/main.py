import requests
import json
import csv
import os # Import the os module
from dotenv import load_dotenv # Import load_dotenv
from perplexity_pro import perplexity_pro_high, perplexity_pro_medium, perplexity_pro_low
# Import the reasoning functions as well
from perplexity_reasoning_pro import perplexity_reasoning_pro_high, perplexity_reasoning_pro_medium, perplexity_reasoning_pro_low
# Import the new OpenAI function
from gpt4_1 import openai_gpt4_1m_search, openai_gpt4_1h_search
from gpt4_1_mini_h import openai_gpt4_1_mini_h_search
# Import the new Gemini function
from gemini_2_0_flash import gemini_2_0_flash_search
# Import the new Exa function
from exa_answer import exa_answer_search

# Import Notion functions
from API_Tests.notion_api import create_notion_page

# --- Function Definitions ---

def load_company_data(csv_file_path: str) -> list[dict]:
    """Loads company data from a CSV file."""
    company_data = []
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company_data.append(row)
        if not company_data:
            print("No data found in the CSV file.")
            exit()
        return company_data
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
        exit()
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        exit()

def select_companies_to_process(company_data: list[dict]) -> list[dict]:
    """Asks the user for a range of companies to process and returns the selected slice."""
    total_companies = len(company_data)
    while True:
        try:
            start_index_input = input(f"Enter the starting row number to process (1-{total_companies}): ")
            start_index = int(start_index_input) - 1 # Convert to 0-based index
            end_index_input = input(f"Enter the ending row number to process ({start_index + 1}-{total_companies}): ")
            end_index = int(end_index_input) # Keep as 1-based for slicing upper bound

            if 0 <= start_index < end_index <= total_companies:
                print(f"Processing companies from row {start_index + 1} to {end_index}.")
                return company_data[start_index:end_index]
            else:
                print(f"Invalid range. Please enter a start row between 1 and {total_companies}, and an end row between {start_index + 1} and {total_companies}.")
        except ValueError:
            print("Invalid input. Please enter numbers for the start and end rows.")

def select_prompt_set(available_sets: dict) -> tuple[str, str, str]:
    """Asks the user to choose a prompt set and returns its name, system prompt, and user prompt template."""
    print("\nAvailable prompt sets:")
    prompt_names = list(available_sets.keys())
    for i, name in enumerate(prompt_names):
        print(f"{i + 1}. {name}")

    while True:
        try:
            choice = int(input(f"Choose a prompt set (1-{len(prompt_names)}): "))
            if 1 <= choice <= len(prompt_names):
                selected_name = prompt_names[choice - 1]
                selected_set = available_sets[selected_name]
                print(f"Using prompt set: {selected_name}")
                return selected_name, selected_set["system"], selected_set["user"]
            else:
                print(f"Please enter a number between 1 and {len(prompt_names)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# --- Configuration ---

# Create a dictionary to hold the available prompt sets for selection
available_prompt_sets = {
    "Business Offer": {
        "system": "Be precise and concise.Your response will only answer these three points: 1. Their core offering 2.What do they do? 3. Who are their customers? Write at most two sentences for each point. Do not delve into too much detail on specific customers or specific products they offer. Your job is to give a great overview.",
        "user": "A company named {company_name} has a location at: {company_address} In Alberta, Canada. Answer these three points about the company. **1.What is their core offering?** meaning, what does this company offer to customers? **2.What do they do?** they manufacture,distribute,have their own retail or leverage other stores,etc? **3.Who are their customers?** Are they B2B or B2C and what channels do they use to deliver to customers. Examples include: a retail store, online,services,wholesaling,etc?",
    },
    "Total Locations": {
            "system": "Be precise and consise. Format your answer like this for each location: (location address)(function: Such as: HQ, Retail store, warehouse,etc). If the company has more than 5 locations, return this format for only all of the ones in Alberta and the HQ. Then name the rest of the locations in a list. Make sure you tell me all the locations they operate in around the world. Client projects do not count as locations.",
            "user": "The company {company_name} has a location at {company_address} in Alberta, Canada. What is the total number of locations this company has. Are they owned by another company? if so, what is the total location count including the parent company? How is each location used by the company? for example, some are offices, warehouses, retail, hq,etc"
    },
    "Just Revenue": {
        "system":"Follow the format instructions from the user prompt.",
        "user": "For {company_name} with a location at: {company_address} what is their most recent revenue numbers? Is this company owned by another business? If so, use the revenue numbers of the highest-level parent company. When searching for your selection, use sites like: Zoominfo, apollo,datanalyse,official reports, news about the company. Choose the number and source you believe to be the most accurate. Then: ONLY ANSWER IN THIS FORMAT Revenue: - (revenue(if not found, say: revenue not found)) DO NOT ADD ANY OTHER TEXT TO YOUR ANSWER TO THE USER"
    },
    "Years in business": {
        "system":"Follow the format instructions given in the user prompt.",
        "user": "For {company_name} with a location at: {company_address} what is the founding year and location? Is this company owned by another business? If so, use the founding year and location of the highest-level parent company. ONLY ANSWER IN THIS FORMAT (founding year/date) - (City of founding)  - (founder name(if present)if not then say(founder name not found)) DO NOT ADD ANY OTHER TEXT TO YOUR ANSWER TO THE USER"
    },
    # --- New prompt set ---
    "employee count": {
        "system":"Follow the format instructions from the user prompt.",
        "user": "For {company_name} with a location at: {company_address} what is their most accurate current employee count? Is this company owned by another business? If so, use the employee count of the highest-level parent company. When searching for your selection, use sites like: Zoominfo, apollo,datanalyse,official reports, news about the company. Choose the employee count and source you believe to be the most accurate. Then: ONLY ANSWER IN THIS FORMAT Employee count: - (employee count(if unknown, say: not found)) DO NOT ADD ANY OTHER TEXT TO YOUR ANSWER TO THE USER"
    },

}

#@TODO: Choose the models to run here by uncommenting the ones you want to run
models_to_run = [
    perplexity_pro_high,
    perplexity_reasoning_pro_high,
    openai_gpt4_1m_search, # Add the new OpenAI function here
    # openai_gpt4_1h_search, # Add the new OpenAI function here
    # openai_gpt4_1_mini_h_search,
    # gemini_2_0_flash_search, # Add the new Gemini function here
    # exa_answer_search, # Add the new Exa function here
]

# --- Main Execution ---

if __name__ == "__main__":
    load_dotenv() # Load environment variables from .env file

    csv_file_path = "test_set.csv"
    # Define the target Notion Database ID to use
    # target_database_id = DEFAULT_NOTION_DATABASE_ID # Or replace with a specific ID string
    target_database_id = os.getenv("NOTION_DATABASE_ID") # Get DB ID from environment

    # Add a check to ensure the database ID was loaded
    if not target_database_id:
        print("Error: NOTION_DATABASE_ID not found in .env file or environment variables.")
        exit()

    # 1. Load data from CSV
    all_company_data = load_company_data(csv_file_path)

    # 2. Select companies to process
    companies_to_process = select_companies_to_process(all_company_data)

    # 3. Select the prompt set
    selected_prompt_name, system_prompt, user_prompt_template = select_prompt_set(available_prompt_sets)

    # 4. Process selected companies with all defined models
    for company_info in companies_to_process:
        company_name = company_info.get('Company', 'N/A')
        company_address = company_info.get('Address', 'N/A')

        print(f"\n--- Processing Company: {company_name} at {company_address} ---")

        # Format the user prompt once per company
        user_prompt = user_prompt_template.format(company_name=company_name, company_address=company_address)

        # Iterate through the selected models to run
        for model_function in models_to_run:
            # Get the model name directly from the function object
            model_name = model_function.__name__
            print(f"\n--- Querying with Model: {model_name} ---")

            # Call the current model function
            response_data = model_function(company_name, company_address, system_prompt, user_prompt)

            # Check if the response is valid before creating Notion page
            if response_data:
                print(f"Sending response for {model_name} to Notion...")
                # Call Notion function with the response data, specific database ID, prompt set name, and model name
                create_notion_page(database_id=target_database_id,
                                   company_name=company_name,
                                   prompt_set_name=selected_prompt_name,
                                   model_name=model_name, # Pass the current model's name
                                   response_data=response_data) # Pass the whole dict
            else:
                # Updated print statement to reflect model name and company
                print(f"Skipping Notion upload for {company_name} ({model_name}) due to empty/failed response.")

    print("\n--- Processing Complete ---")
