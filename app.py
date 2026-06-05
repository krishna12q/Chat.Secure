from flask import Flask, request, redirect, url_for, render_template, flash,session
from werkzeug.security import generate_password_hash , check_password_hash
import sqlite3



# 1. Database Initialization (Runs once when app starts)
conn = sqlite3.connect('db.db')
curr = conn.cursor()
curr.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    nickname TEXT NOT NULL
)
""")
conn.commit()
conn.close() # Close initial connection

app = Flask(__name__)
app.secret_key = 'bahuthitreshatarnaksillaeatingmywekzuegsandwhichmadebyquandaledingleinddyslair'

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/createc", methods=['POST'])
def createchatroom():
    if "username" not in session:
        return "You must log in first"

    return render_template("createchat.html")

@app.route("/joinc", methods=['POST'])
def joinchatroom():
    if "username" not in session:
        return "You must log in first"
    
    return render_template("joinchat.html")

# Displays the registration page
@app.route("/signup", methods=['POST','GET'])
def signup_page():
    return render_template("register.html")

# Process the actual form data submitted by the user
@app.route("/register", methods=['POST'])
def register_user():
    print(request.form)
    # These now run inside the request context safely!
    nick = request.form.get('nickname')
    username = request.form.get('username')
    plaintext_pw = request.form.get('pw')

    # Quick validation to prevent empty fields
    if not username or not plaintext_pw or not nick:
        return "Please fill out all fields", 400

    pw = generate_password_hash(plaintext_pw)

    # Open a fresh connection for this request
    db_conn = sqlite3.connect('db.db')
    cur = db_conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    samematch = cur.fetchone()

    if samematch is None:
        cur.execute("""
            INSERT INTO users (username, password, nickname)
            VALUES (?, ?, ?)
        """, (username, pw, nick))
        db_conn.commit()
        db_conn.close()
        return render_template('home.html') # Redirect to home on success
    else:
        db_conn.close()
        return "Error: Username Occupied", 400

@app.route("/login", methods=['GET', 'POST'])
def loginacc():
    return render_template('login.html')


@app.route("/clogin", methods=['POST','GET'])
def login():

    db_conn = sqlite3.connect('db.db')
    cur = db_conn.cursor()

    uname = request.form.get('username')
    pw = request.form.get('pw')

    cur.execute(
        "SELECT * FROM users WHERE username = ?",
        (uname,)
    )

    user = cur.fetchone()

    db_conn.close()

    if user:
        if check_password_hash(user[2], pw):
            print("Correct password")
            session["username"] = user[1]
            session["nickname"] = user[3]
            return redirect(url_for('home'))
    else:
        print("Error")


if __name__ == "__main__":
    app.run(debug=True)
