from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import mysql.connector
import random, string,threading

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

# ---------------- Global Students ----------------
# session_id -> {name, category, age_group, score, current_question, questions}
students = {}
players={}

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("welcome.html")


# ================= ADMIN LOGIN ROUTES =================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # TEMP login
        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template(
                "admin_login.html",
                error="Invalid username or password"
            )

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin_dashboard.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

# ======================================================    

@app.route("/join", methods=["GET", "POST"])
def join():
    # Fetch categories for dropdown
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if request.method == "POST":
        name = request.form.get("name")
        category_age = request.form.get("category_age")  # e.g., "Maths|10-15"

        # ------------------- Name validation -------------------
        if not name or name.strip() == "":
            return render_template("join.html", categories=categories,
                                   error_name="Please enter your name",
                                   error_category=None)

        # ------------------- Category + Age validation -------------------
        if not category_age or "|" not in category_age:
            return render_template("join.html", categories=categories,
                                   error_name=None,
                                   error_category="Please select category and age")

        # ------------------- Split category & age -------------------
        try:
            category_name, age_group = category_age.split("|")
        except ValueError:
            return render_template("join.html", categories=categories,
                                   error_name=None,
                                   error_category="Invalid category selected")

        # ------------------- Get category_id from DB -------------------
        cursor.execute("SELECT id FROM categories WHERE name=%s", (category_name,))
        cat = cursor.fetchone()
        if not cat:
            return render_template("join.html", categories=categories,
                                   error_name=None,
                                   error_category="Selected category does not exist")
        category_id = cat["id"]

        # ------------------- Load questions -------------------
        cursor.execute("""
            SELECT * FROM questions
            WHERE category_id = %s AND age_group = %s
        """, (category_id, age_group))
        questions = cursor.fetchall()

        if not questions:
            return render_template("join.html", categories=categories,
                                   error_name=None,
                                   error_category="No questions available for this category/age")

        # ------------------- Create session -------------------
        session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        session["sid"] = session_id
        session["name"] = name
        session["category"] = category_name
        session["age_group"] = age_group

        # ------------------- Save student in-memory -------------------
        students[session_id] = {
            "name": name,
            "category": category_name,
            "age_group": age_group,
            "score": 0,
            "current_question": 0,
            "questions": questions
        }

        # ------------------- Redirect to quiz -------------------
        return redirect(url_for("quiz"))

    # ------------------- GET request -------------------
    return render_template("join.html", categories=categories,
                           error_name=None, error_category=None)


@app.route("/quiz")
def quiz():
    if "sid" not in session or session["sid"] not in students:
        return redirect(url_for("join"))
    return render_template("quiz.html")


# ------------------- Socket.IO Events -------------------
@socketio.on("join_quiz")
def join_quiz():
    sid = session.get("sid")
    student = students.get(sid)

    if not student:
        return

    student["current_question"] = 0
    random.shuffle(student["questions"])
    q = student["questions"][0]

    options= [q["option1"], q["option2"], q["option3"], q["option4"]]
    random.shuffle(options)

    emit("new_question", {
        "qno": 1,
        "question": q["question_text"],
        "options": options,
        "time": 10,
        "score": student["score"]

    })


@socketio.on("submit_answer")
def submit_answer(data):
    sid = session.get("sid")
    student = students.get(sid)

    idx = student["current_question"]
    q = student["questions"][idx]

    selected = data.get("answer", "")
    time_left = data.get("time_left", 0)
    total_time=10
    max_score=10
    earned_score=round(max_score*(time_left/total_time)) if selected else 0
    correct = q["correct_option"]

    if selected == q["correct_option"]:
        student["score"]+=earned_score
    else:
        earned_score=0    

    emit("answer_result", {
        "correct": correct,
        "selected": selected,
        "score": student["score"]
    })

    socketio.sleep(2)

    student["current_question"] += 1
    idx = student["current_question"]

    if idx >= len(student["questions"]):
        emit("quiz_finished", {
            "final_score": student["score"]
        })
        return

    q = student["questions"][idx]
    options= [q["option1"], q["option2"], q["option3"], q["option4"]]
    random.shuffle(options)

    emit("new_question", {
        "qno": idx + 1,
        "question": q["question_text"],
        "options": options,
        "time": 10,
        "score": student["score"]
    })   


    
if __name__ == "__main__":
    socketio.run(app, debug=True)