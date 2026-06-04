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

if __name__ == "__main__":
    app.run(debug=True)
