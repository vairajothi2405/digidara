from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import mysql.connector
import random, string

app = Flask(__name__)
app.secret_key = "secret123"
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------- Database ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="quiz__db"
)
cursor = db.cursor(dictionary=True)

# ---------------- Global Memory ----------------
students = {}   # quiz students
players = {}    # admin dashboard live players

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("welcome.html")

# ================= ADMIN LOGIN =================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_home"))
        else:
            return render_template("admin_login.html",
                                   error="Invalid username or password")

    return render_template("admin_login.html")

# ---------------- ADMIN HOME ----------------
@app.route("/admin/home")
def admin_home():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin_home.html")

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin_dashboard.html")

# ---------------- ADD QUESTION ----------------
@app.route("/admin/add-question", methods=["GET", "POST"])
def add_question():
    # Check if admin logged in
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    # Get categories from DB for dropdown
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()  # List of dicts: [{'id':1, 'name':'Maths'}, ...]

    if request.method == "POST":
        # Get form values
        category_name = request.form.get("category")  # name from dropdown
        age_group = request.form.get("age_group")
        question = request.form.get("question")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct = request.form.get("correct")

        # ------------------- Validation -------------------
        if not all([category_name, age_group, question, option1, option2, option3, option4, correct]):
            return render_template("add_question.html",
                                   categories=categories,
                                   error="All fields are required")

        # ------------------- Get category_id -------------------
        cursor.execute("SELECT id FROM categories WHERE name=%s", (category_name,))
        cat = cursor.fetchone()
        if not cat:
            return render_template("add_question.html",
                                   categories=categories,
                                   error="Invalid category selected")
        category_id = cat["id"]
        # 🔍 Duplicate question check
        cursor.execute("""
             SELECT id FROM questions
             WHERE category_id = %s
             AND question_text = %s
             AND age_group = %s
        """, (category_id, question, age_group))

        existing = cursor.fetchone()

        if existing:
             return render_template(
                   "add_question.html",
                    categories=categories,
                    error="⚠ This question already exists!"
             )
        # ------------------- Insert into DB -------------------
        cursor.execute("""
            INSERT INTO questions
            (category_id, question_text, option1, option2, option3, option4, correct_option, age_group)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (category_id, question, option1, option2, option3, option4, correct, age_group))
        db.commit()

        return render_template("add_question.html",
                               categories=categories,
                               success="Question added successfully ✅")

    # GET request → render form
    return render_template("add_question.html", categories=categories)

# ---------------- ADMIN LOGOUT ----------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

# ======================================================
# ================= STUDENT JOIN ========================

@app.route("/join", methods=["GET", "POST"])
def join():
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if request.method == "POST":
        name = request.form.get("name")
        category_age = request.form.get("category_age")

        if not name:
            return render_template("join.html",
                                   categories=categories,
                                   error_name="Enter name",
                                   error_category=None)

        if not category_age or "|" not in category_age:
            return render_template("join.html",
                                   categories=categories,
                                   error_name=None,
                                   error_category="Select category & age")

        category_name, age_group = category_age.split("|")

        cursor.execute("SELECT id FROM categories WHERE name=%s", (category_name,))
        cat = cursor.fetchone()
        if not cat:
            return render_template("join.html",
                                   categories=categories,
                                   error_category="Invalid category")

        cursor.execute("""
            SELECT * FROM questions
            WHERE category_id=%s AND age_group=%s
        """, (cat["id"], age_group))
        questions = cursor.fetchall()

        if not questions:
            return render_template("join.html",
                                   categories=categories,
                                   error_category="No questions available")

        sid = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        session["sid"] = sid

        students[sid] = {
            "name": name,
            "category": category_name,
            "age_group": age_group,
            "score": 0,
            "current_question": 0,
            "questions": questions
        }

        return redirect(url_for("quiz"))

    return render_template("join.html", categories=categories)

@app.route("/quiz")
def quiz():
    if "sid" not in session or session["sid"] not in students:
        return redirect(url_for("join"))
    return render_template("quiz.html")

# ======================================================
# ================= SOCKET EVENTS =======================

@socketio.on("join_quiz")
def join_quiz():
    sid = session.get("sid")
    student = students.get(sid)
    if not student:
        return

    # ADD TO ADMIN DASHBOARD
    players[sid] = {
        "name": student["name"],
        "category": student["category"],
        "score": 0
    }
    emit("update_admin", players, broadcast=True)

    student["current_question"] = 0
    random.shuffle(student["questions"])
    q = student["questions"][0]

    options = [q["option1"], q["option2"], q["option3"], q["option4"]]
    random.shuffle(options)

    emit("new_question", {
        "qno": 1,
        "question": q["question_text"],
        "options": options,
        "time": 10,
        "score": 0
    })

@socketio.on("submit_answer")
def submit_answer(data):
    sid = session.get("sid")
    student = students.get(sid)
    if not student:
        return

    q = student["questions"][student["current_question"]]
    selected = data.get("answer", "")
    time_left = data.get("time_left", 0)

    earned = round(10 * (time_left / 10)) if selected == q["correct_option"] else 0
    student["score"] += earned

    players[sid]["score"] = student["score"]
    emit("update_admin", players, broadcast=True)

    emit("answer_result", {
        "correct": q["correct_option"],
        "selected": selected,
        "score": student["score"]
    })

    socketio.sleep(1.5)

    student["current_question"] += 1
    idx = student["current_question"]

    if idx >= len(student["questions"]):
        emit("quiz_finished", {"final_score": student["score"]})
        players.pop(sid, None)
        emit("update_admin", players, broadcast=True)
        return

    q = student["questions"][idx]
    options = [q["option1"], q["option2"], q["option3"], q["option4"]]
    random.shuffle(options)

    emit("new_question", {
        "qno": idx + 1,
        "question": q["question_text"],
        "options": options,
        "time": 10,
        "score": student["score"]
    })

# ======================================================

if __name__ == "__main__":
    socketio.run(app, debug=True)