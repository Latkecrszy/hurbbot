import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
import time
import onmessagecommands
import asyncio
import random
from discord.ext.commands import CommandNotFound, BadArgument, CommandOnCooldown

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


def getprefix(_bot, message):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)

        return prefixes[str(message.guild.id)]


def is_it_me(ctx):
    return ctx.author.id == 670493561921208320

# bot = commands.Bot(command_prefix=commands.when_mentioned_or('!', '.', '*')

bot = commands.Bot(command_prefix=getprefix)

bot.remove_command("help")
swears = []
print("Loading..")
bot.statuses = ["big brane", "$help", "catch with children", "trivia", "8ball", "python", "DIE POKEMON"]
bot.status = cycle(bot.statuses)
author = []
content = []
nonoWords = ["shit", "fuck", "bitch", "dick", "fuk", "dik", "sht", "btch"]
bot.set_status = ["discord.Status.online", "discord.Status.idle", "discord.Status.offline",
                  "discord.Status.do_not_disturb"]
bot.dictionary = open("/Users/sethraphael/dictionary.txt")
bot.status_now = bot.set_status[0]
bot.token = "NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.B5eSdENH1GLRT7CkMLACTw7KpGE"
# bot.remove_command("help")
bot.playingBoggle = False
bot.boggleWords = []
bot.second = 180
bot.dictionary = bot.dictionary.readlines()
bot.letters = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X",
               "C",
               "V", "B", "N", "M"]
bot.boggleLetters = []


@bot.event
async def on_ready():
    change_status.start()
    print("Ready.")


async def on_error(err, *args):
    if err != "on_command_error":
        await args[0].send("Something went wrong.")
    elif isinstance(err, PermissionError):
        await args[0].send("Sorry, I don't have adequate permissions to accomplish that task.")
    raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        print("Error: Command not found.")
        # await ctx.send(f"I could not find that command, {ctx.author}")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''Error: Missing one or more required argument.''')
    elif isinstance(error, PermissionError):
        await ctx.send("Sorry, I don't have adequate permissions to accomplish that task.")
    elif isinstance(error, BadArgument):
        await ctx.send("Please enter a proper argument for this command.")
    elif isinstance(error, commands.errors.CheckFailure):
        embed = discord.Embed(
            title=f"<:x_:742198871085678642> This command is currently disabled, {ctx.author.display_name}!",
            description=None, color=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, CommandOnCooldown):
        embed = discord.Embed(
            title=f"Whoa there buddy, a little too quick on the commands. You still need to wait {int(error.retry_after)} seconds!",
            color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        raise error


@PermissionError
async def permerr(ctx):
    await ctx.send("Sorry, I don't have adequate permissions to accomplish that task.")


@bot.event
async def on_member_join(member):
    for role in list(member.guild.roles):
        if str(role).lower() == "unverified":
            await member.add_roles(role)
    for channel in member.guild.text_channels:
        if str(channel).lower() == "welcome-and-goodbye" or str(channel).lower() == "welcome" or str(channel).lower() == "wehlcome-and-goodbye":
            if member.guild.id == 746825963286822992:
                await channel.send(
                    f"Welcome to {member.guild.name}, {member.mention}! Please go to the #eh-rules to read the rules of this server, and check out #mehmbers to see who people are!")
            else:
                await channel.send(f"Please welcome {member.mention} to {member.guild.name}!")
        if str(channel) == "verification" or str(channel) == "verehfehcation":
            await channel.send(
                f'''Welcome to {member.guild.name}, {member.mention}! Please read the rules below and type agree to agree to them.
                                           ```1. No spamming outside of #spam or spam pinging anyone or everyone in any channel.
            2. No implied pornography outside of NSFW channel. No porn in any channel, take that somewhere else. (You pervert.)
            3. Please keep everything in its respective channels. This won't be strictly enforced but it would be nice if you would try.
            4. Don’t test the boundaries of the rules, and respect the admin and mods' decisions. It is okay to question unfair punishments, but do so in a respectful manner.
            5. If you are nice enough and tend to help people and obey these rules, you may eventually receive a promotion! But only if you work hard for it.
            6. Be nice in general! Don’t spread hate speech and keep this a friendly environment.

            Punishments for breaking these rules will be decided accordingly. Most aren't too strict, just don’t be excessively rude and annoying and you’ll be fine.```

            Once you have read and agreed to these rules, please type agree in the chat below. This will give you access to the rest of the server.''')


@bot.event
async def on_member_remove(member):
    for channel in member.guild.text_channels:
        if str(channel) == "welcome-and-goodbye":
            await channel.send(
                f"Fffffffuuuuuuccccckkkkkk... another member gone. Can we get an f in the chat for {member.name}?")


@bot.command()
async def prefix(ctx, new_prefix):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = str(new_prefix)

    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"{ctx.guild.name}'s prefix changed to {new_prefix}")


