import requests
import os

# Load API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

def chat(query: str):
    # RunPod API endpoint (replace with actual RunPod endpoint)
    url = f"{OPENAI_API_BASE}/v1/completions"  # Make sure to use the correct RunPod endpoint
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Request body: specify model and input query
    data = {
        "model": "llama-7b",  # Adjust the model name if necessary (make sure it matches RunPod's available model)
        "messages": [{"role": "user", "content": query}]
    }
    
    # Make the API request to RunPod
    response = requests.post(url, headers=headers, json=data)
    
    # Handle response and return the result
    if response.status_code == 200:
        return response.json()  # This should contain the response from the model
    else:
        return {"error": "Failed to get response from RunPod", "details": response.json()}
