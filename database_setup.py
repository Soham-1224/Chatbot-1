import sqlite3

# Connect to SQLite database (or create if it doesn’t exist)
conn = sqlite3.connect('college.db')
cursor = conn.cursor()

# Create a table for FAQs
cursor.execute('''
CREATE TABLE IF NOT EXISTS faq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
''')

# Insert sample data into the table
faq_data = [
    ("What are the admission requirements?", "You need a minimum of 50% in high school."),
    ("What is the fee structure?", "The tuition fee is $5000 per year."),
    ("Do you offer scholarships?", "Yes, we offer merit-based and need-based scholarships."),
    ("What courses are available?", "We offer Computer Science, Electronics, Mechanical, and Civil Engineering."),
    ("Where can I apply?", "You can apply online via our college portal at www.college-website.com.")
]

cursor.executemany("INSERT INTO faq (question, answer) VALUES (?, ?)", faq_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
