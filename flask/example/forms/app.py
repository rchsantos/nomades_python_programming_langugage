import os
from uuid import uuid4

import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)

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

from flask import Flask, request

app = Flask(__name__)

@app.route('/form/file', methods=['GET', 'POST'])
def form_file():
  if request.method == 'POST': # request object has attribute method, which is a string informing the method used in the request
    file = request.files['fileInput']
    filename: str = file.filename
    ext: str = filename.split(".")[-1]
    new_filename: str = f"{uuid4()}.{ext}"
    file.save(os.path.join(CURR_DIR, "uploads", new_filename))
    return 'File uploaded successfully'
  return '''
    <form action="" method="POST" enctype="multipart/form-data">
      <input type="file" name="fileInput">
      <input type="submit" value="Envoyer">
    </form>
  '''

@app.route('/form/files', methods=['GET', 'POST'])
def form_files():
  if request.method == 'POST': # request object has attribute method, which is a string informing the method used in the request
    files = request.files.getlist('fileInput')
    for file in files:
      filename: str = file.filename
      ext: str = filename.split(".")[-1]
      new_filename: str = f"{uuid4()}.{ext}"
      print(file.mimetype, file.name)
      file.save(os.path.join(CURR_DIR, "uploads", new_filename))

    return 'Files uploaded successfully'
  return '''
    <form action="" method="POST" enctype="multipart/form-data">
      <input type="file" name="fileInput" multiple accept="image/jpg, image/png">
      <input type="submit" value="Envoyer">
    </form>
  '''

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)