@bot.event
async def on_guild_join(guild):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '$'

    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=next(bot.status), status=bot.status_now)


@bot.event
async def on_message(message):
    if message.guild.id != 267624335836053506:
        await onmessagecommands.authorize(message)
        await onmessagecommands.chairCheck(message)
        await onmessagecommands.checkSpam(message, author, content)
        await onmessagecommands.nonocheck(message, swears, nonoWords)
        await bot.process_commands(message)


async def mutedrole(message, sleep):
    for role in list(message.guild.roles):
        if str(role).lower() == "muted":
            await message.author.add_roles(role, reason="Don't swear you fucking idiot.")
    await asyncio.sleep(int(sleep))
    await message.channel.send(f"You have been unmuted, {message.author.mention}. Now stop fucking swearing already.")
    for role in list(message.guild.roles):
        if str(role).lower() == "muted":
            await message.author.remove_roles(role=role)


@bot.command()
async def disable(ctx, command):
    found = False
    with open('/Users/sethraphael/PycharmProject/Bots/commands.json', 'r') as f:
        commandsList = json.load(f)
    for Command, condition in commandsList.items():
        if Command == command and condition == "True":
            commandsList[Command] = 'False'
            embed = discord.Embed(title=f"<:check:742198670912651316> Command {command} has been disabled!",
                                  description=None, color=discord.Color.green())
            await ctx.send(embed=embed)
            found = True

    with open('/Users/sethraphael/PycharmProject/Bots/commands.json', 'w') as f:
        json.dump(commandsList, f, indent=4)
    if not found:
        embed = discord.Embed(title=f"<:x_:742198871085678642> Command {command} is already disabled!",
                              description=None, color=discord.Color.red())
        await ctx.send(embed=embed)


@bot.command()
async def enable(ctx, command):
    found = False
    with open('/Users/sethraphael/PycharmProject/Bots/commands.json', 'r') as f:
        commandsList = json.load(f)
    for Command, condition in commandsList.items():
        if Command == command and condition == "False":
            commandsList[Command] = 'True'
            embed = discord.Embed(title=f"<:check:742198670912651316> Command {command} has been enabled!",
                                  description=None, color=discord.Color.green())
            await ctx.send(embed=embed)
            found = True

    with open('/Users/sethraphael/PycharmProject/Bots/commands.json', 'w') as f:
        json.dump(commandsList, f, indent=4)
    if not found:
        embed = discord.Embed(title=f"<:x_:742198871085678642> Command {command} is already enabled!",
                              description=None, color=discord.Color.red())
        await ctx.send(embed=embed)


@commands.cooldown(1, 5, BucketType.user)
@bot.command(aliases=["meme quote", "Quote", "QUOTE", "Meme quote"])
async def quote(ctx):
    with open(
            "/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/memeorable_quotes.json",
            "r") as f:
        quotes = json.load(f)
    quoteNum = len(quotes)  # 10
    newQuoteNum = random.randint(0, quoteNum + 1)  # 3
    newerQuoteNum = 0
    for key, value in quotes.items():
        if newQuoteNum == newerQuoteNum:
            embed = discord.Embed(color=random.choice(embedColors))
            embed.add_field(name=key, value=f"Author: {value}")
            await ctx.send(embed=embed)
            break
        newerQuoteNum += 1


@bot.command()
async def startstar(ctx):
    num = 1
    while True:
        stars = "*" * num
        await ctx.send(f"`{stars}fin`")
        await asyncio.sleep(5)
        num += 1

def catGlee():
    return("""      _      _
     / \    / \\
    |   \__/   |
   /  _o nn o_  \\
  /  /  \  /  \  \\
 /       __       \\
 \    . .\/. .    /
   \   \./\./   / |
     \  v  v  /    \\
       \____/       \\
          |          \\""")

