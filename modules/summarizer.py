import os
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

HF_API_KEY = os.getenv("HF_API_KEY")

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_API_KEY
)

SUMMARY_MODEL = "facebook/bart-large-cnn"


def summarize_text(text):
    if not HF_API_KEY:
        return f"Hugging Face API key is missing. Checked path: {ENV_PATH}"

    short_text = text[:3500]

    try:
        result = client.summarization(
            short_text,
            model=SUMMARY_MODEL
        )

        if isinstance(result, dict):
            return result.get("summary_text", "Could not generate summary.")

        return result.summary_text

    except Exception as e:
        return f"Summarization error: {str(e)}"