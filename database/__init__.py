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

    def push_on_sale_axies(self, axie):
        on_sale_ref = self.db.collection('on_sale')
        on_sale_ref.add({
            u'time': datetime.datetime.now(),
            u'axie': axie,
            u'currentPriceUSD': float(axie["auction"]["currentPriceUSD"]),
            u'class': axie["class"],
            u'id': axie["id"],
            u'image': axie["image"],
            u'player_rank': axie["player_rank"]
        })
