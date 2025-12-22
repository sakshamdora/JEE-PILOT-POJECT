import os
from dotenv import load_dotenv
from flask import Flask,g, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
import sqlite3
from werkzeug.utils import secure_filename
import datetime
import config
import joblib
import pandas as pd
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()  ## LOAD ENVIRONMENT VARIABLES FROM .env FILE



app=Flask(__name__)
app.secret_key = "bd1a7efd9593b65fe910cb1c4af757af"
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["DATABASE"] = config.DATABASE

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True) 

# ------------------ DATABASE CONNECTION ------------------


def get_db():         ## CREATE OR RETURN AN EXISTING DATABASE CONNECTION FOR TIS REQUEST 
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):    ## AUTOMATICALLY CLOSE THE DATABASE CONNECTION AT THE END OF REQUEST 
    db = getattr(g, "_db", None)
    if db:
        db.close()

def allowed_file(filename):      ## CHECK IF THE UPLOADED FILE EXTENSION IS ALLOWED 
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS 

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    user = session.get('username')
    
    return render_template('index.html', user=user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form["name"]
        role = request.form.get('role', 'user')  # Default role is 'user'
        conn = sqlite3.connect('quizmaster.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)", (username, password, name, role))
            conn.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "error")
        finally:
            conn.close()
    return render_template('USER/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?",(username, password)).fetchone()
        conn.close()

        if user:
            session["username"] = user["username"]
            session["role"] = user["role"]
            if user["role"] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('study_dashboard'))
        else:
            flash("Invalid credentials!", "error")

    return render_template('USER/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))

@app.route('/study_dashboard')
def study_dashboard():
    if 'username' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template('USER/study_dashboard.html', user=session['username'])




@app.route("/percentile_predictor")
def percentile_predictor():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('USER/percentile_predictor.html', user=session['username'])

@app.route("/your_feedback")
def your_feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('USER/feedback.html', user=session['username'])

@app.route("/notes")
def notes():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("USER/notes.html", user=session['username'])     

@app.route("/pyqs")
def pyqs():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("USER/pyqs.html", user=session['username'])

@app.route("/tests_pdf")
def tests_pdf():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("USER/tests_pdf.html", user=session['username'])

@app.route("/tests_quiz")
def tests_quiz():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("USER/tests_quiz.html", user=session['username'])



@app.route("/physics_notes")
def physics_notes():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("PHYSICS/physics_notes.html", user=session['username'])
@app.route("/chemistry_notes")
def chemistry_notes():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("CHEMISTRY/chemistry_notes.html", user=session['username'])
@app.route("/maths_notes")
def maths_notes():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("MATHS/maths_notes.html", user=session['username'])

@app.route("/physics_pyqs")
def physics_pyqs():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("PHYSICS/physics_pyqs.html", user=session['username'])
@app.route("/chemistry_pyqs")
def chemistry_pyqs():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("CHEMISTRY/chemistry_pyqs.html", user=session['username'])
@app.route("/maths_pyqs")
def maths_pyqs():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("MATHS/maths_pyqs.html", user=session['username'])

@app.route("/physics_tests")
def physics_tests():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("PHYSICS/physics_tests.html", user=session['username'])
@app.route("/chemistry_tests")
def chemistry_tests():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("CHEMISTRY/chemistry_tests.html", user=session['username'])
@app.route("/maths_tests")
def maths_tests():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("MATHS/maths_tests.html", user=session['username'])
## ------------------- QUIZ FUNCTIONALITY ROUTES ---------------------##

@app.route("/quizzes")       ## DISPLAY LISTS OF QUIZZES FOR USERS 
def quizzes():
    if "username" not in session:
        return redirect(url_for("login"))
    db = get_db()
    quizzes = db.execute("SELECT * FROM quizzes ORDER BY created_at DESC").fetchall()   ## SHOWS ALL QUIZZES IN DESCENDING ORDER OF CREATION DATE/TIME 
    return render_template("USER/quizzes.html", quizzes=quizzes, user=session["username"])

@app.route("/quiz/<int:quiz_id>")
def view_quiz(quiz_id):
    if "username" not in session:
        return redirect(url_for("login"))
    db = get_db()
    quiz = db.execute("SELECT * FROM quizzes WHERE quiz_id = ?", (quiz_id,)).fetchone()
    questions = db.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,)).fetchall()
    return render_template("ADMIN/view_quiz.html", quiz=quiz, questions=questions, user=session["username"], quiz_id=quiz_id)

