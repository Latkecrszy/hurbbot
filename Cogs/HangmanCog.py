import discord
from discord.ext import commands, tasks
import random
import asyncio
import json
from Bots.Cogs.players import refreshBalance

hang1 = '''           ---------------------|
            |                   |
            |                   |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''
hang2 = '''           ---------------------|
            |                   |
            |                   |
            O                   |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''
hang3 = '''           ---------------------|
            |                   |
            |                   |
            O                   |
            |                   |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''
hang4 = '''           ---------------------|
            |                   |
            |                   |
            O                   |
            |                   |
           /                    |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''
hang5 = '''           ---------------------|
            |                   |
            |                   |
            O                   |
            |                   |
           / \                  |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''
hang6 = '''           ---------------------|
            |                   |
            |                   |
            O                   |
            |                   |
           /|\                  |
            |                   |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''
hang7 = '''           ---------------------|
            |                   |
            |                   |
            O                   |
            |                   |
           /|\                  |
            |                   |
           /                    |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''
hang8 = '''           ---------------------|
            |                   |
            |                   |
            O                   |
            |                   |
           /|\                  |
            |                   |
           / \                  |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
        ----------------------------'''

hangs = [hang1, hang2, hang3, hang4, hang5, hang6, hang7, hang8]

words = ["apple", "ant", "armpit", "banana", 'birds', 'blatant', "crocodile", 'cooked', 'crack', 'deepen', 'dark', "depend",
         "entire", 'everlasting', 'entity', 'faceoff', 'flat', "factual", "great", "height", "jumping", "kangaroo", "laughter", "monopoly", "never",
         "opposing", "promise", "question", "respond", "street", "toilet", "under", "violet", "window", "xenon", "yellow",
         "zebra", "computer", "phone", "notebook", "pencil", "program", "coding", "coffee", "scissors", "paper", "school",
         "textbook", "dictionary", "hangman", "silverware", "picture", "photograph", "message", "python", "snake", "chicken",
         "browser", "plate", "sushi", "abandon", "basement", "abduction", "aliens", "conference", "server", "member", "remember",
         "printer", "class", "mug", "speaker", "turtle", "spoon", "mask", "kArEn", "picture", "wires", "python", "classroom",
         "pneumonoultramicroscopicsilicovolcanoconiosis", "drone", "printer", "xylophone", "terminal", "discord",
         "alcohol", "disinfectant", "schedule", "chicken", "website", "glasses", "settings"]


"""class HangmanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word = random.choice(words)
        self.wordList = []
        self.guessedList = []
        self.wrongGuessedList = []
        self.playing = None
        self.wordDash = []
        self.activeHang = 0
        self.hangs = hangs
        self.seconds = 0

    @commands.command()
    async def hangman(self, ctx):
        if self.playing:
            await ctx.send(f"Someone is already playing a game of hangman {ctx.author.mention}! Please don't break me.")
        else:
            self.seconds = 0
            await asyncio.sleep(1)
            self.timeOut.start(ctx)
            self.word = random.choice(words)
            self.wordList = []
            self.guessedList = []
            self.wrongGuessedList = []
            self.wordDash = []
            self.playing = str(ctx.author)
            self.word = random.choice(words)
            self.activeHang = 0
            self.hangs = hangs
            print(self.word)
            for char in self.word:
                self.wordDash.append("_")
                self.wordList.append(char)
            embed = discord.Embed(title=f"`{' '.join(self.wordDash)}`",
                                  description=f"Here are the spaces of your word, {ctx.author.mention}! Start guessing letters by using the `guess <letter>` command!")
            embed.add_field(name=f"You have {8 - int(self.activeHang)} chances.",
                            value=f"```{self.hangs[int(self.activeHang)]}```")
            await ctx.send(embed=embed)

    @commands.command()
    async def guess(self, ctx, letter):
        if self.playing == str(ctx.author):
            self.timeOut.stop()
            self.seconds = 0
            await asyncio.sleep(1)
            self.timeOut.start(ctx)
            if await self.winCheck(ctx):
                if not await self.deathCheck(ctx):
                    inWord = False
                    if letter.lower() in self.guessedList or letter.lower() in self.wrongGuessedList:
                        await ctx.send(f"You already guessed this letter, {ctx.author.mention}!")
                    else:
                        for x in range(len(self.wordList)):
                            if self.wordList[x] == letter.lower():
                                self.guessedList.append(letter.lower())
                                self.wordDash[x] = letter.lower()
                                inWord = True
                        if inWord:
                            if await self.winCheck(ctx):
                                embed = discord.Embed(title="Congrats! That letter was in the word!",
                                                      description=f"`{' '.join(self.wordDash)}`", color=discord.Color.green())
                                embed.add_field(name=f"You have {8-int(self.activeHang)} chances left.", value=f"```{self.hangs[int(self.activeHang)]}```")
                                await ctx.send(embed=embed)
                        elif not inWord:
                            self.activeHang += 1
                            if not await self.deathCheck(ctx):
                                self.wrongGuessedList.append(letter.lower())
                                embed = discord.Embed(title="Sorry. That letter was not in the word.",
                                                      description=f"`{' '.join(self.wordDash)}`", color=discord.Color.red())
                                embed.add_field(name=f"You have {8-int(self.activeHang)} chances left.", value=f"```{self.hangs[int(self.activeHang)]}```")
                                await ctx.send(embed=embed)
                                await self.winCheck(ctx)

        else:
            await ctx.send(f"You are not playing a game of hangman right now, {ctx.author.mention}!")

    async def winCheck(self, ctx):
        if "_" not in self.wordDash:
            self.playing = False
            embed = discord.Embed(title=f"CONGRATS!!!   {ctx.author.display_name}, you won! Good job at beating the game! The word was {self.word}.",
                                  description=f"```{self.hangs[int(self.activeHang)]}```",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.timeOut.stop()
            self.seconds = 0
            return False
        else:
            return True

    async def deathCheck(self, ctx):
        if self.activeHang == 8:
            embed = discord.Embed(title=f"Sorry, {ctx.author.display_name}, you died. The word was {self.word}.",
                                  description=f"```{hang8}```",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            self.playing = ""
            self.timeOut.stop()
            self.seconds = 0
            return True
        else:
            return False

    @tasks.loop(seconds=1)
    async def timeOut(self, ctx):
        self.seconds += 1
        if self.seconds == 90:
            self.seconds = 0
            self.playing = ""
            await ctx.send(embed=discord.Embed(
                title=f"{ctx.author.display_name}, your game of hangman has timed out after 90 seconds of inactivity.",
                color=discord.Color.red()))
            self.timeOut.stop()"""

class HangmanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word = random.choice(words)
        self.wordList = []
        self.guessedList = []
        self.wrongGuessedList = []
        self.playing = None
        self.wordDash = []
        self.activeHang = 0
        self.hangs = hangs
        self.seconds = 0
        self.activeMessage = ""
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    @commands.command()
    async def hangman(self, ctx):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]
        foundHang = False
        for item, value in players[str(ctx.author.id)].items.items():
            if item.name.lower() == "hangman" and value >= 1:
                foundHang = True
        if foundHang:
            if self.playing:
                await ctx.send(f"Someone is already playing a game of hangman {ctx.author.mention}! Please don't break me.")
            else:
                self.seconds = 0
                await asyncio.sleep(1)
                self.timeOut.start(ctx)
                self.word = random.choice(words)
                self.wordList = []
                self.guessedList = []
                self.wrongGuessedList = []
                self.wordDash = []
                self.activeMessage = ""
                self.playing = str(ctx.author)
                self.word = random.choice(words)
                self.activeHang = 0
                self.hangs = hangs
                for char in self.word:
                    self.wordDash.append("_")
                    self.wordList.append(char)
                embed = discord.Embed(title=f"`{' '.join(self.wordDash)}`",
                                      description=f"Here are the spaces of your word, {ctx.author.mention}! Start guessing letters by using the `guess <letter>` command!")
                embed.add_field(name=f"You have {8 - int(self.activeHang)} chances.",
                                value=f"```{self.hangs[int(self.activeHang)]}```")
                self.activeMessage = await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(description=f"You do not yet own this game! You can buy it with the `%buy hangman` command!", color=discord.Color.red()))

    @commands.command()
    async def guess(self, ctx, letter):
        if self.playing == str(ctx.author):
            self.timeOut.stop()
            self.seconds = 0
            await asyncio.sleep(1)
            self.timeOut.start(ctx)
            if await self.winCheck(ctx):
                if not await self.deathCheck(ctx):
                    inWord = False
                    if letter.lower() in self.guessedList or letter.lower() in self.wrongGuessedList:
                        await ctx.send(f"You already guessed {letter}, {ctx.author.mention}!")
                    else:
                        for x in range(len(self.wordList)):
                            if self.wordList[x] == letter.lower():
                                self.guessedList.append(letter.lower())
                                self.wordDash[x] = letter.lower()
                                inWord = True
                        if inWord:
                            if await self.winCheck(ctx):
                                embed = discord.Embed(title="Congrats! That letter was in the word!",
                                                      description=f"`{' '.join(self.wordDash)}`", color=discord.Color.green())
                                embed.add_field(name=f"You have {8-int(self.activeHang)} chances left.", value=f"```{self.hangs[int(self.activeHang)]}```")
                                await self.activeMessage.edit(embed=embed)
                        elif not inWord:
                            self.activeHang += 1
                            if not await self.deathCheck(ctx):
                                self.wrongGuessedList.append(letter.lower())
                                embed = discord.Embed(title="Sorry. That letter was not in the word.",
                                                      description=f"`{' '.join(self.wordDash)}`", color=discord.Color.red())
                                embed.add_field(name=f"You have {8-int(self.activeHang)} chances left.", value=f"```{self.hangs[int(self.activeHang)]}```")
                                await self.activeMessage.edit(embed=embed)
                                await self.winCheck(ctx)
                    await ctx.message.delete()

        else:
            await ctx.send(f"You are not playing a game of hangman right now, {ctx.author.mention}!")

    async def winCheck(self, ctx):
        if "_" not in self.wordDash:
            self.playing = False
            embed = discord.Embed(title=f"CONGRATS!!!   {ctx.author.display_name}, you won! Good job at beating the game! The word was {self.word}.",
                                  description=f"```{self.hangs[int(self.activeHang)]}```",
                                  color=discord.Color.green())
            await self.activeMessage.edit(embed=embed)
            self.timeOut.stop()
            self.seconds = 0
            self.activeMessage = ""
            return False
        else:
            return True

    async def deathCheck(self, ctx):
        if self.activeHang == 8:
            embed = discord.Embed(title=f"Sorry, {ctx.author.display_name}, you died. The word was {self.word}.",
                                  description=f"```{hang8}```",
                                  color=discord.Color.red())
            await self.activeMessage.edit(embed=embed)
            self.playing = ""
            self.timeOut.stop()
            self.seconds = 0
            self.activeMessage = ""
            return True
        else:
            return False

    @tasks.loop(seconds=1)
    async def timeOut(self, ctx):
        self.seconds += 1
        if self.seconds == 90:
            self.seconds = 0
            self.activeMessage = ""
            self.playing = ""
            await ctx.send(embed=discord.Embed(
                title=f"{ctx.author.display_name}, your game of hangman has timed out after 90 seconds of inactivity.",
                color=discord.Color.red()))
            self.timeOut.stop()


def setup(bot):
    bot.add_cog(HangmanCog(bot))
