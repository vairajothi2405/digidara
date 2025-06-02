from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this for security in production!

# Store all submissions in memory for now (will reset if server restarts)
submissions = []

# Simple admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

@app.route('/')
def home():
    
    return render_template("home.html")

@app.route('/student_submission', methods=['GET', 'POST'])
def student_submission():
    if request.method == 'POST':
        # Collect form data from student submission page
        name = request.form.get('name', '').strip()
        regno = request.form.get('regno', '').strip()
        course = request.form.get('course', '').strip()
        department = request.form.get('department', '').strip()
        provider = request.form.get('provider', '').strip()
        email = request.form.get('email', '').strip()
        certificate_links = request.form.getlist('certificate_links')

        # Clean certificate links by removing empty entries and stripping whitespace
        certificate_links = [link.strip() for link in certificate_links if link.strip()]

        # Basic validation: Check if all required fields are filled
        if not (name and regno and course and department and provider and email and certificate_links):
            flash("Please fill all fields and provide at least one certificate link.", "error")
            return redirect(url_for('student_submission'))

        # Check if this student (by regno, name, email) already has submissions
        found = False
        for entry in submissions:
            if (entry['regno'].lower() == regno.lower() and
                entry['name'].lower() == name.lower() and
                entry['email'].lower() == email.lower()):
                # Add new certificate links to existing submission if not duplicate
                for link in certificate_links:
                    if link not in entry['certificate_links']:
                        entry['certificate_links'].append(link)
                found = True
                break

        # If student not found in submissions, add new record
        if not found:
            submissions.append({
                'name': name,
                'regno': regno,
                'course': course,
                'department': department,
                'provider': provider,
                'email': email,
                'certificate_links': certificate_links
            })

        flash("Your certificate submission was successful!", "success")
        return redirect(url_for('student_submission'))

    # For GET request, just show the submission form
    return render_template("student_submission.html")

@app.route('/student_view', methods=['GET', 'POST'])
def student_view():
    student_data = None

    if request.method == 'POST':
        regno = request.form.get('regno', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        # Find submission matching the student's regno, name, and email
        for entry in submissions:
            if (entry['regno'].lower() == regno.lower() and
                entry['name'].lower() == name.lower() and
                entry['email'].lower() == email.lower()):
                student_data = {
                    'name': entry['name'],
                    'regno': entry['regno'],
                    'certificate_links': entry['certificate_links']
                }
                break

        if not student_data:
            flash("No submissions found for the given details.", "error")

    # Show the student view page with data if found
    return render_template("student_view.html", student=student_data)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Simple check against stored admin credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_view'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('admin_login'))

    return render_template("admin_login.html")

@app.route('/admin_view')
def admin_view():
    # Only allow access if admin is logged in
    if not session.get('admin_logged_in'):
        flash("Please log in as admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    # Show all student submissions to admin
    return render_template("admin_view.html", submissions=submissions)

@app.route('/logout')
def logout():
    # Log out the admin
    session.pop('admin_logged_in', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
