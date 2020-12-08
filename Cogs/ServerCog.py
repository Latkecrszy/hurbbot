import discord
import json
from discord.ext import commands
import random
import asyncio

commandsFile = '/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json'

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.editList = {}

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, command):
        found = False
        disabled = True
        with open(commandsFile, 'r') as f:
            commandsList = json.load(f)
        activeList = commandsList[str(ctx.guild.id)]
        for Command, condition in activeList.items():
            if Command == command:
                found = True
                if condition == "True":
                    activeList[Command] = 'False'
                    embed = discord.Embed(title=f"***<a:check:771786758442188871> {command} has been disabled.***",
                                          description=None, color=discord.Color.green())
                    await ctx.send(embed=embed)
                    commandsList[str(ctx.guild.id)] = activeList
                    disabled = False

        with open(commandsFile, 'w') as f:
            json.dump(commandsList, f, indent=4)

        if not found:
            await ctx.send(f"I could not find that command, {ctx.author.mention}!")

        if disabled and found:
            embed = discord.Embed(title=f"***<a:no:771786741312782346> {command} is already disabled.***",
                                  description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def enable(self, ctx, command):
        found = False
        enabled = True
        with open(commandsFile, 'r') as f:
            commandsList = json.load(f)
        activeList = commandsList[str(ctx.guild.id)]
        for Command, condition in activeList.items():
            if Command.lower() == command.lower():
                found = True
                if condition == "False":
                    activeList[Command] = 'True'
                    embed = discord.Embed(title=f"***<a:check:771786758442188871> {command} has been enabled.***",
                                          description=None, color=discord.Color.green())
                    await ctx.send(embed=embed)
                    commandsList[str(ctx.guild.id)] = activeList
                    enabled = False

        with open(commandsFile, 'w') as f:
            json.dump(commandsList, f, indent=4)

        if enabled and found:
            embed = discord.Embed(title=f"***<a:no:771786741312782346> {command} is already enabled.***",
                                  description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

        if not found:
            await ctx.send(f"I could not find that command, {ctx.author.mention}!")

    @commands.command(aliases=["setwelcomechannel"])
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx, channel: discord.TextChannel, *, message=None):
        with open("../servers.json", "r") as f:
            storage = json.load(f)
        if message is not None:
            if str(ctx.guild.id) in storage["welcome"]:
                storage["welcome"].pop(str(ctx.guild.id))
            storage["welcome"][str(ctx.guild.id)] = {str(channel.id): str(message)}
            with open("../servers.json", "w") as f:
                json.dump(storage, f, indent=4)
            await ctx.send(
                f"Ok, {ctx.author.mention}, I've set the welcome channel for this server to {channel.mention}!")
        else:
            await ctx.send(f"Please specify a message to display when people arrive, {ctx.author.mention}!")

    @commands.command(aliases=["setgoodbyechannel"])
    @commands.has_permissions(administrator=True)
    async def goodbye(self, ctx, channelName: discord.TextChannel, *, message=None):
        with open("/Bots/goodbye.json", "r") as f:
            goodbyeChannels = json.load(f)
        if message is not None and str(channelName).lower() != "none":
            if channelName in ctx.guild.text_channels:
                goodbyeChannels.pop(str(ctx.guild.id))
                goodbyeChannels[str(ctx.guild.id)] = {str(channelName): str(message)}
                await ctx.send(
                    f"Ok, {ctx.author.mention}, I've set the goodbye channel for this server to {channelName}!")
            else:
                await ctx.send(
                    "Hmm, I couldn't find that channel on this server. Try checking the spelling, and making sure that you are using a text channel, and try again!")

            with open("/Bots/goodbye.json", "w") as f:
                json.dump(goodbyeChannels, f, indent=4)
        elif str(channelName).lower() == "none":
            goodbyeChannels.pop(str(ctx.guild.id))
            goodbyeChannels[str(ctx.guild.id)] = "None"
        else:
            await ctx.send(f"Please specify a message to display when people leave, {ctx.author.mention}!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('/Bots/prefixes.json', 'r') as h:
            prefixes = json.load(h)

        prefixes[str(guild.id)] = '%'

        with open('/Bots/prefixes.json', 'w') as g:
            json.dump(prefixes, g, indent=4)
        with open(commandsFile, 'r') as f:
            commandsList = json.load(f)
        commandsList[str(guild.id)] = {"goodbye": "False", "nitro": "True", "nonocheck": "False", "welcome": "False",
                                       "invitecheck": "False", "linkcheck": "False", "ranking": "True"}
        with open(commandsFile, 'w') as f:
            json.dump(commandsList, f, indent=4)

        with open('/Bots/welcome.json', 'r') as a:
            welcomeChannels = json.load(a)

        welcomeChannels[str(guild.id)] = "None"

        with open('/Bots/welcome.json', 'w') as b:
            json.dump(welcomeChannels, b, indent=4)

        with open('/Bots/goodbye.json', 'r') as c:
            goodbyeChannels = json.load(c)

        goodbyeChannels[str(guild.id)] = "None"

        with open('/Bots/goodbye.json', 'w') as d:
            json.dump(goodbyeChannels, d, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('/Bots/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('/Bots/prefixes.json', 'w') as a:
            json.dump(prefixes, a, indent=4)

        with open("/Bots/welcome.json", "r") as b:
            welcomeChannels = json.load(b)

        welcomeChannels.pop(str(guild.id))

        with open("/Bots/welcome.json", "w") as c:
            json.dump(welcomeChannels, c, indent=4)

        with open("/Bots/goodbye.json", "r") as d:
            goodbyeChannels = json.load(d)

        goodbyeChannels.pop(str(guild.id))

        with open("/Bots/goodbye.json", "w") as e:
            json.dump(goodbyeChannels, e, indent=4)

        with open(commandsFile, "r") as g:
            commandsList = json.load(g)

        commandsList.pop(str(guild.id))

        with open(commandsFile, "w") as h:
            json.dump(commandsList, h, indent=4)

    @commands.command(aliases=["mutechannel", "lockdown", "lock"])
    @commands.has_permissions(manage_guild=True)
    async def channelmute(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel

        self.editList[str(channel.id)] = []
        for role in ctx.guild.roles:
            perms = channel.overwrites_for(role)
            if perms.send_messages:
                perms.send_messages = False
                await channel.set_permissions(role, overwrite=perms)
                self.editList[str(channel.id)].append(str(role))
        await ctx.send(
            embed=discord.Embed(description=f"<a:check:771786758442188871> {channel.mention} has been locked.",
                                color=discord.Color.green()))

    @commands.command(aliases=["unmutechannel", "unlock", "unlockdown", "unchannelmute"])
    @commands.has_permissions(manage_guild=True)
    async def channelunmute(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        for role in ctx.guild.roles:
            perms = channel.overwrites_for(role)
            if str(role) in self.editList[str(channel.id)]:
                perms.send_messages = True
                await channel.set_permissions(role, overwrite=perms)
        await ctx.send(
            embed=discord.Embed(description=f"<a:check:771786758442188871> {channel.mention} has been unlocked.",
                                color=discord.Color.green()))
        self.editList.pop(str(channel.id))

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite link for Hurb",
                                           description=f"*Click [here]({'https://discord.com/oauth2/authorize?client_id=736283988628602960&permissions=8&scope=bot'}) to invite Hurb to your server!*",
                                           color=discord.Color.green()))

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(color=random.choice(embedColors))

        embed.add_field(name="<:owner:779163811172319232>  Server owner", value=ctx.guild.owner.mention)
        if ctx.guild.premium_subscription_count != 0:
            embed.add_field(name="<a:boost:779165947361624087>  Server Boost Level",
                            value=f"Level {ctx.guild.premium_tier} with {ctx.guild.premium_subscription_count} Boosts")  # 3

        embed.add_field(
            name=f":speech_balloon:  {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)} Channels",
            value=f"<:textchannel:779163783712342017> {len(ctx.guild.text_channels)} text channels\n<:voicechannel:779163754931552306> {len(ctx.guild.voice_channels)} voice channels")  # 5
        embed.add_field(name=f"<:members:779163840201621534>  {len(ctx.guild.members)} Members",
                        value=f"👨 Humans: {len([str(member) for member in ctx.guild.members if not member.bot])}\n🤖 Bots: {len([str(member) for member in ctx.guild.members if member.bot])}")

        embed.add_field(name=f"<a:emojis:779163904592445461>  {len(ctx.guild.emojis)} Emojis",
                        value=f"**<a:catroll:779406198935781376>  {len(ctx.guild.roles)} Roles**")
        embed.add_field(name=f"🗓️ Date Created", value=self.calcdate(ctx.guild))
        embed.set_author(name=f"{ctx.guild} Info", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    def calcdate(self, guild):
        months = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July",
                  "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"}
        created = str(guild.created_at).split(" ")
        newCreate = created[1].split(".")
        del created[1]
        created.append(newCreate)
        created[1][0].split(":")
        createTime = created[0].split("-")
        createMonth = months[str(int(createTime[1]))]
        return f"{createMonth} {createTime[2]}, {createTime[0]}"

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def slowmode(self, ctx, time):
        channel = ctx.channel
        await channel.edit(slowmode_delay=int(time))
        await ctx.send(embed=discord.Embed(description=f"{channel.mention} now has a slowmode of {time} seconds.",
                                           color=discord.Color.green()))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def autorole(self, ctx, *, role: discord.Role):
        with open(
                "/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/autoroles.json") as f:
            autoroles = json.load(f)

        if str(ctx.guild.id) not in autoroles.keys():
            autoroles[str(ctx.guild.id)] = []

        autoroles[str(ctx.guild.id)].append(str(role))
        with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/autoroles.json",
                  "w") as f:
            json.dump(autoroles, f, indent=4)

        await ctx.send(embed=discord.Embed(
            description=f"{role.mention} has been set as an autorole for this server {ctx.author.mention}!"))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removeautorole(self, ctx, *, role: discord.Role):
        with open(
                "/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/autoroles.json") as f:
            autoroles = json.load(f)

        if str(ctx.guild.id) not in autoroles.keys():
            await ctx.send(
                embed=discord.Embed(description=f"You do not have any autoroles for this server {ctx.author.mention}!",
                                    color=discord.Color.red()))
        elif str(role) not in autoroles[str(ctx.guild.id)]:
            await ctx.send(embed=discord.Embed(description=f"This role is not an autorole {ctx.author.mention}!",
                                               color=discord.Color.red()))
        else:
            for i in range(len(autoroles[str(ctx.guild.id)])):
                if str(i).lower() == str(role).lower():
                    autoroles[str(ctx.guild.id)].pop(i)
            with open(
                    "/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/autoroles.json",
                    "w") as f:
                json.dump(autoroles, f, indent=4)

            await ctx.send(embed=discord.Embed(
                description=f"{role.mention} has been removed as an autorole for this server {ctx.author.mention}!"))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, message, number):
        await message.channel.purge(limit=int(int(number) + 1))
        embed = discord.Embed(description=f"\U0001f44d **Purged {number} messages in {message.channel.mention}.**")
        embed.set_footer(text="This message will be deleted in 3 seconds.")
        newMessage = await message.channel.send(embed=embed)
        await asyncio.sleep(3)
        try:
            await newMessage.delete()
        except:
            pass

    @commands.command(aliases=["membercount", "Memcount", "MEMCOUNT", "Membercount", "MEMBERCOUNT"])
    async def memcount(self, ctx):
        members = [str(member) for member in ctx.guild.members if not member.bot]
        bots = [str(member) for member in ctx.guild.members if member.bot]
        Members = [str(member) for member in ctx.guild.members]
        embed = discord.Embed()
        embed.add_field(name="Members:", value=f"**{len(Members)}\nHumans: {len(members)}\nBots: {len(bots)}**")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

    @commands.command()
    async def role(self, ctx, role: discord.Role):
        members_with_role = []
        for member in ctx.guild.members:
            if role in member.roles:
                members_with_role.append(member)
        await ctx.send(
            f"Members with the {role.mention} role:\n{' '.join([member.mention for member in members_with_role])}")


def setup(bot):
    bot.add_cog(ServerCog(bot))