def catNeutral():
    return("""      _      _
     / \    / \\
    |   \__/   |
   /  _o nn o_  \\
  /  /  \  /  \  \\
 /   \_O/  \O_/   \\
 \    . .\/. .    /
   \  __./\.__  / |
     \  v  v  /    \\
       \____/       \\
          |          \\""")

def catAnger():
    return("""      _      _
     / \    / \\
    |   \__/   |
   /  _  nn  _  \\
  /  | \o  o/ |  \\
 /   |_O\  /O_|   \\
 \    . .\/. .    /
   \   _./\._   / |
     \/ v  v \/    \\
       \____/       \\
          |          \\""")


@bot.command()
async def cathappy(ctx):
    await ctx.send(f"```{catGlee()}```")


@bot.command()
async def catneutral(ctx):
    await ctx.send(f"```{catNeutral()}```")


@bot.command()
async def catanger(ctx):
    await ctx.send(f"```{catAnger()}```")

@bot.command()
async def help(ctx):
    serverEmbed = discord.Embed(title="Help command for server management features of Hurb Bot:", color=random.choice(embedColors))
    funEmbed = discord.Embed(title="Help command for fun features of Hurb Bot:", color=random.choice(embedColors))
    funEmbed.add_field(name="Help", value="Displays this thing, why are you even reading this?")
    # embed.add_field(name="|\n", value="|")
    serverEmbed.add_field(name="Enable <command>", value="Enables a disabled command")
    # embed.add_field(name="|\n", value="|")
    serverEmbed.add_field(name="Disable <command>", value="Disables an enabled command")
    # embed.add_field(name="|\n", value="|")
    serverEmbed.add_field(name="Prefix <new prefix>", value="Changes your server prefix to whatever you want")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="BlackJack <bet>", value="Starts a blackjack game with a bet of your choice")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="beg", value="You beg for money")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="search <place>", value="You search for money")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="searchplaces", value="Shows you where you can search")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="hit", value="Makes you hit in a blackjack game")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="stand", value="Makes you stand in a blackjack game")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="joke", value="Tells you a joke")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="multiply <number> <number2>", value="Multiplies two numbers for you")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="add <number> <number2>", value="Adds two numbers for you")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="subtract <number> <number2>", value="Subtracts two numbers for you")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="divide <number> <number2>", value="Divides two numbers for you")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="power <number> <number2>", value="Finds the power of two numbers for you")
    # embed.add_field(name="|\n", value="|")
    serverEmbed.add_field(name="mute <member> <optional: time> <optional: reason>", value="Mutes a member, if you have a mute role on your server. You must have admin privileges to do this.")
    serverEmbed.add_field(name="unmute <member>", value="Unmutes a member. Pretty self-explanatory. You must have admin privileges to do this.")
    serverEmbed.add_field(name="warn <member> <reason>", value="Warns a member, and sends them a dm with the warning. You must have admin privileges to do this.")
    serverEmbed.add_field(name="rename <member> <new name>", value="Renames a member. You must have admin privileges to do this.")
    serverEmbed.add_field(name="rall <new name>", value="renames everyone in your server to whatever you want. Use wisely. You must have admin privileges to do this.")
    serverEmbed.add_field(name="kick <member> <optional: reason>", value="kicks a member from your server. They will be able to rejoin. You must have admin privileges to do this.")
    serverEmbed.add_field(name="ban <member> <optional: reason>", value="bans a member from your server. You can undo this in server settings. You must have admin privileges to do this.")

    funEmbed.add_field(name="Catanger", value="Shows an angry cat face")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="Catneutral", value="Shows a neutral cat face")
    # embed.add_field(name="|\n", value="|")
    funEmbed.add_field(name="Cathappy", value="Shows a happy cat face")
    await ctx.send(embed=serverEmbed)
    await ctx.send(embed=funEmbed)

bot.load_extension("MemberCog")
bot.load_extension("BotFunCog")
bot.load_extension("BlackJackBotCog")
bot.load_extension("TriviaBotCog")
bot.load_extension("JokeCog")
bot.load_extension("ShopCog")
bot.load_extension("MathCog")
bot.load_extension("scratch")

bot.run(bot.token, bot=True, reconnect=True)

# use for bot.event in class:   commands.Cog.listener()
