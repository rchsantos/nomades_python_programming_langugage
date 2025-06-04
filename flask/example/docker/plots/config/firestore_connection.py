import os

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

CURR_DIR: str = os.path.dirname(__file__)

__cred = credentials.Certificate(os.path.join(CURR_DIR, "firestore-creds.json"))
firebase_admin.initialize_app(__cred)
db = firestore.client()