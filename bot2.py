import discord
import asyncio
import random as rand
import cyphertext
import blackjackbot
from discord.ext import commands

# Create the variables
invalidusers = []
channels = ["general", "commands"]
botcommands = ["&hello", "&users", "&encrypt <message here>", "&authorize", "&bothelp", "&8ball <question here>", "&lawrence"]
validusers = [line.rstrip('\n') for line in open("/Users/sethraphael/validusers.txt")]
print(validusers)
cipherlist = []
client = commands.Bot(command_prefix='&')
id = client.get_guild(715450088947712000)


# Check if the bot is ready
@client.event
async def on_ready():
    print("Bot is ready.")


@client.event
async def on_member_join(ctx, member):
    await ctx.send(f'''{member} has joined the server!''')


@client.event
async def on_member_remove(ctx, member):
    await ctx.send(f'''{member} has left the server.''')


@client.command(aliases=["lawrence", "Lawrence"])
async def ping(ctx):
    if str(ctx.author) in validusers:
        await ctx.send(f'''Ping pong''')
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@client.command()
async def hello(ctx):
    if str(ctx.author) in validusers:
        await ctx.send(f'''Hello, {ctx.author}!''')
        await ctx.author.send('👋')
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@client.command()
async def bothelp(ctx):
    if str(ctx.author) in validusers:
        await ctx.send(f'''Hi, {ctx.author}! The commands for this bot are: ''')
        for x in range(0, len(botcommands)):
            await ctx.channel.send(botcommands[x])
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')
    else:
        await ctx.send("Error 404: Command not found.")


@client.command()
async def authorize(ctx, *, password):
    validusers = [line.rstrip('\n') for line in open("/Users/sethraphael/validusers.txt")]
    if str(ctx.author) in validusers:
        await ctx.send(f'''You are already an authorized user, {ctx.author}''')
    elif str(ctx.author) not in validusers:
        if password == "latke" or password == "Latke" or password == "LATKE":
            await ctx.send(f'''Ok, {ctx.author}, you are now an authorized user of this bot!''')
            valid_users = open("/Users/sethraphael/validusers.txt", "a")
            valid_users.write("\n" + str(ctx.author))
            valid_users.close()
            validusers = [line.rstrip('\n') for line in open("/Users/sethraphael/validusers.txt")]
        else:
            await ctx.send(f'''Wrong password, {ctx.author}.''')


@client.command()
async def users(ctx):
    if str(ctx.author) in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')
        id = client.get_guild(717924708741414955)
        await ctx.send(f'''There are {id.member_count} users in this server.''')
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    if str(ctx.author) in validusers:

        responses = ["It is certain.", "Without a doubt.", "It is decidedly so.", "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                     "Very doubtful."]

        await ctx.send(f'''Question: {question}\nAnswer: {rand.choice(responses)}''')
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@client.command()
async def encrypt(ctx, *, words):
    if str(ctx.author) in validusers:
        encryption = cyphertext.cipherText(words)
        await ctx.channel.send(f'''Your encrypted message: {encryption}.''')
        await ctx.channel.send("Would you like to decrypt your message? &Y/&N")

        @client.command()
        async def Y(ctx):
            decryption = cyphertext.normalText(encryption)
            await ctx.channel.send(f'''Your decrypted message: {decryption}.''')

        @client.command()
        async def N(ctx):
            await ctx.channel.send("Ok. Your message will remain a mystery!")
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


# @client.command(aliases=["bj", "BJ", "Bj", "Blackjack", "BLACKJACK", "BlackJack"])
# async def blackjack(ctx, *, bet):
#
#     value = 0
#     await ctx.send("Welcome to the Raphael Casino! Get ready to play some blackjack!!!\n")
#     await blackjackbot.game(ctx)


client.run("NzE1NDQ5MTA2NzY3ODA2NTU0.XvV7FA.q-zKVck-4_DPO1t6RV1rJGYRqyk")
