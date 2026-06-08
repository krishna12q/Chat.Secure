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

curr.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

curr.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    sender TEXT NOT NULL,
    contents TEXT NOT NULL,
    group_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close() # Close initial connection

app = Flask(__name__)
app.secret_key = 'bahuthitreshatarnaksillaeatingmywekzuegsandwhichmadebyquandaledingleinddyslair'

@app.route("/chat")
def chat():

    if "cgroup" not in session:
        return redirect(url_for("joincroom"))

    db_conn = sqlite3.connect("db.db")
    cur = db_conn.cursor()

    cur.execute("""
        SELECT sender, contents, created_at
        FROM messages
        WHERE group_name = ?
        ORDER BY id ASC
    """, (session["cgroup"],))

    messages = cur.fetchall()

    db_conn.close()

    return render_template(
        "chat.html",
        groupname=session["cgroup"],
        messages=messages,
        username=session["username"]
    )

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/sendmessage", methods=['POST','GET'])
def send():
    db_conn = sqlite3.connect('db.db')
    cur = db_conn.cursor()

    message = request.form.get('message')

    cur.execute("INSERT INTO messages (sender,contents,group_name) VALUES (?,?,?)",(session['username'],message,session['cgroup'],))

    db_conn.commit()
    db_conn.close()

    print(session['username'],message,session['cgroup'])

    return redirect(url_for('chat'))


@app.route("/createc", methods=['POST','GET'])
def createchatroom():
    if "username" not in session:
        return "You must log in first"

    return render_template("createchat.html")

@app.route("/processcreate", methods=['POST','GET'])
def func():
    groupname = request.form.get('groupname')
    secretpassword = request.form.get('pw')

    db_conn = sqlite3.connect('db.db')
    cur = db_conn.cursor()
    
    cur.execute("SELECT * FROM groups WHERE name = ?", (groupname,))
    matches = cur.fetchone()

    if not matches:
        if groupname and secretpassword:
            cur.execute("""
                INSERT INTO groups (name,password)
                VALUES (?, ?)
                """, (groupname, secretpassword))
            db_conn.commit()
            db_conn.close()

            print("created")
            return redirect(url_for('home'))
    
        else:
            print("Please Fill All Blanks First")
            return "Please Fill All Blanks First" 
    else:
        print("Name Is Occupied")
        return "Name Is Occupied" 



@app.route("/joinchat", methods=['POST','GET'])
def joincroom():
    if "username" not in session:
        return "You must log in first"
    else:
        return render_template("joinchat.html")
    

@app.route("/joinc", methods=['POST','GET'])
def joinchatroom():
    if "username" not in session:
        return "You must log in first"
    else:
        groupname = request.form.get('groupname')
        pw = request.form.get('pw')

        print(groupname)
        print(request.method)
        print(request.form)

        db_conn = sqlite3.connect('db.db')
        cur = db_conn.cursor()

        cur.execute('''
        SELECT * FROM groups WHERE name = ?
        ''',(groupname,))

        groupfound = cur.fetchone()

        db_conn.close()

        if groupfound[1] == groupname:
            if groupfound[2] == pw:
                session['cgroup'] = groupfound[1]
                return redirect(url_for('chat'))
            else:
                return "Group Exsissts But Wrong Password"
        else:
            return "No Group FOund"

    #return render_template("joinchat.html")
    


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

@app.route("/clogin", methods=['POST'])
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

    if user and check_password_hash(user[2], pw):
        session["username"] = user[1]
        session["nickname"] = user[3]
        return redirect(url_for('home'))

    return "Invalid username or password", 401

if __name__ == "__main__":
    app.run(debug=True)
