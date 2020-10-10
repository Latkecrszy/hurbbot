from discord.ext import commands, tasks
import random as rand
import webbrowser
import json
import time

qotdWinners = open("/Users/sethraphael/PycharmProject/Bots/qotd winners")
winners = qotdWinners.readlines()
qotdWinners.close()
storage = '/Users/sethraphael/accounts.txt'
streak = '/Users/sethraphael/streak.txt'
bot = commands.Bot(command_prefix="$")
bot.validusers = [line.rstrip('\n') for line in open("/Users/sethraphael/validusers.txt")]
print(bot.validusers)
players = {}
triviabattlepoints = {}
bot.playing = False
bot.rightquestions = 0
bot.isreplaced = False
bot.lightninground = False
bot.guess = 0
bot.streak_found = False
bot.triviabattle = False
bot.num = 0
bot.has_answered = False
bot.correct = False
bot.prevstreak = 0
bot.firstround = False
bot.secondround = False
bot.thirdround = False
bot.fourthround = False
bot.fifthround = False
bot.second = 60
bot.joined = 0
bot.playersgone = 0
howmany = 0
how_many = 0
extra_lives = {}


def getprefix(_bot, message):
    with open('/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/welcome.json',
              'r') as f:
        prefixes = json.load(f)

        return prefixes[str(message.guild.id)]


def read_text(storage_space):
    new_account_file = open(storage_space)
    my_account = new_account_file.readlines()
    return my_account


for x in range(len(read_text(str(storage)))):
    how_many = how_many + 1
if how_many == 0:
    friends = 0
else:
    friends = int(how_many) / 2

if how_many == 1:
    bot.accounts = {}
else:
    bot.accounts = {}
    for x in range(0, int(how_many)):
        read_text(storage)[x] = read_text(storage)[x].replace("\n", "")
        if read_text(storage)[x] == "\n" or read_text(storage)[x] == "" or read_text(storage)[x] == " ":
            continue
        oneContacts = read_text(storage)[x].split(",")
        oneContacts[0].replace("\n", "")
        oneContacts[1].replace("\n", "")
        bot.accounts[oneContacts[0]] = oneContacts[1]

for x in range(len(read_text(str(streak)))):
    howmany = howmany + 1
if howmany == 0:
    friends = 0
else:
    friends = int(howmany) / 2

if howmany == 1:
    bot.streak = {}
else:
    bot.streak = {}
    for x in range(0, int(howmany)):
        read_text(streak)[x] = read_text(streak)[x].replace("\n", "")
        if read_text(streak)[x] == "\n" or read_text(streak)[x] == "" or read_text(streak)[x] == " ":
            continue
        one_Contacts = read_text(streak)[x].split(",")
        one_Contacts[0].replace("\n", "")
        one_Contacts[1].replace("\n", "")
        bot.streak[one_Contacts[0]] = one_Contacts[1]

for key, value in bot.accounts.items():
    extra_lives[key] = int(int(value) / 5)


def save_info():
    open_file = open(storage, 'w')
    for name, number in bot.accounts.items():
        open_file.write(name + ",")
        open_file.close()
        open_file = open(storage, 'a')
        open_file.write(number + "\n")
    open_file.close()


def save_streak():
    open_file = open(streak, 'w')
    for name, number in bot.streak.items():
        open_file.write(name + ",")
        open_file.close()
        open_file = open(streak, 'a')
        open_file.write(number + "\n")
    open_file.close()


print(bot.accounts)
print(bot.streak)
theanswers = [
    "B: George III",
    "D: 58 miles",
    "A: Clams or C: Oysters",
    "B: Gentlemen Only Ladies Forbidden",
    "A: 315",
    "B: Mice",
    "B: Brown, it hasn't changed",
    "C: Hearts",
    "C: November",
    "C: Breed’s Hill",
    "D: Finch",
    "D: About a month",
    "A: Light Amplification by Stimulated Emissions of Radiation",
    "C: 150",
    "A: Hippopotomonstrosesquidaliophobia",
    "D: Skunk",
    "B: Set off an atomic bomb"]


