import asyncio
import discord
from discord.ext import commands
import json

agreeing = False
WCI = False
WCIAsk = False
bandAsk = False
band = False
done = False
nonoWords = ["shit", "fuck", "bitch", "dick", "fuk", "dik", "sht", "btch", " ass "]


def is_me(command):
    def predicate(ctx):
        with open('../Bots/servers.json', 'r') as f:
            storage = json.load(f)
            commandsList = storage[str(ctx.guild.id)]["commands"]
            if commandsList[command] == "True":
                return True
            else:
                return False

    return commands.check(predicate)


def predicate(message, command):
    with open('../Bots/servers.json', 'r') as f:
        storage = json.load(f)
        commandsList = storage[str(message.guild.id)]["commands"]
        return commandsList[command] == "True"


class Authorize:
    def __init__(self):
        self.agreeing = False
        self.WCI = False
        self.WCIAsk = False
        self.bandAsk = False
        self.band = False
        self.done = False

    async def authorize(self, message):
        if message.guild.id == 746825963286822992:

            for roles in list(message.author.roles):
                if str(roles).lower() == "unverified":
                    self.agreeing = True
            if self.agreeing:
                if message.content.lower() == "agree" or message.content.lower() == "i agree":
                    await message.channel.send(
                        f"Ok, {message.author.mention}, you have been approved to {message.guild.name}. Now, answer a few questions to set your roles!")
                    await message.channel.send(
                        "If you attend WCI, type `yes` in the chat below. If you do not, or do not know what that even is, type `no`.")
                    self.WCIAsk = True

                elif message.content.lower() == "yes" and self.WCIAsk:
                    self.WCI = True
                    await message.channel.send(
                        f"Ok, {message.author.mention}, you have been marked as a member of WCI. Next question:")
                    await message.channel.send(
                        f"Do you play an instrument of any kind? If yes, type `yes` in the chat below. Otherwise, type `no`.")
                    self.bandAsk = True
                    self.WCIAsk = False
                elif message.content.lower() == "no" and self.WCIAsk:
                    self.WCI = False
                    await message.channel.send(
                        f"Ok, {message.author.mention}, you have been marked as not being a member of WCI. Next question:")
                    await message.channel.send(
                        f"Do you play an instrument of any kind? If yes, type `yes` in the chat below. Otherwise, type `no`.")
                    self.bandAsk = True
                    self.WCIAsk = False
                elif message.content.lower() == "yes" and self.bandAsk:
                    self.band = True
                    await message.channel.send(
                        f"Ok, {message.author.mention}, you have been marked as being able to play an instrument. You are now free to explore the server!")
                    self.done = True
                    self.bandAsk = False
                elif message.content.lower() == "no" and self.bandAsk:
                    self.band = False
                    await message.channel.send(
                        f"Ok, {message.author.mention}, you have been marked as not being able to play an instrument. You are now free to explore {message.author.guild.name}!")
                    self.done = True
                    self.bandAsk = False
                if self.done:
                    if self.WCI:
                        for roles in list(message.author.guild.roles):
                            if str(roles) == "WCI eh":
                                await message.author.add_roles(roles)
                    if self.band:
                        for roles in list(message.author.guild.roles):
                            if str(roles).lower() == "musician eh":
                                await message.author.add_roles(roles)
                    for roles in list(message.author.guild.roles):
                        if str(roles).lower() == "unverified":
                            await message.author.remove_roles(roles)
                        elif str(roles).lower() == "noob eh":
                            await message.author.add_roles(roles)
                    for roles in list(message.author.roles):
                        if str(roles).lower() == "unverified":
                            await message.author.remove_roles(roles)
                        if str(roles) == "Member" or str(roles) == "noob eh":
                            await message.author.add_roles(roles)


@is_me("nonocheck")
async def nonocheck(message, nonoWords):
    if str(message.author) != "Hurb#4980":
        for i in nonoWords:
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
    with open("../Bots/servers.json",
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
        if message.guild is not None and message.guild.id == 770776810837245962:
            if predicate(message, "nonocheck"):
                await nonocheck(message, nonoWords)
            if predicate(message, "linkcheck"):
                await linkcheck(message)
            if predicate(message, "invitecheck"):
                await invitecheck(message)
            await modMuteCheck(message)


def setup(bot):
    bot.add_cog(MessageCommands(bot))
