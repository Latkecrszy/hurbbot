import discord
from discord.ext import commands
import json
import asyncio
import random


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(VoiceCog(bot))
