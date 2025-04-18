import requests
import json
import os # Import os module
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Check if the API key is loaded
if not PERPLEXITY_API_KEY:
    print("Error: PERPLEXITY_API_KEY not found in .env file or environment variables.")
    # You might want to exit or raise an error here depending on your application's needs
    # exit() # Example: exit if key not found

# Define the function
def perplexity_reasoning_pro_high(company_name: str, company_address: str, system_prompt: str, user_prompt: str):
    """Sends a query to the Perplexity API using the sonar-reasoning-pro model with high search context."""
    print("Perplexity Reasoning Pro High")
    url = "https://api.perplexity.ai/chat/completions"

    # Construct the payload using the function arguments
    payload = {
        "model": "sonar-reasoning-pro",
        "messages": [
            {
                "role": "system",
                "content": system_prompt # Use the passed system prompt
            },
            {
                "role": "user",
                "content": user_prompt # Use the passed user prompt
            }
        ],
        "web_search_options": {"search_context_size": "high"}
    }
    headers = {
        # Use the loaded API key
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.request("POST", url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        # Pretty-print the JSON
        print(json.dumps(response_json, indent=4))
        # Return the JSON data
        return response_json
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(f"Response text: {response.text}")
        # Return None if there was an error
        return None

def perplexity_reasoning_pro_medium(company_name: str, company_address: str, system_prompt: str, user_prompt: str):
    """Sends a query to the Perplexity API using the sonar-reasoning-pro model with medium search context."""
    print("Perplexity Reasoning Pro Medium")
    url = "https://api.perplexity.ai/chat/completions"

    # Construct the payload using the function arguments
    payload = {
        "model": "sonar-reasoning-pro",
        "messages": [
            {
                "role": "system",
                "content": system_prompt # Use the passed system prompt
            },
            {
                "role": "user",
                "content": user_prompt # Use the passed user prompt
            }
        ],
        "web_search_options": {"search_context_size": "medium"}
    }
    headers = {
        # Use the loaded API key
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.request("POST", url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        # Pretty-print the JSON
        print(json.dumps(response_json, indent=4))
        # Return the JSON data
        return response_json
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(f"Response text: {response.text}")
        # Return None if there was an error
        return None

def perplexity_reasoning_pro_low(company_name: str, company_address: str, system_prompt: str, user_prompt: str):
    """Sends a query to the Perplexity API using the sonar-reasoning-pro model with low search context."""
    print("Perplexity Reasoning Pro Low")
    url = "https://api.perplexity.ai/chat/completions"

    # Construct the payload using the function arguments
    payload = {
        "model": "sonar-reasoning-pro",
        "messages": [
            {
                "role": "system",
                "content": system_prompt # Use the passed system prompt
            },
            {
                "role": "user",
                "content": user_prompt # Use the passed user prompt
            }
        ],
        "web_search_options": {"search_context_size": "low"}
    }
    headers = {
        # Use the loaded API key
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.request("POST", url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        # Pretty-print the JSON
        print(json.dumps(response_json, indent=4))
        # Return the JSON data
        return response_json
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(f"Response text: {response.text}")
        # Return None if there was an error
        return None