class Questions(object):
    def __init__(self, question, anser, options):
        self.question = question
        self.options = options
        self.anser = anser

    async def ask(self, ctx):
        await sendquestion(ctx, self.question, self.options)

    async def checkanswer(self, ctx, response):
        if response == self.anser:
            if bot.triviabattle:
                await triviabattleright(ctx)
            else:
                await right(ctx)
        elif response != self.anser:
            if bot.triviabattle:
                await triviabattlewrong(ctx)
            else:
                await wrong(ctx)

    async def checkqotdanswer(self, ctx, response, author):
        if response == self.anser:
            qotdWinners = open("/Users/sethraphael/PycharmProject/Bots/qotd winners", "a")
            qotdWinners.write(f"{author}\n")
            qotdWinners.close()
        await ctx.send(f"Thank you for submitting your answer, {author}! Check back next time to see if you got it correct!")


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


async def on_ready():
    print("Bot is ready.")
    los_questiones = open("/Users/sethraphael/questions.txt")
    losquestiones = los_questiones.read()
    if losquestiones != "" or losquestiones != " ":
        thelist = losquestiones.split("\n")
        for line in range(0, len(thelist)):
            questiones = thelist[line].split(", ")
            theoptions = f'''{questiones[1]}\n{questiones[2]}\n{questiones[3]}\n{questiones[4]}'''
            questions.append(Questions(question=questiones[0], anser=questiones[-1], options=theoptions))
    bot.isreplaced = False


@bot.command()
async def lightninground(ctx, guess):
    if not bot.lightninground:
        bot.has_answered = False
        rand.shuffle(questions)
        bot.lightninground = True
        bot.guess = guess
        await timer(ctx)
    elif bot.lightninground and bot.playing:
        await ctx.send(f'''Someone is already playing a game of trivia, {ctx.author}.''')


async def timer(ctx):
    await ctx.send(f'''Timer has started, {ctx.author}. Answer as many questions as you can in 1 minute!''')
    await questions[bot.num].ask(ctx)
    timer_loop.start(ctx)


@tasks.loop(seconds=1)
async def timer_loop(ctx):
    bot.second -= 1
    if bot.second == 30:
        await ctx.send(f'''30 seconds left, {ctx.author}!''')
    elif bot.second == 15:
        await ctx.send(f'''15 seconds left, {ctx.author}!''')
    elif bot.second == 10:
        await ctx.send(f'''10 seconds left, {ctx.author}!''')
    elif bot.second == 5:
        await ctx.send(f'''5 seconds left, {ctx.author}!''')
    elif bot.second == 0:
        await ctx.send(f'''Time is up, {ctx.author}! Now counting your questions answered correctly!''')
        bot.lightninground = False
        correct = bot.rightquestions
        guess = bot.guess
        if int(correct) >= int(guess):
            earned_points = int(guess) * 2
            extra = int(correct) - int(guess)
            earned_points += extra
            await ctx.send(
                f'''Congratulations, {ctx.author}! You got {correct} questions right! You got your questions right! you earned {earned_points} points!''')
            for name, points in bot.accounts.items():
                if str(ctx.author) == name:
                    del bot.accounts[name]
                    bot.accounts[name] = str(int(int(points) + earned_points))
            for name, the_streak in bot.streak.items():
                if str(ctx.author) == name:
                    del bot.streak[name]
                    bot.streak_found = True
                    bot.streak[name] = str(int(int(the_streak) + 1))
                    break
                else:
                    bot.streak_found = False
            if bot.streak_found:
                pass
            elif not bot.streak_found:
                bot.streak[str(ctx.author)] = "1"

        elif int(correct) < int(guess):
            await ctx.send(
                f'''Sorry, {ctx.author}. You didn't get enough questions correct. You lost {bot.guess} points.''')
            for name, points in bot.accounts.items():
                if str(ctx.author) == name:
                    del bot.accounts[name]
                    bot.accounts[name] = str(int(int(points) - int(guess)))
            for name, the_streak in bot.streak.items():
                if str(ctx.author) == name:
                    del bot.streak[name]
                    bot.streak_found = True
                    bot.streak[name] = "0"
                    break
                else:
                    bot.streak_found = False
            if bot.streak_found:
                pass
            elif not bot.streak_found:
                bot.streak[str(ctx.author)] = "0"
        save_streak()
        timer_loop.end()


