from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Used for sessions and flash messages

# Sample in-memory storage (you can later replace this with a database)
students = []  # Stores student submissions
admins = {'admin': 'password123'}  # Simple admin login (username: admin, password: password123)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Student submission page
@app.route('/student_submission', methods=['GET', 'POST'])
def student_submission():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        regno = request.form['regno']
        course = request.form['course']
        department = request.form['department']
        provider = request.form['provider']
        email = request.form['email']
        links = request.form.getlist('certificate_links')

        # Check if student already submitted
        found = False
        for student in students:
            if student['regno'] == regno and student['email'] == email:
                # Add new links to existing student
                student['links'].extend([link for link in links if link not in student['links']])
                found = True
                break

        # Add new student if not found
        if not found:
            students.append({
                'name': name,
                'regno': regno,
                'course': course,
                'department': department,
                'provider': provider,
                'email': email,
                'links': links
            })

        flash("Certificate submitted successfully!")
        return redirect(url_for('student_submission'))

    return render_template('student_submission.html')

# Student view page
@app.route('/student_view', methods=['GET', 'POST'])
def student_view():
    student_data = None

    if request.method == 'POST':
        regno = request.form['regno']
        name = request.form['name']
        email = request.form['email']

        for student in students:
            if student['regno'] == regno and student['name'] == name and student['email'] == email:
                student_data = student
                break

        if not student_data:
            flash("Student not found!")

    return render_template('student_view.html', student=student_data)

# Admin login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if admins.get(username) == password:
            session['admin'] = username
            return redirect(url_for('admin_view'))
        else:
            flash("Invalid credentials!")

    return render_template('admin_login.html')

# Admin view page
@app.route('/admin_view')
def admin_view():
    if 'admin' not in session:
        flash("Please log in as admin first.")
        return redirect(url_for('admin_login'))
    return render_template('admin_view.html', students=students)

# Admin logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
