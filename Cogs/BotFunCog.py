import discord
from discord.ext import commands, tasks
import random
import asyncio
import json
import aiohttp
from discord.ext.commands.cooldowns import BucketType
from youtube_search import YoutubeSearch
from itertools import cycle


embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]

topics = ["What hobbies do you have?", "How much free time do you have?",
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
          "Should schools give out homework and have shorter days or give out no homework and have longer days?",
          "Should schools should block YouTube, Discord, and other such sites on their computers?",
          "Should schools have lockers?", "Should schools give out detention?", "Should sex-ed be mandatory in school?",
          "Homeschooling or traditional school?",
          "What punishment is suitable for the person who banned discord from school computers?",
          "What is the best kind of cheese?", "Am I the best discord bot you've ever seen?",
          "What is the best discord bot? Other than me, obviously.",
          "What's your favorite exercise?", "Are you left or right handed?", "What is the best ice cream flavor?",
          "What is the worst teacher/boss that you've ever had?", "WHERE THE FUCK IS OLD ZEALAND TELL ME NOW"]

kills = ["was devoured by wumpus.",
         "drank too much bleach, what an idiot.",
         "injected purell into their veins and contracted death.", "was murdered by the Hurb mafia.",
         "ran with scissors and stabbed their eyes out.",
         "was a fucking idiot and didn't wear a mask and caught COVID and died.", "choked on an airpod.",
         "forgot to feed their dog and was murdered by it.", "was stabbed 69 times.",
         "was shot 69 times.", "was crushed by a giant turtle.", "literally laughed their ass of and died of blood loss.",
         "was burned alive.", "was stepped on by a giant fucking cockroach, now they know how it feels.",
         "was defenestrated.", "was not the imposter but deserved to fucking die anyways.", "was eaten by the imposter.",
         "fell into the toilet and drowned.", "was crushed by a falling piano.", "asked their crush out, got accepted, then died of a heart attack.",
         "cut themselves in half, but flex tape wasn't enough to save them.", "took their toaster into the bath and was electecuted by it.",
         "didn't get enough MILK and died."]

random.shuffle(topics)
nowTopic = cycle(topics)


def is_it_me(ctx):
    return ctx.author.id == 670493561921208320


class BotFunCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    async def gif(self, ctx, num=1, *, img):
        img = img.replace(" ", "+")
        async with aiohttp.ClientSession() as cs:
            link = "http://api.giphy.com/v1/gifs/search?q=" + img + "&api_key=HIxNUDiCJmENIyZimfquvn7g20ILt4Dc&limit=15"
            async with cs.get(link) as r:
                num -= 1
                res = await r.json()  # returns dict
                result = res["data"][num]["url"]
                message = await ctx.send(result)

    """@commands.command()
    async def youtube(self, ctx, num: int, *, video):
        results = YoutubeSearch(video, max_results=20).to_dict()
        result = results[num - 1]['url_suffix']
        url = 'https://www.youtube.com' + result
        await ctx.send(url)"""

    @gif.error
    async def gif_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(title=f"Sorry, I couldn't find that gif. Try again with different keywords!",
                                           color=discord.Color.red()))

    @commands.command()
    async def say(self, ctx, *, message):
        embed = discord.Embed(title=message)
        await ctx.message.delete()
        embed.set_footer(text=f"-{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def servers(self, ctx):
        embed = discord.Embed(title=f"My Servers:")
        members = 0
        message = ''''''
        for i in range(len(self.bot.guilds)):
            server = self.bot.guilds[i]
            message += f"#{i+1} **{server.name}**\n\n"
            members += len([member for member in server.members])
        embed.add_field(name=f"Serving {len(self.bot.guilds)} servers", value=f"And {members} members!")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        await ctx.send(message)
        await ctx.send(embed=embed)


    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title=f"My Servers:")
        members = 0
        for server in self.bot.guilds:
            members += len([member for member in server.members])
        embed.add_field(name=f"Serving {len(self.bot.guilds)} servers", value=f"And {members} members!")
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.guild)
    async def topic(self, ctx):
        currentTopic = next(nowTopic)
        await ctx.send(embed=discord.Embed(title=currentTopic,
                                           color=random.choice(embedColors)))

    @commands.command(aliases=["dog", "doggy"])
    async def doggo(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DOGGO!!!", color=random.choice(embedColors))
        embed.set_image(url=res["message"])
        embed.set_footer(text="Powered by https://dog.ceo")
        await ctx.send(embed=embed)

    @commands.command(aliases=["cat", "catty"])
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

    @commands.command(aliases=["autocat"])
    async def autocatto(self, ctx):
        self.autoCatto.start(ctx)

    @commands.command(aliase=["stopautocat"])
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

    @commands.command(aliases=["autodog"])
    async def autodoggo(self, ctx):
        self.autoDoggo.start(ctx)

    @commands.command()
    async def stopautodoggo(self, ctx):
        self.autoDoggo.stop()
        await ctx.send("FINE, one more and then I'll stop.")

    @commands.command(aliases=["murder"])
    @commands.cooldown(1, 15, BucketType.user)
    async def kill(self, ctx, *, member):
        death = random.choice(kills)
        if str(member).lower().find("latkecrszy") != -1 or str(member).lower().find("670493561921208320") != -1:
            await ctx.send(f"Don't you fucking try to kill my creator, imma kill you instead. {ctx.author.mention} {death}")
        elif str(member.lower()) == "me":
            await ctx.send("You died.")
        elif str(member.lower()) == "i":
            await ctx.send(f"NOPE, you can't get me to kill myself SON. {ctx.author.mention} {death}")
        else:
            await ctx.send(f"{member} {death}")

    @commands.command(aliases=["8ball"])
    @commands.cooldown(1, 10, BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.", "Without a doubt.", "It is decidedly so.", "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                     "Very doubtful."]
        if question.lower().startswith("who"):
            member = random.choice(ctx.guild.members)
            while not member.guild_permissions.manage_guild or member.bot:
                member = random.choice(ctx.guild.members)
            await ctx.send(
                embed=discord.Embed(title=f'''Question: {question}''', description=f"**Answer: {member.mention}**"))
        else:
            await ctx.send(embed=discord.Embed(title=f'''Question: {question}''',
                                               description=f"**Answer: {random.choice(responses)}**"))

    @commands.command(aliases=["ducc", "ducco", "ducko"])
    async def duck(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random-d.uk/api/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DUCCCY!!!", color=random.choice(embedColors))
        embed.set_image(url=res["url"])
        embed.set_footer(text=res["message"])
        await ctx.send(embed=embed)

    @commands.command(aliases=["pander", "pando"])
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as r:
                res = await r.json()
        embed = discord.Embed(title=f"PANDA!!!", color=random.choice(embedColors))
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["bird", "birdo", "birbo"])
    async def birb(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/birb") as r:
                res = await r.json()
        embed = discord.Embed(title=f"BIRB!!!", color=random.choice(embedColors))
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["foxo", "foxxo", "foxy", "foxxy"])
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/fox") as r:
                res = await r.json()
        embed = discord.Embed(title=f"FOXXY!!!", color=random.choice(embedColors))
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["redpando", "redpander"])
    async def redpanda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/red_panda") as r:
                res = await r.json()
        embed = discord.Embed(title=f"RED PANDO!!!", color=random.choice(embedColors))
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["koaler"])
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/koala") as r:
                res = await r.json()
        embed = discord.Embed(title=f"KOALA!!!", color=random.choice(embedColors))
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command()
    async def lyrics(self, ctx, *, title):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://some-random-api.ml/lyrics?title="{title}"') as r:
                res = await r.json()
        await ctx.send(f"Author: {res['author']}")
        await ctx.send(f"Lyrics: {res['lyrics']}")


def setup(bot):
    bot.add_cog(BotFunCog(bot))