@bot.command(aliases=["Trivia", "TRIVIA", "t", "T"])
async def trivia(ctx):
    if not bot.playing:
        bot.has_answered = False
        rand.shuffle(questions)
        bot.num = 0
        await questions[bot.num].ask(ctx)
        print(questions)
        bot.playing = True
    elif bot.playing:
        await ctx.send(f'''Someone is already playing a game of trivia, {ctx.author}.''')


async def sendquestion(ctx, question, options):
    await ctx.send(question)
    await ctx.send(options)


async def right(ctx):
    if bot.playing or bot.lightninground:
        bot.playing = False
        bot.correct = True
        if not bot.has_answered:
            if bot.lightninground:
                bot.has_answered = False
            elif bot.lightninground:
                bot.has_answered = True
            account = False
            await ctx.send(f'''Congratulations, {ctx.author}, you got it right!''')
            for thatkey, thatvalue in bot.accounts.items():
                if str(ctx.author) == thatkey:
                    account = True
            if account:
                for that_key, that_value in bot.accounts.items():
                    if str(ctx.author) == that_key:
                        del bot.accounts[that_key]
                        bot.accounts[that_key] = str(int(that_value) + 1)
                        break
                if bot.lightninground:
                    bot.rightquestions += 1
                    rand.shuffle(questions)
                    await questions[bot.num].ask(ctx)
                elif not bot.lightninground:
                    await ctx.send(f'''Good job, you earned a point!''')
            elif not account:
                if bot.lightninground:
                    bot.rightquestions += 1
                    rand.shuffle(questions)
                    await questions[0].ask(ctx)
                elif not bot.lightninground:
                    await ctx.send(
                        f'''It appears that you do not have an account yet, {ctx.author}. I will start one for you now.''')
                    bot.accounts[str(ctx.author)] = "0"
                    await ctx.send(f'''Ok, {ctx.author}, I have started an account for you.''')
                    for the_key, the_value in bot.accounts.items():
                        if str(ctx.author) == the_key:
                            del extra_lives[the_key]
                            extra_lives[the_key] = int(int(the_value) / 5)
                            break
            for name, the_streak in bot.streak.items():
                if str(ctx.author) == name:
                    del bot.streak[name]
                    bot.streak_found = True
                    bot.streak[name] = str(int(int(the_streak) + 1))
                    break
                else:
                    bot.streak_found = False
            if bot.streak_found:
                pass
            elif not bot.streak_found:
                bot.streak[str(ctx.author)] = "1"
            save_streak()
            save_info()
        elif bot.has_answered:
            await ctx.send(f'''You have already answered this question, {ctx.author}.''')

    elif not bot.playing and not bot.lightninground:
        await ctx.send(f'''No one is playing a trivia game right now, {ctx.author}.''')


