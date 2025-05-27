from flask import Flask,render_template,request,redirect 
from flask_mysqldb import MySQL
certificate=Flask(__name__)
certificate.config['MYSQL__HOST']='localhost'
certificate.config['MYSQL__USER']='root'
certificate.config['MYSQL__PASSWORD']='yourpassword'
certificate.config['MYSQL__DB']='certificate'

mysql=MySQL(certificate)

@certificate.route('/submit',methods=['GET','POST'])
def submit_cert():
    if request.method=='POST':
        name=request.form['student_name']
        email=request.form['email']
        course=request.form['course_name']
        provider=request.form['provider']
        link=request.form['certificate_link']

        cur=mysql.connection.cursor()
        cur.execute('''
           INSERT INTO cert_tracker_db(student_name,email,course,provider,certificate_link)VALUES(%s,%s,%s,%s,%s)''',(name,email,course,provider,link))
        mysql.connection.commit()
        return redirect(f'/my_certifications?email={email}')
    return render_template('submit_certification.html')   

@certificate.route('/my_certifications')
def my_certifications():
    email=request.args.get('email')
    cur=mysql.connection.cursor()
    cur.execute("SELECT*FROM cert_tracker_db WHERE email=%s",(email))
    certs=cur.fetchall()
    return render_template('my_certifications.html',certs=certs,email=email)   

@certificate.route('/admin')
def admin_certifications():
    cur=mysql.connection.cursor()
    cur.execute("SELECT *FROM cert_tracker_db ORDER BY submitted_on DESC")
    all_certs=cur.fetchall()
    return render_template('admin_certifications.html',certs=all_certs)     

if(__name__)=='__main__':
    certificate.run()                                 
                                     