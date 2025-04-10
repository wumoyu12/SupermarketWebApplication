from flask import Flask, render_template, request, redirect, url_for
import os.path
from os import path

app = Flask(__name__)

# File to store user credentials
USER_DB = "users.db"

@app.route("/")
def main():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("txtloginusername")
        password = request.form.get("txtloginpassword")
        
        if not username or not password:
            return render_template("login.html", error="Please fill in all fields")
        
        if not path.exists(USER_DB):
            return render_template("login.html", error="No users registered yet")
        
        with open(USER_DB, "r") as f:
            for line in f:
                stored_user, stored_pass = line.strip().split(",")
                if username == stored_user and password == stored_pass:
                    return redirect(url_for('welcome', username=username))
        
        return render_template("login.html", error="Invalid username or password")
    
    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("txtsignupusername")
    password = request.form.get("txtpassword")
    rpassword = request.form.get("txtsignuprpassword")
    
    if not username or not password or not rpassword:
        return render_template("login.html", signup_error="Please fill in all fields", show_signup=True)
    
    if password != rpassword:
        return render_template("login.html", signup_error="Passwords don't match", show_signup=True)
    
    # Check if user already exists
    if path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            for line in f:
                stored_user, _ = line.strip().split(",")
                if username == stored_user:
                    return render_template("login.html", signup_error="Username already exists", show_signup=True)
    
    # Save new user
    with open(USER_DB, "a") as f:
        f.write(f"{username},{password}\n")
    
    return render_template("login.html", success="Account created successfully! Please log in.")

@app.route("/welcome/<username>")
def welcome(username):
    return f"<h1>Welcome to Supermarket, {username}!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
