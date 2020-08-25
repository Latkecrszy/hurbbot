import discord
import discord.ext
from discord.ext import commands, tasks
import random
import time
import asyncio

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]

print("Loading...")
iogames = {"diep": "Diep.io Link: https://diep.io/",
           "flyordie": "Fly or Die.io Link: https://flyordie.io/",
           "bonk": "Bonk.io Link: https://bonk.io/",
           "curve": "CurveFever.io Link: https://curvefever.pro/",
           "agar": "Agar.io Link: https://agar.io/",
           "wings": "Wings.io Link: https://wings.io/",
           "gats": "Gats.io Link: https://gats.io/",
           "starve": "Gats.io Link: https://gats.io/",
           "doom": "Doomed.io Link: https://doomed2.io/",
           "zombs": "Zombs.io Link: https://zombs.io/",
           "sword": "Swordz.io Link: https://swordz.io/",
           "krunker": "Krunker.io Link: https://krunker.io/",
           "drednot": "Drednot.io Link: https://drednot.io/",
           "zlap": "Zlap.io Link: https://zlap.io/",
           "slither": "Slither.io Link: https://slither.io/",
           "devast": "Devast.io Link: https://devast.io/",
           "creatur": "Creatur.io Link: https://creatur.io/",
           "hole": "Hole.io Link: https://hole.io/",
           "diepio": "Diep.io Link: https://diep.io/",
           "flyordieio": "Fly or Die.io Link: https://flyordie.io/",
           "bonkio": "Bonk.io Link: https://bonk.io/",
           "curveio": "CurveFever.io Link: https://curvefever.pro/",
           "agario": "Agar.io Link: https://agar.io/",
           "wingsio": "Wings.io Link: https://wings.io/",
           "gatsio": "Gats.io Link: https://gats.io/",
           "starveio": "Gats.io Link: https://gats.io/",
           "doomio": "Doomed.io Link: https://doomed2.io/",
           "zombsio": "Zombs.io Link: https://zombs.io/",
           "swordio": "Swordz.io Link: https://swordz.io/",
           "krunkerio": "Krunker.io Link: https://krunker.io/",
           "drednotio": "Drednot.io Link: https://drednot.io/",
           "zlapio": "Zlap.io Link: https://zlap.io/",
           "slitherio": "Slither.io Link: https://slither.io/",
           "devastio": "Devast.io Link: https://devast.io/",
           "creaturio": "Creatur.io Link: https://creatur.io/",
           "holeio": "Hole.io Link: https://hole.io/",
           "diep.io": "Diep.io Link: https://diep.io/",
           "flyordie.io": "Fly or Die.io Link: https://flyordie.io/",
           "bonk.io": "Bonk.io Link: https://bonk.io/",
           "curve.io": "CurveFever.io Link: https://curvefever.pro/",
           "agar.io": "Agar.io Link: https://agar.io/",
           "wings.io": "Wings.io Link: https://wings.io/",
           "gats.io": "Gats.io Link: https://gats.io/",
           "starve.io": "Gats.io Link: https://gats.io/",
           "doom.io": "Doomed.io Link: https://doomed2.io/",
           "zombs.io": "Zombs.io Link: https://zombs.io/",
           "sword.io": "Swordz.io Link: https://swordz.io/",
           "krunker.io": "Krunker.io Link: https://krunker.io/",
           "drednot.io": "Drednot.io Link: https://drednot.io/",
           "zlap.io": "Zlap.io Link: https://zlap.io/",
           "slither.io": "Slither.io Link: https://slither.io/",
           "devast.io": "Devast.io Link: https://devast.io/",
           "creatur.io": "Creatur.io Link: https://creatur.io/",
           "hole.io": "Hole.io Link: https://hole.io/"
           }


class Questions(object):
    def __init__(self, question, anser, options):
        self.question = question
        self.options = options
        self.anser = anser

    async def ask(self, message):
        await sendquestion(message, self.question, self.options)

    async def checkqotdanswer(self, ctx, response, author):
        if response == self.anser:
            qotdWinners = open("/Users/sethraphael/PycharmProject/Bots/qotd winners", "a")
            qotdWinners.write(f"{author}\n")
            qotdWinners.close()
        await ctx.send(
            f"Thank you for submitting your answer, {author}! Check back next time to see if you got it correct!")


