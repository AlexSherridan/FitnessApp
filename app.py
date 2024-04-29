from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "GET":
       return render_template("index.html") 
    else:
        f = open("login.txt", "r")
        un = f.readline().strip() #remove /n
        pw = f.readline().strip()
        f.close()  
        if un == request.form["un"] and pw == request.form["pw"]:
            return "Hello" + un
        else:  
            return "User not recognised!"
        
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
       return render_template("signup.html")
    else:
        f = open("login.txt", "w")
        f.write(request.form["un"])
        f.write("\n")
        f.write(request.form["pw"])
        f.close()
        return "signup succesful!"