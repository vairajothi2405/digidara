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

# ---------------- Routes ----------------
@app.route("/")
def index():
    return redirect(url_for("join"))

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
    if not sid or sid not in students:
        return

    student = students[sid]
    send_next_question(student)


def send_next_question(student):
    cq_index = student["current_question"]
    if cq_index >= len(student["questions"]):
        emit("quiz_finished", {"final_score": student["score"]})
        return

    question = student["questions"][cq_index]
    options = [question["option1"], question["option2"], question["option3"], question["option4"]]
    random.shuffle(options)

    emit("new_question", {
        "qno": cq_index + 1,
        "question": question["question_text"],
        "options": options,
        "time": 15  # seconds per question
    })


@socketio.on("submit_answer")
def submit_answer(data):
    sid = session.get("sid")
    if not sid or sid not in students:
        return

    student = students[sid]
    cq_index = student["current_question"]
    question = student["questions"][cq_index]

    selected = data.get("answer", "")
    time_taken = int(data.get("time_taken", 15))

    correct = question["correct_option"]
    score_increment = max(0, 10 - time_taken) if selected == correct else 0
    student["score"] += score_increment

    emit("answer_result", {"correct": correct, "selected": selected, "score": student["score"]},room=request.sid)

    # Move to next question
    student["current_question"] += 1
    send_next_question(student)

@socketio.on("submit_answer")
def handle_answer(data):
    sid = request.sid  # unique socket for student
    if sid not in students:
        return
    
    student = students[sid]
    q_index = student["current_question"]
    
    # Get current question
    question = student["questions"][q_index]
    
    selected = data.get("answer")
    correct = question["correct_option"]
    time_taken = data.get("time_taken", 0)
    
    # Score calculation (speed-based)
    if selected == correct:
        student["score"] += max(0, 10 - time_taken)  # 10 marks max minus seconds taken
    
    # Emit result to that student ONLY
    emit("answer_result", {
        "selected": selected,
        "correct": correct,
        "score": student["score"]
    }, room=sid)
    
    # Move to next question
    student["current_question"] += 1
    
    if student["current_question"] < len(student["questions"]):
        next_q = student["questions"][student["current_question"]]
        emit("new_question", {
            "qno": student["current_question"] + 1,
            "question": next_q["question_text"],
            "options": [
                next_q["option1"], next_q["option2"],
                next_q["option3"], next_q["option4"]
            ],
            "time": 15  # seconds
        }, room=sid)
    else:
        # Quiz finished
        emit("quiz_finished", {
            "final_score": student["score"]
        }, room=sid)   

    


if __name__ == "__main__":
    socketio.run(app, debug=True)