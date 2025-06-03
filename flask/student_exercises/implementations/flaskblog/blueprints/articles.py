import os, sys
CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)

sys.path.append(ROOT_DIR)

from flask import Blueprint, session, render_template

from config.firestore_connection import db, DocumentReference, DocumentSnapshot
from helpers.decorators import authenticated

article_bp: Blueprint = Blueprint("articles", __name__, url_prefix="/articles")

@article_bp.route("/my")
@authenticated
def get_all_my_articles():
  user_ref: DocumentReference = db.collection("users").document(session["firestore_user_id"])
  user: dict[str, str | int] = user_ref.get().to_dict()
  user_fullname: str = f"{user['firstname']} {user['lastname']}"
  my_articles: list[DocumentSnapshot] = db.collection("articles").where("author", "==", user_ref).get()
  
  my_dict_articles: list[dict[str, str]] = []
  for article in my_articles:
    article_data: dict[str, str | DocumentReference] = article.to_dict()
    article_data["author_fullname"] = user_fullname
    my_dict_articles.append(article_data)

  return render_template("articles/list.html", articles=my_dict_articles)

@article_bp.route("/add") # TODO: accept both get and post methods
@authenticated
def add_article():
  # TODO: Check if we are comming from get request
    # TODO: if we come from get request, validate the form (title and body should not be null)
    # TODO: Add the article in database
    # TODO: redirect to display all my articles
  # TODO: if we are comming from get request, render the articles.new_articles template
  return ""

# TODO: Create a route that displays all the articles from the database, ordered by title