import re


STOP_WORDS = {
    "the", "and", "that", "this", "with", "from", "into", "your",
    "about", "there", "their", "which", "when", "where", "what",
    "will", "would", "should", "could", "because", "using", "based",
    "material", "document", "student", "system", "project", "helps"
}


def clean_text(text):
    text = re.sub(r"\[Page \d+\]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_sentences(text):
    text = clean_text(text)
    sentences = re.split(r"(?<=[.!?])\s+", text)

    good_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if 50 <= len(sentence) <= 240 and "?" not in sentence:
            good_sentences.append(sentence)

    return good_sentences


def find_keyword(sentence):
    words = re.findall(r"\b[A-Za-z][A-Za-z\-]{4,}\b", sentence)

    candidates = [
        word.strip(".,:;()[]")
        for word in words
        if word.lower() not in STOP_WORDS
    ]

    if candidates:
        return candidates[0]

    return None


def generate_flashcards(text, number_of_cards=8):
    sentences = extract_sentences(text)
    flashcards = []

    for sentence in sentences:
        keyword = find_keyword(sentence)

        if not keyword:
            continue

        question = f"What does '{keyword}' refer to in this material?"
        answer = sentence

        flashcards.append({
            "term": keyword,
            "question": question,
            "answer": answer
        })

        if len(flashcards) >= number_of_cards:
            break

    return flashcards


def flashcards_to_text(flashcards):
    output = []

    for i, card in enumerate(flashcards, start=1):
        output.append(
            f"Flashcard {i}\n"
            f"Term: {card['term']}\n"
            f"Question: {card['question']}\n"
            f"Answer: {card['answer']}\n"
        )

    return "\n".join(output)