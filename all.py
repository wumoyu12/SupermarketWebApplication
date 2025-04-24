from flask import Flask, render_template, request, redirect
import os.path
from os import path

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def GetInfo():
    username = request.form.get("txtusername")
    userpasswd = request.form.get("txtpassword")
    
    if username == "" or userpasswd == "":
        return render_template("login.html", error="Please enter both fields")
    else:
        if username == "admin":
            admin_file = "admin.txt"
            if path.exists(admin_file):
                pyfile = open(admin_file, "r")
                lines = pyfile.readlines()
                pyfile.close()
                if len(lines) >= 2 and userpasswd == lines[1].strip():
                    pyfile = open("current.txt", "w")
                    pyfile.write("admin")
                    pyfile.close()
                    return redirect("/admin")
                else:
                    return render_template("login.html", error="Invalid admin password")
            else:
                return render_template("login.html", error="Admin account not set up")
        else:
            userfile = username + ".txt"
            if path.exists(userfile):
                pyfile = open(userfile, "r")
                stored_pass = pyfile.read().strip()
                pyfile.close()
                if userpasswd == stored_pass:
                    pyfile = open("current.txt", "w")
                    pyfile.write(username)
                    pyfile.close()
                    return redirect("/user")
                else:
                    return render_template("login.html", error="Invalid password")
            else:
                return render_template("login.html", error="User not found")

@app.route("/signup", methods=["POST"])
def SignUp():
    username = request.form.get("txtsignupusername")
    password = request.form.get("txtsignuppassword")
    rpassword = request.form.get("txtsignuprpassword")

    if username == "" or password == "" or rpassword == "":
        return render_template("login.html", signuperror="Please fill all fields", show_signup="true")
    elif password != rpassword:
        return render_template("login.html", signuperror="Passwords don't match", show_signup="true")
    elif username == "admin":
        return render_template("login.html", signuperror="Cannot use admin as username", show_signup="true")
    else:
        userfile = username + ".txt"
        if path.exists(userfile):
            return render_template("login.html", signuperror="Username already exists", show_signup="true")
        else:
            pyfile = open(userfile, "w")
            pyfile.write(password)
            pyfile.close()
            return render_template("login.html", success="Account created! Please login")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/fruit", methods=["GET", "POST"])
def fruit():
    if request.method == "POST":
        product = request.form.get("product")
        price = request.form.get("price")
        unit = request.form.get("unit")
        
        if float(price) < 0.01:
            return render_template("fruit.html", error="Price must be at least 0.01")
        elif unit == "":
            return render_template("fruit.html", error="Please select a unit")
        else:
            pyfile = open("fruit.txt", "a")
            pyfile.write(f"{product},{price},{unit}\n")
            pyfile.close()
            return render_template("fruit.html", success="Product added successfully")
    
    return render_template("fruit.html")

@app.route("/userfruit")
def userfruit():
    if path.exists("fruit.txt"):
        pyfile = open("fruit.txt", "r")
        products = pyfile.readlines()
        pyfile.close()
        product_list = []
        for product in products:
            details = product.strip().split(",")
            product_list.append({
                "name": details[0],
                "price": details[1],
                "unit": details[2]
            })
        return render_template("userfruit.html", products=product_list)
    else:
        return render_template("userfruit.html", empty=True)

@app.route("/addtocart", methods=["POST"])
def addtocart():
    product = request.form.get("product")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    
    pyfile = open("current.txt", "r")
    username = pyfile.read().strip()
    pyfile.close()
    
    cart_file = username + "cart.txt"
    pyfile = open(cart_file, "a")
    pyfile.write(f"{product},{price},{quantity}\n")
    pyfile.close()
    
    return redirect("/userfruit")

@app.route("/cart")
def cart():
    pyfile = open("current.txt", "r")
    username = pyfile.read().strip()
    pyfile.close()
    
    cart_file = username + "cart.txt"
    if path.exists(cart_file):
        pyfile = open(cart_file, "r")
        items = pyfile.readlines()
        pyfile.close()
        
        cart_items = []
        total = 0.0
        for item in items:
            details = item.strip().split(",")
            item_total = float(details[1]) * int(details[2])
            total += item_total
            cart_items.append({
                "product": details[0],
                "price": details[1],
                "quantity": details[2],
                "total": "{:.2f}".format(item_total)
            })
        
        return render_template("cart.html", items=cart_items, total="{:.2f}".format(total))
    else:
        return render_template("cart.html", empty=True)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    pyfile = open("current.txt", "r")
    username = pyfile.read().strip()
    pyfile.close()
    
    info_file = username + "basicinfo.txt"
    basic_info = {}
    if path.exists(info_file):
        pyfile = open(info_file, "r")
        lines = pyfile.readlines()
        pyfile.close()
        if len(lines) >= 3:
            basic_info = {
                "name": lines[0].strip(),
                "phone": lines[1].strip(),
                "email": lines[2].strip()
            }
    
    if request.method == "POST":
        if "name" in request.form:  # Saving basic info
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            
            if name == "" or phone == "" or email == "":
                return render_template("checkout.html", error="Please fill all basic info fields", has_info=path.exists(info_file), info=basic_info)
            
            pyfile = open(info_file, "w")
            pyfile.write(f"{name}\n{phone}\n{email}\n")
            pyfile.close()
            
            return render_template("checkout.html", has_info=True, info={
                "name": name,
                "phone": phone,
                "email": email
            })
        else:  # Processing payment
            address = request.form.get("address")
            card = request.form.get("card")
            exp = request.form.get("exp")
            security = request.form.get("security")
            
            if address == "":
                return render_template("checkout.html", error="Please select an address", has_info=True, info=basic_info)
            elif len(card) not in [16, 19] or not card.isdigit():
                return render_template("checkout.html", error="Card number must be 16 or 19 digits", has_info=True, info=basic_info)
            elif len(security) not in [3, 4] or not security.isdigit():
                return render_template("checkout.html", error="Security code must be 3 or 4 digits", has_info=True, info=basic_info)
            
            # Clear cart
            cart_file = username + "cart.txt"
            if path.exists(cart_file):
                pyfile = open(cart_file, "w")
                pyfile.close()
            
            return render_template("ordercomplete.html")
    
    return render_template("checkout.html", has_info=path.exists(info_file), info=basic_info)

if __name__ == "__main__":
    app.run()
