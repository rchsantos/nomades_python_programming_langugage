import os
import hashlib
import json
from uuid import uuid4
from functools import wraps

from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

from helpers.random_password_generator import generate_password as generate_salt
from forms.login import RegisterForm

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

def authenticated(func):
  @wraps(func)
  def inner(*args, **kwargs):
    if not session.get("firestore_user_id", ""):
      flash("Please login first", "warning")
      return redirect(url_for("login"))

    return func(*args, **kwargs)
  return inner

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
  """
  Register function should add a new user to the users.csv file
  """
  register_form = RegisterForm(request.form, data=request.files)

  if request.method == "POST" and register_form.validate():
    firstname: str = register_form.firstname.data
    lastname: str = register_form.lastname.data
    uid: str = register_form.uid.data
    email: str = register_form.email.data
    age: int = register_form.age.data
    profile_picture = register_form.pp.data
    pwd: str = register_form.pwd.data

    users: list[DocumentSnapshot] = db.collection("users").where("uid", "==", uid).get()
    if len(users) != 0:
      flash("User already exists", "warning")
      return render_template("login/register.html", form=register_form)

    users: list[DocumentSnapshot] = db.collection("users").where("email", "==", email).get()
    if len(users) != 0:
      flash("User already exists", "warning")
      return render_template("login/register.html", form=register_form)
    
    salt: str = generate_salt(True, False, False, False, 10)
    pwd_h: str = hashlib.sha256((pwd+salt).encode("utf-8")).hexdigest()

    try:
      filename: str = f"{uuid4()}.{profile_picture.filename.split('.')[-1]}"
    except:
      filename = ""

    profile_picture.save(os.path.join(CURR_DIR, 'static', 'imgs', 'uploads', filename))

    # Add the new user to the firestore users collection
    # Create a dictionnary representing the new user
    user: dict[str, str | int] = {
      'firstname': firstname,
      'lastname': lastname,
      'uid': uid,
      'email': email,
      'age': age,
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
  
  return render_template("login/register.html", form=register_form)
  
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
  
    users: list[DocumentSnapshot] = db.collection("users").where("uid", "==", uid).get()
    if len(users) == 0:
      users = db.collection("users").where("email", "==", uid).get()
      if len(users) == 0:
        flash("Wrong credentials", "danger")
        return render_template("login/login.html")
    
    assert len(users) == 1, f"More than 1 user matched {uid}"
    user_data: dict[str, str | int] = users[0].to_dict()
    pwd_h: str = hashlib.sha256((pwd+user_data.get("salt", "")).encode("utf-8")).hexdigest()

    if pwd_h != user_data["pwd"]:
      flash("Wrong credentials", "danger")
      return render_template("login/login.html")
    
    session["firestore_user_id"] = users[0].id
    session["loggedin"] = True
    flash("Login successfull", "success")
    return redirect(url_for("userinfo"))
  
  return render_template("login/login.html")

# Create the logout route
@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("login"))
  
# cretae user info route accessible via GET
@app.route("/userinfo")
@authenticated
def userinfo(): 
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

@app.route("/secret")
@authenticated
def secret():
  return "<h1>This is secret</h1>"
 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)