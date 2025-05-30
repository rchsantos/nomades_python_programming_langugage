import os
import hashlib
import json

from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

from helpers.random_password_generator import generate_password

CURR_DIR: str = os.path.dirname(__file__)
UPLOADS_DIR: str = os.path.join(CURR_DIR, "static", "uploads")

cred = credentials.Certificate(os.path.join(CURR_DIR, 'config', "firestore-creds.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()

with open(os.path.join(CURR_DIR, "config", "creds.json")) as json_config:
  config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]

CURR_DIR: str = os.path.dirname(__file__)

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

    # TODO: Add the new user to the firestore users collection
      # TODO: Create a dictionnary representing the new user
      # TODO: call the add function on the collection reference
      # TODO: add user id in session
      # TODO: redirect the user to the user info page

    # TODO(BONUS): Check if user already exists
    # TODO(BONUS): hash the password, using salt
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

    # TODO: Get all the users from the database
    # TODO: Loop throught the users
    #   TODO: Check if username / password match
      # TODO: if login successful -> add user id in session; redirect to userinfo route
    # TODO: otw, return "Wrong credentials"
    return f"{uid} - {pwd}"
  else:
    return render_template("login/login.html")

# TODO: Create the logout route
  
# TODO: cretae user info route accessible via GET
# TODO: This route should be protected by login (if not logged -> redirect to login)
# TODO: This route do a get on the connected user
# TODO: Return the users/userinfo.html template and gives the firestore user data as parameters (firstname, lastname, age, email, uid)
 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)