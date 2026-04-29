import re
import random


STOP_WORDS = {
    "the", "and", "that", "this", "with", "from", "into", "your",
    "about", "there", "their", "which", "when", "where", "what",
    "will", "would", "should", "could", "because", "using", "based",
    "material", "document", "student", "system", "project"
}


def clean_text(text):
    text = re.sub(r"\[Page \d+\]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_sentences(text):
    text = clean_text(text)
    sentences = re.split(r"(?<=[.!?])\s+", text)

    good_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 40:
            continue

        if len(sentence) > 220:
            continue

        if "?" in sentence:
            continue

        words = sentence.split()
        if len(words) < 8:
            continue

        good_sentences.append(sentence)

    return good_sentences


def choose_answer(sentence):
    words = re.findall(r"\b[A-Za-z][A-Za-z\-]{4,}\b", sentence)

    candidates = [
        word for word in words
        if word.lower() not in STOP_WORDS
    ]

    if candidates:
        return candidates[0]

    return words[0] if words else None


def make_question(sentence, answer):
    blanked = re.sub(rf"\b{re.escape(answer)}\b", "_____", sentence, count=1)
    return f"Fill in the blank: {blanked}"


def generate_distractors(correct_answer):
    distractor_pool = [
        "model",
        "dataset",
        "interface",
        "algorithm",
        "summary",
        "retrieval",
        "assistant",
        "workflow",
        "application",
        "response",
        "feature",
        "context"
    ]

    distractors = [
        word for word in distractor_pool
        if word.lower() != correct_answer.lower()
    ]

    selected = random.sample(distractors, 3)
    options = selected + [correct_answer]
    random.shuffle(options)

    return options


def generate_quiz(text, number_of_questions=5):
    sentences = get_sentences(text)

    if len(sentences) == 0:
        return []

    selected_sentences = sentences[:number_of_questions]
    quiz = []

    for sentence in selected_sentences:
        answer = choose_answer(sentence)

        if not answer:
            continue

        question = make_question(sentence, answer)
        options = generate_distractors(answer)

        quiz.append({
            "question": question,
            "options": options,
            "correct_answer": answer,
            "source_sentence": sentence
        })

    return quiz