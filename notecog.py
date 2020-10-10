import discord
from discord.ext import commands, tasks
import json
import asyncio


class NoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.noteTaker = ""

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.noteTaker == str(message.author):
            with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/notes.json", "r") as f:
                notes = json.load(f)