from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from hashlib import sha256
import sqlite3 

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.secret_key = 'your_secret_key'

db = "database.db"

def connect_db():
     return sqlite3.connect(db)

@app.route("/", methods = ['POST', 'GET'])
def index():
        print("Rendering index page")
        if request.method == 'GET':
            return render_template('index.html', USER_ID = session.get("email"))  

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
       
        #session["email"] = request.form.get("email")

        hashed_password = sha256(password.encode('utf-8')).hexdigest() 

        #print("Session data after login:", session)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE Email=? AND Password=?",
                     (email, hashed_password))
        row = cursor.fetchall()

        print("database data", email, hashed_password)

        if len(row) == 1:
            
            session['user_id'] = row[0][0]
            session['name'] = row[0][1]
            session['surname'] = row[0][2]
            session['email'] = row[0][3]
            session['dateofbirth'] = row[0][5]
            
            print("Session data after login:", session)

            return redirect("/")    
        
        else:
            return redirect("/login")
        
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


@app.route("/progress")
def progress():
        return render_template('progress.html')

@app.route("/calorieTracking")
def calorieTracking():
        return render_template('calorieTracking.html')

@app.route("/calorieEntering", methods = ['POST', 'GET'])
def calorieEntering():
    if request.method == 'GET':
        return render_template('calorieEntering.html')
    
    else:
        calories = request.form['calories']
        date = request.form['date']

        conn = connect_db()
        cursor = conn.cursor()
        
        USER_ID = session.get("user_id")
        
        #cursor.execute("INSERT INTO calorieIntake (Calorie, DateCalorieIn) VALUES (?, ?)", (calories, date))
        cursor.execute("INSERT INTO calorieIntake (USER_ID, Calorie, DateCalorieIn) VALUES (?, ?, ?)", (USER_ID, calories, date))

        conn.commit()
        conn.close()  
        print ("Calories succesfully logged.", "success")
        return redirect('/')
    

@app.route("/logout")
def logout(): 
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True) 


