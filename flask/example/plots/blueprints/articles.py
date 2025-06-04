import os, sys
CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)

sys.path.append(ROOT_DIR)

from flask import Blueprint, session, render_template, request, flash, redirect, url_for

from config.firestore_connection import db, DocumentReference, DocumentSnapshot
from helpers.decorators import authenticated
from forms.articles import AddArticle

article_bp: Blueprint = Blueprint("articles", __name__, url_prefix="/articles")

@article_bp.route("/")
@authenticated
def get_all_articles():
  current_user_ref: DocumentReference = db.collection("users").document(session["firestore_user_id"])
  articles: list[DocumentSnapshot] = db.collection("articles").order_by("title").get()
  
  articles_dict: list[dict[str, str]] = []
  for article in articles:
    article_data: dict[str, str | DocumentReference] = article.to_dict()
    user: dict[str, str | int] = article_data["author"].get().to_dict()
    print(user)
    try:
      user_fullname: str = f"{user['firstname']} {user['lastname']}"
    except:
      user_fullname = "None"

    article_data["author_fullname"] = user_fullname
    article_data["id"] = article.id
    articles_dict.append(article_data)

  return render_template("articles/list.html", articles=articles_dict, user_ref=current_user_ref, page_title="Articles")


@article_bp.route("/my")
@authenticated
def get_all_my_articles():
  current_user_ref: DocumentReference = db.collection("users").document(session["firestore_user_id"])
  user: dict[str, str | int] = current_user_ref.get().to_dict()
  user_fullname: str = f"{user['firstname']} {user['lastname']}"
  my_articles: list[DocumentSnapshot] = db.collection("articles").where("author", "==", current_user_ref).get()
  
  my_dict_articles: list[dict[str, str]] = []
  for article in my_articles:
    article_data: dict[str, str | DocumentReference] = article.to_dict()
    article_data["author_fullname"] = user_fullname
    article_data["id"] = article.id
    my_dict_articles.append(article_data)

  return render_template("articles/list.html", articles=my_dict_articles, user_ref=current_user_ref, page_title="My articles")

@article_bp.route("/add", methods=["GET", "POST"]) # accept both get and post methods
@authenticated
def add_article():
  add_article_form = AddArticle(request.form)

  # Check if we are comming from get request
  # if we come from get request, validate the form (title and body should not be null)
  if request.method == "POST" and add_article_form.validate():
    # Add the article in database
    article: dict[str, str | DocumentReference] = {
      "title": add_article_form.title.data,
      "body": add_article_form.body.data,
      "author": db.document(f"users/{session['firestore_user_id']}")
    }
    _, article_ref = db.collection("articles").add(article)
    flash(f"Article successfully created with id {article_ref.id}", "success")
    
    # redirect to display all my articles
    return redirect(url_for("articles.get_all_my_articles"))
  
  # if we are comming from get request, render the articles.new_articles template
  return render_template("articles/new_article.html", form=add_article_form)

@article_bp.route("/delete/<article_id>", methods=["POST"])
@authenticated
def delete_by_id(article_id: str):
  article_ref: DocumentReference = db.document(f"articles/{article_id}")
  article_data: dict[str, str | DocumentReference] = article_ref.get().to_dict()
  current_user_ref: DocumentReference = db.document(f"users/{session['firestore_user_id']}")

  if current_user_ref != article_data.get("author"):
    flash(f"User with id {session['firestore_user_id']} can't delete article with id {article_id}", "danger")
    return redirect(url_for("articles.get_all_my_articles"))
  
  article_ref.delete()
  flash("Post sucessfully deleted", "success")
  return redirect(url_for("articles.get_all_my_articles"))


# Create a route that displays all the articles from the database, ordered by title
