# Blackjack with betting
# Created by Seth Raphael
# Created on 5/16/2020
# Import the random module
import random as rand
from discord.ext import commands

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

# Create the card class
class Card:
    # Define card and value
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


def playagain():
    again = input("Would you like to play again? Y/N >>> ")
    if again == "Y" or again == "y" or again == "Yes" or again == "yes":
        dealerhand = []
        playerhand = []
        value = 0
        deck = [ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king] * 4
        game(value)

    else:
        print("Ok. Thanks for playing at Raphael Casino!")
        exit()


def deal(carddeck):
    hand = []
    for x in range(2):
        rand.shuffle(carddeck)
        onecard = deck.pop()
        hand.append(onecard)
    return hand


def hit(hand):
    card = deck.pop()
    hand.append(card)
    return hand


def total(hand, value):
    for cards in hand:
        if cards == ace:
            if value >= 11:
                value += 1
            elif value > 21:
                value -= 11
            else:
                value += 11
        else:
            value += card.cardvalue(cards)
    return value


def returncards(dealerhand, playerhand, value):
    print("Dealers cards:  ")
    for x in range(0, len(dealerhand)):
        print(dealerhand[x])
    print("Dealers Value:  " + str(total(dealerhand, value)))
    print("\n\n")
    print("My cards:  ")
    for i in range(0, len(playerhand)):
        print(playerhand[i])
    print("Value:  " + str(total(playerhand, value)))


def blackjackcheck(dealerhand, playerhand, bet):
    if total(playerhand, value) == 21:
        returncards(dealerhand, playerhand, value)
        print("Congrats! You got blackjack!")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bet * 1.5
        themoney.write(str(money))
        themoney.close()
        playagain()
    elif total(dealerhand, value) == 21:
        returncards(dealerhand, playerhand, value)
        print("Sorry, you lost. The dealer had a blackjack.")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bet * 1.5
        themoney.write(str(money))
        themoney.close()
        playagain()


def score(dealerhand, playerhand, bet, value):
    if total(playerhand, value) == 21:
        returncards(dealerhand, playerhand, value)
        print("Congratulations! You got a Blackjack!\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bet * 1.5
        themoney.write(str(money))
        themoney.close()
    elif total(dealerhand, value) == 21:
        returncards(dealerhand, playerhand, value)
        print("Sorry, you lose. The dealer got a blackjack.\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money -= bet
        themoney.write(str(money))
        themoney.close()
    elif total(playerhand, value) > 21:
        returncards(dealerhand, playerhand, value)
        print("Sorry. You busted. You lose.\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money -= bet
        themoney.write(str(money))
        themoney.close()
    elif total(dealerhand, value) > 21:
        returncards(dealerhand, playerhand, value)
        print("Dealer busts. You win!\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bet
        themoney.write(str(money))
        themoney.close()
    elif total(playerhand, value) < total(dealerhand, value):
        returncards(dealerhand, playerhand, value)
        print("Sorry. Your score isn't higher than the dealer. You lose.\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney = open("/Users/sethraphael/money.txt", "w")
        money -= bet
        themoney.write(str(money))
        themoney.close()
    elif total(playerhand, value) > total(dealerhand, value):
        returncards(dealerhand, playerhand, value)
        print("Congratulations. Your score is higher than the dealer. You win\n")
        themoney = open("/Users/sethraphael/money.txt")
        money = themoney.read()
        money = float(money)
        themoney.close()
        themoney = open("/Users/sethraphael/money.txt", "w")
        money += bet
        themoney.write(str(money))
        themoney.close()


def getbet():
    themoney = open("/Users/sethraphael/money.txt")
    money = themoney.read()
    themoney.close()
    money = float(money)
    print("You have $" + str(money) + ".")
    bet = float(input("How much money would you like to bet? >>> "))
    if bet > money:
        print("You do not have enough money to bet $" + str(bet))
        exit()


def checkbust(playerhand, dealerhand, value):
    if total(playerhand, value) > 21:
        returncards(dealerhand, playerhand, value)
        print("You busted. You lost.")
        playagain()


def game(value):
    money = 0
    bet = 0
    getbet()
    choice = "none"
    print("Welcome to the Raphael Casino! Get ready to play some blackjack!!!\n")
    dealerhand = deal(deck)
    playerhand = deal(deck)
    while choice != "q":
        print("Dealer card: ")
        print(dealerhand[0])
        print("Your cards: ")
        for x in range(0, len(playerhand)):
            print(playerhand[x])
        print("Your value is " + str(total(playerhand, value)))
        blackjackcheck(dealerhand, playerhand, money)
        options = input("Do you want to hit, stand, surrender, double down, or quit? H/ST/SU/DD/Q >>> ").lower()
        if options == "h":
            hit(playerhand)
            checkbust(playerhand, dealerhand, value)
        elif options == "st":
            while total(dealerhand, value) < 17:
                hit(dealerhand)
            score(dealerhand, playerhand, bet, value)
            playagain()
        elif options == "su":
            themoney = open("/Users/sethraphael/money.txt", "w")
            bet /= 2
            money -= bet
            themoney.write(str(money))
            themoney.close()
            playagain()
        elif options == "dd":
            hit(playerhand)
            while total(dealerhand, value) < 17:
                hit(dealerhand)
            bet *= 2
            score(dealerhand, playerhand, bet, value)
            playagain()

        elif options == "q":
            print("Ok. Your bet has been returned and your game canceled.")


value = 0
game(value)
