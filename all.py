from flask import Flask, render_template, request, redirect
import os.path
from os import path

app = Flask(__name__)

def read_file(filename):
    if path.exists(filename):
        pyfile = open(filename, "r")
        content = pyfile.read()
        pyfile.close()
        return content
    return ""

def write_file(filename, content):
    pyfile = open(filename, "w")
    pyfile.write(content)
    pyfile.close()

@app.route("/")
def main():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("txtusername")
    password = request.form.get("txtpassword")

    if username == "" or password == "":
        return render_template("login.html", error="Please enter both fields")
    
    if username == "admin":
        admin_data = read_file("admin.txt")
        if admin_data == "":
            if password == "abc123":
                write_file("current.txt", "admin")
                return redirect("/admin")
            else:
                return render_template("login.html", error="Invalid admin password")
        else:
            lines = admin_data.split("\n")
            if len(lines) >= 2 and username == lines[0] and password == lines[1]:
                write_file("current.txt", "admin")
                return redirect("/admin")
            else:
                return render_template("login.html", error="Invalid admin credentials")
    else:
        user_data = read_file(username + ".txt")
        if user_data == "":
            return render_template("login.html", error="User not found")
        else:
            lines = user_data.split("\n")
            if len(lines) >= 2 and username == lines[0] and password == lines[1]:
                write_file("current.txt", username)
                return redirect("/user")
            else:
                return render_template("login.html", error="Invalid password")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("txtsignupusername")
    password = request.form.get("txtsignuppassword")
    rpassword = request.form.get("txtsignuprpassword")

    if username == "" or password == "" or rpassword == "":
        return render_template("login.html", signuperror="Please fill all fields", show_signup="true")
    elif password != rpassword:
        return render_template("login.html", signuperror="Passwords don't match", show_signup="true")
    elif username == "admin":
        return render_template("login.html", signuperror="Cannot use admin as username", show_signup="true")
    elif path.exists(username + ".txt"):
        return render_template("login.html", signuperror="Username already exists", show_signup="true")
    else:
        write_file(username + ".txt", username + "\n" + password)
        return render_template("login.html", success="Account created! Please login")

@app.route("/admin")
def admin():
    current_user = read_file("current.txt")
    if current_user != "admin":
        return redirect("/")
    return render_template("admin.html")

@app.route("/user")
def user():
    current_user = read_file("current.txt")
    if current_user == "" or current_user == "admin":
        return redirect("/")
    return render_template("user.html")

@app.route("/fruit", methods=["GET", "POST"])
def fruit():
    current_user = read_file("current.txt")
    if current_user != "admin":
        return redirect("/")
    
    if request.method == "POST":
        product = request.form.get("productname")
        price = request.form.get("txtprice")
        unit = request.form.get("selunit")
        
        if float(price) < 0.01:
            return render_template("fruit.html", error="Price must be at least 0.01")
        elif unit == "":
            return render_template("fruit.html", error="Please select a unit")
        else:
            pyfile = open("fruit.txt", "a")
            pyfile.write(product + "," + price + "," + unit + "\n")
            pyfile.close()
            return render_template("fruit.html", success="Product added successfully")
    
    return render_template("fruit.html")

@app.route("/userfruit")
def userfruit():
    current_user = read_file("current.txt")
    if current_user == "" or current_user == "admin":
        return redirect("/")
    
    if path.exists("fruit.txt"):
        products = []
        pyfile = open("fruit.txt", "r")
        for line in pyfile:
            parts = line.strip().split(",")
            if len(parts) == 3:
                products.append({
                    "name": parts[0],
                    "price": parts[1],
                    "unit": parts[2]
                })
        pyfile.close()
        
        if len(products) > 0:
            return render_template("userfruit.html", products=products)
    
    return render_template("emptydept.html", dept="Fruit")

@app.route("/addtocart", methods=["POST"])
def addtocart():
    current_user = read_file("current.txt")
    if current_user == "" or current_user == "admin":
        return redirect("/")
    
    product = request.form.get("product")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    
    cartfile = current_user + "cart.txt"
    pyfile = open(cartfile, "a")
    pyfile.write(product + "," + price + "," + quantity + "\n")
    pyfile.close()
    
    return redirect("/userfruit")

@app.route("/cart")
def cart():
    current_user = read_file("current.txt")
    if current_user == "" or current_user == "admin":
        return redirect("/")
    
    cartfile = current_user + "cart.txt"
    if path.exists(cartfile):
        items = []
        total = 0.0
        pyfile = open(cartfile, "r")
        for line in pyfile:
            parts = line.strip().split(",")
            if len(parts) == 3:
                item_total = float(parts[1]) * int(parts[2])
                total += item_total
                items.append({
                    "product": parts[0],
                    "price": parts[1],
                    "quantity": parts[2],
                    "total": "{:.2f}".format(item_total)
                })
        pyfile.close()
        
        return render_template("cart.html", items=items, total="{:.2f}".format(total))
    else:
        return render_template("cart.html", empty=True)



@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    current_user = read_file("current.txt")
    if current_user == "" or current_user == "admin":
        return redirect("/")
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        
        if name != "" and email != "" and phone != "":
            write_file(current_user + "basicinfo.txt", name + "\n" + email + "\n" + phone)
        
        cardnumber = request.form.get("cardnumber").replace(" ", "")
        expmonth = request.form.get("expmonth")
        expyear = request.form.get("expyear")
        securitycode = request.form.get("securitycode")
        
        if len(cardnumber) not in [16, 19]:
            return render_template("checkout.html", error="Card number must be 16 or 19 digits")
        if len(expmonth) != 2 or len(expyear) != 4:
            return render_template("checkout.html", error="Invalid expiration date")
        if len(securitycode) not in [3, 4]:
            return render_template("checkout.html", error="Security code must be 3 or 4 digits")
        
        cartfile = current_user + "cart.txt"
        if path.exists(cartfile):
            pyfile = open(cartfile, "w")
            pyfile.close()
        
        return render_template("checkoutsuccess.html")
    
    else:
        basicinfo = {}
        basicfile = current_user + "basicinfo.txt"
        if path.exists(basicfile):
            lines = read_file(basicfile).split("\n")
            if len(lines) >= 3:
                basicinfo = {
                    "name": lines[0],
                    "email": lines[1],
                    "phone": lines[2]
                }
        
        return render_template("checkout.html", basicinfo=basicinfo)

if __name__ == "__main__":
    app.run()
