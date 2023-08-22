from dotenv import load_dotenv
import os

load_dotenv('.env')

MONGODB_URL = os.getenv("URI")
DB_NAME = os.getenv("DB")
COLLECTION_NAME = os.getenv("collection")
