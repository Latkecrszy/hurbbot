import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
import os
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from dotenv import load_dotenv
from Bots.Cogs.mongoclient import MotorClient as client


load_dotenv()
intents = discord.Intents.default()
intents.members = True

TOKEN, LINK = os.environ.get('TOKEN', None), os.environ.get("LINK", None)


embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


async def getprefix(_bot, message):
    if message.guild is not None:
        guild = await bot.cluster.find_one({"id": str(message.guild.id)})
        return commands.when_mentioned_or(guild['prefix'])(_bot, message)
    else:
        return commands.when_mentioned_or("%")(_bot, message)


bot = commands.Bot(command_prefix=getprefix, help_command=None, intents=intents, case_insensitive=True)

bot.remove_command("help")
bot.cluster = client()
print("Loading..")
bot.statuses = [discord.Game("Blackjack (and winning) | %blackjack"), discord.Game("%help or @Hurb help"),
                discord.Game("bad jokes | %joke"), discord.Game("screw rick rolls, I do react roles | %reactionrole"),
                discord.Game("hangman (he died) | %hangman"), discord.Game("get BANNED"),
                discord.Game("OMG LOOK AT THESE DOGGOS!!! | %doggo"),
                discord.Game("Check out the website | hurb.gg")]
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
    storage = await bot.cluster.find_one({"id": str(ctx.guild.id)})
    if new_prefix is None:
        await ctx.send(
            embed=discord.Embed(description=f"The prefix for this server is `{storage['prefix']}`"))
    else:
        storage['prefix'] = new_prefix
        await bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)

        await ctx.send(f"{ctx.guild.name}'s prefix has been changed to `{new_prefix}`")


@tasks.loop(minutes=1)
async def change_status():
    await bot.change_presence(activity=next(bot.status), status=discord.Status.online)


@bot.command()
async def ping(ctx):
    await ctx.send(f"YOU HAVE BEEN PINGED {ctx.author.mention}. PING IS {round(bot.latency, 3)}.")


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
                message = await webhook.send(avatar_url="https://image.flaticon.com/icons/png/512/1026/1026658.png",
                                             content=f"Hello {member.mention}! Welcome to Art Gatherings! Make sure to check out {bot.get_channel(id=751671495335608413).mention} to get some roles, and if you want, write a short intro about yourself in {bot.get_channel(id=768124436149698580).mention} to help us get to know you. But before you do all that, be sure to ping __**one**__ mod to let them know to verify you. Enjoy the server!")
                await asyncio.sleep(60)
                try:
                    await message.delete()
                except:
                    pass
                break


@tasks.loop(hours=12)
async def backup():
    collection = bot.cluster.client.settings
    backup_collection = bot.cluster.client.settings_backup
    await backup_collection.drop()
    await bot.cluster.client.create_collection("settings_backup")
    results = collection.find().to_list(length=50000)
    for document in await results:
        await backup_collection.insert_one({key: value for key, value in document.items() if key != "_id"})


@bot.command()
async def fixroles(ctx):
    collection = bot.cluster.client.reaction_roles
    results = collection.find().to_list(length=50000)
    for document in await results:
        if 'roles' not in document.keys():
            await collection.find_one_and_delete({"id": document['id']})
            print("found a bad one")
    await ctx.send("Done :)")



backup.start()

extensions = ["ServerCog", "fun", "blackjack", "ErrorCog", "JokeCog", "MemberCog", "HangmanCog", "SlotsAndRouletteCog",
              "HelpCog",
              "NQNCog", "BuyRoleCog", "players", "ChatBotCog", "RankCog", "votecog", "reactionroles",
              "onmessagecommands", "pong", "voice", "pets"]

for extension in extensions:
    bot.load_extension(f"Cogs.{extension}")

bot.run(TOKEN, bot=True, reconnect=True)
