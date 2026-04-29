# SmartCourse AI

SmartCourse AI is an AI-powered study assistant for PDF course materials.

The project turns a static academic PDF into an interactive learning tool. A user can upload a PDF, ask questions about the content, generate a summary, take an interactive quiz, and create flashcards for revision.

## Features

- Upload PDF course materials
- Extract text from PDF files
- Ask questions about the uploaded document
- Generate summaries
- Generate an interactive quiz
- Choose quiz answers and check score
- 5-minute quiz timer
- Generate flashcards for revision
- Download generated summaries and flashcards

## Technologies Used

- Python
- Streamlit
- PyPDF2
- Hugging Face Inference API
- python-dotenv

## Project Structure

```text
smartcourse-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── qa_engine.py
│   ├── summarizer.py
│   ├── quiz_generator.py
│   └── flashcard_generator.py
│
└── prompts/
    ├── qa_prompt.txt
    ├── quiz_prompt.txt
    └── summary_prompt.txt
