import discord
from discord.ext import commands
import asyncio
import json
import random


class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.petList = {"dog": 100000, "cat": 200000, "turtle": 300000, "monkey": 400000, "rock": 50000, "fish": 75000}

    @commands.command(aliases=["petlist", "petshop"])
    async def pets(self, ctx):
        embed = discord.Embed(title=f"Pet shop:")
        for pet, cost in self.petList.items():
            embed.add_field(name=pet.capitalize(), value=f"Cost: ${cost}")
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Pets(bot))
