import os
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, Content, Part
import json
import logging # Added for error logging
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get Gemini API Key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.error("GEMINI_API_KEY not found in .env file or environment variables.")
    # Handle the absence of the key appropriately, e.g., raise an error or exit

# Initialize the client globally or consider passing it if managing multiple clients/keys
# Keep the API key as is, per instructions.
client = None # Initialize client to None
if GEMINI_API_KEY:
    try:
        # Use the loaded API key
        client = genai.Client(api_key=GEMINI_API_KEY)
        logging.info("GenAI Client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize GenAI Client: {e}")
else:
    logging.warning("GenAI Client could not be initialized due to missing API key.")

# Define the Google Search tool for grounding
google_search_tool = Tool(
    google_search=GoogleSearch()
)

# Configuration for the generation, including the grounding tool
gen_config = GenerateContentConfig(
    tools=[google_search_tool],
    # Specifying TEXT modality might be useful depending on expected output
    # response_modalities=["TEXT"], # Optional: uncomment if needed
)

def gemini_2_0_flash_search(company_name: str, company_address: str, system_prompt: str, user_prompt: str) -> dict | None:
    """
    Queries the Gemini 2.0 Flash model with Google Search grounding.

    Args:
        company_name: The name of the company.
        company_address: The address of the company.
        system_prompt: The system prompt for the model.
        user_prompt: The user prompt (template should be formatted in main.py).

    Returns:
        A dictionary containing the response text, or None if an error occurs.
    """
    if not client:
        logging.error("GenAI Client is not initialized. Cannot perform search.")
        return None

    # Combine system and user prompts. Gemini API often uses a structured 'contents' list.
    # We'll put the system prompt first, then the user prompt.
    # Note: The effectiveness of system prompts can vary. This is a common pattern.
    # The user_prompt is expected to be pre-formatted by the caller (main.py)
 

    try:
        logging.info(f"Querying Gemini 2.0 Flash for: {company_name}")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_prompt,
            config=gen_config # Use the config with the search tool
        )

        # Process the response to extract text
        # Based on grounding example, iterate through parts
        response_text = ""
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                 response_text += part.text
        else:
             # Handle cases where the response might be structured differently or empty
             response_text = response.text # Fallback to the simpler text attribute if parts aren't populated as expected

        # Log grounding metadata if available (optional)
        if response.candidates and response.candidates[0].grounding_metadata:
            search_entry = response.candidates[0].grounding_metadata.search_entry_point
            if search_entry:
                 logging.info(f"Grounding search query used: {search_entry.rendered_content}")
            # You could potentially extract and return web search results too if needed
            # web_results = response.candidates[0].grounding_metadata.web_search_queries

        logging.info(f"Successfully received response for: {company_name}")
        # Return in the format expected by main.py
        return {'response': response_text.strip()}

    except Exception as e:
        logging.error(f"Error querying Gemini 2.0 Flash for {company_name}: {e}")
        # Optional: Log the full response object upon error for debugging
        # logging.error(f"Full error response object: {response}")
        return None

