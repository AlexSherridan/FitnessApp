from cs50 import SQL
from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
import sqlite3


app = Flask(__name__)
app.secret_key = "your_secret_key"

db2 = SQL("sqlite:///database.db")
db = "database.db"

def connect_db():
    return sqlite3.connect(db)

@app.route("/", methods = ['POST', 'GET'])
def index():
        return render_template('index.html')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        #UserInfo  = db2.execute("SELECT * FROM User WHERE Email = email")
        cmdString = "SELECT * FROM User WHERE Email = email"
        cmdString2 = "SELECT * FROM User WHERE Email ='" + email + "'"
        print(cmdString)
        print(cmdString2)
        UserInfo  = db2.execute(cmdString2)
        #UserInfo  = db2.execute("SELECT * FROM User WHERE Email = email ")
        InfoList = UserInfo[0]
        hashed_password = generate_password_hash(password)
        hashed_password2 = generate_password_hash(password)
        print("Email: " + email)
        print (InfoList)
        print (hashed_password)
        print (hashed_password2)
        print (InfoList["Name"])
        print (InfoList["Surname"])
        print (InfoList["Password"])
        if hashed_password == InfoList["Password"]:
            return 'welcome ' + InfoList["Name"]

        else:
            return 'User not found'


@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        dateofbirth = request.form['dob']

        hashed_password = generate_password_hash(password)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO User (Name, Surname, Email, Password, DateOfBirth) VALUES (?, ?, ?, ?, ?)",(name, surname, email, hashed_password, dateofbirth))
            conn.commit()
            conn.close()
            flash("Signup succesful! You can now log in.", "success")
            return redirect('/')
        except sqlite3.IntegrityError:
            flash("Email allready exists. Please use a different email")

if __name__ == '__main__':
    app.run(debug=True)


