import discord
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from Bots.PlayerStart import Item, refreshBalance, saveMoney
import json
import random
import asyncio


class BlackJackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 16
        self.suits = [":clubs:", ":hearts:", ":diamonds:", ":spades:"]
        self.deck = {}
        for card in self.cards:
            for suit in self.suits:
                self.deck[card] = suit
        self.dealerHand = []
        self.playerHand = []
        self.hand = []
        self.bet = 0
        self.playerValue = 0
        self.dealerValue = 0
        self.playing = ""
        self.seconds = 0
        self.canSplit = False
        self.playerHand2 = []
        self.playerHand3 = []
        self.playerHand4 = []
        self.playerHand5 = []
        self.playerHand6 = []
        self.playerHand7 = []
        self.playerHand8 = []
        self.playerHands = [self.playerHand,
                            self.playerHand2,
                            self.playerHand3,
                            self.playerHand4,
                            self.playerHand5,
                            self.playerHand6,
                            self.playerHand7,
                            self.playerHand8]
        self.splitTimes = 0
        self.handsDone = 0

    def deal(self, hand):
        random.shuffle(self.cards)
        for x in range(2):
            oneCard = self.cards.pop()
            hand.append(oneCard)
        return hand

    def hitHand(self, hand):
        oneCard = self.cards.pop()
        hand.append(oneCard)
        return hand

    @commands.command(aliases=["HIT", "Hit", "h", "H"])
    async def hit(self, ctx):
        if self.playing == str(ctx.author):
            self.timeOut.stop()
            self.seconds = 0
            await asyncio.sleep(1)
            self.timeOut.start(ctx)
            if self.handsDone == 0:
                self.hitHand(self.playerHand)
                if not self.blackJackCheck(self.dealerHand, self.playerHand):
                    if not self.checkBust(self.dealerHand, self.playerHand):
                        await self.game(ctx, self.dealerHand, self.playerHand)
                    elif self.checkBust(self.dealerHand, self.playerHand):
                        await self.checkBustSend(ctx, self.dealerHand, self.playerHand)
                elif self.blackJackCheck(self.dealerHand, self.playerHand):
                    await self.blackJackCheckSend(ctx, self.dealerHand, self.playerHand)
        elif self.playing != str(ctx.author):
            embed = discord.Embed(title=f"You are not playing a game of blackjack, {ctx.author.display_name}!", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=["STAND", "Stand", "s", "S"])
    async def stand(self, ctx):
        if self.playing == str(ctx.author):
            self.timeOut.stop()
            self.seconds = 0
            await asyncio.sleep(1)
            self.timeOut.start(ctx)
            while self.total(self.dealerHand) < 17:
                self.hitHand(self.dealerHand)
            if self.checkBust(self.dealerHand, self.playerHand):
                await self.checkBustSend(ctx, self.dealerHand, self.playerHand)
            elif not self.checkBust(self.dealerHand, self.playerHand):
                await self.score(ctx, self.dealerHand, self.playerHand)
        elif self.playing != str(ctx.author):
            embed = discord.Embed(title=f"You are not playing a game of blackjack, {ctx.author.display_name}!", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=["dd", "Doubledown", "DoubleDown", "DD", "Dd", "DOUBLEDOWN"])
    async def doubledown(self, ctx):
        if self.playing == str(ctx.author):
            players = refreshBalance()
            player = players[str(ctx.author)]
            if int(self.bet)*2 > int(player.money):
                await ctx.send(embed=discord.Embed(description=f"You do not have enough money to double down {ctx.author.mention}!",
                                                   color=discord.Color.red()))
            else:
                self.hitHand(self.playerHand)
                self.bet = int(self.bet)
                self.bet *= 2
                self.timeOut.stop()
                self.seconds = 0
                await asyncio.sleep(1)
                self.timeOut.start(ctx)
                while self.total(self.dealerHand) < 17:
                    self.hitHand(self.dealerHand)
                if self.checkBust(self.dealerHand, self.playerHand):
                    await self.checkBustSend(ctx, self.dealerHand, self.playerHand)
                elif not self.checkBust(self.dealerHand, self.playerHand):
                    await self.score(ctx, self.dealerHand, self.playerHand)
        elif self.playing != str(ctx.author):
            embed = discord.Embed(title=f"You are not playing a game of blackjack, {ctx.author.display_name}!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

    async def score(self, ctx, dealerHand, playerHand):
        self.timeOut.stop()
        self.seconds = 0
        playerDisplayHand = ""
        for i in playerHand:
            playerDisplayHand += f"`{i}` "
        dealerDisplayHand = ""
        for i in dealerHand:
            dealerDisplayHand += f"`{i}` "
        playerTotal = self.total(playerHand)
        dealerTotal = self.total(dealerHand)
        dealerScore = self.total(dealerHand)
        playerScore = self.total(playerHand)
        if dealerScore > playerScore:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.red())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                            value=f"Total ==> `{playerTotal}`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                            value=f"Total ==> `{dealerTotal}`", inline=True)
            embed.add_field(name="The dealer got a higher value than you. You lost.", value=f"You lost ${self.bet}.",
                            inline=False)
            players = refreshBalance()
            player = players[str(ctx.author)]
            player.money -= self.bet
            await saveMoney(ctx, players)
            self.playing = ""
            await ctx.send(embed=embed)
        elif playerScore > dealerScore:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                            value=f"Total ==> `{playerTotal}`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                            value=f"Total ==> `{dealerTotal}`", inline=True)
            embed.add_field(name="You won! Your score was higher than the dealer's!", value=f"You won ${self.bet}!",
                            inline=False)
            players = refreshBalance()
            player = players[str(ctx.author)]
            player.money += self.bet
            await saveMoney(ctx, players)
            self.playing = ""
            await ctx.send(embed=embed)
        elif playerScore == dealerScore:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.gold())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                            value=f"Total ==> `{playerTotal}`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                            value=f"Total ==> `{dealerTotal}`", inline=True)
            embed.add_field(name="It's a tie! Your score was the same as the dealer's",
                            value="Your balance stayed the same.", inline=False)
            self.playing = ""
            await ctx.send(embed=embed)

    def total(self, hand):
        aces = 0
        value = 0
        for cards in hand:
            if cards == "1" or cards == "2" or cards == "3" or cards == "4" or cards == "5" or cards == "6" or cards == "7" or cards == "8" or cards == "9" or cards == "10":
                value += int(cards)
            elif cards == "J" or cards == "Q" or cards == "K":
                value += 10
            elif cards == "A":
                aces += 1
        for x in range(aces):
            if value < 11:
                value += 11
            elif value >= 11:
                value += 1
        return value

    """def addCardTotal(self, hand, value):
        if hand[-1] in self.cards[1:10]:
            value += int(hand[-1])
        elif hand[-1] == "J" or hand[-1] == "Q" or hand[-1] == "K":
            value += 10
        elif hand[-1] == "A":
            if value < 11:
                value += 11
            elif value >= 11:
                value += 1
        return value"""

    def blackJackCheck(self, dealerHand, playerHand):
        gameOver = False
        if self.total(playerHand) == 21 or self.total(dealerHand) == 21:
            gameOver = True
            self.playing = ""
            self.timeOut.stop()
        return gameOver

    async def blackJackCheckSend(self, ctx, dealerHand, playerHand):
        playerDisplayHand = ""
        for i in playerHand:
            playerDisplayHand += f"`{i}` "
        dealerDisplayHand = ""
        for i in dealerHand:
            dealerDisplayHand += f"`{i}` "
        playerTotal = self.total(playerHand)
        dealerTotal = self.total(dealerHand)
        if self.total(playerHand) == 21:
            self.timeOut.stop()
            if self.total(dealerHand) == 21:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.gold())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                                value=f"Total ==> `{playerTotal}`", inline=True)
                embed.add_field(name=f"**Hurb**:\nCards ==> {playerDisplayHand}",
                                value=f"Total ==> `{playerTotal}`", inline=True)
                embed.add_field(name="It's a tie! You both got blackjack!", value="Your balance stayed the same.",
                                inline=False)
                await ctx.send(embed=embed)
                self.playing = ""

            elif self.total(dealerHand) != 21:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.green())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                                value=f"Total ==> `{playerTotal}`", inline=True)
                embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                                value=f"Total ==> `{dealerTotal}`", inline=True)
                embed.add_field(name="You won! You reached 21 before the dealer!", value=f"You won ${self.bet}!",
                                inline=False)
                await ctx.send(embed=embed)
                players = refreshBalance()
                player = players[str(ctx.author)]
                player.money += self.bet
                await saveMoney(ctx, players)

        elif self.total(dealerHand) == 21:
            self.timeOut.stop()
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.red())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                            value=f"Total ==> `{playerTotal}`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                            value=f"Total ==> `{dealerTotal}`", inline=True)
            embed.add_field(name="The dealer reached 21 before you did. You lost.", value=f"You lost ${self.bet}.",
                            inline=False)
            await ctx.send(embed=embed)
            players = refreshBalance()
            player = players[str(ctx.author)]
            player.money -= self.bet
            await saveMoney(ctx, players)
            self.playing = ""

    def checkBust(self, dealerHand, playerHand):
        gameOver = False
        if self.total(playerHand) > 21 or self.total(dealerHand) > 21:
            gameOver = True
            self.timeOut.stop()
        return gameOver

    async def checkBustSend(self, ctx, dealerHand, playerHand):
        playerDisplayHand = ""
        for i in playerHand:
            playerDisplayHand += f"`{i}` "
        dealerDisplayHand = ""
        for i in dealerHand:
            dealerDisplayHand += f"`{i}` "
        playerTotal = self.total(playerHand)
        dealerTotal = self.total(dealerHand)
        if self.total(playerHand) > 21:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.red())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                            value=f"Total ==> `{playerTotal}`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                            value=f"Total ==> `{dealerTotal}`", inline=True)
            embed.add_field(name="You busted! You lost.", value=f"You lost ${self.bet}.", inline=False)
            players = refreshBalance()
            player = players[str(ctx.author)]
            player.money -= self.bet
            await saveMoney(ctx, players)
            await ctx.send(embed=embed)
            self.playing = ""

        elif self.total(dealerHand) > 21:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                            value=f"Total ==> `{playerTotal}`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                            value=f"Total ==> `{dealerTotal}`", inline=True)
            embed.add_field(name="The dealer busted! You won!", value=f"You won ${self.bet}.", inline=False)

            players = refreshBalance()
            player = players[str(ctx.author)]
            player.money += self.bet
            await saveMoney(ctx, players)
            await ctx.send(embed=embed)
            self.playing = ""

    async def game(self, ctx, dealerHand, playerHand):
        playerDisplayHand = ""
        for i in playerHand:
            playerDisplayHand += f"`{i}` "
        dealerDisplayHand = f"`{dealerHand[0]}`"
        playerTotal = self.total(playerHand)
        embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.dark_green())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                        value=f"Total ==> `{playerTotal}`", inline=True)
        embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                        value=f"Total ==> `?`", inline=True)
        if not self.canSplit:
            embed.set_footer(text=f"Your options are: hit, stand, or surrender.")
        else:
            embed.set_footer(text=f"Your options are: hit, stand, split, or surrender.")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(aliases=["bj", "BJ", "Blackjack", "BLACKJACK", "BlackJack", "blackJack"])
    async def blackjack(self, ctx, bet):
        if await self.tooMuchCheck(ctx, bet):
            if self.playing == str(ctx.author):
                embed = discord.Embed(
                    title=f"You are already playing a game of blackjack, {ctx.author.display_name}! Please don't break me :(",
                    color=discord.Color.red())
                await ctx.send(embed=embed)
            elif self.playing != "":
                embed = discord.Embed(
                    title=f"Someone is already playing a game of blackjack, {ctx.author.display_name}! Please don't break me :(",
                    color=discord.Color.red())
                await ctx.send(embed=embed)
            elif self.playing == "":
                self.seconds = 0
                self.timeOut.start(ctx)
                self.playing = str(ctx.author)
                self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4
                self.suits = [":clubs:", ":hearts:", ":diamonds:", ":spades:"]
                self.dealerHand = []
                self.playerHand = []
                self.hand = []
                self.playerValue = 0
                self.dealerValue = 0
                self.bet = int(bet)
                self.deal(self.dealerHand)
                self.deal(self.playerHand)
                self.total(self.dealerHand)
                self.total(self.playerHand)

                if self.blackJackCheck(dealerHand=self.dealerHand, playerHand=self.playerHand):
                    await self.blackJackCheckSend(ctx, dealerHand=self.dealerHand, playerHand=self.playerHand)
                elif not self.blackJackCheck(dealerHand=self.dealerHand, playerHand=self.playerHand):
                    await self.game(ctx, self.dealerHand, self.playerHand)

    async def allCheck(self, ctx, bet):
        if bet >= 2**31:
            embed = discord.Embed(title="Bro, that number is WAY too big; come back to me when it's smaller.")
            await ctx.send(embed=embed)
            return True
        elif bet <= 0:
            await ctx.send(embed=discord.Embed(title=f"Don't try to bet less than 0 lol stealing money is not good."))
            return True

    async def tooMuchCheck(self, ctx, bet: int):
        players = refreshBalance()
        player = players[str(ctx.author)]
        if int(bet) > int(player.money):
            embed = discord.Embed(title=f"Bro, don't try to bet more than you have. I don't want to break ;(")
            await ctx.send(embed=embed)
            return False
        elif int(bet) <= 0:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> `A` `K`",
                            value=f"Total ==> `BLACKJACK!!!`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> `2` `2`",
                            value=f"Total ==> `4`", inline=True)
            embed.add_field(name="You won! You got a BlackJack!", value=f"You won ${bet}!",
                            inline=False)
            await ctx.send(embed=embed)
            player.money = int(player.money)
            player.money += int(bet)
            if player.money < 0:
                player.money = 0
            await saveMoney(ctx, players)
            return False

        else:
            return True

    @tasks.loop(seconds=1)
    async def timeOut(self, ctx):

        self.seconds += 1
        if self.seconds == 90:
            self.playing = ""
            players = refreshBalance()
            player = players[str(ctx.author)]
            player.money -= self.bet
            await saveMoney(ctx, players)
            embed = discord.Embed(
                title=f"{ctx.author.display_name}, your game of blackjack has timed out after 90 seconds of inactivity. Your bet has NOT been returned, because you should know better than to leave me waiting like that you asshole.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
            self.timeOut.stop()

    @commands.cooldown(1, 300, BucketType.user)
    @commands.command()
    async def search(self, ctx, place):
        players = refreshBalance()
        place = place.lower()
        newMoney = random.randint(0, 500)
        players[str(ctx.author)].money = int(players[str(ctx.author)].money)
        players[str(ctx.author)].money += newMoney
        places = {"desk": f"You searched the desk and found ${newMoney}, why would you leave this here?,",
                  "table": f"You search the table top and bottom, and found ${newMoney}, where did this come from?",
                  "book": f"You flip through the pages and ${newMoney} falls out. Lucky!",
                  "bathroom": f"There's shit in the toilet, but a crisp {newMoney} dollar bill too.",
                  "computer": f"You find ${newMoney} in bitcoin on your computer, who the fuck even uses bitcoin though smh",
                  "cup": f"There's a ${newMoney} coin sitting at the bottom of your diet coke, why would you drink diet coke tho loser"}
        if str(place).lower() in places.keys():
            await ctx.send(embed=discord.Embed(title=places[place.lower()], color=discord.Color.teal()))
        else:
            await ctx.send(embed=discord.Embed(title=f"What were you ***THINKING*** man that's not a valid option smh", color=discord.Color.red()))
        await saveMoney(ctx, players)

    @commands.command()
    async def searchplaces(self, ctx):
        embed = discord.Embed(title="Places to search are: Desk, table, book, bathroom, computer, and cup.", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=["Donate", "give", "d", "D", "G", "g", "Give", "DONATE", "GIVE"])
    async def donate(self, ctx, member: discord.Member, amount):
        players = refreshBalance()
        if int(amount) <= 0:
            await ctx.send("Bruh don't try to steal money from people lmfao")
        else:
            if int(players[str(ctx.author)].money) >= int(amount):
                players[str(member)].money += int(amount)
                players[str(ctx.author)].money -= int(amount)
            await saveMoney(ctx, players)
            embed = discord.Embed(title=f"${amount} has been given to {member.display_name} from {ctx.author.display_name}.",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)

    @commands.command(aliases=["Coinflip", "COINFLIP", "coin", "COIN", "Coin", "flip", "Flip", "FLIP"])
    async def coinflip(self, ctx, bet: int, choice):
        players = refreshBalance()
        if await self.tooMuchCheck(ctx, bet):
            choices = ["heads", "tails"]
            choice = choice.lower()
            if not await self.allCheck(ctx, bet):
                botChoice = random.choice(choices)
                if botChoice == choice:
                    embed = discord.Embed(title=f"Congrats, {ctx.author.display_name}! It was {botChoice}! You won ${bet}.", color=discord.Color.green())
                    players[str(ctx.author)].money += int(bet)
                    await ctx.send(embed=embed)
                elif botChoice != choice:
                    embed = discord.Embed(title=f"Sorry, {ctx.author.display_name} the coin came out to {botChoice}. You lose ${bet}.", color=discord.Color.red())
                    players[str(ctx.author)].money -= int(bet)
                    await ctx.send(embed=embed)
                await saveMoney(ctx, players)

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
            responses = ["It is certain.", "Without a doubt.", "It is decidedly so.", "Yes - definitely.",
                         "You may rely on it.",
                         "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                         "Reply hazy, try again.",
                         "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                         "Concentrate and ask again.",
                         "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                         "Very doubtful."]

            await ctx.send(embed=discord.Embed(title=f'''Question: {question}\nAnswer: {random.choice(responses)}'''))


    @commands.command()
    async def roll(self, ctx, number: int):
        roll = random.randint(0, number)
        if roll == 1:
            await ctx.send(f"Your roll of a d{number} was {roll}, {ctx.author.mention}! You got a critical FAIL hahaha loser")
        elif roll == int(number):
            await ctx.send(f"Your roll of a d{number} was {roll}, {ctx.author.mention}! You got a critical hit!")
        else:
            await ctx.send(f"Your roll of a d{number} was {roll}, {ctx.author.mention}!")


def setup(bot):
    bot.add_cog(BlackJackCog(bot))
