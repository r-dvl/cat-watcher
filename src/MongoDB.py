from pymongo import MongoClient
from configuration import MONGO_USER, MONGO_PASSWORD, MONGO_URI, MONGO_DB


class MongoDB:
    def __init__(self):
        self.user = MONGO_USER
        self.password = MONGO_PASSWORD
        self.uri = MONGO_URI
        self.db = MONGO_DB
        self.collection = 'photos'
        self.completeUri = f"mongodb://{self.user}:{self.password}@{self.uri}/{self.db}"

    def post_photo(self, image, date):
        client = MongoClient(self.completeUri)
        db = client[self.db]
        collection = db[self.collection]

        document = {
            "image": image,
            "date": date,
        }

        post = collection.insert_one(document)

        print('Photo uploaded')
