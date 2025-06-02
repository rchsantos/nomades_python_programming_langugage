import os
import hashlib
import json
from uuid import uuid4

from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

from helpers.random_password_generator import generate_password as generate_salt

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
    firstname: str = request.form.get("firstname", "")
    lastname: str = request.form.get("lastname", "")
    uid: str = request.form.get("uid", "")
    email: str = request.form.get("email", "")
    age: str = request.form.get("age", "")
    profile_picture = request.files.get("profile_picture")
    pwd: str = request.form.get("pwd", "")
    pwd2: str = request.form.get("pwd2", "")

    # Validate that the two passwords are the same
    if pwd != pwd2:
      flash("Passswords must be the same !", "danger")
      return render_template("login/register.html")
    
    if not (
      firstname 
      and lastname 
      and uid 
      and email 
      and age 
      and pwd
    ):
      flash("Please complete the form", "danger")
      return render_template("login/register.html")
    
    try:
      age_int: int = int(age)
    except:
      flash("Please provide a numerical value for the age", "danger")
      return render_template("login/register.html")
    
    salt: str = generate_salt(True, False, False, False, 10)
    pwd_h: str = hashlib.sha256((pwd+salt).encode("utf-8")).hexdigest()

    filename: str = f"{uuid4()}.{profile_picture.filename.split('.')[-1]}"
    profile_picture.save(os.path.join(CURR_DIR, 'static', 'imgs', 'uploads', filename))

    # Add the new user to the firestore users collection
    # Create a dictionnary representing the new user
    user: dict[str, str | int] = {
      'firstname': firstname,
      'lastname': lastname,
      'uid': uid,
      'email': email,
      'age': age_int,
      'pwd': pwd_h,
      'salt': salt,
      'pp_filename': filename
    }
    # call the add function on the collection reference
    _, user_ref = db.collection("users").add(user)
    # add firestore's user id in session
    session["firestore_user_id"] = user_ref.id
    session["loggedin"] = True
    # redirect the user to the user info page
    flash("User inserted successfully", "success")
    return redirect(url_for("userinfo"))
    # TODO(BONUS): Check if user already exists
  return render_template("login/register.html")
  
@app.route("/login", methods=["GET", "POST"])
def login():
  """
  The login functiojn should authenticate a user using his uid and pwd
  """
  if request.method == "POST":
    uid: str = request.form["uid"]
    pwd: str = request.form["pwd"]

    if not (uid and pwd):
      flash("Please enter valid values", "danger")
      return render_template("login/login.html")

    # Get all the users from the database
    # Loop throught the users
    for user in db.collection("users").get():
      user_data: dict[str, str | int] = user.to_dict()
      
      if user_data.get("uid", "") == uid or user_data.get("email", "") == uid:
        pwd_h: str = hashlib.sha256((pwd+user_data.get("salt", "")).encode("utf-8")).hexdigest()

        if pwd_h == user_data.get("pwd", ""):
          session["firestore_user_id"] = user.id
          session["loggedin"] = True
          flash("Login successfull", "success")
          return redirect(url_for("userinfo"))

    flash("Wrong credentials", "warning")
  return render_template("login/login.html")

# Create the logout route
@app.route("/signout")
def logout():
  session.clear()
  return redirect(url_for("login"))
  
# cretae user info route accessible via GET
@app.route("/userinfo")
def userinfo():
  # This route should be protected by login (if not logged -> redirect to login)
  if not session.get("firestore_user_id", ''):
    flash("Login first", "warning")
    return redirect(url_for("login"))
  
  # This route do a get on the connected user
  user_data: dict[str, str | int] = db.collection("users").document(session["firestore_user_id"]).get().to_dict()

  # Return the users/userinfo.html template and gives the firestore user data as parameters (firstname, lastname, age, email, uid)
  return render_template("users/userinfo.html", 
                         firstname=user_data["firstname"],
                         lastname=user_data["lastname"],
                         age=user_data["age"],
                         email=user_data["email"],
                         uid=user_data["uid"],
                         profile_picture_filename=user_data["pp_filename"]
  )
 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)