async def triviabattleright(ctx):
    if bot.firstround:
        bot.playersgone += 1
        await ctx.send(
            f'''Congrats, {ctx.author}, you got your first question right! One point has been added to your score for this game.''')
        playerfound = False
        for item, definition in triviabattlepoints.items():
            if str(ctx.author) == item:
                del triviabattlepoints[item]
                triviabattlepoints[str(ctx.author)] = str(int(int(definition) + 1))
                playerfound = True
                break
        if not playerfound:
            triviabattlepoints[ctx.author] = "1"
        await firstround(ctx)

    elif bot.secondround:
        bot.playersgone += 1
        await ctx.send(
            f'''Congrats, {ctx.author}, you got your second question right! One point has been added to your score for this game.''')
        playerfound = False
        for item, definition in triviabattlepoints.items():
            if str(ctx.author) == item:
                del triviabattlepoints[item]
                triviabattlepoints[str(ctx.author)] = str(int(int(definition) + 1))
                playerfound = True
                break
        if not playerfound:
            triviabattlepoints[ctx.author] = "1"
        await secondround(ctx)

    elif bot.thirdround:
        bot.playersgone += 1
        await ctx.send(
            f'''Congrats, {ctx.author}, you got your third question right! One point has been added to your score for this game.''')
        playerfound = False
        for item, definition in triviabattlepoints.items():
            if str(ctx.author) == item:
                del triviabattlepoints[item]
                triviabattlepoints[str(ctx.author)] = str(int(int(definition) + 1))
                playerfound = True
                break
        if not playerfound:
            triviabattlepoints[ctx.author] = "1"
        await thirdround(ctx)

    elif bot.fourthround:
        bot.playersgone += 1
        await ctx.send(
            f'''Congrats, {ctx.author}, you got your fourth question right! One point has been added to your score for this game.''')
        playerfound = False
        for item, definition in triviabattlepoints.items():
            if str(ctx.author) == item:
                del triviabattlepoints[item]
                triviabattlepoints[str(ctx.author)] = str(int(int(definition) + 1))
                playerfound = True
                break
        if not playerfound:
            triviabattlepoints[ctx.author] = "1"
        await fourthround(ctx)

    elif bot.fifthround:
        bot.playersgone += 1
        await ctx.send(
            f'''Congrats, {ctx.author}, you got your final question right! One point has been added to your score for this game.''')
        playerfound = False
        for item, definition in triviabattlepoints.items():
            if str(ctx.author) == item:
                del triviabattlepoints[item]
                triviabattlepoints[str(ctx.author)] = str(int(int(definition) + 1))
                playerfound = True
                break
        if not playerfound:
            triviabattlepoints[ctx.author] = "1"
        await fifthround(ctx)


async def wrong(ctx):
    if bot.playing or bot.lightninground:
        bot.playing = False
        bot.correct = False
        if not bot.has_answered:
            await ctx.send(f'''Sorry, {ctx.author}, you got it wrong.''')
            if bot.lightninground:
                pass
            elif not bot.lightninground:
                bot.has_answered = True
            account = False
            for thosekey, thosevalue in bot.accounts.items():
                if str(ctx.author) == thosekey:
                    account = True
            if account:
                for those_key, those_value in bot.accounts.items():
                    if str(ctx.author) == those_key:
                        del bot.accounts[those_key]
                        if not bot.isreplaced:
                            # bot.accounts[value].replace("\n", "")
                            bot.isreplaced = True
                        bot.accounts[those_key] = str(int(those_value) - 1)
                        break
                if bot.lightninground:
                    rand.shuffle(questions)
                    await questions[0].ask(ctx)
                elif not bot.lightninground:
                    await ctx.send(f'''Sorry, you lost a point.''')
            elif not account:
                if bot.lightninground:
                    rand.shuffle(questions)
                    await questions[0].ask(ctx)
                elif not bot.lightninground:
                    await ctx.send(
                        f'''It appears that you do not have an account yet, {ctx.author}. I will start one for you now.''')
                    bot.accounts[str(ctx.author)] = "0"
                    await ctx.send(f'''Ok, {ctx.author}, I have started an account for you.''')
                    for the_key, the_value in bot.accounts.items():
                        if str(ctx.author) == the_key:
                            del extra_lives[the_key]
                            extra_lives[the_key] = int(int(the_value) / 5)
                            break
            for name, the_streak in bot.streak.items():
                if str(ctx.author) == name:
                    bot.prevstreak = the_streak
                    del bot.streak[name]
                    bot.streak_found = True
                    bot.streak[name] = "0"
                    break
                else:
                    bot.streak_found = False
            if bot.streak_found:
                pass
            elif not bot.streak_found:
                bot.streak[str(ctx.author)] = "0"
            save_streak()
            save_info()
        elif bot.has_answered:
            await ctx.send(f'''You have already answered this question, {ctx.author}.''')
    elif not bot.playing and not bot.lightninground:
        await ctx.send(f'''No one is playing a trivia game right now, {ctx.author}.''')


