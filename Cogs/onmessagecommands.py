import asyncio
import discord
from discord.ext import commands
import json


def predicate(message, command):
    with open('servers.json', 'r') as f:
        storage = json.load(f)
        commandsList = storage[str(message.guild.id)]["commands"]
        return commandsList[command] == "True"


async def nonocheck(message):
    if str(message.author) != "Hurb#4980":
        for i in ["shit", "fuck", "bitch", "dick", "fuk", "dik", "sht", "btch", " ass "]:
            if message.content.lower().find(str(i)) != -1:
                await message.delete()
                sent = await message.channel.send(
                    embed=discord.Embed(description=f"Swearing is disabled in this server {message.author.mention}.",
                                        color=discord.Color.red()))
                await asyncio.sleep(5)
                await sent.delete()
                break


async def linkcheck(message):
    if message.content.find("https://") != -1 and message.content.find("discord.gg/") or message.content.find(
            "http://") != -1 and message.content.find("discord.gg/"):
        if message.content.find("https://cdn.discordapp.com") and message.content.find("https://tenor.com"):
            await message.delete()
            embed = discord.Embed(description=f"Link sharing is disabled in {message.guild} {message.author.mention}!",
                                  color=discord.Color.red())
            warning = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await warning.delete()


async def invitecheck(message):
    if not message.content.find("https://discord.gg/"):
        await message.delete()
        warning = await message.channel.send(embed=discord.Embed(
            description=f"You are not allowed to post invites in {message.guild.name} {message.author.mention}!",
            color=discord.Color.red()))
        await asyncio.sleep(5)
        await warning.delete()


async def modMuteCheck(message):
    with open("servers.json",
              "r") as f:
        storage = json.load(f)
    if "mutedmods" in storage[str(message.guild.id)].keys():
        if str(message.author.id) in storage[str(message.guild.id)]["mutedmods"].keys():
            if storage[str(message.guild.id)]["mutedmods"][str(message.author.id)] == str(message.guild.id):
                await message.delete()


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            storage = json.load(open("servers.json"))
            if str(message.guild.id) not in storage:
                storage[str(message.guild.id)] = {"prefix": '%',
                                      "commands": {"goodbye": "False", "nitro": "False", "nonocheck": "False",
                                                   "welcome": "False",
                                                   "invitecheck": "False", "linkcheck": "False", "antispam": "False",
                                                   "ranking": "False"},
                                      "blacklist": {},
                                      "goodbye": {},
                                      "welcome": {},
                                      "levelupmessage": "Congrats {member}! You leveled up to level {level}!",
                                      "levelroles": {}}
                json.dump(storage, open("servers.json", "w"), indent=4)
            if predicate(message, "nonocheck"):
                await nonocheck(message)
            if predicate(message, "linkcheck"):
                await linkcheck(message)
            if predicate(message, "invitecheck"):
                await invitecheck(message)
            await modMuteCheck(message)


def setup(bot):
    bot.add_cog(MessageCommands(bot))
