import dbl
import discord
from discord.ext import commands
import json
import logging


class VoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        logger.info('Received an upvote')
        print(data)


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(VoteCog(bot))