async def triviabattlewrong(ctx):
    bot.playersgone += 1
    if bot.firstround:
        await ctx.send(f'''Sorry, {ctx.author}, you got your first question wrong. You earned no points this round.''')
        await firstround(ctx)

    elif bot.secondround:
        await ctx.send(f'''Sorry, {ctx.author}, you got your second question wrong. You earned no points this round.''')
        await secondround(ctx)

    elif bot.thirdround:
        await ctx.send(f'''Sorry, {ctx.author}, you got your third question wrong. You earned no points this round.''')
        await thirdround(ctx)

    elif bot.fourthround:
        await ctx.send(f'''Sorry, {ctx.author}, you got your fourth question wrong. You earned no points this round.''')
        await fourthround(ctx)

    elif bot.fifthround:
        await ctx.send(f'''Sorry, {ctx.author}, you got your final question wrong. You earned no points this round.''')
        await fifthround(ctx)


@bot.command()
async def submit(ctx, *, question):
    if bot.playing or bot.lightninground:
        await ctx.send(f'''You cannot submit a question while a trivia game is in session, {ctx.author}''')
    elif not bot.playing and not bot.lightninground:
        for keys, values in bot.accounts.items():
            if str(ctx.author) == keys:
                if int(values) >= 15:
                    del bot.accounts[keys]
                    bot.accounts[keys] = str(int(int(values) - 1))
                    the_questions = question.split(", ")
                    theoptions = f'''{the_questions[1]}\n{the_questions[2]}\n{the_questions[3]}\n{the_questions[4]}'''
                    questions.append(Questions(question=the_questions[0], anser=the_questions[5], options=theoptions))
                    file = open("/Users/sethraphael/questions.txt", "a")
                    file.write(
                        the_questions[0] + ", " + the_questions[1] + ", " + the_questions[2] + ", " + the_questions[
                            3] + ", " +
                        the_questions[4] + ", " + the_questions[5])
                    file.close()
                    await questions[-1].ask(ctx)
                    await ctx.send(
                        f'''Ok, {ctx.author}, your question has been submitted, and 15 points taken from your account!''')


@bot.command()
async def answer(ctx, *, response):
    response = response.upper()
    if bot.lightninground:
        await questions[0].checkanswer(ctx, response)
    elif bot.playing:
        await questions[0].checkanswer(ctx, response)
    elif bot.triviabattle:
        await questions[bot.playersgone].checkanswer(ctx, response)
    elif not bot.playing and not bot.lightninground and not bot.triviabattle:
        await ctx.send(f'''Not playing a trivia game right now, {ctx.author}!''')
    else:
        await ctx.send(f'''Error!''')


@bot.command()
async def addbot(ctx):
    if str(ctx.author) in bot.validusers:
        if str(ctx.author) == "Latkecrszy#0947":
            webbrowser.open(
                "https://discordapp.com/oauth2/authorize?client_id=715449106767806554&scope=bot&permissions=8")
            await ctx.send(f'''Ok, Latkecrszy, I've opened a page in your browser for you to add this bot!''')
        else:
            await ctx.send(f'''Ok, {ctx.author}, I've sent you a link to add this bot to another server!''')
            await ctx.author.send(f'''Here is the link to add this bot, {ctx.author}!''')
            await ctx.author.send(
                f'''https://discordapp.com/oauth2/authorize?client_id=715449106767806554&scope=bot&permissions=8''')
            await ctx.author.webbrowser.open(
                f'''https://discordapp.com/oauth2/authorize?client_id=715449106767806554&scope=bot&permissions=8''')
    elif str(ctx.author) not in bot.validusers:
        await ctx.send(f'''You are not authorized with this bot, {ctx.author}!''')


@bot.command()
async def authorize(ctx, *, password):
    if password.lower() == "latke":
        if str(ctx.author) in bot.validusers:
            await ctx.send(f'''You are already an authorized user, {ctx.author}''')
        elif str(ctx.author) not in bot.validusers:
            await ctx.send(f'''Ok, {ctx.author}, you are now an authorized user of this bot!''')
            valid_users = open("/Users/sethraphael/validusers.txt", "a")
            valid_users.write("\n" + str(ctx.author))
            valid_users.close()
            bot.validusers = [lines.rstrip('\n') for lines in open("/Users/sethraphael/validusers.txt")]
    else:
        await ctx.send(f'''Incorrect password, {ctx.author}.''')


