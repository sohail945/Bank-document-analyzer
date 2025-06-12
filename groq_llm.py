import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = os.getenv("GROQ_ENDPOINT")


def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",  
        "messages": [
            {"role": "system", "content": "You are a helpful document assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(GROQ_ENDPOINT, json=data, headers=headers)
    json_response = response.json()

    if "choices" in json_response:
        return json_response["choices"][0]["message"]["content"]
    else:
        print("Error from Groq:", json_response)
        return "Error: Could not get response from LLM"


