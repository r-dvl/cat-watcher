from pymongo import MongoClient


class MongoDB:
    def __init__(self, uri, db, collection):
        self.uri = uri
        self.db = db
        self.collection = collection

    def post_photo(self, image, date):
        client = MongoClient(self.uri)
        db = client[self.db]
        collection = db[self.collection]

        document = {
            "image": image,
            "date": date,
        }

        post = collection.insert_one(document)

        print('Photo uploaded')
