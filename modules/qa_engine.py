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

QA_MODEL = "deepset/roberta-base-squad2"


def simple_retrieve(question, chunks, top_k=3):
    question_words = set(question.lower().split())
    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(question_words.intersection(chunk_words))
        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    best_chunks = [chunk for score, chunk in scored_chunks[:top_k]]

    return "\n\n".join(best_chunks)


def answer_question(question, chunks):
    if not HF_API_KEY:
        return f"Hugging Face API key is missing. Checked path: {ENV_PATH}"

    context = simple_retrieve(question, chunks)

    try:
        result = client.question_answering(
            question=question,
            context=context[:4000],
            model=QA_MODEL
        )

        if isinstance(result, dict):
            return result.get("answer", "No clear answer found.")

        return result.answer

    except Exception as e:
        return f"Question answering error: {str(e)}"