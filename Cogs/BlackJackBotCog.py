import discord
from discord.ext import commands, tasks
import asyncio
from Bots.Cogs.players import refreshBalance, saveMoney
from discord.ext.commands.cooldowns import BucketType
import random


class BlackJackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 16
        self.suits = [":clubs:", ":hearts:", ":diamonds:", ":spades:"]
        self.deck = {}
        for card in self.cards:
            for suit in self.suits:
                self.deck[card] = suit
        self.info = {}  # {"player_id": {"player_hand": [card1, card2], "dealer_hand": [card1, card2], "bet": bet}

    def deal(self, id, person):
        if person == "player":
            self.info[str(id)]["player_hand"] = [random.choice(self.cards), random.choice(self.cards)]
            return self.info[str(id)]["player_hand"]
        elif person == "dealer":
            self.info[str(id)]["dealer_hand"] = [random.choice(self.cards), random.choice(self.cards)]
            return self.info[str(id)]["dealer_hand"]

    def hitHand(self, id, person):
        if person == "player":
            self.info[str(id)]["player_hand"].append(random.choice(self.cards))
            return self.info[str(id)]["player_hand"]
        elif person == "dealer":
            self.info[str(id)]["dealer_hand"].append(random.choice(self.cards))
            return self.info[str(id)]["dealer_hand"]

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

    async def blackJackCheck(self, ctx):
        if self.total(self.info[str(ctx.author.id)]["player_hand"]) == 21 or self.total(self.info[str(ctx.author.id)]["dealer_hand"]) == 21:
            playerDisplayHand = ""
            playerHand = self.info[str(ctx.author.id)]["player_hand"]
            dealerHand = self.info[str(ctx.author.id)]["dealer_hand"]
            for i in playerHand:
                playerDisplayHand += f"`{i}` "
            dealerDisplayHand = ""
            for i in dealerHand:
                dealerDisplayHand += f"`{i}` "
            playerTotal = self.total(playerHand)
            dealerTotal = self.total(dealerHand)
            if self.total(playerHand) == 21:
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
                    self.info.pop(str(ctx.author.id))

                elif self.total(dealerHand) != 21:
                    embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.green())
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                                    value=f"Total ==> `{playerTotal}`", inline=True)
                    embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                                    value=f"Total ==> `{dealerTotal}`", inline=True)
                    if len(self.info[str(ctx.author.id)]["player_hand"]) == 2:
                        embed.add_field(name="You won! You got a blackjack!", value=f"You won ${int(self.info[str(ctx.author.id)]['bet'])*1.5}!",
                                        inline=False)
                        await ctx.send(embed=embed)
                        players = refreshBalance()
                        player = players[str(ctx.author.id)]
                        player.money += self.info[str(ctx.author.id)]['bet']*1.5
                        self.info.pop(str(ctx.author.id))
                    else:
                        embed.add_field(name="You won! You reached 21 before the dealer!",
                                        value=f"You won ${int(self.info[str(ctx.author.id)]['bet'])}!",
                                        inline=False)
                        await ctx.send(embed=embed)
                        players = refreshBalance()
                        player = players[str(ctx.author.id)]
                        player.money += self.info[str(ctx.author.id)]['bet']
                        self.info.pop(str(ctx.author.id))
                    await saveMoney(ctx, players)
                return True

            elif self.total(dealerHand) == 21:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.red())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                                value=f"Total ==> `{playerTotal}`", inline=True)
                embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                                value=f"Total ==> `{dealerTotal}`", inline=True)
                embed.add_field(name="The dealer reached 21 before you did. You lost.", value=f"You lost ${self.info[str(ctx.author.id)]['bet']}.",
                                inline=False)
                await ctx.send(embed=embed)
                players = refreshBalance()
                player = players[str(ctx.author.id)]
                player.money -= self.info[str(ctx.author.id)]['bet']
                await saveMoney(ctx, players)
                self.info.pop(str(ctx.author.id))
                return True

        else:
            return False

    async def checkBust(self, ctx):
        playerHand = self.info[str(ctx.author.id)]["player_hand"]
        dealerHand = self.info[str(ctx.author.id)]["dealer_hand"]
        if self.total(playerHand) > 21 or self.total(dealerHand) > 21:
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
                embed.add_field(name="You busted! You lost.", value=f"You lost ${self.info[str(ctx.author.id)]['bet']}.", inline=False)
                players = refreshBalance()
                player = players[str(ctx.author.id)]
                player.money -= int(self.info[str(ctx.author.id)]["bet"])
                await saveMoney(ctx, players)
                await ctx.send(embed=embed)
                self.info.pop(str(ctx.author.id))
                return True

            elif self.total(dealerHand) > 21:
                embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.green())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                                value=f"Total ==> `{playerTotal}`", inline=True)
                embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                                value=f"Total ==> `{dealerTotal}`", inline=True)
                embed.add_field(name="The dealer busted! You won!", value=f"You won ${self.info[str(ctx.author.id)]['bet']}.", inline=False)

                players = refreshBalance()
                player = players[str(ctx.author.id)]
                player.money += self.info[str(ctx.author.id)]['bet']
                await saveMoney(ctx, players)
                await ctx.send(embed=embed)
                self.info.pop(str(ctx.author.id))
                return True

        else:
            return False

    @commands.command(aliases=["HIT", "Hit", "h", "H"])
    async def hit(self, ctx):
        if str(ctx.author.id) in self.info.keys():
            self.hitHand(ctx.author.id, "player")
            if not await self.blackJackCheck(ctx):
                if not await self.checkBust(ctx):
                    await self.game(ctx)
        else:
            embed = discord.Embed(title=f"You are not playing a game of blackjack, {ctx.author.display_name}!", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=["STAND", "Stand", "s", "S"])
    async def stand(self, ctx):
        if str(ctx.author.id) in self.info.keys():
            while self.total(self.info[str(ctx.author.id)]["dealer_hand"]) < 17:
                self.hitHand(str(ctx.author.id), "dealer")
            if not await self.checkBust(ctx):
                await self.score(ctx)
        else:
            embed = discord.Embed(title=f"You are not playing a game of blackjack, {ctx.author.display_name}!", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=["dd", "Doubledown", "DoubleDown", "DD", "Dd", "DOUBLEDOWN"])
    async def doubledown(self, ctx):
        if str(ctx.author.id) in self.info.keys():
            players = refreshBalance()
            player = players[str(ctx.author.id)]
            if int(self.info[str(ctx.author.id)]['bet'])*2 > int(player.money):
                await ctx.send(embed=discord.Embed(description=f"You do not have enough money to double down {ctx.author.mention}!",
                                                   color=discord.Color.red()))
            else:
                self.hitHand(ctx.author.id, "player")
                self.info[str(ctx.author.id)]['bet'] = int(self.info[str(ctx.author.id)]['bet'])
                self.info[str(ctx.author.id)]['bet'] *= 2
                while self.total(self.info[str(ctx.author.id)]["dealer_hand"]) < 17:
                    self.hitHand(ctx.author.id, "dealer")
                if not await self.checkBust(ctx):
                    await self.score(ctx)
        else:
            embed = discord.Embed(title=f"You are not playing a game of blackjack, {ctx.author.display_name}!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

    async def score(self, ctx):
        playerHand = self.info[str(ctx.author.id)]["player_hand"]
        dealerHand = self.info[str(ctx.author.id)]["dealer_hand"]
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
            embed.add_field(name="The dealer got a higher value than you. You lost.", value=f"You lost ${self.info[str(ctx.author.id)]['bet']}.",
                            inline=False)
            players = refreshBalance()
            player = players[str(ctx.author.id)]
            player.money -= self.info[str(ctx.author.id)]['bet']
            await saveMoney(ctx, players)
            self.info.pop(str(ctx.author.id))
            await ctx.send(embed=embed)
        elif playerScore > dealerScore:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game:", color=discord.Color.green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"**{ctx.author.display_name}**:\nCards ==> {playerDisplayHand}",
                            value=f"Total ==> `{playerTotal}`", inline=True)
            embed.add_field(name=f"**Hurb**:\nCards ==> {dealerDisplayHand}",
                            value=f"Total ==> `{dealerTotal}`", inline=True)
            embed.add_field(name="You won! Your score was higher than the dealer's!", value=f"You won ${self.info[str(ctx.author.id)]['bet']}!",
                            inline=False)
            players = refreshBalance()
            player = players[str(ctx.author.id)]
            player.money += self.info[str(ctx.author.id)]['bet']
            await saveMoney(ctx, players)
            self.info.pop(str(ctx.author.id))
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
            self.info.pop(str(ctx.author.id))
            await ctx.send(embed=embed)



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



    async def game(self, ctx):
        playerHand = self.info[str(ctx.author.id)]["player_hand"]
        dealerHand = self.info[str(ctx.author.id)]["dealer_hand"]
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
        embed.set_footer(text=f"Your options are: %hit, %stand, or %doubledown.")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(aliases=["bj", "BJ", "Blackjack", "BLACKJACK", "BlackJack", "blackJack"])
    async def blackjack(self, ctx, bet):
        if await self.tooMuchCheck(ctx, bet):
            if str(ctx.author.id) in self.info.keys():
                embed = discord.Embed(
                    title=f"You are already playing a game of blackjack, {ctx.author.display_name}! Please don't break me :(",
                    color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                self.info[str(ctx.author.id)] = {"player_hand": [], "dealer_hand": [], "bet": int(bet)}
                self.deal(ctx.author.id, "player")
                self.deal(ctx.author.id, "dealer")

                if not await self.blackJackCheck(ctx):
                    await self.game(ctx)

    async def allCheck(self, ctx, bet):
        if bet >= 2**31:
            embed = discord.Embed(title="The bot can't handle numbers that large. Can you try a smaller number?")
            await ctx.send(embed=embed)
            return True
        elif bet <= 0:
            await ctx.send(embed=discord.Embed(title=f"You can't bet negative. Please try a positive value"))
            return True

    async def tooMuchCheck(self, ctx, bet: int):
        players = refreshBalance()
        player = players[str(ctx.author.id)]
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

    @commands.command()
    async def gimmemoney(self, ctx):
        if ctx.author.id == 592503405122027520:
            players = refreshBalance()
            players[str(ctx.author.id)].money += 10000
            await saveMoney(ctx, players)
            await ctx.send("I gotchu bro, here's $10k \U0001f44d")



def setup(bot):
    bot.add_cog(BlackJackCog(bot))

