from flask import Flask, request, jsonify, render_template
import sqlite3
import nltk
from nltk.chat.util import Chat, reflections
import os

app = Flask(__name__)

# Database Configuration
DATABASE = "college.db"

def create_connection():
    """Create and return a database connection"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
    except sqlite3.Error as e:
        print(e)
    return conn

def initialize_database():
    """Create table if not exists and insert initial FAQs"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    """)

    # Pre-populate FAQs if empty
    cursor.execute("SELECT COUNT(*) FROM faqs")
    if cursor.fetchone()[0] == 0:
        faqs = [
            ("hi", "Hello! How can I assist you today?"),
            ("hello", "Hi there! How may I help you?"),
            ("what courses do you offer?", "We offer Engineering, Arts, Science, and Commerce courses."),
            ("admission process", "The admission process includes an entrance exam and an interview."),
            ("fees structure", "The fee structure varies based on the course. Please visit the college website for details."),
            ("how can I apply?", "You can apply online through the college website. Contact the admission office for more details."),
            ("bye", "Goodbye! Have a great day."),
        ]
        cursor.executemany("INSERT INTO faqs (question, answer) VALUES (?, ?)", faqs)
        conn.commit()

    conn.close()

# Initialize database
initialize_database()

def get_response_from_db(user_message):
    """Retrieve response from the database"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT answer FROM faqs WHERE question = ?", (user_message.lower(),))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None

# Predefined chatbot responses (if not found in DB)
pairs = [
    ["hi|hello|hey", ["Hello! How can I assist you today?"]],
    ["bye|goodbye", ["Goodbye! Have a great day."]],
]

chatbot = Chat(pairs, reflections)

@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is inside the /templates folder

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message").strip().lower()
    
    # Try fetching response from the database first
    response = get_response_from_db(user_message)

    # If no database match, use chatbot patterns
    if response is None:
        response = chatbot.respond(user_message)

    # If no chatbot match either, return default response
    if response is None:
        response = "I'm sorry, I didn't understand that. Can you rephrase?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
