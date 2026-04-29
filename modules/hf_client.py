import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")


def call_huggingface(model_url, payload):
    if not HF_API_KEY:
        return {
            "error": "Hugging Face API key is missing. Add HF_API_KEY to your .env file."
        }

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload["options"] = {
        "wait_for_model": True
    }

    try:
        response = requests.post(
            model_url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return {
                "error": f"API error {response.status_code}: {response.text}"
            }

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}"
        }