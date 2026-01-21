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

# ---------------- Global Students ----------------
# session_id -> student details
students = {}

# ---------------- Admin Live Players ----------------
# session_id -> {name, category, score}
players = {}

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

        # TEMP admin login
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

# ================= JOIN QUIZ =================

@app.route("/join", methods=["GET", "POST"])
def join():
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if request.method == "POST":
        name = request.form.get("name")
        category_age = request.form.get("category_age")

        if not name:
            return render_template("join.html", categories=categories,
                                   error_name="Enter your name",
                                   error_category=None)

        if not category_age or "|" not in category_age:
            return render_template("join.html", categories=categories,
                                   error_name=None,
                                   error_category="Select category & age")

        category_name, age_group = category_age.split("|")

        cursor.execute("SELECT id FROM categories WHERE name=%s", (category_name,))
        cat = cursor.fetchone()
        if not cat:
            return render_template("join.html", categories=categories,
                                   error_name=None,
                                   error_category="Invalid category")

        cursor.execute("""
            SELECT * FROM questions
            WHERE category_id=%s AND age_group=%s
        """, (cat["id"], age_group))
        questions = cursor.fetchall()

        if not questions:
            return render_template("join.html", categories=categories,
                                   error_name=None,
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

    return render_template("join.html", categories=categories,
                           error_name=None, error_category=None)


@app.route("/quiz")
def quiz():
    if "sid" not in session or session["sid"] not in students:
        return redirect(url_for("join"))
    return render_template("quiz.html")

# ================= SOCKET EVENTS =================

@socketio.on("join_quiz")
def join_quiz():
    sid = session.get("sid")
    student = students.get(sid)
    if not student:
        return

    # ADMIN LIVE JOIN
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

    idx = student["current_question"]
    q = student["questions"][idx]

    selected = data.get("answer", "")
    time_left = data.get("time_left", 0)

    total_time = 10
    max_score = 10
    earned_score = round(max_score * (time_left / total_time)) if selected else 0

    if selected == q["correct_option"]:
        student["score"] += earned_score

    # UPDATE ADMIN SCORE LIVE
    if sid in players:
        players[sid]["score"] = student["score"]
        emit("update_admin", players, broadcast=True)

    emit("answer_result", {
        "correct": q["correct_option"],
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

        # REMOVE FROM ADMIN LIST
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


@socketio.on("disconnect")
def handle_disconnect():
    sid = session.get("sid")
    if sid in players:
        players.pop(sid, None)
        emit("update_admin", players, broadcast=True)

# ================= RUN =================

if __name__ == "__main__":
    socketio.run(app, debug=True)