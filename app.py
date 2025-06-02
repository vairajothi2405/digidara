from flask import Flask, render_template, request, redirect, url_for, session, flash
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # change this in production

# In-memory data store (replace with DB in real use)
submissions = []

# Simple admin credentials (change for production)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/student_submission', methods=['GET', 'POST'])
def student_submission():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name').strip()
        regno = request.form.get('regno').strip()
        course = request.form.get('course').strip()
        department = request.form.get('department').strip()
        provider = request.form.get('provider').strip()
        email = request.form.get('email').strip()
        cert_links = request.form.getlist('certificate_links')

        # Clean links (remove empty)
        cert_links = [link.strip() for link in cert_links if link.strip()]

        if not (name and regno and course and department and provider and email and cert_links):
            flash("Please fill in all fields and provide at least one certificate link.", "error")
            return redirect(url_for('student_submission'))

        # Check if student already submitted before
        found = False
        for s in submissions:
            if s['regno'] == regno and s['name'].lower() == name.lower() and s['email'].lower() == email.lower():
                # Append new links (avoid duplicates)
                for link in cert_links:
                    if link not in s['certificate_links']:
                        s['certificate_links'].append(link)
                found = True
                break
        if not found:
            submissions.append({
                'name': name,
                'regno': regno,
                'course': course,
                'department': department,
                'provider': provider,
                'email': email,
                'certificate_links': cert_links
            })
        flash("Submission successful!", "success")
        return redirect(url_for('student_submission'))

    return render_template("student_submission.html")

@app.route('/student_view', methods=['GET', 'POST'])
def student_view():
    student_data = None
    if request.method == 'POST':
        regno = request.form.get('regno').strip()
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()

        # Find matching submissions
        filtered = []
        for s in submissions:
            if s['regno'].lower() == regno.lower() and s['name'].lower() == name.lower() and s['email'].lower() == email.lower():
                filtered.append(s)

        if filtered:
            # Since regno, name, email are unique per student, combine certificate links
            combined_links = []
            for f in filtered:
                combined_links.extend(f['certificate_links'])
            combined_links = list(set(combined_links))  # remove duplicates

            student_data = {
                'name': name,
                'regno': regno,
                'certificate_links': combined_links
            }
        else:
            flash("No submission found for provided details.", "error")

    return render_template("student_view.html", student=student_data)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_view'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('admin_login'))

    return render_template("admin_login.html")

@app.route('/admin_view')
def admin_view():
    if not session.get('admin_logged_in'):
        flash("Please log in as admin.", "error")
        return redirect(url_for('admin_login'))

    return render_template("admin_view.html", submissions=submissions)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
