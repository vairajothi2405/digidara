from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Dhanush@1',
    'database': 'certification_tracker'
}

@app.route('/vhome')
def home():
    return render_template('vhome.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['email'],
            request.form['course'],
            request.form['department'],
            request.form['aadhar'],
            request.form['regno'],
            request.form['provider'],
            request.form['certlink'],
            request.form['certdate']
        )
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO certificates (name, email, course, department, aadhar, regno, provider, certlink, certdate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)
        conn.commit()
        cursor.close()
        conn.close()
        session['student_email'] = request.form['email']
        return redirect(url_for('my_certificate'))
    return render_template('submit.html')

@app.route('/my_certificate')
def my_certificate():
    email = session.get('student_email')
    if not email:
        return redirect(url_for('submit'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certificates WHERE email = %s", (email,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('my_certificate.html', student=student)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin:
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials")
    return render_template('admin.html')

@app.route('/admin_certificate')
def admin_certificate():
    if 'admin' not in session:
        return redirect(url_for('admin'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certificates")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_certificate.html', students=students)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('vhome')) 

if __name__ == '__main__':
    app.run(debug=True)