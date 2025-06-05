from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'  # Change this
app.config['MYSQL_DB'] = 'cert_tracker_db'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/student_submission', methods=['GET', 'POST'])
def student_submission():
    if request.method == 'POST':
        name = request.form['name'].strip()
        regno = request.form['regno'].strip()
        course = request.form['course'].strip()
        department = request.form['department'].strip()
        provider = request.form['provider'].strip()
        email = request.form['email'].strip()
        certificate_links = [link.strip() for link in request.form.getlist('certificate_links') if link.strip()]

        if not (name and regno and course and department and provider and email and certificate_links):
            flash("Please fill all fields and provide at least one certificate link.", "error")
            return redirect(url_for('student_submission'))

        cur = mysql.connection.cursor()

        # Verify student
        cur.execute("SELECT * FROM students WHERE regno = %s AND email = %s", (regno, email))
        student = cur.fetchone()

        if not student:
            flash("You are not a registered student. Submission denied.", "error")
            cur.close()
            return redirect(url_for('student_submission'))

        for link in certificate_links:
            cur.execute("""
                INSERT INTO student_certificates 
                (name, regno, course, department, provider, email, certificate_link)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, regno, course, department, provider, email, link))

        mysql.connection.commit()
        cur.close()

        flash("Your certificate submission was successful!", "success")
        return redirect(url_for('student_submission'))

    return render_template("student_submission.html")

@app.route('/student_view', methods=['GET', 'POST'])
def student_view():
    student_data = []

    if request.method == 'POST':
        regno = request.form['regno'].strip().lower()
        name = request.form['name'].strip().lower()
        email = request.form['email'].strip().lower()

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT name, regno, certificate_link
            FROM student_certificates
            WHERE LOWER(name) = %s AND LOWER(regno) = %s AND LOWER(email) = %s
        """, (name, regno, email))

        student_data = cur.fetchall()
        cur.close()

        if not student_data:
            flash("No submissions found for the given details.", "error")

    return render_template("student_view.html", student=student_data)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin_users WHERE username = %s AND password = %s", (username, password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_view'))
        else:
            flash("Invalid username or password.", "error")

    return render_template("admin_login.html")

@app.route('/admin_view')
def admin_view():
    if not session.get('admin_logged_in'):
        flash("Please log in as admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student_certificates ORDER BY regno")
    all_data = cur.fetchall()
    cur.close()

    return render_template("admin_view.html", submissions=all_data)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
