from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

# FIXED: Corrected spelling to match a clean url convention
@app.route("/createc", methods=['POST'])
def createchatroom():
    return render_template("createchat.html")

@app.route("/joinc", methods=['POST'])
def joinchatroom():
    return render_template("joinchat.html")

@app.route("/signup", methods=['POST'])
def createacc():
    return render_template("register.html")

@app.route("/login", methods=['POST'])
def loginacc():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
