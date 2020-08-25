import discord
from discord.ext import commands
import random
import asyncio
import json


def is_me(command):
    def predicate(ctx):
        with open('/Users/sethraphael/PycharmProject/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
            return commandsList[command] == "True"

    return commands.check(predicate)


class BotFunCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @is_me("rps")
    @commands.command()
    async def rps(self, ctx, choice):
        choice = choice.lower()
        choices = ["rock", "paper", "scissors"]
        botChoice = random.choice(choices)
        if choice == botChoice:
            embed = discord.Embed(title=f"You tied! We both chose {choice}!")
        elif choice == "rock" and botChoice == "paper":
            embed = discord.Embed(
                title=f"<:check:742198670912651316> I won! Paper triumphs! HAHA ***LOSER*** You suck lol")
        elif choice == "rock" and botChoice == "scissors":
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> Oh fucking shit, you won. Rock beats scissors. I'll beat the shit out of you next time.")
            embed.set_image(
                url="https://external-preview.redd.it/WWKFVkxfVnaWZkeOS0MT0BOfLtfk7V1NlXBSfLY2N7c.jpg?auto=webp&s=a52bcb55f2fdd09346665cc650bbdca01dd9c595")
        elif choice == "paper" and botChoice == "rock":
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> Oh fucking shit, you won. Paper beats rock. I'll beat the shit out of you next time.")
            embed.set_image(
                url="https://external-preview.redd.it/WWKFVkxfVnaWZkeOS0MT0BOfLtfk7V1NlXBSfLY2N7c.jpg?auto=webp&s=a52bcb55f2fdd09346665cc650bbdca01dd9c595")
        elif choice == "paper" and botChoice == "scissors":
            embed = discord.Embed(
                title=f"<:check:742198670912651316> I won! Scissors triumphs! HAHA ***LOSER*** You suck lol")
        elif choice == "scissors" and botChoice == "paper":
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> Oh fucking shit, you won. Scissors beats paper. I'll beat the shit out of you next time.")
            embed.set_image(
                url="https://external-preview.redd.it/WWKFVkxfVnaWZkeOS0MT0BOfLtfk7V1NlXBSfLY2N7c.jpg?auto=webp&s=a52bcb55f2fdd09346665cc650bbdca01dd9c595")
        elif choice == "scissors" and botChoice == "rock":
            embed = discord.Embed(
                title=f"<:check:742198670912651316> I won! Rock triumphs! HAHA ***LOSER*** You suck lol")
        else:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> What the fuck were you THINKING man that ain't an option.")
        await ctx.send(embed=embed)

    @is_me("testreaction")
    @commands.command()
    async def testreaction(self, message):
        controller = await message.channel.send("Hit me with that 👍 reaction!")
        await controller.add_reaction('👎')
        await controller.add_reaction('👍')
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=None)
        except asyncio.TimeoutError:
            await message.channel.send('👎')
        else:
            print(reaction)

    @is_me("purge")
    @commands.command()
    async def purge(self, message, number):
        await message.channel.purge(limit=int(int(number) + 1))

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''Please specify how many messages you would like to purge.''')
        else:
            raise error.original


def setup(bot):
    bot.add_cog(BotFunCog(bot))
