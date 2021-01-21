import pymongo, dotenv, os
from pymongo import MongoClient

dotenv.load_dotenv()
LINK = os.environ.get("LINK", None)
cluster = AsyncIOMotorClient(LINK)
settings = cluster["hurb"]["settings"]
post = {"_id": 0, "name": "seth"}
stuff = await settings.find_one_and_replace(post).inserted_id
