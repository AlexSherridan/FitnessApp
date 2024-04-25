from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    un = request.args.get('un')
    pw = request.args.get("pw")
    if un == None:
        return render_template("index.html")
    elif un == "bob" and pw == "123":
        return "Hello " + un
    else:
        return "User not recognised!"