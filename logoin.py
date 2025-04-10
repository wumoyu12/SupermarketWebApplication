from flask import Flask,render_template, request, redirect
import os.path
from os import path

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("login.html")

@app.route("/login",methods=["POST"])

def GetInfo():
    username = request.form.get("txtusername")
    userpasswd = request.form.get("txtpassword")

    
if __name__ == "__main__":
    app.run();
