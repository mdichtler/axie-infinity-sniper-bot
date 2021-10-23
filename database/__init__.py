import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

# Use a service account
cred = credentials.Certificate('./database/serviceAccountKey.json')
firebase_admin.initialize_app(cred)




class Database():
    def __init__(self):
        self.db = firestore.client()

    def push_leaderboard_to_db(self, data):
        leaderboard_ref = self.db.collection('leaderboards')
        leaderboard_ref.add({
            u'time': datetime.datetime.now(),
            u'data': data
        })