@bot.command()
async def unauthorize(ctx, password, user):
    if password.lower() == "latke":
        if str(user) == "Latkecrszy#0947":
            await ctx.send(f'''You cannot unauthorize Seth, as he is the owner of the bot!''')
            for count in range(0, len(bot.validusers)):
                if ctx.author == bot.validusers[count]:
                    del bot.validusers[count]
                    await ctx.send(f'''You have been unauthorized, {ctx.author} for trying to unauthorize Seth.''')
                    break
        else:
            for i in range(0, len(bot.validusers)):
                if user == bot.validusers[i]:
                    del bot.validusers[i]
                    await ctx.send(f'''Ok, {ctx.author}, I have unauthorized {user}.''')
                    break
    else:
        await ctx.send(f'''Wrong password, {ctx.author}''')


@bot.command()
async def startaccount(ctx):
    account = False
    for those_keys, those_values in bot.accounts.items():
        if str(ctx.author) == those_keys:
            await ctx.send(f'''You already have an account, {ctx.author}''')
            account = True
            break
    if not account:
        bot.accounts[str(ctx.author)] = "0"
        await ctx.send(f'''Ok, {ctx.author}, I have started an account for you.''')


@bot.command()
async def viewpoints(ctx):
    for thosekeys, thosevalues in bot.accounts.items():
        if str(ctx.author) == thosekeys:
            await ctx.send(f'''You have {thosevalues} points, {ctx.author}.''')
            break


@bot.command()
async def bothelp(ctx):
    await ctx.send('''Ok, here is a list of commands for this bot.
   bothelp ==> shows this page
   startaccount ==> starts an account for your points with this bot
   viewpoints ==> shows you how many points you have
   unauthorize <password> <person you want to unauthorize> ==> makes a user unable to use this bot
   authorize <password> ==> allows you to use this bot
   addbot ==> sends you a link to add this bot to another server
   submit <question>, <A: option1>, <B: option2>, <C: option3>, <D: option4>, <letter of answer>, <genre> ==> submits a trivia question to this bot
   trivia ==> gives you a trivia question
   answer <letter of answer> ==> allows you to answer the question
   viewlives ==> shows you how many extra lives you have
   uselife ==> allows you to use a life in a question and give you a second chance
   lightninground <amount of questions you expect to answer correctly in one minute> ==> starts a one player game of trivia 
   in which you attempt to answer as many questions correctly in a minute as you think you can; 
   e.g, "..lightninground 10" means that I think that I can answer 10 questions correctly in 60 seconds. 
   If you succeed in getting your amount of questions correct, you get twice as many points as how many you answered. 
   If you don't, you lose however many points you thought you would get.
   hello ==> says 'hello', and sends you a wavy hand emoji.
   8ball <question> ==> answers your question in the magic 8 bally way!
   blackjack <bet here> ==> lets you play a dysfunctional blackjack game!
   roll <diesize> ==> randomly rolls a die of the size of your choice.

   If you need additional help, contact me at Latkecrszy#0947.''')


@bot.command()
async def viewlives(ctx):
    for keys, values in extra_lives.items():
        if str(ctx.author) == keys:
            await ctx.send(f'''You have {values} lives, {ctx.author}''')
            break


@bot.command()
async def uselife(ctx):
    if bot.has_answered:
        if not bot.correct:
            bot.has_answered = True
            for the_keys, the_values in extra_lives.items():
                if str(ctx.author) == the_keys:
                    await ctx.send(
                        f'''Ok, {ctx.author}, I have used one of your lives, and therefore 5 of your points. Your streak is safe!''')
                    for thekeys, thevalues in bot.accounts.items():
                        if str(ctx.author) == thekeys:
                            del bot.accounts[key]
                            if not bot.isreplaced:
                                # bot.accounts[value].replace("\n", "")
                                bot.isreplaced = True
                            bot.accounts[key] = str(int(value) - 5)
                            break
                    for name, theStreak in bot.streak.items():
                        if str(ctx.author) == name:
                            del bot.streak[name]
                            bot.streak[name] = str(bot.prevstreak)
                    save_streak()
        elif bot.correct:
            await ctx.send(f'''You got the question correct, {ctx.author}. No need to use a life!''')
    elif not bot.has_answered:
        bot.has_answered = False
        await ctx.send(
            f'''You have not answered a question already, {ctx.author}. If you answer wrong, then you may use an extra life.''')


