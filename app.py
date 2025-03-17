from flask import Flask, render_template, request, redirect, session, jsonify
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


# @app.route("/calorieEntering", methods = ['POST', 'GET'])
# def calorieEntering():
#     if request.method == 'GET':
#         return render_template('calorieEntering.html')
    
#     else:
#         calories = request.form['calories']
#         date = request.form['date']

#         conn = connect_db()
#         cursor = conn.cursor()
        
#         USER_ID = session.get("user_id")
        
#         cursor.execute("INSERT INTO calorieIntake (USER_ID, Calorie, DateCalorieIn) VALUES (?, ?, ?)", (USER_ID, calories, date))

#         conn.commit()
#         conn.close()  
#         print ("Calories succesfully logged.", "success")
#         return redirect('/')

@app.route("/calorieEntering", methods=['POST', 'GET'])
def calorieEntering():
    if request.method == 'GET':
        return render_template('calorieEntering.html')


    else:
        calories = request.form['calories']
        date = request.form['date']

        conn = connect_db()
        cursor = conn.cursor()
        
        USER_ID = session.get("user_id")
        
        cursor.execute("INSERT INTO calorieIntake (USER_ID, Calorie, DateCalorieIn) VALUES (?, ?, ?)", 
                       (USER_ID, calories, date))

        conn.commit()
        conn.close()  
        print("Calories successfully logged.", "success")
        return redirect('/')


# Route to fetch calorie data for the graph
@app.route('/calorie-data')
def calorie_data():
    conn = connect_db()
    cursor = conn.cursor()
    
    USER_ID = session.get("user_id")  # Get the logged in User ID

    # Fetch data only for the logged in user
    cursor.execute("SELECT DateCalorieIn, Calorie FROM calorieIntake WHERE USER_ID = ? ORDER BY DateCalorieIn", 
                   (USER_ID,))
    
    data = cursor.fetchall()
    conn.close()

    # Convert data to JSON format
    return jsonify([{"date": row[0], "calories": row[1]} for row in data])


@app.route("/weightTracking")
def weightTracking():
        return render_template('weightTracking.html')


# Route to enter weight into the table
@app.route("/weightEntering", methods=['POST', 'GET'])
def weightEntering():
    if request.method == 'GET':
        return render_template('weightEntering.html')


    else:
        weight = request.form['weight']
        date = request.form['date']

        conn = connect_db()
        cursor = conn.cursor()
        
        USER_ID = session.get("user_id")
        
        cursor.execute("INSERT INTO Weight (USER_ID, Weight, DateWeighIn) VALUES (?, ?, ?)", 
                       (USER_ID, weight, date))

        conn.commit()
        conn.close()  
        print("Weight successfully logged.", "success")
        return redirect('/')
    
# Route to fetch Weight data for the graph
@app.route('/weight-data')
def weight_data():
    conn = connect_db()
    cursor = conn.cursor()
    
    USER_ID = session.get("user_id")  # Get the logged in User ID

    # Fetch data only for the logged in user
    cursor.execute("SELECT DateWeighIn, Weight FROM Weight WHERE USER_ID = ? ORDER BY DateWeighIn", 
                   (USER_ID,))
    
    data = cursor.fetchall()
    conn.close()

    # Convert data to JSON format
    return jsonify([{"date": row[0], "weight": row[1]} for row in data])


@app.route("/createWorkout")
def createWorkout():
        return render_template('createWorkout.html')

@app.route("/logout")
def logout(): 
    session.clear()
    return redirect("/")


@app.route("/saveWorkout", methods=["POST"])
def saveWorkout():
    # Ensure the user is logged in
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "User not logged in."}), 401

    user_id = session["user_id"]
    data = request.get_json()
    # Expected JSON format:
    # {
    #   "workouts": {
    #       "Workout One": [
    #           {"exercise": "Push-ups", "reps": 15},
    #           {"exercise": "Squats", "reps": 20}
    #       ],
    #       "Workout Two": [
    #           {"exercise": "Bench Press", "reps": 10}
    #       ]
    #   }
    # }
    workouts = data.get("workouts")
    if not workouts:
        return jsonify({"status": "error", "message": "No workout data received."}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # For each workout slot, delete previous entries and insert the new ones.
    for slot, exercises in workouts.items():
        # Delete existing workouts for this user and workout slot
        cursor.execute("DELETE FROM Workouts WHERE USER_ID=? AND WorkoutSlot=?", (user_id, slot))
        # Insert each new exercise
        for exercise in exercises:
            exercise_name = exercise.get("exercise")
            reps = exercise.get("reps")
            cursor.execute(
                "INSERT INTO Workouts (USER_ID, WorkoutSlot, ExerciseName, Reps) VALUES (?, ?, ?, ?)",
                (user_id, slot, exercise_name, reps)
            )
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Workout saved."})

@app.route("/getWorkout", methods=["GET"])
def getWorkout():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "User not logged in."}), 401

    user_id = session["user_id"]
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch all saved workouts for this user
    cursor.execute("SELECT WorkoutSlot, ExerciseName, Reps FROM Workouts WHERE USER_ID=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    # Organize data into JSON format
    workout_data = {}
    for slot, exercise, reps in rows:
        if slot not in workout_data:
            workout_data[slot] = []
        workout_data[slot].append({"exercise": exercise, "reps": reps})

    return jsonify({"status": "success", "workouts": workout_data})


if __name__ == '__main__':
    app.run(debug=True) 


