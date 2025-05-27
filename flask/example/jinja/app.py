import pandas as pd
from flask import Flask, render_template

app = Flask(__name__, template_folder="pages")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/variable")
def variable():
  name: str = "test test test"
  return render_template("variables.html", fullname=name, coucou="salut")

@app.route("/variable/<name>")
def variable_dyn(name: str):
  return render_template("variables.html", fullname=name, coucou="Hello")

@app.route("/for")
def jinja_for():
  fruits: list[str] = [
    "apple",
    "banana",
    "orange",
    "watermelon",
    "peach",
    "strawberry",
    "kiwi",
    "pineapple",
    "grape",
    "mango",
    "lemon",
    "coconut"
  ]
  return render_template("for.html", fruits=fruits)

@app.route("/if")
def jinja_if():
  age = 22
  return render_template("if.html", age=age)

@app.route("/safe")
def jinja_safe():
  html: str = '<script>alert("Hacked!!!")</script>'
  return render_template("filter.html", html=html)

@app.route("/pandas")
def jinja_pandas_safe():
  df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "<script>alert('Hacked!!!')</script>"],
    "age": [25, 30, 35]
  })
  html: str = df.to_html()
  return render_template("filter.html", html=html)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)