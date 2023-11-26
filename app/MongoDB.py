import os
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.db = 'lima'
        self.collection = 'cat-watcher'
        self.completeUri = os.environ["MONGODB_URL"]

    def post_photo(self, image, date):
        client = MongoClient(self.completeUri)
        db = client[self.db]
        collection = db[self.collection]

        document = {
            "image": image,
            "date": date,
            "cat": True,
        }

        post = collection.insert_one(document)

        print('Photo uploaded')
