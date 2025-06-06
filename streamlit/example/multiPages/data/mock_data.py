import random
from datetime import datetime, timedelta

# pip install wonderwords
from wonderwords import RandomSentence

from firestore_connection import db, DocumentReference

def create_users() -> list[dict[str, str | int | DocumentReference]]:
  users: list[dict[str, str | int]] = [{
    "firstname": "Kevin",
    "lastname": "Blackman",
    "age": 52
  },
  {
    "firstname": "Francis",
    "lastname": "Lauper",
    "age": 44
  },
  {
    "firstname": "Marlène",
    "lastname": "Joris",
    "age": 34
  }, 
  {
    "firstname": "Ashton",
    "lastname": "Alphandery",
    "age": 39
  }]

  for user in users:
    _, userRef = db.collection("users").add(user)
    user["ref"] = userRef

  print("Users successfully inserted")
  return users

def generate_random_date(start_date: datetime, end_date: datetime) -> datetime:
  delta = end_date - start_date
  random_days: int = random.randint(0, delta.days)
  return start_date + timedelta(days=random_days)


def create_articles(users: list[dict[str, str | int | DocumentReference]]):
  sentence: RandomSentence = RandomSentence()
  start_date: datetime = datetime(2025, 5, 28)
  end_date: datetime = datetime(2025, 6, 6)

  for _ in range(100):
    db.collection("articles").add({
      "title": f"t: {sentence.sentence()}",
      "body": "\n".join([sentence.sentence() for _ in range(random.randint(5, 10))]),
      "created_at": generate_random_date(start_date, end_date),
      "author": random.choice(users)["ref"]
    })
  
  print("Articles successfully inserted")

create_articles(create_users())