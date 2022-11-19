from turtle import st
from flask import Flask, render_template, request,redirect, url_for, session,flash
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
    conn = ibm_db.connect(dsn, "", "")
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

@app.route('/add-donor')
def adddonor():
    return render_template('adddonor.html')

@app.route('/request_1')
def request_1():
    return render_template('request.html')


@app.route('/dashboard')
def welcome():
    return render_template('dashboard.html')

@app.route('/donor-dashboard')
def donor():
    return render_template('donordashboard.html',msg="WELCOME Donor")

@app.route('/receiver-dashboard')
def receiver():
    return render_template('receiverdashboard.html',msg="WELCOME receiver")


@app.route('/log-in', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "select * from user where username=? and password=?"
        stmt = ibm_db.prepare(conn, sql)
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
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('signup.html', msg="Username Already Taken")


        if request.form['password'] == request.form['repassword']:

            sql = "insert into user(username,email,password,repassword) values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, sql)
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



@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        pin = request.form['pin']
        state = request.form['state']
        country = request.form['country']
        bloodgroup = request.form['bloodgroup']
        command = request.form['command']
        sql = "SELECT * FROM donor WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('donordashboard.html', msg2="You are already registered as a donor")
        else:
            insert_sql = "INSERT INTO donor VALUES (?,?,?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3,email )
            ibm_db.bind_param(prep_stmt, 4, phone)
            ibm_db.bind_param(prep_stmt, 5,street )
            ibm_db.bind_param(prep_stmt, 6, city)
            ibm_db.bind_param(prep_stmt, 7, pin)
            ibm_db.bind_param(prep_stmt, 8,state)
            ibm_db.bind_param(prep_stmt, 9,country )
            ibm_db.bind_param(prep_stmt, 10,bloodgroup )
            ibm_db.bind_param(prep_stmt, 11,command )
            ibm_db.execute(prep_stmt)

        return render_template('donordashboard.html', msg2="Your Data saved successfuly..")


@app.route('/donorlist')
def donorlist():
    donor = []
    sql = "SELECT * FROM donor"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        # print ("The Name is : ",  dictionary)
        donor.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)

    if donor:
        return render_template("list.html", donor=donor)



@app.route('/requestplasma', methods=['POST', 'GET'])
def requestplasma():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        gender=request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        bloodgroup=request.form['bloodgroup']
        street = request.form['street']
        city = request.form['city']
        region=request.form['region']
        pin = request.form['pin']
        state = request.form['state']
        country = request.form['country']
        hoscity = request.form['hoscity']
        hosregion=request.form['hosregion']
        hospin = request.form['hospin']
        hosstate = request.form['hosstate']
        hoscountry = request.form['hoscountry']
        sql = "SELECT * FROM receivers WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('receiverdashboard.html', msg2="You are already requested")
        else:
            insert_sql = "INSERT INTO receivers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, gender)
            ibm_db.bind_param(prep_stmt, 4, bloodgroup)
            ibm_db.bind_param(prep_stmt, 5,email )
            ibm_db.bind_param(prep_stmt, 6, phone)
            ibm_db.bind_param(prep_stmt, 7,street )
            ibm_db.bind_param(prep_stmt, 8, city)
            ibm_db.bind_param(prep_stmt, 9, region)
            ibm_db.bind_param(prep_stmt, 10, pin)
            ibm_db.bind_param(prep_stmt, 11,state)
            ibm_db.bind_param(prep_stmt, 12,country )
            ibm_db.bind_param(prep_stmt, 13, hoscity)
            ibm_db.bind_param(prep_stmt, 14, hosregion)
            ibm_db.bind_param(prep_stmt, 15, hospin)
            ibm_db.bind_param(prep_stmt, 16,hosstate)
            ibm_db.bind_param(prep_stmt, 17,hoscountry )
            ibm_db.execute(prep_stmt)
        return render_template('receiverdashboard.html', msg2="Plasma Requested Successfully")

# @app.route('/requestlist')
# def requestlist():
#     receivers = []
#     sql = "SELECT * FROM receivers"
#     stmt = ibm_db.exec_immediate(conn, sql)
#     dictionary = ibm_db.fetch_both(stmt)
#     while dictionary != False:
#         # print ("The Name is : ",  dictionary)
#         receivers.append(dictionary)
#         dictionary = ibm_db.fetch_both(stmt)

#     if receivers:
#         return render_template("donordashboard.html", receivers=receivers)



@app.route('/requestlist')
def requestlist():
    receiver = []
    sql = "SELECT * FROM receivers"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        # print ("The Name is : ",  dictionary)
        receiver.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)

    if receiver:
        return render_template("donordashboard.html", req=receiver)

@app.route('/delete/<name>')
def delete(name):
    sql = f"SELECT * FROM Students WHERE name='{escape(name)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    student = ibm_db.fetch_row(stmt)
    print("The Name is : ", student)
    if student:
        sql = f"DELETE FROM Students WHERE name='{escape(name)}'"
        print(sql)
        stmt = ibm_db.exec_immediate(db2, sql)

        students = []
        sql = "SELECT * FROM Students"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            students.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)
        if students:
            return render_template("list.html", students=students, msg="student detail Deleted successfully")


if __name__ == '__main__':
    app.run(debug=True)


