import pymongo, dotenv, os
from pymongo import MongoClient

dotenv.load_dotenv()
LINK = os.environ.get("LINK", None)
cluster = MongoClient(LINK)
db = cluster["hurb"]
collection = db["settings"]
post = {"_id": 0, "name": "seth"}
stuff = collection.find_one_and_replace(post).inserted_id
