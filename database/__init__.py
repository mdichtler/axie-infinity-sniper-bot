import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

# Use a service account, you can get this from project settings of your firebase project,
# either adjust path or create file at the given location.
# TODO: Add Service Account Key
cred = credentials.Certificate('./database/serviceAccountKey.json')
firebase_admin.initialize_app(cred)




class Database():
    def __init__(self):
        self.db = firestore.client()

    # push latest leaderboard to be picked up by next scraper
    def push_leaderboard_to_db(self, data):
        leaderboard_ref = self.db.collection('leaderboards')
        leaderboard_ref.add({
            u'time': datetime.datetime.now(),
            u'data': data
        })

