from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
app = Flask(__name__)
import ibm_db
hostname = "9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
uid = "wth08341"
pwd = "c8Xk4BUv4Cg6b3SB"
driver = "{IBM DB2 ODBC DRIVER}"
db = "bludb"
port = " 32459"
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
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE username =?"
        stmt = ibm_db.prepare(db2, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template('signup.html', msg="Username Already Taken")
        else:
            sql = "insert into user(username,email,password) values(?,?,?)"
            prep_stmt = ibm_db.prepare(db2, sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            return redirect(url_for('signin'))
@app.route('/login', methods=['POST', 'GET'] )
def login():
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
            return render_template('home.html', msg="WELCOME TO FLASK APPLICATION")
        else:
            msg = "Invalid Username or Password"
            return render_template('signin.html', msg=msg)
    elif request.method == 'GET':
        msg = "Invalid Username or Password"
        return render_template('signin.html', msg=msg)
if __name__ == '__main__':
    app.run(debug=True)