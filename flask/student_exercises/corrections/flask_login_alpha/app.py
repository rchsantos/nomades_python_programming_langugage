import os
import csv
import hashlib

from flask import Flask, render_template, request

from helpers.random_password_generator import generate_password as generate_salt

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, 'users.csv')

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
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
      return "Please provide the same passwords"
    
    if uid == "" or pwd == "":
      return "Please provide UID and PWD"
    
    if ',' in uid or ',' in pwd:
      return "Please avoid the use of ',' (coma) in UID and PWD"
    
    salt: str = generate_salt(True, False, False, False, 10)
    h_pwd: str = hashlib.sha256((pwd+salt).encode("utf-8")).hexdigest()
    
    # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
    with open(CSV_FILE, "r") as users_csv_file:
      reader = csv.DictReader(users_csv_file)
      # Loop throught the lines and check if the current line is the user's one
      for row in reader:
        if row["uid"] == uid:
          return "User already exists"

    # Open in "a" mode the users csv file using the constant CSV_FILE
    with open(CSV_FILE, "a") as users_csv_file:
      # Add the new user to the CSV file
      writer = csv.writer(users_csv_file)
      writer.writerow([uid, salt, h_pwd])

    return f"User successfully registered"

  return render_template("login/register.html")
  
@app.route("/login", methods=["GET", "POST"])
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
            return "Login successful"
          else:
            return "Wrong credentials"
      
      # otw, return "Wrong credentials"
      return "Wrong credentials"
  else:
    return render_template("login/login.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)