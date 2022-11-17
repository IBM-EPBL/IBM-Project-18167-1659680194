from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

app = Flask(__name__)

import ibm_db

hostname = "764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
uid = "qph68689"
pwd = "igr5nkXqgfIHqv7r"
driver = "{IBM DB2 ODBC DRIVER}"
db = "bludb"
port = "32536"
protocol = "TCPIP"
cert = "abc.crt"

dsn = (
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "UID={3};"
    "SECURITY=SSL;"
    "SSLServerCertificate={4};"
    "PWD={5};"
).format(db, hostname, port, uid, cert, pwd)
print(dsn)
try:
    db2 = ibm_db.connect(dsn, "", "")
    print("Connected to data base")
except:
    print("Unable to connect", ibm_db.conn_errormsg())


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/logout')
def logout():
    return render_template('home.html')




@app.route('/dashboard')
def welcome():
    return render_template('dashboard.html')


@app.route('/log-in', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "select * from user where username=? and password=?"
        stmt = ibm_db.prepare(db2, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        dic = ibm_db.fetch_assoc(stmt)
        print(dic)
        if dic:
            msg = username
            return render_template('dashboard.html', msg=msg)
        else:
            msg = "Invalid Username or Password"
            return render_template('signin.html', msg=msg)

    elif request.method == 'GET':
        msg = "Invalid Username or Password"
        return render_template('signin.html', msg=msg)


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['repassword']
        sql = "SELECT * FROM user WHERE username =?"
        stmt = ibm_db.prepare(db2, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('signup.html', msg="Username Already Taken")


        if request.form['password'] == request.form['repassword']:

            sql = "insert into user(username,email,password,repassword) values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(db2, sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.bind_param(prep_stmt, 4, repassword)
            ibm_db.execute(prep_stmt)
            return render_template('signin.html ', msg="Account Created Successfully.")
        else:
            return render_template('signup.html ', msg="Please enter password and repassword correctly")

    elif request.method == 'GET':
        return render_template('signup.html')



if __name__ == '__main__':
    app.run(debug=True)
