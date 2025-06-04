import os, sys
CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

PLOTS_DIR: str = os.path.join(ROOT_DIR, "static", "imgs", "plots")

from matplotlib.figure import Figure
import plotly.express as px
import pandas as pd

from flask import Blueprint, render_template

statistics_bp: Blueprint = Blueprint("statistics", __name__, url_prefix="/statistics")

@statistics_bp.route("/matplotlib")
def dummy_stats():
  x = list(range(1, 13))
  y = [xi*xi for xi in x]

  fig = Figure()
  ax = fig.subplots()
  ax.plot(x, y, label="Sales 2025")
  ax.title = "Sales"
  ax.set_xlabel("Month number")
  ax.set_ylabel("Quantity saled")
 
  fig.savefig(os.path.join(PLOTS_DIR, "sales.png"), format="png")

  return render_template("statistics/matplotlib.html")

@statistics_bp.route("/plotly")
def plotly_dummy():
  x = list(range(1, 13))
  y = [xi*xi for xi in x]
  df = pd.DataFrame({"months": x, "sales 2025": y})
  plot = px.line(df, "months", "sales 2025")
  bar = px.bar(df, "months", "sales 2025").to_html(full_html=False)

  return render_template("statistics/plotly.html", plot=plot.to_html(full_html=False), bar=bar)