import os

import pandas as pd
from flask import Flask, render_template, request

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
    # TODO: get the user uid from form
    # TODO: get the user password from form
    # TODO: get the user password 2 from form

    # TODO: Validate that the two passwords are the same

    # TODO: Open in "a" mode the users csv file using the constant CSV_FILE
    # TODO: Add the new user to the CSV file

    # TODO(BONUS): Check if user already exists in csv file, if so -> return "User already exists"
    return f""
  else:
    return render_template("login/register.html")
  
@app.route("/login", methods=["GET", "POST"])
def login():
  """
  The login functiojn should authenticate a user using his uid and pwd
  """
  if request.method == "POST":
    uid: str = request.form["uid"]
    pwd: str = request.form["pwd"]

    # TODO: Open in "r" mode the users csv file using the constant CSV_FILE
    # TODO: Loop throught the lines and check if the current line is the user's one
    # TODO: Check if password match, between users.csv password and the user's form password
    # TODO: if login successful -> return "Login successful"
    # TODO: otw, return "Wrong credentials"
    return f"{uid} - {pwd}"
  else:
    return render_template("login/login.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)