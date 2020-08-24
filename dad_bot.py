from discord.ext import commands
import random
from discord.ext.commands import CommandNotFound
import time

print("Loading..")

bot = commands.Bot(command_prefix="dad ")

bot.jokes = ["Dad, will you hand me my sunglasses?;As soon as you hand me my dadglasses, son.",
             "What did the pen say to the other pen?;You're inkredible!",
             "It was easy for me to master braille.;But only once I got a feel for it!",
             "What did one eye say to the other eye?;Between you and me, something smells.",
             "Dad, can you put my shoes on?;I don't think they'd fit me.",
             "I tell dad jokes but i have no kids.;I'm a faux pa.",
             "What do you call a small mother?;A minimum!",
             "I'm terrified of elevators.;I'm going to start taking steps to avoid them.",
             "As a child, it was my dream to make a perfect bar of soap.;Somehow, it just slipped away.",
             "What do snowmen do in their spare time?;They just chill",
             "Did you hear about the man who invented the knock-knock joke?;He won the No Bell Prize.",
             "What do you call someone with no body and no nose?;Nobody knows.",
             "Do you want to hear a joke about paper?;Never mind, it's tearable.",
             "The bank robber took a bath after a heist.;He wanted to make a clean getaway.",
             "Why did the boy bring a ladder to chorus?;He wanted to sing higher!",
             "Did you hear about the houses that fell in love?;It was a lawn-distance relationship.",
             "Why did the belt go to jail?;Because it held up a pair of pants!",
             "Our wedding was so beautiful.;Even the cake was in tiers!",
             "Never buy anything with velcro.;It's a total ripoff.",
             "Why did the scarecrow win an award?;Because he was outstanding in his field.",
             "Dad, are you going to take a bath?;No, I'm leaving it where it is.",
             "Did you hear about the fire in the shoe factory?;Hundreds of soles were lost.",
             "I worked out so hard, the police put me in jail.;I was charged with resisting a rest.",
             "Why can't you have a nose that is twelve inches long?;Because then it would be a foot!",
             "Did you hear about the calendar thief?;He got twelve months.",
             "Can February march?;No, but April may.",
             "What did one bell say to the other?;Be my valenchime!",
             "I gave away all my dead batteries today.;They were free of charge!",
             "What's black, white, and red all over?;The panda I just murdered!",
             "I used to hate facial hair.;That is, until it started to grow on me.",
             "When does a bed grow longer?;At night, when two feet are added to it!",
             "Dad, how do I look?;With your eyes!",
             "Somebody stole all my lamps.;I couldn't be more delighted.",
             "Who is the strongest thief?;A shoplifter!",
             "What do teeth call their sexy selfies?;Toothpics!",
             "Why did the man throw the clock out the window?;Because he heard that time flies."]


@bot.event
async def on_ready():
    print("ready")


@bot.event
async def on_message(message):
    if message.content.lower() == "im dad" or message.content.lower() == "i'm dad" or message.content.lower() == "i am dad":
        await message.channel.send(f'''You're not dad, I'm dad!''')
    elif message.content.startswith("im "):
        name_list = []
        for char in str(message.content):
            name_list.append(str(char))
        del name_list[0]
        del name_list[0]
        name = "".join(name_list)
        await message.channel.send(f'''Hi,{str(name)}, I'm dad!''')
    if message.content.startswith("Im "):
        name_list = []
        for char in str(message.content):
            name_list.append(str(char))
        del name_list[0]
        del name_list[0]
        name = "".join(name_list)
        await message.channel.send(f'''Hi,{str(name)}, I'm dad!''')
    elif message.content.startswith("i'm "):
        name_list = []
        for char in str(message.content):
            name_list.append(str(char))
        del name_list[0]
        del name_list[0]
        del name_list[0]
        name = "".join(name_list)
        await message.channel.send(f'''Hi,{str(name)}, I'm dad!''')
    elif message.content.startswith("I'm "):
        name_list = []
        for char in str(message.content):
            name_list.append(str(char))
        del name_list[0]
        del name_list[0]
        del name_list[0]
        name = "".join(name_list)
        await message.channel.send(f'''Hi,{str(name)}, I'm dad!''')
    elif message.content.startswith("i am "):
        name_list = []
        for char in str(message.content):
            name_list.append(str(char))
        del name_list[0]
        del name_list[0]
        del name_list[0]
        del name_list[0]
        name = "".join(name_list)
        await message.channel.send(f'''Hi,{str(name)}, I'm dad!''')
    elif message.content.startswith("I am "):
        name_list = []
        for char in str(message.content):
            name_list.append(str(char))
        del name_list[0]
        del name_list[0]
        del name_list[0]
        del name_list[0]
        name = "".join(name_list)
        await message.channel.send(f'''Hi,{str(name)}, I'm dad!''')
    await bot.process_commands(message)


@bot.command()
async def joke(ctx):
    current_joke = random.choice(bot.jokes)
    the_joke = current_joke.split(";")
    await ctx.send(the_joke[0])
    time.sleep(2.5)
    await ctx.send(the_joke[1])


@bot.command()
async def submit(ctx, *, the_question):
    questions = the_question.split(", ")
    question = questions[0]
    answer = questions[1]
    new_question = question + ";" + answer
    bot.jokes.append(new_question)
    await ctx.send(question)
    time.sleep(2.5)
    await ctx.send(answer)


@bot.command()
async def catch(ctx):
    choices = [1, 2, 3]
    choices2 = [1, 2]
    choice = random.choice(choices)
    if choice == 1:
        await ctx.send("Good throw, son! Here, catch!")
        choice2 = random.choice(choices2)
        if choice2 == 1:
            time.sleep(2)
            await ctx.send("Great catch, son!")
        elif choice2 == 2:
            time.sleep(2)
            await ctx.send("Oh, the frisbee isn't supposed to go down your throat, son!")
    elif choice == 2 or choice == 3:
        await ctx.send("Well son, you were supposed to throw it to me, not get it stuck on the roof!")


@bot.command()
async def purge(message, number):
    await message.channel.purge(limit=int(int(number) + 1))
    await bot.process_commands(message)

@bot.command()
async def shit(ctx):
    await ctx.send("I have let out an enormous shit.")


@bot.event
async def on_error(err, *args):
    if err == "on_command_error":
        await args[0].send("Something went wrong.")
    raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f"I could not find that command, {ctx.author}")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''Error: Missing one or more required argument.''')
    else:
        raise error.original


@bot.command(aliases=["COVID", "Covid", "covid-19", "COVID-19", "Covid-19"])
async def covid(ctx):
    await ctx.send("Oh shit, oh no, we're all gonna die!")
    time.sleep(2)
    await ctx.send("BUY ALL THE TOILET PAPER!!!")
    time.sleep(2)
    await ctx.send("STOCKPILE 50 POUNDS OF MEAT!!!")
    time.sleep(2)
    await ctx.send("AND QUARANTINE FOR GODS SAKE!!!")

bot.run("NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.B5eSdENH1GLRT7CkMLACTw7KpGE")

# DAD BOT TOKEN:

# NzM0ODQ4MDgzOTQyNDQxMDYx.Xxd2Hw.P0WeJ6GuHo-cViKoEJg_V8m6OJY