async def sendquestion(message, question, options):
    with open("/Users/sethraphael/PycharmProject/Bots/qotd winners", "r") as f:
        people = f.readlines()
        f.close()
    correct = ", ".join(open("/Users/sethraphael/PycharmProject/Bots/qotd winners").readlines())
    correct.replace("\n", " ")
    with open("/Users/sethraphael/PycharmProject/Bots/qotd winners", "w") as f:
        f.write("")
        f.close()
    bot.quesnum += 1
    correctpeeps = 0
    for x in people:
        correctpeeps += 1
    correctpeeps -= 1
    await message.channel.send("Hey <@&632939598166622208>, guess what?")
    embed = discord.Embed(title=f"A whole {correctpeeps} people got this question right!",
                          description=f"Good job to {correct}! They are the ones that got it right! Next question: ",
                          color=random.choice(embedColors))
    embed.add_field(name=question, value=options)
    questionSent = await message.channel.send(embed=embed)
    await questionSent.add_reaction('🇦')
    await questionSent.add_reaction('🇧')
    await questionSent.add_reaction('🇨')
    await questionSent.add_reaction('🇩')
    await asyncio.sleep(10)
    await questions[bot.quesnum].ask(message)



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
              options="A: Blue\nB: Brown, it hasn't changed\nC: Green\nD: Red"),
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
              options="A: Eat bread\nB: Set off an atomic bomb\nC: Sell pineapples\nD: Make a multi-million dollar industry"),
    Questions(question="What food was served as a medicinal product in the 1800s?", anser="B",
              options="A: Chicken\nB: Tomato Sauce\nC: Plantain\nD: Apple Juice"),
    Questions(question="How many pleats (folds) does a chef's hat have?", anser="C",
              options="A: 238\nB: 138\nC: 100\nD: 120"),
    Questions(question="Which fruit is not a natural fruit, but a hybrid of two others?", anser="B",
              options="A: Apple\nB: Orange\nC: Grapefruit\nD: Grape"),
    Questions(question="In 1922, stop signs were what color?", anser="C",
              options="A: Red\nB: Orange\nC: Yellow\nD: Green"),
    Questions(question="What is the hottest temperature ever recorded on Earth?", anser="A",
              options="A: 3.6 Billion Degrees Fahrenheit\nB: 1.5 Billion Degrees Fahrenheit\nC: 820.4 Million Degrees Fahrenheit\nD: 920.8 Million Degrees Fahrenheit"),
    Questions(question="Which famous political figure is actually a trained mechanic?", anser="B",
              options="A: Barack Obama\nB: Queen Elizabeth II\nC: Queen Elizabeth III\nD: Donald Trump"),
    Questions(question="How many full mouth licks does it take to get to the center of a Tootsie Pop?", anser="D",
              options="A: 278\nB: 735\nC: 389\nD: 364"),
    Questions(question="In french, the word dandelion means what?", anser="A",
              options="A: pissenlit, meaning 'wet the bed'\nB: pisluen, meaning 'pee a lot'\nC: luenpis, meaning 'lots of pee'\nD: litpissen, meaning 'bed wetter'"),
    Questions(question="What is the name of the blob of toothpaste on your toothbrush?", anser="D",
              options="A: globlet\nB: Globet\nC: nuget (no, not nugget, nuget)\nD: nurdle"),
    Questions(question="What was the dying wish of the creator of this game or puzzle?", anser="C",
              options="A: The creator of basketball had his remains put inside of one\nB: The creator of football had his remains put inside of one\nC: The creator of frisbee golf had his remains turned into a frisbee\nD: The creator of the Rubik's Cube had his ashes placed in the corner of a cube"),
    Questions(question="Which food makes an excellent water filter?", anser="C",
              options="A: Orange peel\nB: Potato skin\nC: Banana peel\nD: Pancakes"),
    Questions(question="What is the name of the dot over a lowercase i?", anser="B",
              options="A: ribble\nB: tittle\nC: mipple\nD: It doesn't have a name. Let this one thing remain sacred!"),
    Questions(question="What is Cookie Monster's real name?", anser="D",
              options="A: Dave\nB: Jer\nC: Cookie Monster\nD: Sid"),
    Questions(question="What... interesting line was read on BBC in 1930?", anser="A",
              options="A: There is no news\nB: All of our reporters are absent today\nC: There is currently a chicken loose in our studio\nD: I am extremely hungry"),
    Questions(question="Which creature has it's bladder in its head?", anser="D",
              options="A: Caterpillar\nB: Slug\nC: Crab\nD: Lobster"),
    Questions(question="What was the first potato chip flavor?", anser="C",
              options="A: Barbecue\nB: Cool Ranch\nC: Cheese and Onion\nD: Potato Flavor"),
    Questions(question="What was the one part of his body that Charlie Chaplin insured?", anser="A",
              options="A: His feet\nB: His liver\nC: His bladder\nD: His penis"),
    Questions(question="What character speaks first in all of Star Wars?", anser="A",
              options="A: C-3PO\nB: R2D2\nC: Yoda\nD: Obi-Wan Kanobi"),
    Questions(question="What is it illegal to do in French vineyards?", anser="B",
              options="A: Set off an atomic bomb\nB: Land a flying saucer\nC: Eat Baguettes\nD: Laugh"),
    Questions(question="According to Russian law, what must a homeless person be doing after 10:00 PM?", anser="C",
              options="A: Wearing clothes\nB: Staring at a wall\nC: Be at home\nD: Be talking with other homeless people"),
    Questions(question="What is the crossbreed between a donkey and a zebra known as?", anser="A",
              options="A: Zonkey\nB: Debra\nC: Zenkey\nD: Dobra"),
    Questions(question="What color is the 'black box' on an airplane?", anser="B",
              options="A: Red\nB: Orange\nC: Green\nD: Black"),
    Questions(question="How many noses does a slug have?", anser="D", options="A: One\nB: Two\nC: Three\nD: Four"),
    Questions(question="What the hell is a haboob?", anser="B",
              options="A: A bird\nnB: A sandstorm\nC: A tropical storm\nD: A Dinosaur"),
    Questions(question="What were clocks missing before 1577?", anser="B",
              options="A: Hour hands\nB: Minute hands\nC: Second hands\nD: Numbers"),
    Questions(question="What is the main ingredient of Bombay Duck?", anser="C",
              options="A: Fish\nB: Duck\nC: Dog\nD: Rabbit"),
    Questions(question="What is the official name for the hashtag symbol?", anser="D",
              options="A: Hashtag\nB: Sextacross\nC: Sextrathrope\nD: Octothrope"),
    Questions(question="What is the national animal of Scotland?", anser="C",
              options="A: Dragon\nB: Hydra\nC: Unicorn\nD: Centaur"),
    Questions(question="What is the speed of a computer mouse measured in?", anser="B",
              options="A: Traps\nB: Mickeys\nC: Cat\nD: Minnies"),
    Questions(question="What is the fear of the number 13?", anser="C",
              options="A: Tripadepaphobia\nB: Trecadecaphobia\nC: Triskaidekaphobia\nD: Tripledeckerphobia"),
    Questions(question="What is the worst color to wear to a job interview?", anser="B",
              options="A: Red\nB: Orange\nC: Yellow\nD: Green"),
    Questions(question="Which of these fruits is actually a berry?", anser="D",
              options="A: Cherry\nB: Cucumber\nC: Tomato\nD: Banana"),
    Questions(question="Which of these 'berries' is not actually a berry?", anser="C",
              options="A: Raspberry\nB: Blueberry\nC: Strawberry\nD: Cranberry"),
    Questions(question="What is the only domestic animal not mentioned in the Bible?", anser="A",
              options="A: Cat\nB: Dog\nC: Goat\nD: Mouse")]


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command()
async def link(ctx, game):
    found = False
    if game.lower() == "random":
        choice = random.choice(iogames)
        await ctx.send(choice)
    elif game.lower() == "explore":
        await ctx.send("Click here to explore .io games on your own! https://iogames.space/make")
    elif game.lower() != "random":
        for key, value in iogames.items():
            if game.lower() == key:
                await ctx.send(value)
                found = True
        if not found:
            await ctx.send(f"I could not find that game, {ctx.author.mention}.")


