from discord.ext import commands
import webbrowser
import cyphertext
import random as rand
import blackjackbot

bot = commands.Bot(command_prefix=".")
# botcommands = [".hello", ".users", ".encrypt <message here>", ".authorize <password here>", ".bothelp",
# ".8ball <question here>", ".lawrence", ".blackjack <bet here>", ".trivia", ".triviabattle", ".join", ".startgame"]
bot.validusers = [line.rstrip('\n') for line in open("/Users/sethraphael/validusers.txt")]
print(bot.validusers)


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command(aliases=["Ha", "HA", "haha", "HAHA", "Haha", "hah", "hahah", "hahaha", "hahahah", "hahahaha", "hahahahah",
                      "hahahahaha", "hahahahahaha", "hahahahahahah", "hahahahahahaha", "hahahahahahahaha"])
async def ha(ctx):
    await ctx.send("Screw you eric.")
    await ctx.author.send("Screw you stop it.")
    del bot.validusers[-1]


@bot.command(aliases=["lawrence", "Lawrence"])
async def ping(ctx):
    if str(ctx.author) in bot.validusers:
        await ctx.send(f'''Ping pong''')
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command()
async def hello(ctx):
    if str(ctx.author) in bot.validusers:
        await ctx.send(f'''Hello, {ctx.author}!''')
        await ctx.author.send('👋')
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command()
async def bothelp(ctx):
    if str(ctx.author) in bot.validusers:
        await ctx.send(f'''Hi, {ctx.author}! The commands for this bot are: ''')
        # for x in range(0, len(botcommands)):
        # await ctx.channel.send(botcommands[x])
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')
    else:
        await ctx.send("Error 404: Command not found.")


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
    if str(ctx.author) in bot.validusers:
        id = bot.get_guild(717924708741414955)
        await ctx.send(f'''There are {id.member_count} users in this server.''')
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    if str(ctx.author) in bot.validusers:

        responses = ["It is certain.", "Without a doubt.", "It is decidedly so.", "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                     "Very doubtful."]

        await ctx.send(f'''Question: {question}\nAnswer: {rand.choice(responses)}''')
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command()
async def encrypt(ctx, *, words):
    if str(ctx.author) in bot.validusers:
        encryption = cyphertext.cipherText(words)
        await ctx.channel.send(f'''Your encrypted message: {encryption}.''')
        await ctx.channel.send("Would you like to decrypt your message? &Y/&N")

        @bot.command()
        async def Y(ctx):
            decryption = cyphertext.normalText(encryption)
            await ctx.channel.send(f'''Your decrypted message: {decryption}.''')

        @bot.command()
        async def N(ctx):
            await ctx.channel.send("Ok. Your message will remain a mystery!")
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command(aliases=["bj", "BJ", "Bj", "Blackjack", "BLACKJACK", "BlackJack"])
async def blackjack(ctx):
    if str(ctx.author) in bot.validusers:
        await ctx.send("Welcome to the Raphael Casino! Get ready to play some blackjack!!!\n")
        await blackjackbot.game(ctx)
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not an authorized user of this bot, {ctx.author}.''')


@bot.command()
async def addbot(ctx):
    if str(ctx.author) in bot.validusers:
        if str(ctx.author) == "Latkecrszy#0947":
            webbrowser.open(
                "https://discordapp.com/oauth2/authorize?client_id=716376818072027167&scope=bot&permissions=0")
            await ctx.send(f'''Ok, Latkecrszy, I've opened a page in your browser for you to add this bot!''')
        else:
            await ctx.send(f'''Ok, {ctx.author}, I've sent you a link to add this bot to another server!''')
            await ctx.author.send(f'''Here is the link to add this bot, {ctx.author}!''')
            await ctx.author.send(
                f'''https://discordapp.com/oauth2/authorize?client_id=716376818072027167&scope=bot&permissions=0''')
            await ctx.author.webbrowser.open(
                f'''https://discordapp.com/oauth2/authorize?client_id=716376818072027167&scope=bot&permissions=0''')
    elif str(ctx.author) not in bot.validusers:
        ctx.send(f'''You are not authorized with this bot, {ctx.author}!''')


@bot.command()
async def roll(ctx, *, diesize):
    number = rand.randint(1, diesize + 1)
    ctx.send(f'''You rolled the die, and it landed on... {number}!''')


@bot.command()
async def trivia(ctx):
    await triviatime(ctx)


bot.run("NzE2Mzc2ODE4MDcyMDI3MTY3.XvWE1g.iYBGg2qEmkUoGHtk6hCxsFolzjk")
