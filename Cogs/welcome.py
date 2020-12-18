import discord
from discord.ext import commands
import asyncio
import json


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(WelcomeCog(bot))
