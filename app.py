import time
import streamlit as st

from modules.document_loader import load_pdf, pages_to_full_text
from modules.text_splitter import split_text
from modules.qa_engine import answer_question
from modules.summarizer import summarize_text
from modules.quiz_generator import generate_quiz
from modules.flashcard_generator import generate_flashcards, flashcards_to_text


st.set_page_config(
    page_title="SmartCourse AI",
    page_icon="🎓",
    layout="wide"
)


QUIZ_TIME_LIMIT_SECONDS = 5 * 60


def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def reset_quiz_state():
    st.session_state.quiz_questions = []
    st.session_state.quiz_started = False
    st.session_state.quiz_submitted = False
    st.session_state.quiz_start_time = None
    st.session_state.quiz_score = 0


def main():
    st.title("🎓 SmartCourse AI")
    st.subheader("AI Study Assistant for PDF Course Materials")

    st.write(
        "Upload a PDF, ask questions, generate a summary, take a quiz, and create flashcards."
    )

    if "quiz_questions" not in st.session_state:
        reset_quiz_state()

    uploaded_file = st.file_uploader(
        "Upload your course PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            pages = load_pdf(uploaded_file)
            full_text = pages_to_full_text(pages)
            chunks = split_text(full_text)

        st.success(f"PDF loaded successfully. Pages found: {len(pages)}")

        with st.expander("View extracted text"):
            st.text_area(
                "Extracted text",
                full_text,
                height=300
            )

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Ask Questions", "Summary", "Quiz Generator", "Flashcards", "Project Info"]
        )

        with tab1:
            st.header("Ask Questions About the PDF")

            question = st.text_input(
                "Enter your question",
                placeholder="Example: What is the main idea of this document?"
            )

            if st.button("Get Answer"):
                if question.strip():
                    with st.spinner("Searching and generating answer..."):
                        answer = answer_question(question, chunks)

                    st.subheader("Answer")
                    st.write(answer)
                else:
                    st.warning("Please enter a question first.")

        with tab2:
            st.header("Generate Summary")

            if st.button("Summarize PDF"):
                with st.spinner("Generating summary..."):
                    summary = summarize_text(full_text)

                st.subheader("Summary")
                st.write(summary)

                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="smartcourse_summary.txt",
                    mime="text/plain"
                )

        with tab3:
            st.header("Interactive Quiz Generator")
            st.write("Generate a quiz, choose your answers, and check your score.")

            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("Generate New Quiz"):
                    quiz_questions = generate_quiz(full_text)

                    if quiz_questions:
                        st.session_state.quiz_questions = quiz_questions
                        st.session_state.quiz_started = True
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_start_time = time.time()
                        st.session_state.quiz_score = 0

                        for i in range(len(quiz_questions)):
                            key = f"quiz_answer_{i}"
                            if key in st.session_state:
                                del st.session_state[key]

                        st.success("Quiz generated. Timer started!")
                    else:
                        st.error("Could not generate quiz questions from this PDF.")

            with col2:
                if st.button("Reset Quiz"):
                    reset_quiz_state()
                    st.success("Quiz reset.")

            if st.session_state.quiz_started and st.session_state.quiz_questions:
                elapsed_time = time.time() - st.session_state.quiz_start_time
                remaining_time = max(0, QUIZ_TIME_LIMIT_SECONDS - elapsed_time)

                st.subheader("Timer")
                st.info(f"Time remaining: {format_time(remaining_time)}")

                progress_value = remaining_time / QUIZ_TIME_LIMIT_SECONDS
                st.progress(progress_value)

                time_is_up = remaining_time <= 0

                if time_is_up and not st.session_state.quiz_submitted:
                    st.error("Time is up! Click 'Check Answers' to see your result.")

                st.subheader("Quiz Questions")

                for i, item in enumerate(st.session_state.quiz_questions):
                    st.markdown(f"### Question {i + 1}")
                    st.write(item["question"])

                    st.radio(
                        label="Choose your answer:",
                        options=item["options"],
                        key=f"quiz_answer_{i}",
                        disabled=st.session_state.quiz_submitted
                    )

                if not st.session_state.quiz_submitted:
                    if st.button("Check Answers"):
                        score = 0

                        for i, item in enumerate(st.session_state.quiz_questions):
                            user_answer = st.session_state.get(f"quiz_answer_{i}")
                            correct_answer = item["correct_answer"]

                            if user_answer == correct_answer:
                                score += 1

                        st.session_state.quiz_score = score
                        st.session_state.quiz_submitted = True

                if st.session_state.quiz_submitted:
                    total = len(st.session_state.quiz_questions)
                    score = st.session_state.quiz_score

                    st.success(f"Your score: {score}/{total}")

                    if score == total:
                        st.balloons()
                        st.write("Excellent! You got all answers correct.")
                    elif score >= total / 2:
                        st.write("Good work. Review the incorrect answers below.")
                    else:
                        st.write("Keep practicing. Review the correct answers below.")

                    st.subheader("Correct Answers")

                    for i, item in enumerate(st.session_state.quiz_questions):
                        user_answer = st.session_state.get(f"quiz_answer_{i}")
                        correct_answer = item["correct_answer"]

                        st.markdown(f"### Question {i + 1}")
                        st.write(item["question"])

                        if user_answer == correct_answer:
                            st.success(f"Your answer: {user_answer} ✅")
                        else:
                            st.error(f"Your answer: {user_answer} ❌")
                            st.info(f"Correct answer: {correct_answer}")

                        with st.expander("Show source sentence"):
                            st.write(item["source_sentence"])

            else:
                st.info("Click 'Generate New Quiz' to start a 5-minute quiz.")

        with tab4:
            st.header("Flashcard Generator")
            st.write("Generate revision flashcards from the uploaded PDF.")

            number_of_cards = st.slider(
                "Number of flashcards",
                min_value=3,
                max_value=12,
                value=8
            )

            if st.button("Generate Flashcards"):
                flashcards = generate_flashcards(full_text, number_of_cards)

                if flashcards:
                    st.subheader("Generated Flashcards")

                    for i, card in enumerate(flashcards, start=1):
                        with st.expander(f"Flashcard {i}: {card['term']}"):
                            st.write(f"**Question:** {card['question']}")
                            st.write(f"**Answer:** {card['answer']}")

                    flashcard_text = flashcards_to_text(flashcards)

                    st.download_button(
                        label="Download Flashcards",
                        data=flashcard_text,
                        file_name="smartcourse_flashcards.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Could not generate flashcards from this PDF.")

        with tab5:
            st.header("About This Project")

            st.write("""
            **SmartCourse AI** is an AI-powered study assistant for PDF course materials.

            It uses:
            - PDF text extraction
            - Text chunking
            - Simple retrieval
            - Hugging Face question-answering model
            - Hugging Face summarization model
            - Rule-based interactive quiz generation
            - Flashcard generation
            - Prompt engineering principles

            Main features:
            - Upload course PDF
            - Ask questions from the document
            - Generate summaries
            - Generate interactive quizzes
            - Check answers and calculate score
            - 5-minute quiz timer
            - Generate downloadable flashcards

            This project demonstrates how AI can transform static academic documents into interactive learning tools.
            """)

    else:
        st.info("Upload a PDF to start.")


if __name__ == "__main__":
    main()