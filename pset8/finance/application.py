import os
import time

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Returns the table with the stocks owned by the user
    rows = db.execute("SELECT symbol, SUM(shares) AS sum, price FROM ledger WHERE userID = :userID GROUP BY symbol HAVING sum >= 1", userID=session["user_id"])

    # Returns the total amount of cash the user currently has
    userCash = round(db.execute("SELECT cash FROM users WHERE id = :userID", userID=session["user_id"])[0]["cash"])
    total = int(userCash)

    # Returns the latest stock prices for the owned stocks
    stockPrices={}
    for row in rows:
        s = row["symbol"]
        l = lookup(s)
        stockPrices[s] = l["price"]
        total += l["price"] * row["sum"]
        total = round(total)

    return render_template("index.html", stocks=rows, stockPrices=stockPrices, userCash=userCash, total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Stores values of symbol and amount of shares into variables
        symbol = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")

        # Ensures that both symbol and amount of shares were filled in correctly
        if not symbol or not request.form.get("symbol"):
            return apology("symbol not found", 400)

        if not request.form.get("shares") or int(shares) < 1:
            return apology("Must input amount of shares", 400)

        # Calculates the total amount of the purchase
        total = int(shares) * symbol["price"]

        # Returns the amount of cash that the user has
        rows = db.execute("SELECT * FROM users WHERE id = :userID", userID=session["user_id"])
        userCash = rows[0]["cash"]

        # Ensures that the user has enough cash to purchase the stock
        if total > userCash:
            return apology("Not enough money to buy this amount of shares", 403)

        # Updates the amount of cash the user has after the purchase
        db.execute("UPDATE users SET cash = cash - :total WHERE id = :userID", total=total, userID=session["user_id"])

        # Insert record of transaction into ledger
        db.execute("INSERT INTO ledger (userID, time, symbol, price, shares, total) VALUES (:userID, :time, :symbol, :price, :shares, :total)",
           userID=session["user_id"], time=time.strftime('%Y-%m-%d %H:%M:%S'), symbol=symbol["symbol"], price=symbol["price"], shares=shares, total=total)

        # Displays message of successful purchase and redirect user to homepage
        flash('Purchase completed')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, shares, price, time FROM ledger WHERE userID = :userID", userID=session["user_id"])
    for row in rows:
        stock_info = lookup(row['symbol'])
        row['curr_price'] = stock_info["price"]

    return render_template("history.html", rows=rows)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("quote.html")
    else:
        # Checks if the symbol exists
        if not lookup(request.form.get("symbol")):
            return apology("symbol not found", 400)

        # Returns the symbol and price
        symbol = lookup(request.form.get("symbol"))
        return render_template("quoted.html", symbol=symbol["symbol"], price=usd(symbol["price"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirm_password"):
            return apology("must confirm password", 403)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("passwords must match", 403)

        # Query database for submited username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username doesn`t exists
        if len(rows) != 0:
            return apology("username already taken", 403)

        # Adds user to database
        add_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                      username=request.form.get("username"),
                      password=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=4))

        # Remember which user has registered
        session["user_id"] = add_user

        # Redirect user to home page
        flash('Registration done!')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Stores values of symbol and amount of shares into variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensures that both symbol and amount of shares were filled in correctly
        if not symbol or not shares:
            return apology("Must insert information", 400)

        shares = int(shares)

        # Checks for validity of symbol
        resp = lookup(symbol)

        if not resp:
            return apology("Invalid symbol", 400)

        # Checks validaty of amount of shares
        if shares < 1:
            return apology("Invalid amount of shares", 400)

        # Checks in the user has the amount of shares it wants to sell
        stock = db.execute("SELECT SUM(shares) AS sum FROM ledger WHERE userID = :userID AND symbol = :symbol GROUP BY symbol", userID=session["user_id"], symbol=symbol)[0]
        if shares > stock["sum"] or len(stock) != 1:
            return apology("You don`t have this amount of stock to sell", 403)

        # Updates the amount of cash the user has after the sell
        db.execute("UPDATE users SET cash = cash + :total WHERE id = :userID", total=shares*resp["price"], userID=session["user_id"])

        # Insert record of transaction into ledger
        db.execute("INSERT INTO ledger (userID, time, symbol, price, shares, total) VALUES (:userID, :time, :symbol, :price, :shares, :total)",
           userID=session["user_id"], time=time.strftime('%Y-%m-%d %H:%M:%S'), symbol=symbol, price=resp["price"], shares=-shares, total=shares*resp["price"])

        # Displays message of successful sell and redirect user to homepage
        flash('Sold')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        stocks_owned = db.execute("SELECT symbol FROM ledger WHERE userID = :userID GROUP BY symbol", userID=session["user_id"])
        return render_template("sell.html", stocks_owned=stocks_owned)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Delete users account"""
    #Prompts user if it wants to delete account
    if request.method == "POST":
        db.execute("DELETE FROM users WHERE id = :userID", userID=session["user_id"])
        db.execute("DELETE FROM ledger WHERE userID = :userID", userID=session["user_id"])

        # Clears session
        session.clear()

        # Confirms deletion and returns to homepage
        flash('Account Deleted!')
        return render_template("login.html")

    else:
        return render_template("delete.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
