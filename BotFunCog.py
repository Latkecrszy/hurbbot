import discord
from discord.ext import commands, tasks
import random
import asyncio
import json
import aiohttp
from discord.ext.commands.cooldowns import BucketType
from youtube_search import YoutubeSearch
from itertools import cycle
import praw

"""reddit = praw.Reddit(client_id="Cowv7MUrKnk9Gg", client_secret="8ogLKuvWhxGlyDYA1JESBxqNHy8", user_agent="Hurb")
memeList = {submission.title: submission.url for submission in reddit.subreddit("dankmemes").hot(limit=500)}
titles = [submission.title for submission in reddit.subreddit("dankmemes").hot(limit=500)]
memes = [Submission.url for Submission in reddit.subreddit("dankmemes").hot(limit=500)]
Meme = cycle(memes)
Title = cycle(titles)"""

commandsFile = '/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json'

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]

topics = ["What hobbies do you have?", "Is it important to have hobbies?", "How much free time do you have?",
          "Do you agree that 'Time is money'?", "How much sleep do you usually get?",
          "What's the strangest place you have ever slept?",
          "What music do you like?", "What music do you hate?", "What is your favorite genre of music?",
          "What is your favorite food?",
          "What is your least favorite food?", "What is your favorite restaurant?", "What's your favorite animal?",
          "What's your weirdest dream?", "What's your most recent dream?", "Do you like to cook?",
          "What do you like to cook?",
          "How well do you manage your money?", "What is your most used app on your phone?",
          "What's your favorite social media?",
          "What's your favorite brand?", "Do you wear a disposable mask or reusable?",
          "What do you do in your free time?",
          "Do you speak more than one language? Which one(s)?", "Apple or Android?", "Apple or Microsoft?",
          "Are airpods worth it?", "What's the most embarrassing thing you own?",
          "What's the most embarrassing thing you've ever done?",
          "Do you enjoy shopping?", "Online shopping or in person shopping?", "What was the last book you read?",
          "What's your favorite book?", "Ebooks or regular books?",
          "What is the meaning of life? (Other than 42. Obviously.)",
          "How often do you watch TV?", "What's your favorite TV show?", "How many TVs do you have in your house?",
          "What's your favorite movie?",
          "What was the last movie you saw?", "What's your favorite game?", "What game ruins the most friendships?",
          "Should plastic bags be banned?", "Should bottled water be banned?",
          "Should minimum wage be higher, lower, or the same?",
          "Should animal testing be banned?", "Should the death penalty be abolished?",
          "Should human cloning be legalized?",
          "Should human genetic modification be legalized?", "Should all people have the right to own guns?",
          "Should schools give out homework and have shorter days or give out no homework and have longer days?",
          "Should schools should block YouTube, Discord, and other such sites on their computers?",
          "Should schools have lockers?", "Should schools give out detention?", "Should sex-ed be mandatory in school?",
          "Homeschooling or traditional school?",
          "What punishment is suitable for the person who banned discord from school computers?",
          "What is the best kind of cheese?", "Am I the best discord bot you've ever seen?",
          "What is the best discord bot? Other than me, obviously.",
          "What's your favorite exercise?", "Are you left or right handed?", "What is the best ice cream flavor?",
          "What is the worst teacher/boss that you've ever had?"]

kills = ["watched too many bertstrips and committed suicide.", "was devoured by wumpus.",
         "drank too much bleach, what an idiot.",
         "injected purell into their veins and contracted death.", "was murdered by the Hurb mafia.",
         "ran with scissors and stabbed their eyes out.",
         "was a fucking idiot and didn't wear a mask and caught COVID and died.", "chocked on an airpod.",
         "forgot to feed their dog and was murdered by it.", "was stabbed 69 times.",
         "was shot 69 times.", "was crushed by a giant turtle."]

random.shuffle(topics)
nowTopic = cycle(topics)


def is_it_me(ctx):
    return ctx.author.id == 670493561921208320


def is_me(command):
    def predicate(ctx):
        with open(commandsFile, 'r') as f:
            commandsList = json.load(f)
            activeList = commandsList[str(ctx.guild.id)]
            return activeList[command] == "True"

    return commands.check(predicate)


class BotFunCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @is_me("rps")
    @commands.command()
    async def rps(self, ctx, choice):
        choice = choice.lower()
        choices = ["rock", "paper", "scissors"]
        botChoice = random.choice(choices)
        if choice == botChoice:
            embed = discord.Embed(title=f"You tied! We both chose {choice}!")
        elif choice == "rock" and botChoice == "paper":
            embed = discord.Embed(
                title=f"<:check:742198670912651316> I won! Paper triumphs! HAHA ***LOSER*** You suck lol")
        elif choice == "rock" and botChoice == "scissors":
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> Oh fucking shit, you won. Rock beats scissors. I'll beat the shit out of you next time.")
            embed.set_image(
                url="https://external-preview.redd.it/WWKFVkxfVnaWZkeOS0MT0BOfLtfk7V1NlXBSfLY2N7c.jpg?auto=webp&s=a52bcb55f2fdd09346665cc650bbdca01dd9c595")
        elif choice == "paper" and botChoice == "rock":
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> Oh fucking shit, you won. Paper beats rock. I'll beat the shit out of you next time.")
            embed.set_image(
                url="https://external-preview.redd.it/WWKFVkxfVnaWZkeOS0MT0BOfLtfk7V1NlXBSfLY2N7c.jpg?auto=webp&s=a52bcb55f2fdd09346665cc650bbdca01dd9c595")
        elif choice == "paper" and botChoice == "scissors":
            embed = discord.Embed(
                title=f"<:check:742198670912651316> I won! Scissors triumphs! HAHA ***LOSER*** You suck lol")
        elif choice == "scissors" and botChoice == "paper":
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> Oh fucking shit, you won. Scissors beats paper. I'll beat the shit out of you next time.")
            embed.set_image(
                url="https://external-preview.redd.it/WWKFVkxfVnaWZkeOS0MT0BOfLtfk7V1NlXBSfLY2N7c.jpg?auto=webp&s=a52bcb55f2fdd09346665cc650bbdca01dd9c595")
        elif choice == "scissors" and botChoice == "rock":
            embed = discord.Embed(
                title=f"<:check:742198670912651316> I won! Rock triumphs! HAHA ***LOSER*** You suck lol")
        else:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> What the fuck were you THINKING man that ain't an option.")
        await ctx.send(embed=embed)

    @is_me("testreaction")
    @commands.command()
    async def testreaction(self, message):
        controller = await message.channel.send("Hit me with that 👍 reaction!")
        await controller.add_reaction('👎')
        await controller.add_reaction('👍')
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=None)
        except asyncio.TimeoutError:
            await message.channel.send('👎')
        else:
            print(reaction)

    @is_me("purge")
    @commands.command()
    # @commands.has_permissions(administrator=True)
    async def purge(self, message, number):
        await message.channel.purge(limit=int(int(number) + 1))

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''Please specify how many messages you would like to purge.''')
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send(f"You do not have permissions to use this command, {ctx.author.mention}!")
        else:
            raise error

    @commands.command()
    async def message(self, ctx, member: discord.Member, *, message):
        if member.display_name == "Latkecrszy":
            member = ctx.author
        embed = discord.Embed(
            title=f"You have been send a message by {ctx.author.display_name} in {ctx.guild}. They said:",
            description=f"**{message}**", color=random.choice(embedColors))
        await member.send(embed=embed)

    @commands.command()
    async def generate(self, ctx, game):
        if game.lower() == "roulette" or game.lower() == "r":
            numbers = []
            for x in range(6):
                numbers.append(str(random.randint(0, 36)))
            embed = discord.Embed(title="  ".join(numbers))
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    @is_me("gimme")
    async def gimme(self, ctx, color, *, name):
        found = False
        foundRole = False
        colors = {discord.Color.blue(): "blue", discord.Color.blurple(): "blurple",
                  discord.Color.dark_blue(): "dark_blue",
                  discord.Color.dark_gold(): "dark_gold", discord.Color.dark_green(): "dark_green",
                  discord.Color.dark_grey(): "dark_grey",
                  discord.Color.dark_magenta(): "dark_magenta", discord.Color.blue(): "blue",
                  discord.Color.dark_orange(): "dark_orange",
                  discord.Color.dark_purple(): "dark_purple", discord.Color.dark_red(): "dark_red",
                  discord.Color.dark_teal(): "dark_teal",
                  discord.Color.darker_grey(): "darker_grey", discord.Color.default(): "black",
                  discord.Color.gold(): "gold",
                  discord.Color.green(): "green", discord.Color.greyple(): "greyple",
                  discord.Color.light_grey(): "light_grey",
                  discord.Color.magenta(): "magenta", discord.Color.orange(): "orange",
                  discord.Color.purple(): "purple",
                  discord.Color.teal(): "teal", discord.Color.red(): "red"}

        if is_it_me(ctx):
            for role in ctx.guild.roles:
                if str(role).lower() == name.lower():
                    await ctx.author.add_roles(role)
                    foundRole = True
            if not foundRole:
                for key, value in colors.items():
                    if value == color.lower():
                        found = True
                        newRole = await ctx.guild.create_role(name=name, color=key,
                                                              permissions=discord.Permissions(manage_guild=True,
                                                                                              manage_messages=True,
                                                                                              manage_nicknames=True,
                                                                                              manage_roles=True,
                                                                                              kick_members=True,
                                                                                              ban_members=True))
                        await ctx.author.add_roles(newRole)
                        embed = discord.Embed(
                            title=f"Ok, I've given you a role called {name} with the color {color}, {ctx.author.display_name}!",
                            color=key)
                        await ctx.send(embed=embed)
                if not found:
                    embed = discord.Embed(title=f"Sorry, I couldn't find that color, {ctx.author.display_name}.")
                    await ctx.send(embed=embed)
        else:
            for key, value in colors.items():
                if value == color.lower():
                    found = True
                    newRole = await ctx.guild.create_role(name=name, color=key,
                                                          permissions=discord.Permissions(read_messages=True))
                    await ctx.author.add_roles(newRole)
                    embed = discord.Embed(
                        title=f"Ok, I've given you a role called {name} with the color {color}, {ctx.author.display_name}!",
                        color=key)
                    await ctx.send(embed=embed)
            if not found:
                embed = discord.Embed(title=f"Sorry, I couldn't find that color, {ctx.author.display_name}.")
                await ctx.send(embed=embed)

    @commands.command()
    async def memcount(self, ctx):
        members = 0
        for member in ctx.guild.members:
            members += 1
        embed = discord.Embed(title=f"There are {members} members in {ctx.guild}!")
        await ctx.send(embed=embed)

    @commands.command()
    async def gif(self, ctx, num=1, *, img):
        img = img.replace(" ", "+")
        async with aiohttp.ClientSession() as cs:
            link = "http://api.giphy.com/v1/gifs/search?q=" + img + "&api_key=HIxNUDiCJmENIyZimfquvn7g20ILt4Dc&limit=15"
            async with cs.get(link) as r:
                num -= 1
                res = await r.json()  # returns dict
                result = res["data"][num]["url"]
                # embed = discord.Embed(color=random.choice(embedColors))
                # embed.set_image(url=str(result))
                # print(result)
                # await ctx.send(embed=embed)
                # await ctx.send(embed=discord.Embed(title=result))
                # embed = discord.Embed()
                # embed.set_thumbnail(url=result)
                # await ctx.send(embed=embed)
                message = await ctx.send(result)
                # await message.add_reaction("\U000025c0")
                # await message.add_reaction('\U000025b6')
                """try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=None)
                except asyncio.TimeoutError:
                    await message.channel.send('👎')
                print(str(reaction))
                if str(reaction) == "▶️":
                    result = res["data"][num + 1]["url"]
                    await message.edit(content=result)"""
                # print(json.dumps(res, sort_keys=True, indent=4))

    @commands.command()
    async def youtube(self, ctx, num: int, *, video):
        results = YoutubeSearch(video, max_results=20).to_dict()
        result = results[num - 1]['url_suffix']
        """thumbnail = results[num - 1]['thumbnails'][0]
        name = results[num - 1]['title']
        url = 'https://www.youtube.com' + result
        embed = discord.Embed(title=f"**{name}**", url=url, description=f"**{results[num - 1]['long_desc']}**",
                              color=random.choice(embedColors))
        embed.set_image(url=thumbnail)
        embed.set_thumbnail(url=thumbnail)
        embed.set_author(name=f"From {results[num - 1]['channel']}")
        embed.set_footer(text=f"{results[num - 1]['views']}")
        await ctx.send(embed=embed)"""
        url = 'https://www.youtube.com' + result
        await ctx.send(url)

    @gif.error
    async def gif_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(title=f"Sorry, I couldn't find that gif. Try again with different keywords!",
                                           color=discord.Color.red()))

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

    @commands.command()
    async def emojis(self, ctx, *, guilds=None):
        if guilds is None:
            for guild in self.bot.guilds:
                if guild.emojis:
                    emojis = {}
                    embed = discord.Embed(color=random.choice(embedColors))
                    emojis[str(guild.name)] = []
                    emojis[f"{guild.name} Extra Emojis"] = []
                    for emoji in guild.emojis:
                        emojis[str(guild.name)].append(str(emoji))
                    while len(" ".join(emojis[str(guild.name)])) > 1024:
                        emojis[f"{guild.name} Extra Emojis"].append(emojis[str(guild.name)][-1])
                        del emojis[str(guild.name)][-1]
                    for ids, emoji in emojis.items():
                        if emoji:
                            embed.add_field(name=f"**{ids}**:", value=f"{' '.join(emoji)}")
                    await ctx.send(embed=embed)
        else:
            found = False
            for guild in self.bot.guilds:
                if str(guild.name).lower() == guilds.lower():
                    found = True
                    emojis = {}
                    embed = discord.Embed(color=random.choice(embedColors))
                    emojis[str(guild.name)] = []
                    emojis[f"{guild.name} Extra Emojis"] = []
                    for emoji in guild.emojis:
                        emojis[str(guild.name)].append(str(emoji))
                    while len(" ".join(emojis[str(guild.name)])) > 1024:
                        emojis[f"{guild.name} Extra Emojis"].append(emojis[str(guild.name)][-1])
                        del emojis[str(guild.name)][-1]
                    for ids, emoji in emojis.items():
                        if emoji:
                            embed.add_field(name=f"**{ids}**:", value=f"{' '.join(emoji)}")
                    await ctx.send(embed=embed)

            if not found:
                await ctx.send(f"I am not in that server {ctx.author.mention}!")

    @commands.command()
    async def servers(self, ctx):
        embed = discord.Embed(title=f"My Servers:")
        for server in self.bot.guilds:
            embed.add_field(name=f"{server.name}", value=f"Joined at \n`{server.me.joined_at}`")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.guild)
    async def topic(self, ctx):
        currentTopic = next(nowTopic)
        await ctx.send(embed=discord.Embed(title=currentTopic,
                                           color=random.choice(embedColors)))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction) == "⭐" and user.guild_permissions.administrator and str(
                reaction.message.guild.name) == "Art Gatherings":
            attachment = reaction.message.attachments[0]
            embed = discord.Embed(description=reaction.message.content)
            embed.set_author(name=f"Artwork by {reaction.message.author.display_name}",
                             icon_url=reaction.message.author.avatar_url)
            embed.add_field(name=f"Original message:", value=f"[Jump to message]({reaction.message.jump_url})")
            embed.set_image(url=str(attachment.url))
            embed.set_footer(text=f"Posted to starboard by {user.display_name}", icon_url=str(user.avatar_url))
            channel = discord.utils.get(reaction.message.guild.text_channels, name="🏆masterpieces")
            await channel.send(embed=embed)

    @commands.command(aliases=["dog", "DOGGO", "Doggo", "Dog", "DOG", "doggy", "Doggy", "DOGGY"])
    async def doggo(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DOGGO!!!", color=random.choice(embedColors))
        embed.set_image(url=res["message"])
        embed.set_footer(text="Powered by https://dog.ceo")
        await ctx.send(embed=embed)

    @commands.command(alises=["cat", "Cat", "CAT", "CATTO", "Catto", "catty", "Catty", "CATTY"])
    async def catto(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
                res = await r.json()

        results = res[0]["url"]
        embed = discord.Embed(title=f"CATTO!!!", color=random.choice(embedColors))
        embed.set_image(url=results)
        embed.set_footer(text="Powered by https://thecatapi.com")
        await ctx.send(embed=embed)

    @tasks.loop(seconds=5)
    async def autoCatto(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
                res = await r.json()
        results = res[0]["url"]
        embed = discord.Embed(title=f"CATTO!!!", color=random.choice(embedColors))
        embed.set_image(url=results)
        embed.set_footer(text="Powered by https://thecatapi.com")
        await ctx.send(embed=embed)

    @commands.command()
    async def autocatto(self, ctx):
        self.autoCatto.start(ctx)

    @commands.command()
    async def stopautocatto(self, ctx):
        self.autoCatto.stop()
        await ctx.send("FINE, one more and then I'll stop.")

    @tasks.loop(seconds=5)
    async def autoDoggo(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DOGGO!!!", color=random.choice(embedColors))
        embed.set_image(url=res["message"])
        embed.set_footer(text="Powered by https://dog.ceo")
        await ctx.send(embed=embed)

    @commands.command()
    async def autodoggo(self, ctx):
        self.autoDoggo.start(ctx)

    @commands.command()
    async def stopautodoggo(self, ctx):
        self.autoDoggo.stop()
        await ctx.send("FINE, one more and then I'll stop.")

    @commands.command()
    async def calculateheight(self, ctx, *, height):
        await ctx.send(f"{ctx.author.mention}'s height is {height}.")

    @commands.command()
    async def meme(self, ctx):
        nowMeme = next(Meme)
        nowTitle = next(Title)
        embed = discord.Embed(title=nowTitle, color=random.choice(embedColors))
        embed.set_image(url=nowMeme)
        await ctx.send(embed=embed)

    """@commands.command()
    async def automeme(self, ctx):
        await self.AutoMeme.start(ctx)

    @tasks.loop(seconds=7)
    async def AutoMeme(self, ctx):
        await self.meme(ctx)

    @commands.command()
    async def stopautomeme(self, ctx):
        await self.AutoMeme.stop()
        await ctx.send("Ok, I've stopped automemeing")"""

    @commands.command(aliases=["murder", "Murder", "MURDER", "Kill", "KILL"])
    async def kill(self, ctx, member):
        death = random.choice(kills)
        await ctx.send(f"{member} {death}")

def setup(bot):
    bot.add_cog(BotFunCog(bot))
