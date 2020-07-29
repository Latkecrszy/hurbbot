# Blackjack with betting
# Created by Seth Raphael
# Created on 5/16/2020
# Import the random module
import random as rand
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

# Create the card images
ace = '''--------------------
|        /\        |
|       /  \       |
|      /    \      |
|     /------\     |
|    /        \    |
|   /          \   |
|                  |
|                  |
--------------------\n'''
two = '''--------------------
|                  |
|                  |
|                  |
|        2         |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
three = '''--------------------
|                  |
|                  |
|                  |
|         3        |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
four = '''--------------------
|       /  |       |
|      /   |       |
|     /    |       |
|    /     |       |
|   -------|       |
|          |       |
|          |       |
|                  |
--------------------\n'''
five = '''--------------------
|                  |
|                  |
|                  |
|         5        |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
six = '''--------------------
|                  |
|                  |
|                  |
|        6         |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
seven = '''--------------------
|    ---------     |
|            /     |
|           /      |
|          /       |
|         /        |
|        /         |
|       /          |
|                  |
--------------------\n'''
eight = '''--------------------
|                  |
|                  |
|                  |
|        8         |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
nine = '''--------------------
|                  |
|                  |
|                  |
|        9         |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
ten = '''--------------------
|                  |
|                  |
|                  |
|       10         |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
jack = '''--------------------
|                  |
|                  |
|                  |
|        J         |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
queen = '''--------------------
|                  |
|                  |
|                  |
|        Q         |
|                  |
|                  |
|                  |
|                  |
--------------------\n'''
king = '''--------------------
|      |   /       |
|      |  /        |
|      | /         |
|      |/          |
|      |\          |
|      | \         |
|      |  \        |
|      |   \       |
--------------------\n'''

# Initialize the bet variable
bot.dealerhand = []
bot.playerhand = []
bot.value = 0
bot.bet = 0

# Create the card class

class Card:
    # async define card and value
    def __init__(self, card="none", value=0):
        self.card = card
        self.value = value

    # Create the cardvalue function
    def cardvalue(self, card):
        if self.card == ace:
            self.value = 1
        elif card == two:
            self.value = 2
        elif card == three:
            self.value = 3
        elif card == four:
            self.value = 4
        elif card == five:
            self.value = 5
        elif card == six:
            self.value = 6
        elif card == seven:
            self.value = 7
        elif card == eight:
            self.value = 8
        elif card == nine:
            self.value = 9
        elif card == ten:
            self.value = 10
        elif card == jack:
            self.value = 10
        elif card == queen:
            self.value = 10
        elif card == king:
            self.value = 10
        return self.value

    # Create the cardname function
    def cardname(self, card):
        if card == ace:
            self.card = "ace"
        elif card == two:
            self.card = "two"
        elif card == three:
            self.card = "three"
        elif card == four:
            self.card = "four"
        elif card == five:
            self.card = "five"
        elif card == six:
            self.card = "six"
        elif card == seven:
            self.card = "seven"
        elif card == eight:
            self.card = "eight"
        elif card == nine:
            self.card = "nine"
        elif card == ten:
            self.card = "ten"
        elif card == jack:
            self.card = "jack"
        elif card == queen:
            self.card = "queen"
        elif card == king:
            self.card = "king"
        return self.card


deck = [ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king] * 4

card = Card()


@bot.command()
async def rebet(ctx):
    bot.dealerhand = []
    bot.playerhand = []
    bot.value = 0
    bot.bet = 0
    deck = [ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king] * 4
    await game(ctx)


def deal(carddeck):
    hand = []
    for x in range(2):
        rand.shuffle(carddeck)
        onecard = deck.pop()
        hand.append(onecard)
    return hand


async def hithand(hand):
    card = deck.pop()
    hand.append(card)
    return hand


def total(hand):
    for cards in hand:
        if cards == ace:
            if bot.value >= 11:
                bot.value += 1
            elif bot.value > 21:
                bot.value -= 11
            else:
                bot.value += 11
        else:
            bot.value += card.cardvalue(cards)
    return bot.value


async def returncards(ctx):
    await ctx.send("Dealers cards:  ")
    for x in range(0, len(bot.dealerhand)):
        await ctx.send(bot.dealerhand[x])
    for counter in range(0, len(bot.dealerhand)):
        await ctx.send(card.cardname(bot.dealerhand[counter]))
    await ctx.send("Dealers Value:  " + str(total(bot.dealerhand)))
    await ctx.send("My cards:  ")
    for i in range(0, len(bot.playerhand)):
        await ctx.send(bot.playerhand[i])
    for count in range(0, len(bot.playerhand)):
        await ctx.send(card.cardname(bot.playerhand[count]))
    await ctx.send("Value:  " + str(total(bot.playerhand)))


