import os
from openai import OpenAI
import json # Import json for pretty printing
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The OpenAI client automatically looks for the OPENAI_API_KEY environment variable.
# Ensure it is set in your .env file or system environment.
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in .env file or environment variables.")
    # exit()

# WARNING: Hardcoding API keys is a security risk. Prefer setting environment variables externally.
# Consider removing this line and setting the environment variable in your shell or using a .env file.


def openai_gpt4_1_mini_h_search(company_name: str, company_address: str, system_prompt: str, user_prompt: str):
    """Sends a query to the OpenAI API using gpt-4.1 with web search enabled."""
    print("OpenAI GPT-4.1 Search") # Indicate which function is running
    client = OpenAI()

    # Note: OpenAI's 'responses' API primarily uses 'input' which often combines system/user roles.
    # We'll combine system and user prompts here for simplicity, but you might adjust this logic.


    try:
        # Create a response using GPT-4.1 and enabling the web search tool
        response = client.responses.create(
            model="gpt-4.1-mini",                   # Specify the model
            tools=[{"type": "web_search_preview", "search_context_size": "high",}
                   ], # Enable the web search tool

            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        # Print the raw response for debugging (optional)
        # print("Raw OpenAI Response:")
        # print(response)

        # Extract the main text output
        output_text = response.output_text
        print("OpenAI Response Text:")
        print(output_text)

        # Construct a dictionary similar to Perplexity's output for consistency in main.py
        # This might need adjustment based on the actual structure you need downstream.
        response_data = {
            "model": "gpt-4.1",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": output_text
                    }
                }
            ],
            "usage": response.usage.model_dump() if hasattr(response, 'usage') and response.usage else None # Include usage if available
        }
        print("Formatted Response Data for Notion:")
        print(json.dumps(response_data, indent=4)) # Pretty print the formatted data
        return response_data

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

# Example usage (can be commented out or removed when importing)
# if __name__ == "__main__":
#     test_company = "Example Inc."
#     test_address = "123 Example St"
#     test_system = "You are a helpful assistant."
#     test_user = "What does this company do?"
#     result = openai_gpt4_1_search(test_company, test_address, test_system, test_user)
#     if result:
#         print("\n--- Final Result ---")
#         print(json.dumps(result, indent=4))

# --- Old Code Below (Commented out/Removed) ---
# # Make sure your OpenAI API key is configured, e.g., via the OPENAI_API_KEY environment variable.
# from openai import OpenAI

# # Instantiate the OpenAI client
# client = OpenAI()

# # Create a response using GPT-4.1 and enabling the web search tool
# response = client.responses.create(
#     model="gpt-4.1",  # Specify the model
#     tools=[{"type": "web_search_preview"}],  # Enable the web search tool
#     input="What is the latest news about AI development?"  # Provide the input prompt
# )

# # Print the output text from the response
# print(response.output_text)
