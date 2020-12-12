import discord
from discord.ext import commands
import asyncio
import json
import random


"""class Verification:
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
                    await message.author.add_roles(otherRole)"""

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
    role = discord.utils.get(ctx.guild.roles, name="muted")
    if not role or role is None:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role or role is None:
        newRole = await ctx.guild.create_role(name="muted", color=discord.Color.dark_grey())
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(newRole, overwrite=discord.PermissionOverwrite(send_messages=False))
        role = newRole

    for channel in ctx.guild.text_channels:
        perms = channel.overwrites_for(role)
        if perms.send_messages:
            perms.send_messages = False
            await channel.set_permissions(role, perms)
    return role


class MemberCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mutedRoles = {}

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def mute(self, ctx, member: discord.Member, *, reason="There was no reason for this muting."):
        if not member.guild_permissions.administrator:
            if not discord.utils.get(member.roles, name="muted"):
                role = await muteRole(ctx)
                embed = discord.Embed(
                    description=f"***<a:check:771786758442188871>  {member.mention} has been muted.***",
                    color=discord.Color.green())
                self.mutedRoles[str(member)] = []
                embed.set_footer(text=f"Reason:  {reason}")
                for roles in member.roles:
                    if roles != ctx.guild.default_role:
                        self.mutedRoles[str(member)].append(roles)
                        await member.remove_roles(roles)
                await member.add_roles(role, reason=reason)
                await ctx.send(embed=embed)


            else:
                await ctx.send(
                    embed=discord.Embed(description=f"***<a:no:771786741312782346>  {member.mention} is already muted!***",
                                        color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"***<a:no:771786741312782346>  I can't do that, as {member.mention} is an administrator.***",
                color=discord.Color.red()))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def tempmute(self, ctx, member: discord.Member, muteTime, *, reason="There was no reason for this muting."):
        if not member.guild_permissions.administrator:
            if not discord.utils.get(member.roles, name="muted"):
                role = await muteRole(ctx)
                muteTime = muteTimeCalc(muteTime)
                self.mutedRoles[str(member)] = []
                embed = discord.Embed(
                    description=f"***<a:check:771786758442188871>  {member.mention} has been muted for {muteTime} seconds.***",
                    colour=discord.Colour.green())
                embed.set_footer(text=f"Reason: {reason}")
                await ctx.send(embed=embed)
                for roles in member.roles:
                    if roles != ctx.guild.default_role:
                        self.mutedRoles[str(member)].append(roles)
                        await member.remove_roles(roles)

                await member.add_roles(role, reason=reason)
                await asyncio.sleep(int(muteTime))
                await self.unmute(ctx, member)
            else:
                await ctx.send(
                    embed=discord.Embed(description=f"***<a:no:771786741312782346>  {member.mention} is already muted!***",
                                        color=discord.Colour.red()))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"***<a:no:771786741312782346>  I can't do that, as {member.mention} is an administrator.***",
                color=discord.Colour.red()))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unmute(self, ctx, member: discord.Member):
        if str(member) in self.mutedRoles.keys():
            role = await muteRole(ctx)
            await member.remove_roles(role)
            for roles in self.mutedRoles[str(member)]:
                await member.add_roles(roles)
            for x in range(len(self.mutedRoles[str(member)])):
                self.mutedRoles[str(member)].pop(0)
            await ctx.send(
                embed=discord.Embed(description=f"***<a:check:771786758442188871>  {member.mention} has been unmuted.***",
                                    color=discord.Colour.green()))
        else:
            await ctx.send(embed=discord.Embed(description=f"***<a:no:771786741312782346>  {member.mention} is not muted!***",
                                               color=discord.Colour.red()))

    @mute.error
    async def muteError(self, ctx, error):
        await ctx.send(embed=discord.Embed(
            title="Sorry, something went wrong. To fix this, please try either dragging the mute role higher, or my own role higher.",
            color=discord.Color.red()))

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason="There was no reason for this kicking."):
        if not member.guild_permissions.administrator:
            await member.send(embed=discord.Embed(title=f"You have been kicked from {ctx.guild.name} by {ctx.author}.",
                                                  description=f"Reason: {reason}",
                                                  color=discord.Color.red()))
            await ctx.guild.kick(member)
            embed = discord.Embed(
                description=f"***<:check:742198670912651316> {member.mention} has been kicked by {ctx.author.mention}.***", color=discord.Color.green())
            embed.set_footer(text=f"Reason: {reason}")
            await ctx.send(embed=embed)

        elif member.guild_permissions.administrator:
            embed = discord.Embed(
                description=f"***<:x_:742198871085678642> {member.mention} has failed to be kicked by {ctx.author.mention} because they are an admin/mod.***",
                color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason="There was no reason for this banning."):
        if not member.guild_permissions.administrator:
            try:
                await member.send(embed=discord.Embed(title=f"You have been banned from {ctx.guild.name} by {ctx.author}.",
                                                    description=f"Reason: {reason}",
                                                    color=discord.Color.red()))
            except:
                pass
            await ctx.guild.ban(member)
            await ctx.guild.kick(member)
            embed = discord.Embed(
                description=f"***<:check:742198670912651316> {member.mention} has been banned by {ctx.author.mention}.***",
                color=discord.Color.green())
            embed.set_footer(text=f"Reason: {reason}")
            await ctx.send(embed=embed)

        elif member.guild_permissions.administrator:
            embed = discord.Embed(
                title=f"*<:x_:742198871085678642> {member} has failed to be banned by {ctx.author.display_name} because they are an admin/mod.*",
                description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def unban(self, ctx, member: discord.Member):
        await member.unban()
        await ctx.send(f"{member} has been unbanned from {ctx.guild}.")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, member: discord.Member = None, *, new_name):
        await ctx.send(
            embed=discord.Embed(description=f"***{member.display_name} has been renamed to {member.mention} by {ctx.author.mention}.***",
                                color=random.choice(embedColors)))
        await member.edit(nick=new_name)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        if not member.guild_permissions.administrator:

            await member.send(embed=discord.Embed(title=f"You have been warned in **{ctx.guild}** by **{ctx.author}**.",
                                                  description=f"Reason: {reason}"))
            embed = discord.Embed(
                description=f"***<:check:742198670912651316> {member.mention} has been warned.***", colour=discord.Colour.green())
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(
                title=f"***<:x_:742198871085678642> {member.display_name} cannot be warned, as they are an administrator.***",
                color=discord.Color.red()))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("../Bots/servers.json", "r") as f:
            storage = json.load(f)
        if "welcome" in storage[str(member.guild.id)]:
            welcomeChannels = storage[str(member.guild.id)]["welcome"]
            channel = member.guild.get_channel(int(welcomeChannels["id"]))
            message = welcomeChannels["message"]
            if message.find("{member}"):
                message = message.split("{")
                message2 = message[1].split("}")
                message2 = message2[1]
                message = message[0]
                await channel.send(f"{message}{member.mention}{message2}")
            for role in member.roles:
                if str(role).lower() == "muted":
                    mutedMembers.append(str(member))

            with open("../Bots/servers.json") as f:
                storage = json.load(f)

            if "autoroles" in storage[str(member.guild.id)].keys():
                autoroles = storage[str(member.guild.id)]["autoroles"]
                for role in autoroles[str(member.guild.id)]:
                    addRole = discord.utils.get(member.guild.roles, name=role)
                    if addRole is not None:
                        await member.add_roles(addRole)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open("../Bots/servers.json", "r") as f:
            storage = json.load(f)
        if "goodbye" in storage[str(member.guild.id)].keys():
            goodbyeChannels = storage[str(member.guild.id)]["goodbye"]
            channel = member.guild.get_channel(int(goodbyeChannels["id"]))
            message = goodbyeChannels["message"]
            if message.find("{member}"):
                message = message.split("{")
                message2 = message[1].split("}")
                message2 = message2[1]
                message = message[0]
                await channel.send(f"{message}{member}{message2}")
            for role in member.roles:
                if str(role).lower() == "muted":
                    mutedMembers.append(str(member))

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.display_name}'s info for {ctx.guild.name}:",
                              color=random.choice(embedColors))
        created = str(member.created_at).split(" ")
        time = created[0].split("-")
        months = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July", "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"}
        month = months[str(int(time[1]))]
        joined = str(member.joined_at).split(" ")
        newJoin = joined[1].split(".")
        del joined[1]
        joined.append(newJoin)
        joined[1][0].split(":")
        joinTime = joined[0].split("-")
        joinMonth = months[str(int(joinTime[1]))]
        embed.add_field(name=f"Joined at:", value=f"{joinMonth} {joinTime[2]}, {joinTime[0]}")
        embed.add_field(name="Account created at: ", value=f"{month} {time[2]}, {time[0]}")
        memberRoles = member.roles
        roles = [role.mention for role in memberRoles if role != ctx.guild.default_role]
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
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modmute(self, ctx, member: discord.Member):

        with open("../Bots/servers.json", "r") as f:
            storage = json.load(f)
        if "mutedmods" not in storage[str(ctx.guild.id)].keys():
            storage[str(ctx.guild.id)]["mutedmods"] = {}
        mutedMods = storage[str(ctx.guild.id)]["mutedmods"]
        if str(member.id) == "670493561921208320":
            if str(ctx.author.id) == "670493561921208320":
                embed = discord.Embed(
                    description=f"NUUUU {ctx.author.mention} why would you mute yourself??? You don't get muted. I love you.")
            else:
                embed = discord.Embed(
                    description=f"Uh NOPE {ctx.author.mention}, you ain't pullin that one on my creator. You know what? I'm gonna mute YOU instead.")
                mutedMods[str(ctx.author)] = str(ctx.guild)
        elif str(member.id) == "736283988628602960":
            embed = discord.Embed(description=f"HA you stupid idiot you thought you could mute me? NO son, u gettin the mute instead.", color=discord.Color.red())
            mutedMods[str(ctx.author.id)] = str(ctx.guild)
        elif str(member.id) not in mutedMods.keys():
            embed = discord.Embed(description=f"*<:check:742198670912651316> {member.mention} has been modmuted by {ctx.author.mention}.*",
                                  color=discord.Color.green())
            mutedMods[str(member.id)] = str(ctx.guild.id)
        else:
            embed = discord.Embed(description=f"*<:x_:742198871085678642> {member.mention} is already muted {ctx.author.mention}!*",
                                  color=discord.Color.red())
        await ctx.send(embed=embed)
        storage[str(ctx.guild.id)]["mutedmods"] = mutedMods
        with open("../Bots/servers.json", "w") as f:
            json.dump(storage, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modunmute(self, ctx, member: discord.Member):
        with open("../Bots/servers.json", "r") as f:
            storage = json.load(f)
        if "mutedmods" not in storage[str(ctx.guild.id)].keys():
            storage[str(ctx.guild.id)]["mutedmods"] = {}
        mutedMods = storage[str(ctx.guild.id)]["mutedmods"]
        if str(member.id) in mutedMods.keys() and str(ctx.author.id) not in mutedMods.keys():
            embed = discord.Embed(description=f"*<:check:742198670912651316> {member.mention} has been unmuted by {ctx.author.mention}.*",
                                  color=discord.Color.green())
            mutedMods.pop(str(member.id))
        else:
            embed = discord.Embed(description=f"*<:x_:742198871085678642>{member.mention} is not muted {ctx.author.mention}!*",
                                  color=discord.Color.red())

        await ctx.send(embed=embed)
        storage[str(ctx.guild.id)]["mutedmods"] = mutedMods
        with open("../Bots/servers.json") as f:
            json.dump(storage, f, indent=4)



    @commands.command(aliases=["Timer", "TIMER", "remind", "REMIND", "Remind", "reminder", "Reminder", "REMINDER"])
    async def timer(self, ctx, time, *, reminder="No reminder"):
        timerTime = []
        minute = True
        hour = False
        day = False
        second = False
        for char in time:
            if char.lower() == "m":
                minute = True
            elif char.lower() == "h":
                hour = True
                minute = False
            elif char.lower() == "d":
                day = True
                minute = False
            elif char.lower() == "s":
                second = True
                minute = False
            elif isinstance(char, str):
                timerTime.append(char)
            else:
                pass
        time = "".join(timerTime)
        time = int(time)
        if minute:
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} minutes!")
            await asyncio.sleep(time * 60)
        elif hour:
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} hours!")
            await asyncio.sleep(time * 3600)
        elif day:
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} days!")
            await asyncio.sleep(time * 86400)
        elif second:
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} seconds!")
            await asyncio.sleep(time)
        else:
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} minutes!")
            await asyncio.sleep(time * 60)
        await ctx.send(f"{ctx.author.mention} your timer is up!\nReminder: {reminder}")

    @commands.Cog.listener()
    #@is_me("spamcheck")
    async def on_message(self, message):
        mentions = 0
        content = message.content.split(" ")
        for i in content:
            if i.find(f"<") != -1 and i.find(f">") != -1 and i.find(f"@") != -1:
                mentions += 1
        for i in content:
            if i.find("@everyone") != -1 or i.find(str(message.guild.default_role)) != -1:
                mentions += 1
        if mentions >= 3:
            await message.delete()
            ctx = await self.bot.get_context(message, cls=discord.ext.commands.context.Context)
            await self.mute(ctx, message.author, f"Spam pinging in {message.channel.mention}")

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(member.avatar_url)




def setup(bot):
    bot.add_cog(MemberCog(bot))
