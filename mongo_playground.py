import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://Latkecrszy:LatkeCrazy1746@hurb.rt8i0.mongodb.net/Hurb?retryWrites=true&w=majority")
db = cluster["hurb"]
collection = db["settings"]
post = {"_id": 0, "name": "seth"}
stuff = collection.find_one_and_replace(post).inserted_id
