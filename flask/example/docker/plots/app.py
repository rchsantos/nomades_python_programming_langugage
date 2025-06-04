import os
import json

from flask import Flask, render_template, session

from config.firestore_connection import db
from helpers.decorators import authenticated

from blueprints.login import login_bp
from blueprints.articles import article_bp
from blueprints.statistics import statistics_bp

CURR_DIR: str = os.path.dirname(__file__)
UPLOADS_DIR: str = os.path.join(CURR_DIR, "static", "uploads")

with open(os.path.join(CURR_DIR, "config", "creds.json")) as json_config:
  config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]

app.register_blueprint(login_bp)
app.register_blueprint(article_bp)
app.register_blueprint(statistics_bp)

CURR_DIR: str = os.path.dirname(__file__)

@app.route("/")
def index():
  return render_template("index.html")
  
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