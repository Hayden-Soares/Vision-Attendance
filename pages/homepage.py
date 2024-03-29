from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html", title = "login")

@app.route("/professor")
def professor():    
   return "hello world"

if __name__ == "__main__":
    app.run(debug = True)
