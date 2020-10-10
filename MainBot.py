import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
from Bots.MemberCog import Verification
import Bots.onmessagecommands as onmessagecommands
import Bots.NQNCog
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

messageCommands = onmessagecommands.Authorize()

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


def getprefix(_bot, message):
    with open('/Users/sethraphael/PycharmProject/Hurb/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        if message.guild is None:
            return "%"
        else:
            return commands.when_mentioned_or(prefixes[str(message.guild.id)])(_bot, message)


bot = commands.Bot(command_prefix=getprefix, help_command=None, intents=intents)


def is_me(command):
    def predicate(ctx):
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
            return commandsList[command] == "True"

    return commands.check(predicate)


bot.remove_command("help")
bot.author = ""
swears = []
print("Loading..")
bot.statuses = ["blackjack", "%help", "jokes", "trivia", "hangman", "BANNED"]
bot.status = cycle(bot.statuses)
nonoWords = ["shit", "fuck", "bitch", "dick", "fuk", "dik", "sht", "btch", " ass "]
bot.set_status = ["discord.Status.online", "discord.Status.idle", "discord.Status.offline",
                  "discord.Status.do_not_disturb"]
bot.status_now = bot.set_status[0]


@bot.event
async def on_ready():
    # change_status.start()
    print("Ready.")
    #for guild in bot.guilds:
        #if guild.id == 742382901743845497:
          #  me = guild.get_member(user_id=670493561921208320)
            #for role in guild.roles:
               # if str(role).lower() == "cutie":
                   # await me.add_roles(role)
    # await asyncio.sleep(.5)
    # await bot.change_presence(activity=":bongocat:", status=discord.Status.online)


@bot.command()
async def prefix(ctx, new_prefix=None):
    with open('/Users/sethraphael/PycharmProject/Hurb/bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    prefixes[str(ctx.guild.id)] = str(new_prefix)

    if new_prefix is None:
        await ctx.send(
            embed=discord.Embed(description=f"The prefix for this server, {ctx.author.mention}, is {prefix}!"))
    else:
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"{ctx.guild.name}'s prefix changed to `{new_prefix}`")


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=next(bot.status), status=bot.status_now)


def predicate(message, command):
    with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
        commandsList = json.load(f)
        activeList = commandsList[str(message.guild.id)]
        return activeList[command] == "True"


bot.prevNum = ""


@bot.event
async def on_message(message):
    if message.guild is not None:
        if predicate(message, "nonocheck"):
            await onmessagecommands.nonocheck(message, swears, nonoWords)
        if predicate(message, "authorize"):
            await messageCommands.authorize(message)
        if predicate(message, "numcheck"):
            bot.prevNum = await onmessagecommands.countCheck(message, bot.prevNum)
        NQN = Bots.NQNCog.NQNCog(bot)
        if predicate(message, "nitro"):
            await NQN.NQNCheck(message)
        if predicate(message, "linkcheck"):
            await onmessagecommands.linkcheck(message)
        if predicate(message, "invitecheck"):
            await onmessagecommands.invitecheck(message)
        await onmessagecommands.offlinecheck(message)
        verification = Verification()
        if not isinstance(message.author, discord.User):
            await verification.verifyCheck(message)
        await onmessagecommands.modMuteCheck(message)
    await bot.process_commands(message)


extensions = ["MemberCog", "BotFunCog", "BlackJackBotCog", "TriviaBotCog", "JokeCog", "MathCog",
              "unverifiedHelp", "zombieGame", "ErrorCog", "ServerCog", "HangmanCog", "SlotsAndRouletteCog", "HelpCog",
              "NQNCog", "BuyRoleCog", "AppCog"]

for extension in extensions:
    bot.load_extension(extension)

bot.run("NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.ra2OkTKgLoSf_SYRxUFtw4fX0pQ", bot=True, reconnect=True)
