from . import config
import sqlite3
import google.generativeai as genai
import time
from django.http import JsonResponse
import uuid  # Add this import at the top

# Configure generative AI
genai.configure(api_key='AIzaSyDNm25yHKyLbpjxPGh2OeWq3GT3fG5-aTk')

def initialize_database():
    """Initializes the SQLite database and creates the questions table if it does not exist."""
    with sqlite3.connect('questions.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY,
                            key TEXT UNIQUE,
                            value TEXT,
                            correct_answer TEXT
                          )''')
        conn.commit()

def extract_correct_answer(question):
    """Extracts the correct answer from the formatted question."""
    lines = question.split("\n")
    for line in lines:
        if line.startswith("Correct Answer:"):
            return line.split(":", 1)[1].strip()
    return None

def generate_question(text):
    """Generates multiple-choice questions from the provided text and stores them in the database.
    Returns the questions with their database IDs for display purposes."""
    initialize_database()

    with sqlite3.connect('questions.db') as conn:
        cursor = conn.cursor()
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"""Create a practice test with 10 multiple choice questions on the following text: {text}.
                  Each question should have:
                  - A clear question.
                  - Four answer options
                  - The correct answer clearly indicated.
                  - Questions should be generated in the same language of provided text.
                  Format:
                  ## MCQ
                  [question]
                  A) [option A]
                  B) [option B]  
                  C) [option C]
                  D) [option D]  
                  Correct Answer: [correct option]""")

        questions = response.candidates[0].content.parts[0].text
        mcqs_with_ids = []  # List to hold questions with their database IDs

        for question in questions.split("## MCQ"):
            if question.strip():
                correct_answer = extract_correct_answer(question)
                question_without_answer = "\n".join(
                    line for line in question.split("\n") if not line.startswith("Correct Answer:")
                )

                # Generate a truly unique key using UUID
                key = str(uuid.uuid4())

                # Store the question in the database and fetch its ID
                try:
                    cursor.execute(
                        "INSERT INTO questions (key, value, correct_answer) VALUES (?, ?, ?)",
                        (key, question_without_answer, correct_answer),
                    )
                    question_id = cursor.lastrowid  # Get the database ID of the inserted question

                    # Add question ID and text to the return list
                    mcqs_with_ids.append({'id': question_id, 'question': question_without_answer})
                except sqlite3.IntegrityError as e:
                    print(f"IntegrityError: {e}. Skipping duplicate question.")

        conn.commit()

    return mcqs_with_ids


def get_answer(request, question_id):
    """Fetches the correct answer for a given question ID."""
    with sqlite3.connect('questions.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT correct_answer FROM questions WHERE id = ?", (question_id,))
        result = cursor.fetchone()

    if result:
        return JsonResponse({'correct_answer': result[0]})
    else:
        return JsonResponse({'error': 'Answer not found'}, status=404)
