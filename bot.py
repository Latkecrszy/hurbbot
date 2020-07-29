import discord
import time
import asyncio
from discord.ext import commands
import cyphertext

# Id = 715450088947712000
messages = joined = 0
client = discord.Client()
client2 = commands.Bot(command_prefix="&")
dic = {"Latkecrszy#0974": 2, "Bob#1234": 1}
invalidusers = []
theid = client.get_guild(717924708741414955)
channels = ["general", "commands"]
botcommands = ["&hello", "&users", "&purge", "&authorize", "&help", "&encrypt"]
valid_users = ["Latkecrsz#0947", "just.a.cat.#0457"]
cipherlist = []


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed:
        try:
            with open("stats.txt", "a") as f:
                f.write(f'''Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n''')

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)



@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("seth") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="NO DON'T USE THAT NAME")


@client.event
async def on_member_join(member, message):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await message.channel.send(f'''Welcome to the server, {member.mention} !''')


# Test server id == 715450088947712000
# java peeps id == 717924708741414955


@client.event
async def on_message(message):
    global messages
    messages += 1

    if message.content == botcommands[3]:
        if str(message.author) in valid_users:
            await message.channel.send(f'''You are already an authorized user of this bot, {str(message.author)}.''')
        else:
            await message.channel.send(
                f'''Ok, {str(message.author)}, I've approved you as an autorized user of this bot!''')
            valid_users.append(str(message.author))
    if str(message.channel) in channels and str(message.author) in valid_users and str(
            message.author) != "Discord Bot#2454":
        if message.content.find(botcommands[0]) != -1:
            await message.channel.send(f'''Hi, {message.author}!''')
        elif message.content == botcommands[1]:
            await message.channel.send(f'''There are {theid.member_count} users in the server.''')
        elif message.content == botcommands[4]:
            await message.channel.send(
                f'''The commands for this bot are &hello, &users, &authorize, and &help, {message.author}.''')
        elif message.content.startswith("&encrypt"):
            for char in str(message.content):
                cipherlist.append(char)
            for x in range(0, 5):
                del cipherlist[x]
            await message.channel.send(cyphertext.cipherText(cipherlist))
            await message.channel.send("Would you like to decrypt your message? !Y/!N")
            if message.content == "!Y":
                await message.channel.send(cyphertext.normalText(*cipherlist))
            elif message.content == "!N":
                await message.channel.send("Ok. Your message will remain a mystery!")
        elif str(message.channel) in channels and str(message.author) not in valid_users and str(
                message.content) in botcommands:
            invaliduser = f'''Users: {message.author} tried to use command {message.content} in channel {message.channel}.'''
            await message.channel.send(invaliduser)
            invalidusers.append(invaliduser)
    elif str(message.channel) in channels and str(message.author) not in valid_users and str(
            message.content) in botcommands and str(message.author) != "Discord Bot#2454":
        invaliduser = f'''Users: {message.author} tried to use command {message.content} in channel {message.channel}.'''
        await message.channel.send(invaliduser)
        invalidusers.append(invaliduser)


client.loop.create_task(update_stats())
client.run("NzE2Mzc2ODE4MDcyMDI3MTY3.XvJrIQ.hs_VjmYiEb2VumpaKCUzLnM2AdM")
