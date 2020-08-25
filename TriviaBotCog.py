from discord.ext import commands
import random as rand
import json
import discord
import random


def is_me(command):
    def predicate(ctx):
        with open('/commands.json', 'r') as f:
            commandsList = json.load(f)
            return commandsList[command] == "True"

    return commands.check(predicate)


embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.mro(), discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


class TriviaCog(commands.Cog):
    def __init__(self, bot):
        self.playing = False
        self.correct = False
        self.has_answered = False
        self.num = 0
        self.bot = bot
        self.streak = 0

    @commands.command(aliases=["Trivia", "TRIVIA", "t", "T"])
    async def trivia(self, ctx):
        if not self.playing:
            self.has_answered = False
            rand.shuffle(questions)
            await questions[0].ask(ctx)
            self.playing = True
        elif self.playing:
            embed = discord.Embed(title=f"Someone is already playing a game of trivia, {ctx.author.display_name}.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

    async def sendquestion(self, ctx, question, options):
        embed = discord.Embed(title=question, description=options, color=random.choice(embedColors))
        await ctx.send(embed=embed)

    async def right(self, ctx):
        self.playing = False
        self.correct = True
        if not self.has_answered:
            embed = discord.Embed(title=f"Congratulations, {ctx.author.display_name}, you got it right!",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.playing = False
        elif self.has_answered:
            embed = discord.Embed(
                title=f"You have already answered this question, {ctx.author.display_name}. Don't try and cheat my system",
                color=random.choice(embedColors))
            await ctx.send(embed=embed)
            self.playing = False

    async def wrong(self, ctx):
        self.playing = False
        self.correct = False
        if not self.has_answered:
            embed = discord.Embed(title=f"Nope, you got that wrong {ctx.author.display_name}. HAHA ur so dumb lol",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            self.playing = False
        elif self.has_answered:
            embed = discord.Embed(
                title=f"You have already answered this question, {ctx.author.display_name}. Don't try and cheat my system.",
                color=random.choice(embedColors))
            await ctx.send(embed=embed)
            self.playing = False

    @commands.command()
    async def answer(self, ctx, *, response):
        response = response.upper()
        if self.playing:
            await questions[0].checkanswer(ctx, response)
            self.playing = False
        elif not self.playing:
            embed = discord.Embed(title=f"No one is playing a trivia game right now, {ctx.author.display_name}.",
                                  color=random.choice(embedColors))
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''Error!''')


triviaCog = TriviaCog(commands.Cog)


class Questions(object):
    def __init__(self, question, anser, options):
        self.question = question
        self.options = options
        self.anser = anser

    async def ask(self, ctx):
        await triviaCog.sendquestion(ctx, self.question, self.options)

    async def checkanswer(self, ctx, response):
        if response == self.anser:
            await triviaCog.right(ctx)
        elif response != self.anser:
            await triviaCog.wrong(ctx)


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


def setup(bot):
    bot.add_cog(TriviaCog(bot))