@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if member in list(ctx.guild.members) and reason is not None:
        await member.send(f"You have been warned in server {ctx.guild} by {ctx.author} for {reason}")
        embed = discord.Embed(
            title=f"<:check:742198670912651316>  Success! {member.display_name} has been warned for {reason}",
            description=None, colour=discord.Colour.green())
    elif member in list(ctx.guild.members) and reason is None:
        embed = discord.Embed(
            title=f"<:x_:742198871085678642>  Why would you warn someone for no reason {ctx.author.display_name}? \U0001f914",
            description=None, color=discord.Color.red())
    else:
        embed = discord.Embed(
            title=f"<:x_:742198871085678642> I couldn't find that member {ctx.author.display_name} \U0001f914",
            description=None, color=discord.Color.red())
    await ctx.send(embed=embed)


@bot.command(aliases=["help", "Help", "HELP"])
async def hel(ctx):
    await ctx.send(f'''Here are the commands for this bot:
`$link <game>` ==> gives you a link to a .io game of your choosing.
`$link explore` ==> gives you a link to explore .io games yourself.''')


bot.quesnum = 0
bot.num = 0


@bot.command()
async def questionofday(message):
    await questions[bot.quesnum].ask(message)


@bot.event
async def on_reaction_add(reaction, user):
    if user.id != 736283988628602960:
        reactions = ['🇦', '🇧', '🇨', '🇩']
        if questions[bot.quesnum].anser == "A" and str(reaction) == reactions[0] or questions[
            bot.quesnum].anser == "B" and str(reaction) == reactions[1] or questions[bot.quesnum].anser == "C" and str(reaction) == \
                reactions[2] or questions[bot.quesnum].anser == "D" and str(reaction) == reactions[3]:
            with open("/Users/sethraphael/PycharmProject/Bots/qotd winners", "a") as f:
                f.write(f"{user.display_name}\n")
                f.close()


bot.run("NzQxNDM4OTY4MTQ2NTU4OTk2.Xy3k2Q.v4_ypb4X5W5jORNi9fP3N5S29wM")