async def blackjackcheck(ctx):
    if total(bot.playerhand) == 21 and total(bot.dealerhand) == 21:
        await returncards(ctx)
        await ctx.send("You got a blackjack, but so did the dealer. You tied.")
    if total(bot.playerhand) == 21:
        await returncards(ctx)
        await ctx.send("Congrats! You got blackjack!")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bot.bet * 1.5
        themoney.write(str(money))
        themoney.close()
    elif total(bot.dealerhand) == 21:
        await returncards(ctx)
        await ctx.send("Sorry, you lost. The dealer had a blackjack.")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bot.bet * 1.5
        themoney.write(str(money))
        themoney.close()


async def score(ctx):
    if total(bot.playerhand) == 21:
        await returncards(ctx)
        await ctx.send("Congratulations! You got a Blackjack!\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bot.bet * 1.5
        themoney.write(str(money))
        themoney.close()
    elif total(bot.dealerhand) == 21:
        await returncards(ctx)
        await ctx.send("Sorry, you lose. The dealer got a blackjack.\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money -= bot.bet
        themoney.write(str(money))
        themoney.close()
    elif total(bot.playerhand) > 21:
        await returncards(ctx)
        await ctx.send("Sorry. You busted. You lose.\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money -= bot.bet
        themoney.write(str(money))
        themoney.close()
    elif total(bot.dealerhand) > 21:
        await returncards(ctx)
        await ctx.send("Dealer busts. You win!\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bot.bet
        themoney.write(str(money))
        themoney.close()
    elif total(bot.playerhand) < total(bot.dealerhand):
        await returncards(ctx)
        await ctx.send("Sorry. Your score isn't higher than the dealer. You lose.\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money -= bot.bet
        themoney.write(str(money))
        themoney.close()
    elif total(bot.playerhand) > total(bot.dealerhand):
        await returncards(ctx)
        ctx.send("Congratulations. Your score is higher than the dealer. You win\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney.close()
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bot.bet
        themoney.write(str(money))
        themoney.close()


async def checkbust(ctx):
    if total(bot.playerhand) > 21:
        await returncards(ctx)
        await ctx.send("You busted. You lost.")


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command(aliases=["Hit", "HIT", "H", "h"])
async def hit(ctx):
    await hithand(bot.playerhand)
    await returncards(ctx)
    await checkbust(ctx)
    await game(ctx)


@bot.command(aliases=["stay", "Stay", "Stand", "STAY", "STAND", "st", "St", "ST"])
async def stand(ctx):
    while total(bot.dealerhand) < 17:
        await hithand(bot.dealerhand)
    await score(ctx)


@bot.command(aliases=["Surrender", "SURRENDER"])
async def surrender(ctx):
    themoney = open("/Users/sethraphael/money.txt", "w")
    bot.bet /= 2
    money = themoney.read()
    money -= float(bot.bet)
    themoney.write(str(money))
    themoney.close()
    await returncards(ctx)


@bot.command(aliases=["Doubledown", "dd", "DD", "Dd", "DoubleDown", "DOUBLEDOWN"])
async def doubledown(ctx):
    await hithand(bot.playerhand)
    while total(bot.dealerhand) < 17:
        await hithand(bot.dealerhand)
    bot.bet *= 2
    await score(ctx)


async def game(ctx):
    await ctx.send("Dealer card: ")
    await ctx.send(bot.dealerhand[0])
    await ctx.send("Your cards: ")
    for x in range(0, len(bot.playerhand)):
        await ctx.send(bot.playerhand[x])
    await ctx.send("Your value is " + str(total(bot.playerhand)))
    await blackjackcheck(ctx)
    await ctx.send("Do you want to hit, stand, surrender, double down, or quit?")


@bot.command(aliases=["bj", "BJ", "Bj", "Blackjack", "BLACKJACK", "BlackJack"])
async def blackjack(ctx, bet):
    bot.value = 0
    bot.bet = int(bet)
    bot.playerhand = deal(deck)
    bot.dealerhand = deal(deck)
    await ctx.send("Welcome to the Raphael Casino! Get ready to play some blackjack!!!\n")
    await game(ctx)

bot.run("NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.B5eSdENH1GLRT7CkMLACTw7KpGE")
