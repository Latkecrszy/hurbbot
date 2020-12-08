import discord
from discord.ext import commands
import json
import asyncio
import random
import dbl


class VoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczNjI4Mzk4ODYyODYwMjk2MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA1MjQ1NTYxfQ.bJKBh2Yy0Qa8H47yTED-_GgltkOfZVx9EZEYsuICqyU'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, token=self.token)

    @commands.command()
    async def vote(self, ctx):
        embed = discord.Embed(title=f"Vote for Hurb to get free rewards! (and, you know, make my day :)",
                              description=f"**Click [here](https://top.gg/bot/736283988628602960/vote) to vote!**",
                              color=discord.Color.teal())
        embed.set_footer(text=f"Voting for Hurb can earn you in game currency, along with the satisfaction of helping Hurb to rise in the ranks!")
        await ctx.send(embed=embed)

    """
JSON Params
Field	Type	Description
bot	Snowflake	ID of the bot that received a vote
user	Snowflake	ID of the user who voted
type	String	The type of the vote (should always be "upvote" except when using the test button it's "test")
isWeekend	Boolean	Whether the weekend multiplier is in effect, meaning users votes count as two
query?	String	Query string params found on the /bot/:ID/vote page. Example: ?a=1&b=2
"""

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print("received vote")
        print(data)


def setup(bot):
    bot.add_cog(VoteCog(bot))
