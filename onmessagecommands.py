import asyncio
import time
author = ""


async def authorize(message):
    agreeing = False
    for roles in list(message.author.roles):
        if str(roles).lower() == "unverified":
            agreeing = True
    if agreeing:
        if message.content.lower() == "agree" or message.content.lower() == "i agree":
            await message.channel.send(f"Welcome to the {message.author.guild}, {message.author.mention}!")
            for roles in list(message.author.roles):
                if str(roles).lower() == "unverified":
                    await message.author.remove_roles(roles)
                if str(roles) == "Member" or str(roles) == "noob eh":
                    await message.author.add_roles(roles)


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


async def numCheck(message, author):
    if str(message.channel) == "countehng":
        if str(message.author) == author:
            await message.author.send(f"Don't send messages consecutively, you have friends, {message.author}.")
            await message.channel.purge(limit=1)
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "e", "h", " "]
        for char in str(message.content).lower():
            if char not in numbers:
                await message.channel.purge(limit=1)
                break
        newAuthor = str(message.author)
        return newAuthor


async def nightCheck(message):
    t = time.localtime()
    the_hour = time.strftime("%H", t)
    if str(message.channel) == "late-night-eh":
        if not int(the_hour) >= 21:
            await asyncio.sleep(delay=1)
            await message.channel.purge(limit=0)
            await asyncio.sleep(delay=1)
            await message.author.send(f"Don't send messages in the late night channel until after 9:00 PM, {message.author}.")
        elif not int(the_hour) <= 5:
            await asyncio.sleep(delay=1)
            await message.channel.purge(limit=0)
            await asyncio.sleep(delay=1)
            await message.author.send(
                f"Don't send messages in the late night channel until after 9:00 PM, {message.author}.")



