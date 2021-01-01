import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
import os
import aiohttp
import asyncio
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
    with open('../Bots/servers.json', 'r') as f:
        storage = json.load(f)
        Prefix = storage[str(message.guild.id)]["prefix"]
        if message.guild is None:
            return "%"
        else:
            return commands.when_mentioned_or(Prefix)(_bot, message)


bot = commands.Bot(command_prefix=getprefix, help_command=None, intents=intents)


async def settings():
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f' https://hurbapi.herokuapp.com/') as r:
            res = await r.json()
    return res


bot.remove_command("help")
print("Loading..")
bot.statuses = [discord.Game("Blackjack (and winning) | %blackjack"), discord.Game("%help or @Hurb help"), discord.Game("bad jokes | %joke"), discord.Game("chatty AF | %chatbot"), discord.Game("hangman (he died) | %hangman"), discord.Game("get BANNED"), discord.Game("OMG LOOK AT THESE DOGGOS!!! | %doggo")]
bot.status = cycle(bot.statuses)


@bot.event
async def on_ready():
    print("Ready.")
    try:
        change_status.start()
    except:
        pass


@bot.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, new_prefix=None):
    with open('../Bots/servers.json', 'r') as f:
        storage = json.load(f)

    if new_prefix is None:
        await ctx.send(
            embed=discord.Embed(description=f"The prefix for this server is `{storage[str(ctx.guild.id)]['prefix']}`"))
    else:
        storage[str(ctx.guild.id)]['prefix'] = new_prefix
        with open('../Bots/servers.json', 'w') as f:
            json.dump(storage, f, indent=4)

        await ctx.send(f"{ctx.guild.name}'s prefix has been changed to `{new_prefix}`")


"""@bot.event
async def on_error(event, *args, **kwargs):
    pass"""


@tasks.loop(minutes=1)
async def change_status():
    await bot.change_presence(activity=next(bot.status), status=discord.Status.online)


@bot.command()
async def ping(ctx):
    Ping = bot.latency
    await ctx.send(f"YOU HAVE BEEN PINGED {ctx.author.mention}. PING IS {Ping}.")


@bot.event
async def on_member_join(member):
    if str(member.guild.id) == "751667811931390012":
        channel = bot.get_channel(id=788173997979205672)
        if await channel.webhooks() is None or not await channel.webhooks():
            await channel.create_webhook(name="Welcomer")
        for webhook in await channel.webhooks():
            if webhook.name != "Welcomer":
                await webhook.edit(name="Welcomer")
        for webhook in await channel.webhooks():
            if webhook.name == "Welcomer":
                message = await webhook.send(avatar_url="https://image.flaticon.com/icons/png/512/1026/1026658.png", content=f"Hello {member.mention}! Welcome to Art Gatherings! Make sure to check out {bot.get_channel(id=751671495335608413).mention} to get some roles, and if you want, write a short intro about yourself in {bot.get_channel(id=768124436149698580).mention} to help us get to know you. But before you do all that, be sure to ping __**one**__ mod to let them know to verify you. Enjoy the server!")
                await asyncio.sleep(60)
                try:
                    await message.delete()
                except:
                    pass
                break


@bot.command()
async def fixfile(ctx):
    with open("servers.json") as f:
        storage = json.load(f)

    for server, values in storage.items():
        if server.isnumeric():
            storage[server]["commands"]["antispam"] = "False"
    with open("servers.json", "w") as f:
        json.dump(storage, f, indent=4)
    await ctx.send(f"Done fixing the file :)")


extensions = ["MemberCog", "BotFunCog", "BlackJackBotCog", "ErrorCog", "JokeCog", "MathCog", "ServerCog", "HangmanCog", "SlotsAndRouletteCog", "HelpCog",
              "NQNCog", "BuyRoleCog", "players", "ChatBotCog", "RankCog", "votecog", "reactionroles", "onmessagecommands", "pong", "voice"]

for extension in extensions:
    bot.load_extension(f"Cogs.{extension}")

bot.run(TOKEN, bot=True, reconnect=True)
