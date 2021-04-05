from motor.motor_asyncio import AsyncIOMotorClient
import pymongo.errors as errors
from pymongo import ReturnDocument
import os, dotenv

dotenv.load_dotenv()

LINK = os.environ.get("LINK", None)


class MotorClient:
    def __init__(self):
        self.client = AsyncIOMotorClient(LINK).hurb

    async def find_one_and_replace(self, find, replace, collection=None):
        try:
            if collection is None:
                settings = self.client['settings']
            else:
                settings = self.client[collection]
            return await settings.find_one_and_replace(find, replace, return_document=ReturnDocument.AFTER)

        except errors.AutoReconnect:
            print("reconnecting...")
            self.client = AsyncIOMotorClient(LINK).hurb
            await self.find_one_and_replace(find, replace)

    async def find_one(self, find, collection=None):
        try:
            if collection is None:
                settings = self.client.settings
                result = await settings.find_one(find)
                if result is None or 'commands' not in result:
                    print("inserted one")
                    await settings.insert_one({"prefix": '%',
                                               "commands": {"goodbye": "False", "nitro": "True", "nonocheck": "False",
                                                            "welcome": "False",
                                                            "invitecheck": "False", "linkcheck": "False",
                                                            "antispam": "False",
                                                            "ranking": "True"},
                                               "blacklist": {},
                                               "goodbye": {},
                                               "welcome": {},
                                               "levelupmessage": "Congrats {member}! You leveled up to level {level}!",
                                               "levelroles": {},
                                               "rank": {},
                                               "id": find['id']})
                    result = await settings.find_one(find)
            else:
                settings = self.client[collection]
                result = await settings.find_one(find)
                if result is None:
                    await settings.insert_one(find)
                    result = await settings.find_one(find)
            return result
        except errors.AutoReconnect:
            self.client = AsyncIOMotorClient(LINK).hurb
            await self.find_one(find)

    async def insert_one(self, insert, collection=None):
        try:
            settings = self.client.settings if collection is None else self.client[collection]
            return await settings.insert_one(insert)
        except errors.AutoReconnect:
            self.client = AsyncIOMotorClient(LINK).hurb
            await self.insert_one(insert)


    async def find_one_and_delete(self, find, collection=None):
        try:
            settings = self.client.settings if collection is None else self.client[collection]
            return await settings.find_one_and_delete(find)
        except errors.AutoReconnect:
            self.client = AsyncIOMotorClient(LINK).hurb
            await self.find_one_and_delete(find)
