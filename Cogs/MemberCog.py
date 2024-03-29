from discord.ext import commands
import asyncio, os, discord, pymongo
from Bots.Cogs.mongoclient import MotorClient as client
from motor.motor_asyncio import AsyncIOMotorClient
mutedMembers = []


def muteTimeCalc(muteTime):
    muteList = []
    multiplier = 1
    for char in muteTime:
        if char.lower() == "m":
            multiplier = 60
        elif char.lower() == "h":
            multiplier = 3600
        elif char.lower() == "d":
            multiplier = 86400
        elif char.lower() == "s":
            multiplier = 1
        elif char.isnumeric():
            muteList.append(char)
    muteTime = int("".join(muteList))
    muteTime *= multiplier
    return muteTime


async def muteRole(ctx):
    role = discord.utils.get(ctx.guild.roles, name="muted")
    if role is None:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role is None:
        role = await ctx.guild.create_role(name="muted", color=discord.Color.dark_grey())
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(send_messages=False))
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
        self.spammers = {}


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def mute(self, ctx, member: discord.Member, *, reason="There was no reason for this muting."):
        if not member.guild_permissions.administrator:
            role = await muteRole(ctx)
            if role not in member.roles:
                embed = discord.Embed(
                    description=f"***<a:check:771786758442188871>  {member.mention} has been muted.***",
                    color=discord.Color.green())
                self.mutedRoles[str(member.id)] = []
                embed.set_footer(text=f"Reason:  {reason}")
                for roles in member.roles:
                    if roles != ctx.guild.default_role:
                        self.mutedRoles[str(member.id)].append(roles) if roles != ctx.guild.default_role else None
                        await member.remove_roles(roles)
                await member.add_roles(role, reason=reason)
                await ctx.send(embed=embed)


            else:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"***<a:no:771786741312782346>  {member.mention} is already muted!***",
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
                self.mutedRoles[str(member.id)] = []
                embed = discord.Embed(
                    description=f"***<a:check:771786758442188871>  {member.mention} has been muted for {muteTime} seconds.***",
                    colour=discord.Colour.green())
                embed.set_footer(text=f"Reason: {reason}")
                try:
                    await member.add_roles(role, reason=reason)
                    await ctx.send(embed=embed)
                except discord.errors.Forbidden:
                    await ctx.send(embed=discord.Embed(
                        description=f"I do not have the required permissions to mute that person {ctx.author.mention}! To fix this, please try either moving my role higher than the mute role, or giving me the `manage_roles` permission."))
                for roles in member.roles:
                    if roles != ctx.guild.default_role and roles != role:
                        self.mutedRoles[str(member.id)].append(roles)
                        await member.remove_roles(roles)
                await asyncio.sleep(int(muteTime))
                await self.unmute(ctx, member)
            else:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"***<a:no:771786741312782346>  {member.mention} is already muted!***",
                        color=discord.Colour.red()))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"***<a:no:771786741312782346>  I can't do that, as {member.mention} is an administrator.***",
                color=discord.Colour.red()))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unmute(self, ctx, member: discord.Member):
        role = await muteRole(ctx)
        if str(member.id) in self.mutedRoles.keys() or role in member.roles:
            await member.remove_roles(role)
            if str(member.id) in self.mutedRoles.keys():
                for roles in self.mutedRoles[str(member.id)]:
                    await member.add_roles(roles)
                for x in range(len(self.mutedRoles[str(member.id)])):
                    self.mutedRoles[str(member.id)].pop(0)
            await ctx.send(
                embed=discord.Embed(
                    description=f"***<a:check:771786758442188871>  {member.mention} has been unmuted.***",
                    color=discord.Colour.green()))
        else:
            await ctx.send(
                embed=discord.Embed(description=f"***<a:no:771786741312782346>  {member.mention} is not muted!***",
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
            try:
                await member.send(embed=discord.Embed(title=f"You have been kicked from {ctx.guild.name} by {ctx.author}.",
                                                    description=f"Reason: {reason}",
                                                    color=discord.Color.red()))
            except discord.errors.HTTPException:
                pass
            await ctx.guild.kick(member)
            embed = discord.Embed(
                description=f"***<a:check:771786758442188871> {member.mention} has been kicked by {ctx.author.mention}.***",
                color=discord.Color.green())
            embed.set_footer(text=f"Reason: {reason}")
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=discord.Embed(
                description=f"***<a:no:771786741312782346> {member.mention} has failed to be kicked by {ctx.author.mention} because they are an admin/mod.***",
                color=discord.Color.red()))

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.User, *, reason="There was no reason for this banning."):
        try:
            try:
                await member.send(
                    embed=discord.Embed(title=f"You have been banned from {ctx.guild.name} by {ctx.author}.",
                                        description=f"Reason: {reason}",
                                        color=discord.Color.red()))
            except:
                pass
            await ctx.guild.ban(member)
            embed = discord.Embed(
                description=f"***<a:check:771786758442188871> {member.mention} has been banned by {ctx.author.mention}.***",
                color=discord.Color.green())
            embed.set_footer(text=f"Reason: {reason}")
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=discord.Embed(
                title=f"*<a:no:771786741312782346> {member} has failed to be banned by {ctx.author.display_name} because they are an admin/mod.*",
                description=None, color=discord.Color.red()))

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def unban(self, ctx, member: discord.User):
        await ctx.guild.unban(member)
        await ctx.send(f"{member} has been unbanned from {ctx.guild}.")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, member: discord.Member = None, *, new_name):
        await member.edit(nick=new_name)
        await ctx.send(
            embed=discord.Embed(
                description=f"***{member} has been renamed to {member.mention} by {ctx.author.mention}.***",
                color=discord.Color.green()))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        if not member.guild_permissions.administrator:
            await member.send(embed=discord.Embed(title=f"You have been warned in **{ctx.guild}** by **{ctx.author}**.",
                                                  description=f"Reason: {reason}"))
            embed = discord.Embed(
                description=f"***<a:check:771786758442188871> {member.mention} has been warned.***",
                colour=discord.Colour.green())
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(
                title=f"***<a:no:771786741312782346> {member.display_name} cannot be warned, as they are an administrator.***",
                color=discord.Color.red()))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        storage = await self.bot.cluster.find_one({"id": str(member.guild.id)})
        if "welcome" in storage:
            print(storage)
            if "id" in storage["welcome"]:
                channel = member.guild.get_channel(int(storage["welcome"]["id"]))
                message = storage["welcome"]["message"]
                await channel.send(message.format(member=member.mention))
                for role in member.roles:
                    if str(role).lower() == "muted":
                        mutedMembers.append(str(member))

            await self.bot.cluster.find_one_and_replace({"id": str(member.guild.id)}, storage)

        if "autoroles" in storage.keys():
            for role in storage["autoroles"]:
                addRole = discord.utils.get(member.guild.roles, name=role)
                if addRole is not None:
                    await member.add_roles(addRole)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        storage = await self.bot.cluster.find_one({"id": str(member.guild.id)})
        if "goodbye" in storage.keys():
            goodbyeChannels = storage["goodbye"]
            if "id" in goodbyeChannels:
                channel = member.guild.get_channel(int(goodbyeChannels["id"]))
                message = goodbyeChannels["message"]
                if message.find("{member}"):
                    await channel.send(message.format(member=member.mention))
                for role in member.roles:
                    if str(role).lower() == "muted":
                        mutedMembers.append(str(member))

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.display_name}'s info for {ctx.guild.name}:")
        created = str(member.created_at).split(" ")
        time = created[0].split("-")
        months = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July",
                  "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"}
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
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        if "mutedmods" not in storage.keys():
            storage["mutedmods"] = {}
        mutedMods = storage["mutedmods"]
        if str(member.id) == "670493561921208320":
            if str(ctx.author.id) == "670493561921208320":
                embed = discord.Embed(
                    description=f"NUUUU {ctx.author.mention} why would you mute yourself??? You don't get muted. I love you.")
            else:
                embed = discord.Embed(
                    description=f"Uh NOPE {ctx.author.mention}, you ain't pullin that one on my creator. You know what? I'm gonna mute YOU instead.")
                mutedMods[str(ctx.author.id)] = str(ctx.guild.id)
        elif str(member.id) == "736283988628602960":
            embed = discord.Embed(
                description=f"HA you stupid idiot you thought you could mute me? NO son, u gettin the mute instead.",
                color=discord.Color.red())
            mutedMods[str(ctx.author.id)] = str(ctx.guild.id)
        elif str(member.id) not in mutedMods.keys():
            embed = discord.Embed(
                description=f"*<a:check:771786758442188871> {member.mention} has been modmuted by {ctx.author.mention}.*",
                color=discord.Color.green())
            mutedMods[str(member.id)] = str(ctx.guild.id)
        else:
            embed = discord.Embed(
                description=f"*<a:no:771786741312782346> {member.mention} is already muted {ctx.author.mention}!*",
                color=discord.Color.red())
        await ctx.send(embed=embed)
        storage["mutedmods"] = mutedMods
        await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)

    @commands.command(aliases=["unmodmute"])
    @commands.has_permissions(administrator=True)
    async def modunmute(self, ctx, member: discord.Member):
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        if "mutedmods" not in storage.keys():
            storage["mutedmods"] = {}
        mutedMods = storage["mutedmods"]
        if str(member.id) in mutedMods.keys() and str(ctx.author.id) not in mutedMods.keys():
            embed = discord.Embed(
                description=f"*<a:check:771786758442188871> {member.mention} has been unmuted by {ctx.author.mention}.*",
                color=discord.Color.green())
            mutedMods.pop(str(member.id))
        else:
            embed = discord.Embed(
                description=f"*<a:no:771786741312782346>{member.mention} is not muted {ctx.author.mention}!*",
                color=discord.Color.red())

        await ctx.send(embed=embed)
        storage["mutedmods"] = mutedMods
        await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)

    @commands.command(aliases=["reminder"])
    async def timer(self, ctx, time, *, reminder="No reminder"):
        timerTime = []
        unit = "minute"
        for char in time:
            if char.lower() == "m":
                unit = "minute"
            elif char.lower() == "h":
                unit = "hour"
            elif char.lower() == "d":
                unit = "day"
            elif char.lower() == "s":
                unit = "second"
            elif isinstance(char, str):
                timerTime.append(char)
            else:
                pass
        time = "".join(timerTime)
        time = int(time)
        if unit == "minute":
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} minutes!")
            await asyncio.sleep(time * 60)
        elif unit == "hour":
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} hours!")
            await asyncio.sleep(time * 3600)
        elif unit == "day":
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} days!")
            await asyncio.sleep(time * 86400)
        elif unit == "second":
            await ctx.send(f"{ctx.author.mention} your timer has been set for {time} seconds!")
            await asyncio.sleep(time)
        await ctx.send(f"{ctx.author.mention} your timer is up!\nReminder: {reminder}")

    async def spamcheck(self, message, storage):
        if storage["commands"]["antispam"] == "True":
            mentions = 0
            content = message.content.split(" ")
            for i in content:
                if i.find(f"<") != -1 and i.find(f">") != -1 and i.find(f"@") != -1:
                    mentions += 1
                if i.find("@everyone") != -1 or i.find(str(message.guild.default_role)) != -1:
                    mentions += 1
            if mentions >= 3:
                ctx = await self.bot.get_context(message, cls=discord.ext.commands.context.Context)
                await self.mute(ctx, message.author, reason=f"Spam pinging in {message.channel}")
            elif mentions >= 1:
                if str(message.author.id) in self.spammers.keys():
                    self.spammers[str(message.author.id)] += 1
                else:
                    self.spammers[str(message.author.id)] = 1
            if str(message.author.id) in self.spammers.keys():
                if self.spammers[str(message.author.id)] >= 3:
                    ctx = await self.bot.get_context(message, cls=discord.ext.commands.context.Context)
                    await self.mute(ctx, message.author, reason=f"Spam pinging in {message.channel}")
                await asyncio.sleep(15)
                self.spammers[str(message.author.id)] = 0

    async def blacklistcheck(self, message, storage):
        ctx = await self.bot.get_context(message, cls=discord.ext.commands.context.Context)
        for key, value in storage["blacklist"].items():
            if key in message.content.lower():
                reason = f"Sending the word {key} in {message.guild}."
                await message.delete()
                if value == "ban":
                    await self.ban(ctx, message.author, reason=reason)
                elif value == "kick":
                    await self.kick(ctx, message.author, reason=reason)
                elif value == "mute":
                    await self.mute(ctx, message.author, reason=reason)
                elif value == "warn":
                    await self.warn(ctx, message.author, reason=reason)
                break

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and not isinstance(message.author, discord.User):
            if not message.author.guild_permissions.administrator:
                storage = await self.bot.cluster.find_one({"id": str(message.guild.id)})
                await self.blacklistcheck(message, storage)
                await self.spamcheck(message, storage)

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(member.avatar_url)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def blacklist(self, ctx, condition, word=None, *, punishment=None):
        LINK = os.environ.get("LINK", None)
        Client = pymongo.MongoClient(LINK)
        db = Client['hurb']
        storage = db.settings.find_one({"id": str(ctx.guild.id)})
        if condition.lower() == "add" or condition.lower() == "set":
            punishments = ["ban", "kick", "mute", "warn"]
            word = word.lower()
            if punishment is None:
                await ctx.send(embed=discord.Embed(
                    description=f"Please specify a punishment when ||{word}|| is said {ctx.author.mention}! The punishments to choose from are `{'`, `'.join(punishments)}`, and `delete`.",
                    color=discord.Color.red()))
            elif punishment.lower() in punishments or punishment.lower() == "delete":
                storage["blacklist"][word] = punishment.lower()
                print(storage)
                print(storage['blacklist'])
                LINK = os.environ.get("LINK", None)
                Client = pymongo.MongoClient(LINK)
                db = Client['hurb']
                result = db.settings.find_one_and_replace({'id': str(ctx.guild.id)}, storage)
                await ctx.send(embed=discord.Embed(description=f"||{word}|| has been added to the blacklist.",
                                                   color=discord.Color.green()))
                print("done")
            else:
                await ctx.send(embed=discord.Embed(
                    description=f"Please choose a valid punishment {ctx.author.mention}! Valid punishments are `{'`, `'.join(punishments)}`, and `delete`.",
                    color=discord.Color.red()))
        elif condition.lower() == "remove":
            if word.lower() in storage["blacklist"].keys():
                storage["blacklist"].pop(word.lower())
                await ctx.send(embed=discord.Embed(description=f"{word} has been removed from the blacklist.",
                                                   color=discord.Color.green()))
                await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)
            else:
                await ctx.send(embed=discord.Embed(description=f"{word} is not in the blacklist {ctx.author.mention}!",
                                                   color=discord.Color.red()))
        elif condition.lower() == "view":
            if storage["blacklist"]:
                embed = discord.Embed(title=f"Blacklisted Words")
                for word, punishment in storage["blacklist"].items():
                    embed.add_field(name=f"Word: ||{word}||", value=f"Punishment: **{punishment}**.")

                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=discord.Embed(description=f"There are no blacklisted words in {ctx.guild}!",
                                                   color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"Please choose a valid condition for blacklisting: `add`, `remove`, or `view`.",
                color=discord.Color.red()))


def setup(bot):
    bot.add_cog(MemberCog(bot))
