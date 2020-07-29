from discord.ext import commands
import random as rand
import time as t

bot = commands.Bot(command_prefix=".")
players = []
testplayers = {}
playerpoints = {}


class Questions(object):
    def __init__(self, question, anser, options):
        self.question = question
        self.options = options
        self.anser = anser
        self.player = "none"

    async def sendquestion(self, ctx, player):
        await battlesendquestion(ctx, self.question, self.options, player)

    async def checkanswer(self, ctx, response):
        if response == self.anser:
            await right(ctx)
        elif response != self.anser:
            await wrong(ctx)


questions = [
    Questions(question="Which king of England’s horse threw him off, and then proceeded to sit on him?", anser="B",
              options="A: Henry II\nB: George III\nC: Bill Clinton\nD: George VIII"),
    Questions(question="How long is New Zealand’s Ninety Mile Beach?", anser="D",
              options="A: 90 miles\nB: 45 miles\nC: 33 miles\nD: 58 miles"),
    Questions(question="In Maryland, it is illegal to maltreat what animal?", anser="A",
              options="A: Clams\nB: Cows\nC: Oysters\nD: Sheep\n"),
    Questions(
        question="The word golf is an acronym coming from a scotland game many years ago. What was the name of the game that it originated from?",
        anser="B",
        options="A: Golden Option Linen Flag\nB: Gentlemen Only Ladies Forbidden\nC: Glad Oysters Leak Fluid\nD: Good Olives Lock Food"),
    Questions(question="In the 1996 Webster’s Dictionary, how many entries were misspelled?", anser="A",
              options="A: 315\nB: 0\nC: 100\nD: 229"),
    Questions(question="Walt Disney was afraid of what creature?", anser="B",
              options="A: Whales\nB: Mice\nC: Dogs\nD: Cats"),
    Questions(question="Coca-Cola was originally what color?", anser="B",
              options="A: Blue\nB: Brown, it hasn’t changed\nC: Green\nD: Red"),
    Questions(question="Which is the only king in a deck of cards without a mustache?", anser="C",
              options="A: Clubs\nB: Spades\nC: Hearts\nD: Diamonds"),
    Questions(question="In what month does Russia celebrate the October/Okotber (if you're in russia) Revolution?",
              anser="C", options="A: October\nB: July\nC: November\nD: March"),
    Questions(question="Where was the battle of Bunker Hill?", anser="C",
              options="A: Mount Diablo\nB: Bunker Hill\nC: Breed’s Hill\nD: Camps Hill"),
    Questions(question="Which animal did Charles Darwin use to prove his theory of evolution?", anser="D",
              options="A: Dog\nB: Llama\nC: Beach Chicken(seagull)\nD: Finch"),
    Questions(question="What is laser an acronym for?", anser="A",
              options="A: Light Amplification by Stimulated Emissions of Radiation\nB: Lamp Appendages Seat Eminent Rams\nC: It isn’t an acronym, just a word\nD: List A Super Extreme Rap"),
    Questions(question="Banging your head against a wall burns how many calories per hour?", anser="C",
              options="A: 315\nB: 236\nC: 150\nD: 119"),
    Questions(question="What is the fear of long words?", anser="A",
              options="A: Hippopotomonstrosesquippedaliophobia\nB: Longwordaphobia\nC: There isn’t a word for it\nD: Arachibutyrophobia"),
    Questions(question="In Minnesota it is illegal to tease what animal?", anser="D",
              options="A: Pigeon\nB: Seagull\nC: Mouse\nD: Skunk"),
    Questions(question="The city of Chico, California has made a $500 fine for doing what in the city?", anser="B",
              options="A: Eat bread\nB: Set off an atomic bomb\nC: Sell pineapples\nD: Make a multi-million dollar industry")
]

bot.num = 0


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command(aliases=["Triviabattle", "TriviaBattle", "TRIVIABATTLE", "tb", "TB", "Tb"])
async def triviabattle(ctx):
    rand.shuffle(questions)
    bot.num = 0
    await ctx.send(f'''Ok, {ctx.author}, setting up your game!''')
    players.append(ctx.author)
    testplayers[ctx.author] = rand.randint(0, len(questions))
    playerpoints[ctx.author] = 0


@bot.command(aliases=["j", "Join", "J"])
async def join(ctx):
    for x in range(0, len(players)):
        if ctx.author == players[x]:
            await ctx.send(f'''You are already playing, {ctx.author}!''')
            del players[x]
    players.append(ctx.author)
    testplayers[ctx.author] = rand.randint(0, len(questions))
    playerpoints[ctx.author] = 0


@bot.command(aliases=["Startgame", "StartGame", "STARTGAME", "sg", "Sg", "SG", "sG"])
async def startgame(ctx):
    global turn
    global playerlength
    playerlength = len(players)
    if len(players) >= 1:
        await ctx.send(f'''No more entries! Game is starting in 3...''')
        t.sleep(1.5)
        await ctx.send(f'''2...''')
        t.sleep(1.5)
        await ctx.send(f'''1...''')
        t.sleep(1.5)
        await ctx.send(f'''Game as started!''')
        for x in range(0, len(players)):
            await players[x].send(f'''Here is your question, {players[x]}.''')
            for key, value in testplayers.items():
                if players[x] == testplayers[key]:
                    await questions[value].sendquestion(ctx, players[x])
        turn = players[0]
        await ctx.send(
            f'''{turn}, it is your turn to answer! Please answer in the form of ".answer_question <letter of answer>"''')


    else:
        await ctx.send(f'''Not enough players to start a game!''')


@bot.command()
async def answer_question(ctx, *, response):
    for key, value in testplayers.items():
        if key == ctx.author:
            await questions[value].checkanswer(ctx, response)


async def battlesendquestion(ctx, question, options, player):
    await player.send(question)
    await player.send(options)


async def right(ctx):
    await ctx.send(f'''Congratuations, {ctx.author}, you got it right!''')
    for key, value in playerpoints.items():
        if playerpoints[key] == playerpoints[ctx.author]:
            playerpoints[key] = value + 1
    del players[0]
    turn = players[0]
    await ctx.send(
        f'''{turn}, it is your turn to answer! PLease answer in the for om of ".answer_question <letter of answer>"''')


async def wrong(ctx):
    await ctx.send(f'''Sorry, {ctx.author}, you got it wrong.''')
    for key, value in playerpoints.items():
        if playerpoints[key] == playerpoints[ctx.author]:
            if value == 0:
                pass
            else:
                playerpoints[key] = value - 1
    del players[0]
    turn = players[0]
    await ctx.send(
        f'''{turn}, it is your turn to answer! PLease answer in the for om of ".answer_question <letter of answer>"''')


@bot.command()
async def answer(ctx, *, response):
    await questions[bot.num].checkanswer(ctx, response)


bot.run("NzE2Mzc2ODE4MDcyMDI3MTY3.XvWE1g.iYBGg2qEmkUoGHtk6hCxsFolzjk")