@app.route("/admin")
def admin_dashboard():
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    db = get_db()
    quizzes = db.execute("SELECT * FROM quizzes ORDER BY created_at DESC").fetchall()
    return render_template("ADMIN/admin_dashboard.html", user=session["username"], quizzes=quizzes)

@app.route("/admin/create_quiz", methods=["GET", "POST"])
def create_quiz():      ## ADMIN CREATE A NEW QUIZ 
    if "username" not in session or session.get("role") !="admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        subject = request.form["subject"]

        db = get_db()
        db.execute("INSERT INTO quizzes (title, subject, created_at) VALUES (?,?,?) ", (title, subject, datetime.datetime.now()))
        db.commit()

        flash("QUIZ CREATED SUCCESSFULLY!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("ADMIN/create_quiz.html", user=session["username"])

@app.route("/admin/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    db = get_db()
    quiz = db.execute("SELECT * FROM quizzes WHERE quiz_id= ?", (quiz_id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        subject = request.form["subject"]

        db.execute("UPDATE quizzes SET title=?, subject=?, updated_at = CURRENT_TIMESTAMP WHERE quiz_id=?", (title, subject, quiz_id))
        db.commit()

        flash("Quiz updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("ADMIN/edit_quiz.html", quiz=quiz, user=session["username"], quiz_id=quiz_id)

@app.route('/question_images/<filename>')
def question_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/admin/<int:quiz_id>/add_question", methods=["GET", "POST"])
def add_question(quiz_id):
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    db = get_db()
    quiz = db.execute("SELECT * FROM quizzes WHERE quiz_id = ?", (quiz_id,)).fetchone()

    if request.method == "POST":
        question = request.form["question_text"]
        q_type = request.form["question_type"]
        image = request.files.get("image")
        image_path = None

        if image and image.filename != "" and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = filename    # <-- ONLY store filename

        a = request.form["option_a"]
        b = request.form["option_b"]
        c = request.form["option_c"]
        d = request.form["option_d"]
        correct_option = request.form["correct_option"]
        integer_answer = request.form.get("integer_answer") or None

        db = get_db()
        db.execute("INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, integer_answer, image_path, question_type) VALUES (?,?,?,?,?,?,?,?,?,?)",
                   (quiz_id, question, a, b, c, d, correct_option, integer_answer, image_path, q_type))
        db.commit()

        flash("Question added successfully!", "success")
        return render_template("ADMIN/add_question.html", quiz_id=quiz_id, user=session["username"], quiz=quiz)
    return render_template("ADMIN/add_question.html", quiz_id=quiz_id, user=session["username"], quiz=quiz)

## SHOW QUIZZES TO USERS AND ALLOW THEM TO ATTEMPT ##
@app.route("/quizzes")
@app.route("/quizzes/<subject>")
def quizzes_by_subject(subject=None):
    if "username" not in session:
        return redirect(url_for("login"))
    db = get_db()

    if subject:
        ## FILTER QUIZZES BY SUBJECT 
        quizzes = db.execute("SELECT * FROM quizzes WHERE subject = ? ORDER BY created_at DESC", (subject,)).fetchall()
    else:
        quizzes = db.execute("SELECT * FROM quizzes ORDER BY created_at DESC").fetchall()

    subjects = db.execute("SELECT DISTINCT subject FROM quizzes").fetchall()
    return render_template("USER/quizzes.html", quizzes=quizzes, subjects=subjects, selected_subject=subject, user=session["username"])


## SUBMIT QUIZ ANSWERS AND CALCULATE SCORE ##
@app.route("/quiz/<int:quiz_id>/submit", methods=["POST"])
def submit_quiz(quiz_id):
    if "username" not in session:
        return redirect(url_for("login"))
    db = get_db()
    quiz = db.execute("SELECT * FROM quizzes WHERE quiz_id = ?", (quiz_id,)).fetchone()
    questions = db.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,)).fetchall()

    score = 0
    results = []


    for i, q in enumerate(questions, start=1):
        q_type = q['question_type']
        correct_option = q['correct_option']
        integer_answer = str(q['integer_answer']) if q['integer_answer'] is not None else None
        user_ans = request.form.get(f'q{i}')
       

        if q['question_type'] == 'mcq':
            if user_ans == correct_option:
                score += 4
                result = "✅ Correct (+4)"
            elif user_ans is None:
                result = "⚪ Not Attempted (0)"
            else:
                score -= 1
                result = "❌ Wrong (-1)"

        elif q['question_type'] == 'integer':
            if user_ans == integer_answer:
                score += 4
                result = "✅ Correct (+4)"
            elif user_ans == "" or user_ans is None:
                result = "⚪ Not Attempted (0)"
            else:
                result = "❌ Wrong (0)"

        results.append({
            'question': q['question_text'],
            'your_answer': user_ans,
            'correct_answer': correct_option if q_type == 'mcq' else integer_answer,
            'result': result
        })

    return render_template("USER/results.html", score=score, results=results, total=len(questions), quiz_id=quiz_id, user=session['username'])




## -------------------- RANK PREDICTION MODEL --------------------##

try:
    rank_df = pd.read_excel(r"C:\Users\Dell\Desktop\JEE-PILOT\JEE DATASET.xlsx")

    # Clean column names
    rank_df.columns = rank_df.columns.str.strip().str.upper()  # Ensure RANK and PERCENTILE names

    # Ensure numeric
    rank_df["RANK"] = pd.to_numeric(rank_df["RANK"], errors="coerce")
    rank_df["PERCENTILE"] = pd.to_numeric(rank_df["PERCENTILE"], errors="coerce")

    # Remove invalid or NaN values
    rank_df.dropna(subset=["RANK", "PERCENTILE"], inplace=True)

    # ✅ Remove any rows where percentile <= 0 or > 100
    rank_df = rank_df[(rank_df["PERCENTILE"] > 0) & (rank_df["PERCENTILE"] <= 100)]

    # Sort by percentile ascending (for correct interpolation)
    rank_df.sort_values("PERCENTILE", inplace=True)
    rank_df.reset_index(drop=True, inplace=True)


except Exception as e:
    print("❌ Error loading rank data:", e)
    rank_df = pd.DataFrame(columns=["RANK", "PERCENTILE"])


# ------------------ PREDICTION FUNCTION ------------------
def predict_rank_from_percentile(percentile: float):
    """Interpolates JEE Rank based on Percentile using cleaned rank_df."""
    if percentile <= 0 or percentile > 100:
        return "⚠️ Percentile must be greater than 0 and less than or equal to 100."

    if rank_df.empty:
        return "⚠️ Rank dataset not loaded properly."

    p = rank_df["PERCENTILE"].to_numpy()
    r = rank_df["RANK"].to_numpy()

    # Clip to range to avoid extrapolation
    percentile = np.clip(percentile, p.min(), p.max())

    # Interpolation (no reverse, since p is ascending)
    predicted_rank = np.interp(percentile, p, r)

    # Return integer rank
    return int(round(predicted_rank))


# ------------------ FLASK ROUTE ------------------
@app.route("/rank_predictor", methods=["GET", "POST"])
def rank_predictor():
    if "username" not in session:
        return redirect(url_for("login"))

    # Initialize variables
    predicted_rank = None
    percentile_input = None
    error_message = None

    if request.method == "POST":
        percentile_str = request.form.get("percentile", "").strip()

        try:
            percentile_input = float(percentile_str)
            percentile_input = round(percentile_input, 3)

            result = predict_rank_from_percentile(percentile_input)

            if isinstance(result, str):
                error_message = result
            else:
                predicted_rank = result

        except ValueError:
            error_message = "⚠️ Please enter a valid number for percentile."

    return render_template(
        "USER/rank_predictor.html",
        rank=predicted_rank,
        percentile=percentile_input,
        error=error_message,
        user=session["username"]
    )




## -------------------- PERCENTILE PREDICTION MODEL --------------------##

# ==========================
# Load and prepare data once
# ==========================
# Make sure this Excel file is in the SAME folder as app.py
EXCEL_PATH = "JEE_Main_2025_Marks_to_Percentile_Complete.xlsx"

df = pd.read_excel(EXCEL_PATH)
# Adjust column names if needed
df.columns = ["Score_Range", "Percentile_Range"]

def range_midpoint(text):
    text = str(text).replace('–', '-').replace('_', '-').replace(' ', '')
    parts = text.split('-')
    if len(parts) == 2:
        try:
            low, high = float(parts[0]), float(parts[1])
            return (low + high) / 2.0
        except:
            return np.nan
    try:
        return float(text)
    except:
        return np.nan

def best_percentile(text):
    text = str(text).replace('–', '-').replace('_', '-').replace(' ', '')
    parts = text.split('-')
    if len(parts) == 2:
        try:
            low, high = float(parts[0]), float(parts[1])
            return max(low, high)
        except:
            return np.nan
    try:
        return float(text)
    except:
        return np.nan

# Convert ranges to numeric marks + percentile
df["Marks"] = df["Score_Range"].apply(range_midpoint)
df["Best_Percentile"] = df["Percentile_Range"].apply(best_percentile)

# Drop invalid rows and sort by marks
df = df.dropna(subset=["Marks", "Best_Percentile"]).sort_values(by="Marks")

# Numpy arrays for interpolation
_marks = df["Marks"].astype(float).values
_pcts = df["Best_Percentile"].astype(float).values

# Ensure sorted (should already be)
sort_idx = np.argsort(_marks)
_marks = _marks[sort_idx]
_pcts = _cts = _pcts[sort_idx]

def interpolate_percentile(marks: float) -> float:
    """
    Interpolate percentile from marks using the table.
    Behaves like your Colab interpolation model.
    """
    # Optional: clip to data range
    x = np.clip(marks, _marks.min(), _marks.max())
    y = np.interp(x, _marks, _pcts)
    return float(y)

@app.route("/predict_percentile", methods=["POST"])
def predict_percentile():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        # Get marks from form
        marks = float(request.form["marks"])

        # 🔥 Use interpolation directly (same as Colab)
        percentile_value = interpolate_percentile(marks)

        # Round to 5 decimal places
        percentile_value = round(percentile_value, 5)

        # Clamp to [0, 100] just in case
        percentile_value = min(max(percentile_value, 0.0), 100.0)

        return render_template(
            "USER/percentile_predictor.html",
            prediction_text=f"Predicted JEE Main Percentile: {percentile_value:.5f}",
            user=session["username"]
        )

    except Exception as e:
        return render_template(
            "USER/percentile_predictor.html",
            prediction_text=f"Error : {str(e)}",
            user=session.get("username")
        )


##--------------------COLLEGE PREDICTION MODEL --------------------##

college_df = pd.read_excel(r"C:\Users\Dell\Desktop\JEE-PILOT\college_advance_datset.xlsx")

@app.route("/college_predictor_filters", methods=["POST"])
def college_predictor_filters():
    data = request.get_json()
    institute_type = data.get("institute_type")

    filtered = college_df[college_df["institute_type"] == institute_type]

    states = sorted(filtered["state"].dropna().unique())
    seat_types = sorted(filtered["seat_type"].dropna().unique())
    genders = sorted(filtered["gender"].dropna().unique())
    programs = sorted(filtered["academic_program_name"].dropna().unique())

    return jsonify( {
        "states":states,
        "seat_types":seat_types,
        "genders":genders,
        "programs":programs
    })

@app.route("/college_predictor", methods=["GET", "POST"])
def college_predictor():
    if "username" not in session:
        return redirect(url_for("login"))
    
    results_table = None
    message = None
    institute_types = sorted(college_df["institute_type"].dropna().unique())

    if request.method == "POST":
        filters = request.form
        institute_type = filters.get("institute_type")
        state = filters.get("state")
        seat_type = filters.get("seat_type")
        gender = filters.get("gender")
        program = filters.get("program")
        user_rank = filters.get("user_rank")

        if not user_rank or not institute_type or institute_type == "All":
            message = "Please provide your rank and select an institute type."
            return render_template("USER/college_predictor.html", user=session["username"], institute_types=institute_types, message=message, table=None)

        try:
            user_rank = int(user_rank)
        except (TypeError,ValueError):
            message = "Please enter a valid numeric rank."
            return render_template("USER/college_predictor.html", user=session["username"], institute_types=institute_types, message=message, table=None)
        

        df = college_df.copy()
        df = df[df["institute_type"] == institute_type]

        if state and state != "All":
            df = df[df["state"] == state]
        if seat_type and seat_type != "All":
            df = df[df["seat_type"] == seat_type]
        if gender and gender != "All":
            df = df[df["gender"] == gender]
        if program and program != "All":
            df = df[df["academic_program_name"] == program]

        df = df[df["closing_rank"] >= user_rank]

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.upper()

        if "opening_rank" in df.columns:
            df["opening_rank"] = df["opening_rank"].astype(float).astype(int)
        if "closing_rank" in df.columns:
            df["closing_rank"] = df["closing_rank"].astype(float).astype(int)

        df = df.sort_values(by="closing_rank", ascending=True).head(20)

        if df.empty:
            message = "No colleges found matching your criteria."
            results_table = None
        else:
            results_table = df.to_html(classes="data-table", index=False)
        
    return render_template("USER/college_predictor.html", user=session["username"], institute_types=institute_types, message=message, table=results_table)

##--------------------COLLEGE RECOMMENDOR--------------------##
    
college_data = pd.read_excel(r"C:\Users\Dell\Desktop\JEE-PILOT\college_advance_datset.xlsx")

@app.route("/college_recommender_filters", methods=["POST"])
def college_recommender_filters():
    data = request.get_json()
    institute_type = data.get("institute_type")

    filtered = college_df[college_df["institute_type"] == institute_type]

    states = sorted(filtered["state"].dropna().unique())
    seat_types = sorted(filtered["seat_type"].dropna().unique())
    genders = sorted(filtered["gender"].dropna().unique())
    programs = sorted(filtered["academic_program_name"].dropna().unique())

    return jsonify( {
        "states":states,
        "seat_types":seat_types,
        "genders":genders,
        "programs":programs
    })

@app.route("/college_recommender", methods=["GET", "POST"])
def college_recommender():
    if "username" not in session:
        return redirect(url_for("login"))
    
    results_table = None
    message = None
    institute_types = sorted(college_df["institute_type"].dropna().unique())

    if request.method == "POST":
        filters = request.form
        institute_type = filters.get("institute_type")
        state = filters.get("state")
        seat_type = filters.get("seat_type")
        gender = filters.get("gender")
        program = filters.get("program")
        

        if not institute_type or institute_type == "All":
            message = "Please select an institute type."
            return render_template("USER/college_predictor.html", user=session["username"], institute_types=institute_types, message=message, table=None)
        
        if not seat_type or seat_type == "All":
            message = "Please select a seat type."
            return render_template("USER/college_predictor.html", user=session["username"], institute_types=institute_types, message=message, table=None)

        

        df = college_df.copy()
        df = df[df["institute_type"] == institute_type]

        if state and state != "All":
            df = df[df["state"] == state]
        if seat_type and seat_type != "All":
            df = df[df["seat_type"] == seat_type]
        if gender and gender != "All":
            df = df[df["gender"] == gender]
        if program and program != "All":
            df = df[df["academic_program_name"] == program]

        

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.upper()

        if "opening_rank" in df.columns:
            df["opening_rank"] = df["opening_rank"].astype(float).astype(int)
        if "closing_rank" in df.columns:
            df["closing_rank"] = df["closing_rank"].astype(float).astype(int)

        df = df[df["opening_rank"] >= 0]

        df = df.sort_values(by="opening_rank", ascending=True).head(20)

        if df.empty:
            message = "No colleges found matching your criteria."
            results_table = None
        else:
            results_table = df.to_html(classes="data-table", index=False)
        
    return render_template("USER/college_recommender.html", user=session["username"], institute_types=institute_types, message=message, table=results_table)


# ------------------ GEMINI CHATBOT INTEGRATION ------------------
load_dotenv()  ## LOAD ENVIRONMENT VARIABLES FROM .env FILE

# Configure Gemini API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

# Use Gemini 2.5 Flash (Fast, Free, Multimodal)
model = genai.GenerativeModel('gemini-2.5-flash')

SYSTEM_PROMPT = """
You are 'NeuroDesk JEE Mentor', an AI assistant inside the JEE Pilot project.

Your main goals:
1. Clear JEE Main and JEE Advanced doubts in Physics, Chemistry, and Mathematics.
2. Explain concepts step by step with clear logic and simple language.
3. When the student lists weak topics and asks for a study plan, create a detailed,
   personalized 7-day study plan (Day 1 to Day 7) focusing on those weak topics.
4. When an image (diagram / question screenshot / full question in image form) is provided,
   carefully read the image and answer using both the image and the text prompt.
5. If the student expresses exam stress, anxiety, burnout, or low motivation, respond kindly:
   - Normalize their feelings (many students feel this way).
   - Give healthy coping strategies: breaks, sleep, exercise, simple routines,
     talking to parents/teachers/friends, journaling, breathing exercises.
   - Encourage them to reach out to a trusted adult or a mental health professional
     for serious or persistent problems.
   - Do NOT give medical advice, do NOT recommend specific medicines,
     and do NOT encourage any form of self-harm.
   - If they mention wanting to hurt themselves, tell them to urgently
     contact a trusted adult or local helpline.

Formatting rules (VERY IMPORTANT):
- Always answer in exam-ready format.
- Use headlines: Given, Step 1, Step 2, Conclusion, etc.
- Do Not show chain-of-thought or exploratory reasoning.
- End with boxed final answer.
- Nver write rough work or internal reasoning.
- Output must be valid HTML, NOT Markdown.
- Use <b>...</b> or <strong>...</strong> for bold text, NEVER **bold**.
- Use <sub> and <sup> for subscripts and superscripts:
  - Example: H<sub>2</sub>O, x<sup>2</sup> + y<sup>2</sup>.
- Use <p> for paragraphs.
- Use <ul><li>...</li></ul> or <ol><li>...</li></ol> for lists.
- When giving a 7-day plan, use an ordered list with <ol> and <li>Day 1...</li>.
- For equations, you may use simple HTML like:
  - F = m &times; a
  - v = u + a &times; t
- Do NOT include Markdown code blocks (```), **, __, or similar.
- The HTML should be clean and minimal so it can be rendered directly with innerHTML.

Content rules:
- Only answer JEE-relevant academic doubts, general study skills, and stress/anxiety support.
- If the student asks about something outside JEE / school-level academics / well-being,
  gently say you are focused on JEE-related help.
"""


chat_history = [
    {"role": "user", "parts": [SYSTEM_PROMPT]},
    {"role": "model", "parts": ["Understood. I am ready to assist as a JEE expert and mentor."]}
]

@app.route('/ai_assistant')
def ai_assistant():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("USER/chatbot.html", user=session["username"])

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('msg')
    image_file = request.files.get('image')

    response_text = ""

    try:
        content_to_send = []
        
        # Add text if present
        if user_input:
            content_to_send.append(user_input)

        # Add image if present
        if image_file:
            img = Image.open(image_file)
            content_to_send.append(img)
            content_to_send.append("Analyze this image and answer the JEE related question within it.")

        if not content_to_send:
            return jsonify({'response': "Please provide text or an image."})

        # Generate response
        # Note: For simple chatbot context, we append to history manually or use chat session
        # Here we use a stateless approach for images + text, but we keep context in the prompt list for text-only flows ideally.
        # For simplicity in this pilot with images, we will generate content directly.
        
        response = model.generate_content(content_to_send)
        response_text = response.text

    except Exception as e:
        response_text = f"**Error:** I encountered an issue: {str(e)}. Please try again."

    return jsonify({'response': response_text})

#----------------FEEDBACK FORM------------------#
@app.route("/send_feedback", methods=["POST"])
def send_feedback():
    if "username" not in session:
        return redirect(url_for("login"))
    name = request.form["name"]
    email = request.form["email"]
    rating = request.form["rating"]
    feedback = request.form["feedback"]

    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "New Feedback - JEE Pilot"

    msg["Reply-To"] = email  # email = users's email from form

    body = f"""
    Name: {name}
    Email: {email}
    Rating: {rating}
    Feedback:{feedback}
    """

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()

    return redirect("/your_feedback")





if __name__ == "__main__":
    app.run(debug=True)
