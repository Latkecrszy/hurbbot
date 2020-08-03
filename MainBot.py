from discord.ext import commands
import webbrowser
from cyphertext import cipherText
from cyphertext import normalText
import random as rand
import json


def getprefix(_bot, message):
    with open('/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/scratch_1.json', 'r') as f:
        prefixes = json.load(f)

        return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=getprefix)
# botcommands = [".hello", ".users", ".encrypt <message here>", ".authorize <password here>", ".bothelp",
# ".8ball <question here>", ".lawrence", ".blackjack <bet here>", ".trivia", ".triviabattle", ".join", ".startgame"]
validusers = [line.rstrip('\n') for line in open("/Users/sethraphael/validusers.txt")]
print(validusers)


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command(aliases=["lawrence", "Lawrence"])
async def ping(ctx):
    if str(ctx.author) in validusers:
        await ctx.send(f'''Ping pong''')
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command()
async def hello(ctx):
    if str(ctx.author) in validusers:
        await ctx.send(f'''Hello, {ctx.author}!''')
        await ctx.author.send('👋')
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command()
async def authorize(ctx, *, password):
    if password == "screweric" or password == "Screweric" or password == "SCREWERIC":
        if str(ctx.author) in bot.validusers:
            await ctx.send(f'''You are already an authorized user, {ctx.author}''')
        elif str(ctx.author) not in bot.validusers:
            await ctx.send(f'''Ok, {ctx.author}, you are now an authorized user of this bot!''')
            valid_users = open("/Users/sethraphael/validusers.txt", "a")
            valid_users.write("\n" + str(ctx.author))
            valid_users.close()
            bot.validusers = [line.rstrip('\n') for line in open("/Users/sethraphael/validusers.txt")]
    else:
        await ctx.send(f'''Incorrect password, {ctx.author}.''')


@bot.command()
async def users(ctx):
    if str(ctx.author) in validusers:
        id = bot.get_guild(717924708741414955)
        await ctx.send(f'''There are {id.member_count} users in this server.''')
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command(aliases=["8ball"])
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


@bot.command()
async def encrypt(ctx, *, words):
    if str(ctx.author) in validusers:
        encryption = cipherText(words)
        good_encryption = "".join(encryption)
        await ctx.channel.send(f'''Your encrypted message: {good_encryption}.''')
        await ctx.channel.send("Would you like to decrypt your message? &Y/&N")

        @bot.command()
        async def Y():
            decryption = normalText(encryption)
            good_decryption = "".join(decryption)
            await ctx.channel.send(f'''Your decrypted message: {good_decryption}.''')

        @bot.command()
        async def N():
            await ctx.channel.send("Ok. Your message will remain a mystery!")
    elif str(ctx.author) not in validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command()
async def addbot(ctx):
    if str(ctx.author) in validusers:
        if str(ctx.author) == "Latkecrszy#0947":
            webbrowser.open(
                "https://discordapp.com/oauth2/authorize?client_id=716376818072027167&scope=bot&permissions=8")
            await ctx.send(f'''Ok, Latkecrszy, I've opened a page in your browser for you to add this bot!''')
        else:
            await ctx.send(f'''Ok, {ctx.author}, I've sent you a link to add this bot to another server!''')
            await ctx.author.send(f'''Here is the link to add this bot, {ctx.author}!''')
            await ctx.author.send(
                f'''https://discordapp.com/oauth2/authorize?client_id=716376818072027167&scope=bot&permissions=8''')
            await ctx.author.webbrowser.open(
                f'''https://discordapp.com/oauth2/authorize?client_id=716376818072027167&scope=bot&permissions=8''')
    elif str(ctx.author) not in validusers:
        ctx.send(f'''You are not authorized with this bot, {ctx.author}!''')


@bot.command()
async def roll(ctx, *, diesize):
    number = rand.randint(1, diesize + 1)
    ctx.send(f'''You rolled the die, and it landed on... {number}!''')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''Error: Missing one or more required argument.''')
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        raise error.original


@bot.event
async def on_guild_join(guild):
    with open('/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/scratch_1.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '$'

    with open('/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/scratch_1.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/scratch_1.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('//Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/scratch_1.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
async def prefix(ctx, new_prefix):
    with open('/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/scratch_1.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = str(new_prefix)

    with open('/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/scratch_1.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"{ctx.guild.name}'s prefix changed to {new_prefix}")

bot.run("NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.B5eSdENH1GLRT7CkMLACTw7KpGE")
