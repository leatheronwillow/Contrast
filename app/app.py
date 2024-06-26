import os
from flask import Flask, render_template, session, request, redirect, g
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology, rs

# import relevant modules

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["rs"] = rs

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('contrast.db')
    
    db.row_factory = sqlite3.Row
    return db

#close database connection after use
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# function to query database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    result = cur.fetchall()
    cur.close()
    return (result[0] if result else None) if one else result

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def orders():
    """Show current orders"""
    # retrieve relevant details
    orders_db = query_db("SELECT id, date, quantity, plates_unit_cost, binding_unit_cost, \
                         paper_unit_cost, status, book_id FROM orders")

    orders = []     # initiating list of dictionaries

    billable = 0    # initiating amounts due
    for row in orders_db:
        
        result = query_db("SELECT title FROM books WHERE id = ?", [row["book_id"]], one=True)
        title = result["title"]

        unit_cost = row["plates_unit_cost"] + row["binding_unit_cost"] + row["paper_unit_cost"]
        price = unit_cost * 1.2
        total = price * row["quantity"]

        if row["status"] == "delivered":
            billable = billable + total

        order = {
            "id": row["id"],
            "date": row["date"],
            "title": title,
            "quantity": row["quantity"],
            "unit_cost": unit_cost,
            "price": price,
            "total": total,
            "status": row["status"]
        }

        orders.append(order)

    return render_template("orders.html", orders=orders, billable=billable)

@app.route("/companies", methods=["GET", "POST"])
@login_required
def companies():
    """Show all companies on books"""

    if request.method == "POST":
        # process data
        return
    
    return

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = query_db("SELECT * FROM users WHERE username = ?", [request.form.get("username")], one=True )

        # Ensure username exists and password is correct
        if rows is None:
            return apology("Username not found", 403)
        elif not check_password_hash(rows["hash"], request.form.get("password")):
            return apology("password incorrect", 403)

        # Remember which user has logged in
        session["user_id"] = rows["people_id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    #Forget any user id
    session.clear()

    #Redirect user to login form
    return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # #establish connection with database
    # cur = get_db()

    # if user registered via POST (i.e. submitted the form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)
        
        # Ensure first name is entered
        elif not request.form.get("first-name"):
            return apology("must provide first name", 400)
        
        # Ensure last name is entered
        elif not request.form.get("last-name"):
            return apology("must provide last name", 400)
        
        # Ensure password confirmation matches password field
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Confirmation does not match password", 400)
        
        else:
            result = query_db("SELECT username FROM users WHERE username = ?", [request.form.get("username")], one=True)
            if result:
                return apology("Username already exists", 400)        

        # generate password hash
        hash = generate_password_hash(request.form.get("password"))

        username = str(request.form.get("username"))
        first_name = str(request.form.get("first-name"))
        last_name = str(request.form.get("last-name"))

        if request.form.get("mobile"):
            mobile = str(request.form.get("mobile"))
        else:
            mobile = "not given"
        
        if request.form.get("email"):
            email = str(request.form.get("email"))
        else:
            email = "not given"
        
        # Insert user details into people table
        con = get_db()

        with con:
            con.execute("INSERT INTO people (first_name, last_name, mobile, email) VALUES (?, ?, ?, ?)", (first_name, last_name, mobile, email))
            
            # Insert values for username and password hash into database
            result = con.execute("SELECT id FROM people WHERE first_name = ? AND last_name = ?", [first_name, last_name])
            people_id = result.fetchone()["id"]
            
            con.execute("INSERT INTO users VALUES (?, ?, ?)", [people_id, username, hash])

        return redirect("/login")

    # user reached via GET
    else:
        return render_template("register.html")
    
@app.route("/add_company", methods=["GET", "POST"])
def add_companies():
    """Register companies"""
    
    # #establish connection with database
    # cur = get_db()

    # if user registered via POST (i.e. submitted the form)
    if request.method == "POST":

        # Ensure company name was submitted
        if not request.form.get("name"):
            return apology("must provide company name", 400)

        # Ensure category was submitted
        elif not request.form.get("category"):
            return apology("must provide category", 400)
        
        # Ensure company doesn't already exist in database
        else:
            result = query_db("SELECT name FROM companies WHERE name = ?", [request.form.get("name")], one=True)
            if result:
                return apology("Company already exists", 400)        

        company_name = str(request.form.get("name"))

        if request.form.get("contact") == "not-in-list":
            contact_id = "Not Provided"
        else:
            contact_id = int(request.form.get("contact"))
            
        
        category = str(request.form.get("category"))

        unit = str(request.form.get("unit"))
        block = str(request.form.get("block"))
        street = str(request.form.get("street"))
        city = str(request.form.get("city"))
        
        # Insert company details into company table
        con = get_db()

        with con:
            con.execute("INSERT INTO companies(name, people_id, category, balance_paisa) VALUES (?, ?, ?, 0)", [company_name, contact_id, category])
            
            # Insert values for username and password hash into database
            result = con.execute("SELECT id FROM companies WHERE name = ?", [company_name])
            company_id = result.fetchone()["id"]
            
            con.execute("INSERT INTO address(company_id, unit, block, street, city) VALUES (?, ?, ?, ?, ?)", [company_id, unit, block, street, city])

        return redirect("/")

    # user reached via GET
    else:
        people_db = query_db("SELECT * FROM people")
        
        people = []     # initiating list of dictionaries
        
        for row in people_db:

            person = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
            }

            people.append(person)

        return render_template("add_company.html", people=people)

if __name__ == '__main__':
    app.run(
        debug=True, # Optional but useful for now
        host="0.0.0.0" # Listen for connections directed _to_ any address
    )