@bot.command()
async def viewstreak(ctx):
    for name, theStreak in bot.streak.items():
        if str(ctx.author) == name:
            if int(theStreak) >= 10:
                await ctx.send(f'''Your streak, {ctx.author}, is {theStreak}. That's pretty good!''')
            elif int(theStreak) < 10:
                await ctx.send(f'''Your streak, {ctx.author}, is {theStreak}. Keep working!''')


@bot.command(aliases=["Triviabattle", "TRIVIABATTLE", "TriviaBattle", "tb", "Tb", "TB"])
async def triviabattle(ctx):
    bot.triviabattle = True
    await ctx.send(
        f'''Ok, {ctx.author}, your game of triviabattle has been started.\n Just say `startgame` or `sg` to start the game, or `join` or `j` to join!''')
    rand.shuffle(questions)
    bot.joined += 1
    players[str(ctx.author)] = questions[0]


@bot.command(aliases=["j", "J", "Join", "JOIN"])
async def join(ctx):
    bot.joined += 1
    players[str(ctx.author)] = questions[bot.joined - 1]
    await ctx.send(f'''Ok, {ctx.author}, you have joined the triviabattle!''')


@bot.command(aliases=["Startgame", "StartGame", "sg", "SG", "Sg"])
async def startgame(ctx):
    if bot.playing:
        await ctx.send(f'''Someone is already playing a trivia game, {ctx.author}!''')
    if bot.lightninground:
        await ctx.send(f'''Someone is already playing a game of lightninground, {ctx.author}!''')
    if bot.triviabattle:
        bot.firstround = True
        await ctx.send(f'''Your game has started, {ctx.author}!''')
        player1 = list(players.keys())[0]
        await ctx.send(f'''Question 1, for player {player1}:''')
        await questions[0].ask(ctx)
    else:
        await ctx.send(f'''Not playing a game of triviabattle right now, {ctx.author}!''')


@bot.command()
async def cancel(ctx, *, game):
    if bot.triviabattle or bot.lightninground or bot.playing:
        if game.lower() == "triviabattle" or game.lower() == "tb":
            bot.triviabattle = False
            await ctx.send(f'''Ok, {ctx.author}, your game has been canceled.''')
        elif game.lower() == "lightninground":
            bot.lightninground = False
            await ctx.send(f'''Ok, {ctx.author}, your game has been canceled.''')
        else:
            await ctx.send(f'''Invalid game, {ctx.author}.''')
    else:
        await ctx.send(f'''Not playing a game right now, {ctx.author}!''')


async def firstround(ctx):
    gone = bot.playersgone
    player_num = 0
    for name in players.keys():
        player_num += 1
    if player_num == gone:
        await ctx.send(f'''All players have answered their first questions. Now, for the second round!''')
        bot.playersgone = 0
        rand.shuffle(questions)
        bot.firstround = False
        bot.secondround = True
        player1 = list(players.keys())[0]
        await ctx.send(f'''Question 2, for player{player1}:''')
        await questions[0].ask(ctx)
    elif player_num != gone:
        current_player = list(players.keys())[bot.playersgone]
        await ctx.send(f'''Question 1, for player {current_player}:''')
        await questions[bot.playersgone].ask(ctx)


async def secondround(ctx):
    gone = bot.playersgone
    player_num = 0
    for name in players.keys():
        player_num += 1
    if player_num == gone:
        await ctx.send(f'''All players have answered their second questions. Now, for the third round!''')
        bot.playersgone = 0
        rand.shuffle(questions)
        bot.secondround = False
        bot.thirdround = True
        player1 = list(players.keys())[0]
        await ctx.send(f'''Question 3, for player{player1}:''')
        await questions[0].ask(ctx)
    elif player_num != gone:
        current_player = list(players.keys())[bot.playersgone]
        await ctx.send(f'''Question 2, for player {current_player}:''')
        await questions[bot.playersgone].ask(ctx)


