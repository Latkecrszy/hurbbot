import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
import os
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.members = True

TOKEN = os.environ.get('TOKEN', None)

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
bot.statuses = [discord.Game("Blackjack (and winning) | %blackjack"), discord.Game("%help or @Hurb help"), discord.Game("bad jokes | %joke"), discord.Game("chatty AF | %chatbot"), discord.Game("hangman (he died) | %hangman"), discord.Game("get BANNED"), discord.Game("OMG LOOK AT THESE DOGGOS!!! | %doggo")]
bot.status = cycle(bot.statuses)

bot.set_status = ["discord.Status.online", "discord.Status.idle", "discord.Status.offline",
                  "discord.Status.do_not_disturb"]
bot.status_now = bot.set_status[0]


@bot.event
async def on_ready():
    print("Ready.")
    await change_status.start()

@bot.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, new_prefix=None):
    with open('/Users/sethraphael/PycharmProject/Hurb/bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    prefixes[str(ctx.guild.id)] = str(new_prefix)

    if new_prefix is None:
        await ctx.send(
            embed=discord.Embed(description=f"The prefix for this server is `{prefix}`"))
    else:
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"{ctx.guild.name}'s prefix changed to `{new_prefix}`")


@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(activity=next(bot.status), status=bot.status_now)


def predicate(message, command):
    with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
        commandsList = json.load(f)
        activeList = commandsList[str(message.guild.id)]
        return activeList[command] == "True"


@bot.command()
async def ping(ctx):
    Ping = bot.latency
    await ctx.send(f"YOU HAVE BEEN PINGED {ctx.author.mention}. PING IS {Ping}.")


@bot.event
async def on_error(event, *args):
    pass


@bot.event
async def on_member_join(member):
    if str(member.guild.id) == "751667811931390012":
        channel = bot.get_channel(id=751668603165605928)
        if await channel.webhooks() is None or not await channel.webhooks():
            await channel.create_webhook(name="Welcomer")
        for webhook in await channel.webhooks():
            if webhook.name != "Welcomer":
                await webhook.edit(name="Welcomer")
        for webhook in await channel.webhooks():
            if webhook.name == "Welcomer":
                await webhook.send(avatar_url="https://image.flaticon.com/icons/png/512/1026/1026658.png", content=f"Hello {member.mention}! Welcome to Art Gatherings! Make sure to check out {bot.get_channel(id=751671495335608413).mention} to get some roles, and if you want, write a short intro about yourself in {bot.get_channel(id=768124436149698580).mention} to help us get to know you. Enjoy the server!")
                break


@bot.command()
async def gimmeinvite(ctx, *, guild):
    guild = discord.utils.get(bot.guilds, name=guild)
    if str(ctx.author.id) == "670493561921208320":
        for channel in guild.text_channels:
            invite = await channel.create_invite()
            await ctx.send(invite)
            break
    await ctx.send(embed=discord.Embed())
    

a_dict = {"a": ":regional_indicator_a:", "b": ":regional_indicator_b:","c": ":regional_indicator_c:","d": ":regional_indicator_d:",
          "e": ":regional_indicator_e:", "f": ":regional_indicator_f:","g": ":regional_indicator_g:","h": ":regional_indicator_h:",
          "i": ":regional_indicator_i:", "j": ":regional_indicator_j:","k": ":regional_indicator_k:","l": ":regional_indicator_l:",
          "m": ":regional_indicator_m:", "n": ":regional_indicator_n:","o": ":regional_indicator_o:","p": ":regional_indicator_p:",
          "q": ":regional_indicator_q:", "r": ":regional_indicator_r:","s": ":regional_indicator_s:","t": ":regional_indicator_t:",
          "u": ":regional_indicator_u:", "v": ":regional_indicator_v:","w": ":regional_indicator_w:","x": ":regional_indicator_x:",
          "y": ":regional_indicator_y:", "z": ":regional_indicator_z:"}


@bot.command()
async def sayBig(ctx, *, message):
    newMessage = ""
    for i in message:
        if i in a_dict.keys():
            newMessage += a_dict[i.lower()]
        else:
            newMessage += 1
    await ctx.send(newMessage)


@bot.command()
async def fixfile(ctx, *, file):
    with open(f"{file}.json") as f:
        files = json.load(f)

    with open("servers.json") as f:
        servers = json.load(f)
    for key, value in files.items():
        try:
            servers[key][file] = value
        except:
            servers[key] = {"commands": {"goodbye": "False", "nitro": "True", "nonocheck": "False", "welcome": "False",
                                       "invitecheck": "False", "linkcheck": "False", "ranking": "True"}, "prefix": "%", "rank": value}
    with open("servers.json", "w") as f:
        json.dump(servers, f, indent=4)
    await ctx.send("All done fixing the file :)")


extensions = ["MemberCog", "BotFunCog", "BlackJackBotCog", "JokeCog", "MathCog", "ErrorCog", "ServerCog", "HangmanCog", "SlotsAndRouletteCog", "HelpCog",
              "NQNCog", "BuyRoleCog", "players", "ChatBotCog", "RankCog", "votecog", "reactionroles", "onmessagecommands", "pong"]

for extension in extensions:
    bot.load_extension(f"Cogs.{extension}")

bot.run(TOKEN, bot=True, reconnect=True)
