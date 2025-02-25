from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash
from hashlib import sha256
import sqlite3 


app = Flask(__name__)
app.secret_key = "your_secret_key"

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
       
        hashed_password = sha256(password.encode('utf-8')).hexdigest()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE Email=? AND Password=?",
                    (email, hashed_password))
        row = cursor.fetchall()
        print (row)
        print (hashed_password)
        if len(row) == 1:
            return row
        else:
            return "invalid login"
        

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

        
        hashed_password = sha256(password.encode('utf-8')).hexdigest()

        try:
            conn = connect_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM User WHERE Email=?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                conn.close()
                return render_template('signup.html', email_exists=True, email=email)
            
            cursor.execute("INSERT INTO User (Name, Surname, Email, Password, DateOfBirth) VALUES (?, ?, ?, ?, ?)",(name, surname, email, hashed_password, dateofbirth))
            conn.commit()
            conn.close()
            print ("Signup succesful! You can now log in.", "success")
            return redirect('/')
        except sqlite3.IntegrityError:
            print ("Email allready exists. Please use a different email")

# @app.route("/check_email", methods=['POST'])
# def check_email():
#     email = request.json.get("email")  # Get email from frontend
    
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM User WHERE Email=?", (email,))
#     existing_user = cursor.fetchone()
#     conn.close()
    
#     if existing_user:
#         return jsonify({"exists": True})  # Send response to frontend
#     else:
#         return jsonify({"exists": False})


if __name__ == '__main__':
    app.run(debug=True)