async def thirdround(ctx):
    gone = bot.playersgone
    player_num = 0
    for name in players.keys():
        player_num += 1
    if player_num == gone:
        await ctx.send(f'''All players have answered their third questions. Now, for the fourth round!''')
        bot.playersgone = 0
        rand.shuffle(questions)
        bot.thirdround = False
        bot.fourthround = True
        player1 = list(players.keys())[0]
        await ctx.send(f'''Question 4, for player{player1}:''')
        await questions[0].ask(ctx)
    elif player_num != gone:
        current_player = list(players.keys())[bot.playersgone]
        await ctx.send(f'''Question 3, for player {current_player}:''')
        await questions[bot.playersgone].ask(ctx)


async def fourthround(ctx):
    gone = bot.playersgone
    player_num = 0
    for name in players.keys():
        player_num += 1
    if player_num == gone:
        await ctx.send(f'''All players have answered their fourth questions. Now, for the fifth round!''')
        bot.playersgone = 0
        rand.shuffle(questions)
        bot.fourthround = False
        bot.fifthround = True
        player1 = list(players.keys())[0]
        await ctx.send(f'''Question 5, for player{player1}:''')
        await questions[0].ask(ctx)
    elif player_num != gone:
        current_player = list(players.keys())[bot.playersgone]
        await ctx.send(f'''Question 4, for player {current_player}:''')
        await questions[bot.playersgone].ask(ctx)


async def fifthround(ctx):
    gone = bot.playersgone
    player_num = 0
    for name in players.keys():
        player_num += 1
    if player_num == gone:
        await ctx.send(
            f'''All players have answered their fifth questions. Now, the totals will be counted. Whoever has the most points will reign victorious!!''')
        scores = []
        names = []
        winning_name = ""
        for name, points in players.items():
            scores.append(int(points))
            names.append(name)
        winning_score = max(scores)
        for a in range(0, len(scores)):
            if winning_score == int(scores[a]):
                winning_name = str(names[a])
        if winning_name == "":
            await ctx.send(f'''Error in tallied scores. I guess we'll never know who won. :(''')
        else:
            await ctx.send(f'''All players' scores have been tallied up, and the winner is...''')
            await ctx.send(f'''{winning_name}! With a score of {winning_score}, {winning_name} is the winner!''')

    elif player_num != gone:
        current_player = list(players.keys())[bot.playersgone]
        await ctx.send(f'''Question 5, for player {current_player}:''')
        await questions[bot.playersgone].ask(ctx)



bot.quesnum = 0


@bot.command()
async def qotdstart(ctx):
    startNum = 0
    await questions[bot.num].ask(ctx)
    time.sleep(86400)
    bot.quesnum += startNum
    for ques in range(len(questions)):
        bot.quesnum += 1
        await questions[ques + startNum].ask(ctx)
        time.sleep(86400)
        correctpeeps = 0
        for i in open("/Users/sethraphael/PycharmProject/Bots/qotd winners").readlines():
            correctpeeps += 1
        await ctx.send(f"Hey @here - guess what? A whole {correctpeeps} got this question right!")
        correctos = ", ".join(open("/Users/sethraphael/PycharmProject/Bots/qotd winners").readlines())
        await ctx.send(f"Good job to {correctos}! They are the ones that got it right!")


@bot.command(aliases=["qa", "qotdans"])
async def qotdanswer(ctx, response):
    response = response.upper()
    await questions[bot.quesnum].checkqotdanswer(ctx, response, str(ctx.author))


bot.run("NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.B5eSdENH1GLRT7CkMLACTw7KpGE")
# TRIVIA BOT TOKEN:
# NzE1NDQ5MTA2NzY3ODA2NTU0.Xvk_ww.awjbeGAT_Yw_0yNAjGdZewF2pWE

# Why does on_message make my commands stop working?
# Overriding the default provided on_message forbids any extra commands from running. To fix this, add a bot.process_commands(message) line at the end of your on_message. For example:

# @bot.event
# async def on_message(message):
# do some extra stuff here

# await bot.process_commands(message)
# Get user id https://discordapp.com/channels/336642139381301249/381965515721146390/731215144348024873
