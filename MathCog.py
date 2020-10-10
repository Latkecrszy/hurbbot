import discord
from discord.ext import commands
import random

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


class MathCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def multiply(self, ctx, num1: int, num2: int):
        await ctx.send(embed=discord.Embed(title=f"{num1} multiplied by {num2} equals {num1*num2}", color=random.choice(embedColors)))

    @commands.command()
    async def divide(self, ctx, num1: int, num2: int):
        await ctx.send(embed=discord.Embed(title=f"{num1} divided by {num2} equals {num1/num2}", color=random.choice(embedColors)))

    @commands.command()
    async def add(self, ctx, num1: int, num2: int):
        await ctx.send(embed=discord.Embed(title=f"{num1} added to {num2} equals {num1+num2}", color=random.choice(embedColors)))

    @commands.command()
    async def subtract(self, ctx, num1: int, num2: int):
        await ctx.send(embed=discord.Embed(title=f"{num1} subtracted from {num2} equals {num1-num2}", color=random.choice(embedColors)))

    @commands.command(aliases=["power"])
    async def exponent(self, ctx, num1: int, num2: int):
        await ctx.send(embed=discord.Embed(title=f"{num1} to the power of {num2} equals {num1**num2}",
                                           color=random.choice(embedColors)))

    @commands.command()
    async def point_slope(self, ctx, point, slope):
        if slope.find("/") != -1:
            slope = slope.split("/")
        pointList = []
        for char in point:
            if char != "(" and char != ")":
                pointList.append(char)
        point = "".join(pointList)
        point = point.split(",")
        if isinstance(slope, list):
            await ctx.send(embed=discord.Embed(title=f"y - {point[0]} = {slope[0]}/{slope[1]}(x-{point[1]})"))
        else:
            await ctx.send(embed=discord.Embed(title=f"y - {point[0]} = {slope}(x-{point[1]})"))

    @commands.command()
    async def slope_intercept(self, ctx):
        pass


def setup(bot):
    bot.add_cog(MathCog(bot))

