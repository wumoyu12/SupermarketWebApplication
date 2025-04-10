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

    if(username == "" or userpasswd == ""):
        return render_template("login.html")
    else:
        ExistsFile()

    if (exists == "n"):
        msg = "Account not found! Create Account?"
        
def ExistsFile():
    global exists
    userfile = username + ".txt"
    fileDir = os.path.dirname(os.path.realpath("__file__"))
    fileexist = bool(path.exists(userfile))
    
    if (fileexist == False):
        exists = "n"
    else:
        exists = "y"

    
if __name__ == "__main__":
    app.run();
