from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecret'  


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='Dhanush@1' 
app.config['MYSQL_DB'] = 'certification_tracker'

mysql = MySQL(app)

@app.route('/vhome')
def homepage():
    return render_template('vhome.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_cert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        department = request.form['department']
        aadhar = request.form['aadhar']
        regno = request.form['regno']
        provider = request.form['provider']
        certlink = request.form['certlink']
        certdate = request.form['certdate']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO certificates (student_name, email, course_name, department, aadhar, regno, provider, certificate_link, cert_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, email, course, department, aadhar, regno, provider, certlink, certdate))
        mysql.connection.commit()
        cur.close()
        return redirect(f'/student_dashboard?regno={regno}')
    return render_template('submit.html')


# Route 2: Student Dashboard
@app.route('/student_dashboard')
def student_dashboard():
    regno = request.args.get('regno')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM certificates WHERE regno = %s", (regno,))
    student = cur.fetchone()
    cur.close()
    return render_template('my_certificate.html', student=student)


# Route 3: Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect('/admin_dashboard')
        else:
            flash('Invalid credentials')
    return render_template('admin.html')


# Route 4: Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin_login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM certificates ORDER BY department DESC")
    certs = cur.fetchall()
    cur.close()
    return render_template('admin_certificate.html', students=certs)


# Route 5: Logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin_login')




if __name__ == '__main__':
    app.run(debug=True)