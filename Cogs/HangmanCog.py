import discord
from discord.ext import commands, tasks
import random
import json

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


class HangmanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}


    @commands.command()
    async def hangman(self, ctx):
        storage = json.load(open("servers.json"))
        players = storage["players"]
        foundHang = {item: value for item, value in players[str(ctx.author.id)]["items"].items() if item.lower() == "hangman" and int(value) >= 1}
        if foundHang:
            if str(ctx.author.id) not in self.data:
                word = random.choice(words)
                self.data[str(ctx.author.id)] = {"word": word, "word_list": [char for char in word], "guessed": [], "incorrect": [], "dashes": ["_" for _ in word], "hang": 0, "seconds": 0, "message": None, "letters": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]}
                embed = discord.Embed(title=f"`{' '.join(self.data[str(ctx.author.id)]['dashes'])}`",
                                      description=f"Here are the spaces of your word, {ctx.author.mention}! Start guessing letters by using the `%guess <letter>` command!")
                embed.add_field(name=f"You have {8 - int(self.data[str(ctx.author.id)]['hang'])} chances.",
                                value=f"```{hangs[self.data[str(ctx.author.id)]['hang']]}```")
                self.data[str(ctx.author.id)]['message'] = await ctx.send(embed=embed)
                try:
                    self.timeOut.start(ctx)
                except:
                    pass
            else:
                await ctx.send(embed=discord.Embed(description=f"You are already playing a game of hangman {ctx.author.mention}!"))
        else:
            await ctx.send(embed=discord.Embed(description=f"You do not yet own this game! You can buy it with the `%buy hangman` command!", color=discord.Color.red()))

    @commands.command()
    async def guess(self, ctx, letter):
        await ctx.message.delete()
        if str(ctx.author.id) in self.data:
            self.data[str(ctx.author.id)]['seconds'] = 0
            if await self.winCheck(ctx):
                if not await self.deathCheck(ctx):
                    if len(letter) == 1:
                        inWord = False
                        if letter.lower() in self.data[str(ctx.author.id)]['guessed'] or letter.lower() in self.data[str(ctx.author.id)]['incorrect']:
                            await ctx.send(f"You already guessed {letter}, {ctx.author.mention}!")
                        else:
                            for x in range(len(self.data[str(ctx.author.id)]['word_list'])):
                                if self.data[str(ctx.author.id)]['word_list'][x] == letter.lower():
                                    self.data[str(ctx.author.id)]['guessed'].append(letter.lower())
                                    self.data[str(ctx.author.id)]['dashes'][x] = letter.lower()
                                    inWord = True
                            if inWord:
                                if await self.winCheck(ctx):
                                    embed = discord.Embed(title="Congrats! That letter was in the word!",
                                                          description=f"`{' '.join(self.data[str(ctx.author.id)]['dashes'])}`", color=discord.Color.green())
                                    embed.add_field(name=f"You have {8-int(self.data[str(ctx.author.id)]['hang'])} chances left.", value=f"```{hangs[self.data[str(ctx.author.id)]['hang']]}```")
                                    await self.data[str(ctx.author.id)]['message'].edit(embed=embed)
                            elif not inWord:
                                self.data[str(ctx.author.id)]['hang'] += 1
                                if not await self.deathCheck(ctx):
                                    self.data[str(ctx.author.id)]['incorrect'].append(letter.lower())
                                    embed = discord.Embed(title=f"Sorry. {letter.lower()} was not in the word.",
                                                          description=f"`{' '.join(self.data[str(ctx.author.id)]['dashes'])}`", color=discord.Color.red())
                                    embed.add_field(name=f"You have {8-self.data[str(ctx.author.id)]['hang']} chances left.", value=f"```{hangs[self.data[str(ctx.author.id)]['hang']]}```")
                                    await self.data[str(ctx.author.id)]['message'].edit(embed=embed)
                                    await self.winCheck(ctx)
                        await ctx.message.delete()
                    else:
                        if letter.lower() == self.data[str(ctx.author.id)]['word'].lower():
                            embed = discord.Embed(
                                title=f"CONGRATS!!!   {ctx.author.display_name}, you won! Good job at beating the game! The word was {self.data[str(ctx.author.id)]['word']}.",
                                description=f"```{hangs[self.data[str(ctx.author.id)]['hang']]}```",
                                color=discord.Color.green())
                            await self.data[str(ctx.author.id)]['message'].edit(embed=embed)
                            self.data.pop(str(ctx.author.id))

        else:
            await ctx.send(f"You are not playing a game of hangman right now, {ctx.author.mention}!")

    async def winCheck(self, ctx):
        if "_" not in self.data[str(ctx.author.id)]['dashes']:
            embed = discord.Embed(title=f"CONGRATS!!!   {ctx.author.display_name}, you won! Good job at beating the game! The word was {self.data[str(ctx.author.id)]['word']}.",
                                  description=f"```{hangs[self.data[str(ctx.author.id)]['hang']]}```",
                                  color=discord.Color.green())
            await self.data[str(ctx.author.id)]['message'].edit(embed=embed)
            self.data.pop(str(ctx.author.id))
            return False
        else:
            return True

    async def deathCheck(self, ctx):
        if self.data[str(ctx.author.id)]['hang'] == 8:
            embed = discord.Embed(title=f"Sorry, {ctx.author.display_name}, you died. The word was {self.data[str(ctx.author.id)]['word']}.",
                                  description=f"```{hang8}```",
                                  color=discord.Color.red())
            await self.data[str(ctx.author.id)]['message'].edit(embed=embed)
            return True
        else:
            return False

    @tasks.loop(seconds=1)
    async def timeOut(self, ctx):
        self.data[str(ctx.author.id)]['seconds'] += 1
        if self.data[str(ctx.author.id)]['seconds'] == 90:
            await ctx.send(embed=discord.Embed(
                title=f"{ctx.author.display_name}, your game of hangman has timed out after 90 seconds of inactivity.",
                color=discord.Color.red()))
            self.data.pop(str(ctx.author.id))


def setup(bot):
    bot.add_cog(HangmanCog(bot))
