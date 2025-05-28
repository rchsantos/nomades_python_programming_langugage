import os
import csv
import hashlib
import json

from flask import Flask, render_template, request, session, redirect, url_for, flash

from helpers.random_password_generator import generate_password as generate_salt

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, 'users.csv')

with open(os.path.join(CURR_DIR, "config", "creds.json")) as json_config:
  config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def register():
  """
  Register function should add a new user to the users.csv file
  """
  if request.method == "POST":
    # get the user uid from form
    uid: str = request.form.get("uid", "")
    # get the user password from form
    pwd: str = request.form.get("pwd", "")
    # get the user password 2 from form
    pwd2: str = request.form.get("pwd2", "")

    # Validate that the two passwords are the same
    if pwd != pwd2:
      flash("Please provide the same passwords", "danger")
      return render_template("login/register.html")
     
    if uid == "" or pwd == "":
      flash("Please provide UID and PWD", "danger")
      return render_template("login/register.html")
    
    if ',' in uid or ',' in pwd:
      flash("Please avoid the use of ',' (coma) in UID and PWD", "danger")
      return render_template("login/register.html")
    
    salt: str = generate_salt(True, False, False, False, 10)
    h_pwd: str = hashlib.sha256((pwd+salt).encode("utf-8")).hexdigest()
    
    # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
    with open(CSV_FILE, "r") as users_csv_file:
      reader = csv.DictReader(users_csv_file)
      # Loop throught the lines and check if the current line is the user's one
      for row in reader:
        if row["uid"] == uid:
          flash("User already exists", "danger")
          return render_template("login/register.html")

    # Open in "a" mode the users csv file using the constant CSV_FILE
    with open(CSV_FILE, "a") as users_csv_file:
      # Add the new user to the CSV file
      writer = csv.writer(users_csv_file)
      writer.writerow([uid, salt, h_pwd])

    session["loggedin"] = True
    session["uid"] = uid
    flash("Login successfull", "success") 
    return redirect(url_for("private"))

  return render_template("login/register.html")
  
@app.route("/signin", methods=["GET", "POST"])
def login():
  """
  The login functiojn should authenticate a user using his uid and pwd
  """
  if request.method == "POST":
    uid: str = request.form["uid"]
    pwd: str = request.form["pwd"]

    # Open in "r" mode the users csv file using the constant CSV_FILE
    with open(CSV_FILE, "r") as users_csv_file:
      reader = csv.DictReader(users_csv_file)
      # Loop throught the lines and check if the current line is the user's one
      for row in reader:
        # Check if password match, between users.csv password and the user's form password
        if row["uid"] == uid:
          h_pwd: str = hashlib.sha256((pwd+row["salt"]).encode("utf-8")).hexdigest()
          if row["pwd"] == h_pwd:
            # if login successful -> return "Login successful"
            session["loggedin"] = True
            session["uid"] = uid
            flash("Login successfull", "success")
            return redirect(url_for("private"))
          else:
            return "Wrong credentials"
      
      # otw, return "Wrong credentials"
      return "Wrong credentials"
  else:
    return render_template("login/login.html")

@app.route("/signout")
def logout():  
  session["loggedin"] = False
  del session["loggedin"]
  session.clear()

  return redirect(url_for("login"))
  
@app.route("/private")
def private() -> str:
  """
  This function checks if the user is logged in, and if so, returns a private message
  """
  print(session)
  if not session.get("loggedin", False):
    # If user is NOT logged in
    flash("Please login first", "warning")
    return redirect(url_for("login"))
  else:
    return render_template('private.html')
  
@app.route("/click")
def click():
  session["clicked"] = session.get("clicked", 0) + 1
  return f"<h1>You have clicked {session.get('clicked', 0)} times</h1><a href='{url_for('click')}'>Click Me</a>"

@app.route("/clicked", methods=["POST"])
def click_post():
  session["clicked"] = session.get("clicked", 0) + 1
  return f"<h1>You have clicked {session.get('clicked', 0)} times</h1><a href='{url_for('click')}'>Click Me</a>"
 
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)