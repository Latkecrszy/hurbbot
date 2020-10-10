import discord
from discord.ext import commands
import time
from datetime import datetime
import asyncio
import json
import random


class Verification:
    def __init__(self):
        self.agreeing = False

    async def verify(self, member):
        self.agreeing = True
        guild = member.guild
        choose_your_roles = discord.utils.get(guild.text_channels, name="#🌱choose-your-roles")
        rules = discord.utils.get(guild.text_channels, name="#🌱rules")
        channel = discord.utils.get(guild.text_channels, name="🌱verification")
        if str(guild.name).lower() == "art gatherings":
            await member.add_roles(discord.utils.get(member.guild.roles, name="unverified"))
            await channel.send(
                f"Welcome to Art Gatherings {member.mention}! Check out {choose_your_roles} to get the roles best fit to you!")
            await channel.send(
                f"Once you've done that, go to {rules} and read through them carefully to make sure that you understand.")
            await channel.send(f"Then, type `agree` in this channel to gain access to the server!")
            await channel.send(f"After that, you're all set! Enjoy the server!")

    async def verifyCheck(self, message):
        if str(message.guild.name) == "Art Gatherings":
            if discord.utils.get(message.author.roles, name="unverified"):
                if str(message.content).lower() == "agree":
                    await message.channel.send(f"You have been verified to Art Gatherings {message.author.mention}!")
                    role = discord.utils.get(message.guild.roles, name="unverified")
                    otherRole = discord.utils.get(message.guild.roles, name="Artists")
                    await message.author.remove_roles(role)
                    await message.author.add_roles(otherRole)


commandsFile = '/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json'


mutedMembers = []
kicked = []

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


def is_it_me(ctx):
    return ctx.author.id == 670493561921208320


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


def is_me(command):
    def predicate(ctx):
        with open(commandsFile, 'r') as f:
            commandsList = json.load(f)
            activeList = commandsList[str(ctx.guild.id)]
            return activeList[command] == "True"

    return commands.check(predicate)


def muteTimeCalc(muteTime):
    muteList = []
    minute = False
    hour = False
    day = False
    for char in muteTime:
        if char.lower() == "m":
            minute = True
        elif char.lower() == "h":
            hour = True
        elif char.lower() == "d":
            day = True
        elif char.lower() == "s":
            pass
        elif isinstance(char, str):
            muteList.append(char)
        else:
            pass
    muteTime = "".join(muteList)
    muteTime = int(muteTime)
    if minute:
        muteTime *= 60
    if hour:
        muteTime *= 3600
    if day:
        muteTime *= 86400
    return muteTime


async def muteRole(ctx):
    overwrite = discord.PermissionOverwrite(send_messages=False)
    role = discord.utils.get(ctx.guild.roles, name="muted")
    if not role or role is None:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role or role is None:
        newRole = await ctx.guild.create_role(name="muted", color=discord.Color.dark_grey())
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(newRole, overwrite=overwrite)
        role = newRole

    for channel in ctx.guild.text_channels:
        await channel.set_permissions(role, overwrite=overwrite)
    return role


class MemberCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mutedRoles = {}

    @is_me("mute")
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def mute(self, ctx, member: discord.Member, *, reason="There was no reason for this muting."):
        if not member.guild_permissions.administrator:
            if not discord.utils.get(member.roles, name="muted"):
                role = await muteRole(ctx)
                for roles in member.roles:
                    if roles != ctx.guild.default_role:
                        self.mutedRoles[str(member)] = []
                        self.mutedRoles[str(member)].append(roles)
                        await member.remove_roles(roles)
                await member.add_roles(role, reason=reason)
                await ctx.send(embed=discord.Embed(
                    title=f"<:check:742198670912651316>  {member.display_name} has been muted.",
                    description=f"Reason: {reason}", colour=discord.Colour.green()))

            else:
                await ctx.send(embed=discord.Embed(description=f"<:x_:742198871085678642>  {member.mention} is already muted!",
                                                   color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:x_:742198871085678642>  I can't do that, as {member.mention} is an administrator.",
                                               color=discord.Color.red()))

    @is_me("mute")
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def tempmute(self, ctx, member: discord.Member, muteTime, *, reason="There was no reason for this muting."):
        if not member.guild_permissions.administrator:
            if not discord.utils.get(member.roles, name="muted"):
                role = await muteRole(ctx)
                muteTime = muteTimeCalc(muteTime)
                self.mutedRoles[str(member)] = []
                for roles in member.roles:
                    if roles != ctx.guild.default_role:
                        self.mutedRoles[str(member)].append(roles)
                        await member.remove_roles(roles)
                await member.add_roles(role, reason=reason)
                await ctx.send(embed=discord.Embed(
                    title=f"<:check:742198670912651316>  {member.display_name} has been muted for {muteTime} seconds.",
                    description=f"Reason: {reason}",
                    colour=discord.Colour.green()))
                await asyncio.sleep(int(muteTime))
                if str(member) in self.mutedRoles.keys():
                    for roles in self.mutedRoles[str(member)]:
                        await member.add_roles(roles)
                    for x in range(len(self.mutedRoles[str(member)])):
                        self.mutedRoles[str(member)].pop(x)
                await member.remove_roles(role)
                await ctx.send(embed=discord.Embed(
                    description=f"<:check:742198670912651316>  {member.mention} has been unmuted.", color=discord.Colour.green()))
            else:
                await ctx.send(embed=discord.Embed(description=f"<:x_:742198871085678642>  {member.mention} is already muted!",
                                                   color=discord.Colour.red()))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:x_:742198871085678642>  I can't do that, as {member.mention} is an administrator.",
                                               color=discord.Colour.red()))

    @is_me("unmute")
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unmute(self, ctx, member: discord.Member):
        if discord.utils.get(member.roles, name="muted"):
            role = await muteRole(ctx)
            if str(member) in self.mutedRoles.keys():
                for roles in self.mutedRoles[str(member)]:
                    await member.add_roles(roles)
                for x in range(len(self.mutedRoles[str(member)])):
                    self.mutedRoles[str(member)].pop(x)
            await member.remove_roles(role)
            await ctx.send(embed=discord.Embed(description=f"<:check:742198670912651316>  {member.mention} has been unmuted.", color=discord.Colour.green()))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:x_:742198871085678642>  {member.mention} is not muted!",
                                               color=discord.Colour.red()))

    @mute.error
    async def muteError(self, ctx, error):
        await ctx.send(embed=discord.Embed(title="Sorry, something went wrong. To fix this, please try either dragging the mute role higher, or my own role higher.",
                                           color=discord.Color.red()))

    @is_me("kick")
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def kick(self, ctx, member: discord.Member, *, reason="There was no reason for this kicking."):
        if not member.guild_permissions.administrator:
            await member.send(embed=discord.Embed(title=f"You have been kicked from {ctx.guild.name} by {ctx.author}.",
                                                  description=f"Reason: {reason}",
                                                  color=discord.Color.red()))
            await ctx.guild.kick(member)
            embed = discord.Embed(
                title=f"<:check:742198670912651316> {member.display_name} has been kicked by {ctx.author.display_name}.",
                description=f"Reason: {reason}", color=discord.Color.green())
            await ctx.send(embed=embed)

        elif member.guild_permissions.administrator:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> {member} has failed to be kicked by {ctx.author.display_name} because they are an admin/mod.",
                color=discord.Color.red())
            await ctx.send(embed=embed)

    @is_me("ban")
    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, member: discord.Member, *, reason="There was no reason for this banning."):
        if not member.guild_permissions.administrator:
            await member.send(embed=discord.Embed(title=f"You have been banned from {ctx.guild.name} by {ctx.author}.",
                                                  description=f"Reason: {reason}",
                                                  color=discord.Color.red()))
            await ctx.guild.ban(member)
            await ctx.send(embed=discord.Embed(title=f"<:check:742198670912651316> {member} has been banned by {ctx.author}",
                                               description=f"Reason: {reason}"))

        elif member.guild_permissions.administrator:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> {member} has failed to be banned by {ctx.author.display_name} because they are an admin/mod.",
                description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

    @is_me("rall")
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def rall(self, ctx, *, rename_to):
        for user in list(ctx.guild.members):
            try:
                await user.edit(nick=rename_to)
                print(f"{user.name} has been renamed to {rename_to} in {ctx.guild.name}")
            except:
                print(f"{user.name} has NOT been renamed to {rename_to} in {ctx.guild.name}")
        print("Action Completed: rall")

    @is_me("rename")
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rename(self, ctx, member: discord.Member = None, *, new_name):
        await member.edit(nick=new_name)
        await ctx.send(embed=discord.Embed(description=f"{member.mention} has been renamed to {new_name} by {ctx.author.mention}.",
                       color=random.choice(embedColors)))

    @is_me("warn")
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        if not member.guild_permissions.administrator:

            await member.send(embed=discord.Embed(title=f"You have been warned in *{ctx.guild}* by *{ctx.author}*.",
                                                  description=f"Reason: {reason}"))
            embed = discord.Embed(
                title=f"<:check:742198670912651316> {member.display_name} has been warned.",
                description=None, colour=discord.Colour.green())
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title=f"<:x_:742198871085678642> {member.display_name} cannot be warned, as they are an administrator.",
                                               color=discord.Color.red()))

    @commands.Cog.listener()
    @is_me("welcome")
    async def on_member_join(self, member):
        for x in range(len(mutedMembers)):
            if mutedMembers[x] == str(member):
                for roles in member.guild.roles:
                    if str(roles).lower() == "muted":
                        await member.add_roles(roles)
                        del mutedMembers[x]
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/welcome.json", "r") as f:
            welcomeChannels = json.load(f)
        welcomeMessage = welcomeChannels[str(member.guild.id)]
        if welcomeMessage != "None" and welcomeMessage != "False":
            for Channel in member.guild.text_channels:
                for key, value in welcomeMessage.items():
                    value = value.split(" ")
                    for i in range(len(value)):
                        if value[i].lower() == "member" or value[i].lower() == "member!" or value[i].lower() == "member.":
                            value[i] = member.mention
                    if str(key) == str(Channel):
                        embed = discord.Embed(description=" ".join(value), color=random.choice(embedColors))
                        await Channel.send(embed=embed)
        """with open("/Users/sethraphael/PycharmProject/Hurb/Bots/welcomeroles.json", "r") as f:
            welcomeroles = json.load(f)
        for role in member.guild.roles:
            if str(role.mention).lower() == str(welcomeroles[str(member.guild.id)]).lower():
                await member.add_roles(role)"""

    @commands.Cog.listener()
    @is_me("goodbye")
    async def on_member_remove(self, member):
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/goodbye.json", "r") as f:
            goodbyeChannels = json.load(f)
        goodbyeMessage = goodbyeChannels[str(member.guild.id)]
        if goodbyeMessage != "None" and goodbyeMessage != "False":
            for Channel in member.guild.text_channels:
                for key, value in goodbyeMessage.items():
                    value = value.split(" ")
                    for i in range(len(value)):
                        if value[i].lower() == "member" or value[i].lower() == "member." or value[i].lower() == "member!":
                            value[i] = member.mention

                    if str(key) == str(Channel):
                        embed = discord.Embed(description=" ".join(value), color=random.choice(embedColors))
                        await Channel.send(embed=embed)
        for role in member.roles:
            if str(role).lower() == "muted":
                mutedMembers.append(str(member))

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.display_name}'s info for {ctx.guild.name}:",
                              color=random.choice(embedColors))
        embed.add_field(name=f"Joined at:", value=member.joined_at)
        memberRoles = member.roles
        roles = []
        for role in memberRoles:
            roles.append(role.mention)
        roleString = " ".join(roles)
        extraRoles = []
        while len(roleString) > 1024:
            if roles[-1] != ctx.guild.default_role:
                extraRoles.append(roles[-1])
            del roles[-1]
            roleString = " ".join(roles)
        roles = " ".join(roles)

        embed.add_field(name=f"**Roles**:",
                        value=roles)
        if extraRoles:
            extraRoles = " ".join(extraRoles)
            embed.add_field(name=f"**Other Roles**:", value=extraRoles)
        embed.set_author(icon_url=member.avatar_url, name=member.display_name)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modmute(self, ctx, member: discord.Member):
        with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/mutedMods.json", "r") as f:
            mutedMods = json.load(f)
        if str(member) == "Latkecrszy#0947":
            embed = discord.Embed(description=f"Uh NOPE {ctx.author.mention}, you ain't pullin that one on my creator. You know what? I'm gonna mute YOU instead.")
            mutedMods[str(ctx.author)] = str(ctx.guild)
        elif str(member) not in mutedMods.keys():
            embed = discord.Embed(description=f"{member.mention} has been modmuted by {ctx.author.mention}.", color=discord.Color.green())
            mutedMods[str(member)] = str(ctx.guild)
        else:
            embed = discord.Embed(description=f"{member.mention} is already muted {ctx.author.mention}!", color=discord.Color.red())
        await ctx.send(embed=embed)
        with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/mutedMods.json", "w") as f:
            json.dump(mutedMods, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modunmute(self, ctx, member: discord.Member):
        with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/mutedMods.json",
                  "r") as f:
            mutedMods = json.load(f)

        if str(member) in mutedMods.keys() and str(ctx.author) not in mutedMods.keys():
            embed = discord.Embed(description=f"{member.mention} has been unmuted by {ctx.author.mention}.", color=discord.Color.green())
            mutedMods.pop(str(member))
        else:
            embed = discord.Embed(description=f"{member.mention} is not muted {ctx.author.mention}!", color=discord.Color.red())

        await ctx.send(embed=embed)
        with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/mutedMods.json", "w") as f:
            json.dump(mutedMods, f, indent=4)

    @commands.command()
    async def setstatus(self, ctx, *, status):
        if is_it_me(ctx):
            await self.bot.change_presence(status=discord.Status.online, activity=status)
            await ctx.send(f"Status changed to {status}")
        else:
            await ctx.send(f"You do not have permission to use this command {ctx.author.mention}!")


def setup(bot):
    bot.add_cog(MemberCog(bot))
