import os, sys
CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)

sys.path.append(ROOT_DIR)

import hashlib
from uuid import uuid4

from flask import Blueprint, request, flash, render_template, url_for, redirect, session

from config.firestore_connection import db, DocumentSnapshot
from forms.login import RegisterForm
from helpers.random_password_generator import generate_password as generate_salt

login_bp: Blueprint = Blueprint("login", __name__)

@login_bp.route("/register", methods=["GET", "POST"])
def register():
  """
  Register function should add a new user to the users.csv file
  """
  if session.get("firestore_user_id"):
    return redirect(url_for("userinfo"))

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

@login_bp.route("/login", methods=["GET", "POST"])
def login():
  """
  The login functiojn should authenticate a user using his uid and pwd
  """
  if session.get("firestore_user_id"):
    return redirect(url_for("userinfo"))
  
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

@login_bp.route("/logout")
def logout():
  session.clear()
  flash("Successfully logged out", "success")
  return redirect(url_for("login.login"))