import requests
import json
import os # Import os module
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add Notion API configuration
# NOTION_API_KEY = "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"
NOTION_API_KEY = os.getenv("NOTION_API_KEY") # Get key from environment

# Check if the API key is loaded
if not NOTION_API_KEY:
    print("Error: NOTION_API_KEY not found in .env file or environment variables.")
    # exit()

# Keep the default database ID here for potential use in main.py or elsewhere
# DEFAULT_NOTION_DATABASE_ID = "1d5addd5ec47809a8d28f6979fd19b9a"
# We load the Database ID in main.py now, but keeping the variable here doesn't hurt
# unless you want to remove unused variables.
DEFAULT_NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID") # Also load DB ID here just in case it's used in example

def create_notion_page(database_id: str, company_name: str, prompt_set_name: str, model_name: str, response_data: dict):
    """Creates a new page in a specified Notion database with API response data"""
    url = "https://api.notion.com/v1/pages"

    # Check if API key is available before making request
    if not NOTION_API_KEY:
        print("Error: Cannot create Notion page because NOTION_API_KEY is missing.")
        return None # Return None or raise an error

    headers = {
        # Use the loaded API key
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Convert the response data to a formatted JSON string
    json_string = json.dumps(response_data, indent=2)
    max_chunk_size = 1900 # Set max size slightly below 2000 for safety

    # Split the JSON string into chunks
    chunks = [json_string[i:i + max_chunk_size]
              for i in range(0, len(json_string), max_chunk_size)]

    # Create a list of code block objects, one for each chunk
    content_blocks = []
    for chunk in chunks:
        content_blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": chunk
                    }
                }],
            }
        })

    # Use arguments for database_id and create a dynamic title including the prompt set name
    page_title = f"{company_name} - {prompt_set_name}"
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": page_title
                        }
                    }
                ]
            },
            "Model": {
                "select": {
                    "name": model_name
                }
            },
            "Prompt Set": {
                "select": {
                    "name": prompt_set_name
                }
            }
        },
        "children": content_blocks
    }

    response = requests.post(url, json=payload, headers=headers)

    # Print the response status code for feedback
    print(f"Notion API Response Status: {response.status_code} for {page_title}")
    if response.status_code != 200:
        try:
            # Try to print JSON error response if possible
            print(f"Notion API Error Body: {response.json()}")
        except json.JSONDecodeError:
            # Otherwise print raw text
            print(f"Notion API Error Body (non-JSON): {response.text}")

    return response.status_code

# Removed Perplexity API call functions from this file

# Example of how to call the function (for testing purposes, can be removed)
if __name__ == "__main__":
    # Example usage:
    test_response_data = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "sonar-medium-online",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "\n\n1. Core Offering: Widgets.\n2. What they do: Manufacture widgets.\n3. Customers: B2B.",
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }
    # Use the default database ID for the test and add the model name
    status = create_notion_page(DEFAULT_NOTION_DATABASE_ID, "Test Co", "Test Model", "Claude", test_response_data)
    print(f"Test call finished with status: {status}")