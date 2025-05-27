import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    uid: str = request.form["uid"]
    pwd: str = request.form["pwd"]
    return f"{uid} - {pwd}"
  else:
    return render_template("login/login.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)