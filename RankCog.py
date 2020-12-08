import discord
from discord.ext import commands
import json
import asyncio
import random


def is_me(command):
    def predicate(ctx):
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
            return commandsList[command] == "True"

    return commands.check(predicate)


class RankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@is_me("ranking")
    @commands.Cog.listener()
    async def on_message(self, message):
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json") as f:
            messages = json.load(f)
        if str(message.guild.id) in messages.keys():
            if str(message.author.id) in messages[str(message.guild.id)].keys():
                print("working")
                print(str(message.author))
                messages[str(message.guild.id)][str(message.author.id)]["messages"] += 1
                print(messages[str(message.guild.id)][str(message.author.id)]["messages"])
                #messages[str(message.guild.id)][str(message.author.id)]["xp"] += random.randint(int(messages[str(message.guild.id)][str(message.author.id)]["level"])/2, int(messages[str(message.guild.id)][str(message.author.id)]["level"]*2))
                #await self.levelupcheck(message, messages)
                with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json", "w") as f:
                    json.dump(messages, f, indent=4)

            else:
                messages[str(message.guild.id)][str(message.author.id)] = {"messages": 1, "xp": random.randint(1, 5), "level": 1}
                with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json", "w") as f:
                    json.dump(messages, f, indent=4)
        else:
            messages[str(message.guild.id)] = {}
            with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json", "w") as f:
                json.dump(messages, f, indent=4)
            await self.on_message(message)
        await self.bot.process_commands()

    async def levelupcheck(self, message, messages):
        if messages[str(message.guild.id)][str(message.author.id)]["xp"] >= int(messages[str(message.guild.id)][str(message.author.id)]["level"]*200):
            messages[str(message.guild.id)][str(message.author.id)]["xp"] = 0
            await message.channel.send(embed=discord.Embed(description=f"Congrats {message.author.mention}! You leveled up to level {messages[str(message.guild.id)][str(message.author.id)]['level']+1}!"))
            messages[str(message.guild.id)][str(message.author.id)]["level"] += 1
        return messages

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json") as f:
            messages = json.load(f)
        embed = discord.Embed(title=f"{member}'s rank in {ctx.guild}")
        embed.add_field(name=f"Messages sent: ", value=str(messages[str(ctx.guild.id)][str(member.id)]["messages"])+" messages")
        embed.add_field(name=f"Experience Points:", value=str(messages[str(ctx.guild.id)][str(member.id)]["xp"]))
        embed.add_field(name="Level:", value=str(messages[str(ctx.guild.id)][str(member.id)]["level"]))
        embed.add_field(name="XP needed to level up:", value=str(messages[str(ctx.guild.id)][str(member.id)]["level"]*200-messages[str(ctx.guild.id)][str(member.id)]["xp"])+" more XP")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RankCog(bot))
