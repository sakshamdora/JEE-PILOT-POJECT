import sqlite3

conn = sqlite3.connect("quizmaster.db")
cursor = conn.cursor()

# USERS TABLE WITH ROLE 
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               name TEXT NOT NULL,
               role TEXT NOT NULL CHECK(role IN ("user", "admin"))
)
""")

# QUIZES TABLE 
cursor.execute("""
CREATE TABLE IF NOT EXISTS quizzes (
               quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               subject TEXT NOT NULL,
               created_at TIMESTAMP DEAFULT CURRENT_TIMESTAMP,
               updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
# QUESTIONS TABLE 
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
               question_id INTEGER PRIMARY KEY AUTOINCREMENT,
               quiz_id INTEGER NOT NULL,
               question_text TEXT NOT NULL,
               option_a TEXT NOT NULL,
               option_b TEXT NOT NULL,
               option_c TEXT NOT NULL,
               option_d TEXT NOT NULL,
               correct_option TEXT,
               integer_answer INTEGER,
               image_path TEXT,
               question_type TEXT NOT NULL,
               FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
)
""")

cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?,?,?)", ("sakshamdora","SAKSHAM","admin"))
conn.commit()
conn.close()
print("DATABASE")