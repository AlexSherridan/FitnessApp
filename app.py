from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3

@app.route("/view")
    con = sqlite3.connect("database.db")
    cur = con.cursor()
        cur.execute("SELECT * FROM user")
        match = cur.fetchall()
        return str(match[0][0])


        if request.method == "GET":
            return render_template("index.html") 
        else:
            con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE username=? AND password=?",
                    (request.form["un"],request.form["pw"]))
        match = len(cur.fetchall())
        if match > 0:
            return "Hello" + request.form["un"]
        else:  
            return "User not recognised!"
        
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
       return render_template("signup.html")
    else:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO user (username, password) VALUES (?,?)",
                    (request.form["un"],request.form["pw"]))
        con.commit()
        return request.form["un"] + " added"