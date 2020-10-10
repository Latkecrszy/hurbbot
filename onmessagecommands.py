import asyncio
import time

author = ""
import discord
from discord.ext import commands
import json

agreeing = False
WCI = False
WCIAsk = False
bandAsk = False
band = False
done = False


def is_me(command):
    def predicate(ctx):
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
            if commandsList[command] == "True":
                return True
            else:
                return False

    return commands.check(predicate)


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
async def nonocheck(message, swears, nonoWords):
    if str(message.author) != "Hurb#4980":
        for i in nonoWords:
            if message.content.lower().find(str(i)) != -1:
                await message.channel.send("Don't fuckin swear bro")
                swears.append(str(message.author))
                msgAuthor = str(message.author)
                swearCount = 0
                for p in swears:
                    if msgAuthor == p:
                        swearCount += 1
                if swearCount == 5:
                    await message.channel.send(
                        f"You have sworn 5 times, {message.author.mention}. If you continue, there will be punishment.")
                elif swearCount == 10:
                    await message.channel.send(
                        f"You have sworn 10 times, {message.author.mention}. If you swear 20 times, you will be muted for 10 minutes.")
                elif swearCount == 20:
                    await message.channel.send(
                        f"You have sworn 20 times, {message.author.mention}. You have been muted for 10 minutes.")
                    await mutedrole(message, 600)
                elif swearCount == 25:
                    await message.channel.send(
                        f"{message.author.mention}, bro, you gotta stop swearing already. That's 25 swears! If it reaches 30, I'm muting you for half an hour.")
                elif swearCount == 30:
                    await message.channel.send(
                        f"You have sworn 30 times, {message.author.mention}. You have been muted for 30 minutes.")
                    await mutedrole(message, 1800)
                elif swearCount == 40:
                    await message.channel.send(
                        f"{message.author.mention}, bro, what's it going to take to get through to you? STOP SWEARING!!! If you swear 50 times, I'm gonna mute you for an hour.")
                elif swearCount == 50:
                    await message.channel.send(
                        f"You fucking, fucking idiot. Why do you insist upon swearing so much??? I'm muting you for an hour to teach you a lesson.")
                    await mutedrole(message, 3600)
                break


async def checkSpam(message, author, content):
    if len(author) >= 5 and len(content) >= 5 and str(message.channel) != "spam":
        mesg1 = author[-1]
        mesg2 = author[-2]
        mesg3 = author[-3]
        mesg4 = author[-4]
        mesg5 = author[-5]
        cont1 = content[-1]
        cont2 = content[-2]
        cont3 = content[-3]
        cont4 = content[-4]
        cont5 = content[-5]
        if mesg1 == mesg2 == mesg3 == mesg4 == mesg5:
            if cont1 == cont2 == cont3 == cont4 == cont5:
                await message.channel.purge(limit=5)
                for x in range(len(content)):
                    del content[x]
                    del author[x]


async def chairCheck(message):
    if message.content.lower().find("!admin me") != -1:
        await message.author.kick(reason="You have asked for admin. You have been kicked for your insolence.")
        await message.channel.send(f"{message.author} has been kicked for asking for admin.")


async def mutedrole(message, sleep):
    for role in list(message.guild.roles):
        if str(role).lower() == "muted":
            await message.author.add_roles(role, reason="Don't swear you fucking idiot.")
    await asyncio.sleep(int(sleep))
    await message.channel.send(f"You have been unmuted, {message.author.mention}. Now stop fucking swearing already.")
    for role in list(message.guild.roles):
        if str(role).lower() == "muted":
            await message.author.remove_roles(role=role)


@is_me("nightcheck")
async def nightCheck(message):
    t = time.localtime()
    the_hour = time.strftime("%H", t)
    hour = 0
    for x in range(0, int(the_hour)):
        hour += 1
    if str(message.channel) == "late-night-eh":
        if not hour <= 21:
            await asyncio.sleep(delay=1)
            await message.channel.purge(limit=1)
            await asyncio.sleep(delay=1)
            await message.author.send(
                f"Don't send messages in the late night channel until after 9:00 PM, {message.author}.")
        elif not hour >= 5:
            await asyncio.sleep(delay=1)
            await message.channel.purge(limit=1)
            await asyncio.sleep(delay=1)
            await message.author.send(
                f"Don't send messages in the late night channel until after 9:00 PM, {message.author}.")


async def countCheck(message, prevNum):
    content = str(message.content)
    isNum = True
    for char in content:
        if not isinstance(char, int):
            isNum = False
    if not isNum:
        if str(message.channel).lower() == "counting":
            await message.delete()
            await message.author.send("Bro only send numbers in counting")
    else:
        if str(message.channel).lower() == "counting":
            if int(content) != int(prevNum) + 1:
                await message.delete()
                await message.author.send("Bro don't send the wrong numbers")
            else:
                return prevNum + 1


async def checkNQN(message):
    if message.content.startswith(":"):
        emoji = str(message.content)
        if await message.channel.webhooks() is None:
            avatar = await message.author.avatar_url.read()
            await message.channel.create_webhook(name=str(message.author.display_name))  # , avatar=avatar)
        for webhook in await message.channel.webhooks():
            avatar = await message.author.avatar_url.read()
            await webhook.edit(name=str(message.author.display_name))  # , avatar=avatar)
            for emojis in message.guild.emojis:
                emojiList = []
                for char in str(emojis):
                    emojiList.append(char)
                del emojiList[0]
                del emojiList[-1]
                if emojiList[0] == "a":
                    del emojiList[0]
                Emoji = "".join(emojiList)
                emojiList = []
                for char in Emoji:
                    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
                    if char not in numbers:
                        emojiList.append(char)
                Emoji = "".join(emojiList)
                if Emoji.lower() == str(emoji).lower():
                    await message.channel.purge(limit=1)
                    await webhook.send(emojis)
                print(str(Emoji))
            break


async def linkcheck(message):
    if message.content.find("https://") != -1 and not message.content.find("discord.gg/") or message.content.find("http://") != -1 and not message.content.find("discord.gg/"):
        await message.delete()
        embed = discord.Embed(description=f"Link sharing is disabled in {message.guild} {message.author.mention}!",
                              color=discord.Color.red())
        warning = await message.channel.send(embed=embed)
        await asyncio.sleep(5)
        await warning.delete()


async def invitecheck(message):
    if not message.content.find("https://discord.gg/"):
        await message.delete()
        warning = await message.channel.send(embed=discord.Embed(description=f"You are not allowed to post invites in {message.guild.name} {message.author.mention}!", color=discord.Color.red()))
        await asyncio.sleep(5)
        await warning.delete()


async def offlinecheck(message):
    if str(message.content).lower() == "@offline":
        members = []
        for member in message.guild.members:
            if member.status == discord.Status.offline:
                members.append(member.mention)
        for member in members:
            await message.channel.send(member)


async def modMuteCheck(message):
    with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/mutedMods.json", "r") as f:
        mutedMods = json.load(f)

    if str(message.author) in mutedMods.keys():
        if mutedMods[str(message.author)] == str(message.guild):
            await message.delete()

