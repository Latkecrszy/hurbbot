import discord
import json
from discord.ext import commands
import random
import asyncio

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
        self.everyoneStatus = {}

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, command):
        found = False
        disabled = True
        with open('servers.json', 'r') as f:
            storage = json.load(f)
            commandsList = storage[str(ctx.guild.id)]["commands"]
        for Command, condition in commandsList.items():
            if Command == command.lower():
                found = True
                if condition == "True":
                    commandsList[Command] = 'False'
                    embed = discord.Embed(title=f"***<a:check:771786758442188871> {command} has been disabled.***",
                                          description=None, color=discord.Color.green())
                    await ctx.send(embed=embed)
                    storage[str(ctx.guild.id)]["commands"] = commandsList
                    disabled = False

        with open('servers.json', 'w') as f:
            json.dump(storage, f, indent=4)

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
        with open('servers.json', 'r') as f:
            storage = json.load(f)
            commandsList = storage[str(ctx.guild.id)]["commands"]
        for Command, condition in commandsList.items():
            if Command == command.lower():
                found = True
                if condition == "False":
                    commandsList[Command] = 'True'
                    embed = discord.Embed(title=f"***<a:check:771786758442188871> {command} has been enabled.***",
                                          description=None, color=discord.Color.green())
                    await ctx.send(embed=embed)
                    storage[str(ctx.guild.id)]["commands"] = commandsList
                    enabled = False

        with open('servers.json', 'w') as f:
            json.dump(storage, f, indent=4)

        if not found:
            await ctx.send(f"I could not find that command, {ctx.author.mention}!")

        if enabled and found:
            embed = discord.Embed(title=f"***<a:no:771786741312782346> {command} is already enabled.***",
                                  description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=["setwelcomechannel"])
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx, channel: discord.TextChannel, *, message=None):
        with open("servers.json", "r") as f:
            storage = json.load(f)
        if message is not None:
            if "welcome" in storage[str(ctx.guild.id)].keys():
                storage[str(ctx.guild.id)].pop("welcome")
            storage[str(ctx.guild.id)]["welcome"] = {"id": str(channel.id), "message": str(message)}
            with open("servers.json", "w") as f:
                json.dump(storage, f, indent=4)
            await ctx.send(
                f"Ok, {ctx.author.mention}, I've set the welcome channel for this server to {channel.mention}!")
        else:
            await ctx.send(f"Please specify a message to display when people arrive, {ctx.author.mention}!")

    @commands.command(aliases=["setgoodbyechannel"])
    @commands.has_permissions(manage_guild=True)
    async def goodbye(self, ctx, channel: discord.TextChannel, *, message=None):
        with open("servers.json", "r") as f:
            storage = json.load(f)
        if message is not None:
            if "goodbye" in storage[str(ctx.guild.id)].keys():
                storage[str(ctx.guild.id)].pop("goodbye")
            storage[str(ctx.guild.id)]["goodbye"] = {"id": str(channel.id), "message": str(message)}
            with open("servers.json", "w") as f:
                json.dump(storage, f, indent=4)
            await ctx.send(
                f"Ok, {ctx.author.mention}, I've set the goodbye channel for this server to {channel.mention}!")
        else:
            await ctx.send(f"Please specify a message to display when people leave, {ctx.author.mention}!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('servers.json', 'r') as f:
            storage = json.load(f)
        if str(guild.id) not in storage.keys():
            storage[str(guild.id)] = {"prefix": '%',
                                      "commands": {"goodbye": "False", "nitro": "True", "nonocheck": "False",
                                                   "welcome": "False",
                                                   "invitecheck": "False", "linkcheck": "False", "antispam": "False",
                                                   "ranking": "True", "economy": "True", "moderation": "True"},
                                      "blacklist": {},
                                      "goodbye": {},
                                      "levelupmessage": "Congrats {member}! You leveled up to level {level}!",
                                      "levelroles": {}}

        with open('servers.json', 'w') as f:
            json.dump(storage, f, indent=4)

    @commands.command(aliases=["mutechannel", "lockdown", "lock"])
    @commands.has_permissions(manage_guild=True)
    async def channelmute(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel

        self.editList[str(channel.id)] = []
        everyonePerms = channel.overwrites_for(ctx.guild.default_role)
        if everyonePerms.send_messages or everyonePerms.send_messages is None:
            self.everyoneStatus[str(channel.id)] = everyonePerms.send_messages
            everyonePerms.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=everyonePerms)
        for role in ctx.guild.roles:
            if role != ctx.guild.default_role:
                perms = channel.overwrites_for(role)
                if perms.send_messages:
                    perms.send_messages = False
                    await channel.set_permissions(role, overwrite=perms)
                    self.editList[str(channel.id)].append(role.id)
        await ctx.send(
            embed=discord.Embed(description=f"<a:check:771786758442188871> {channel.mention} has been locked.",
                                color=discord.Color.green()))

    @commands.command(aliases=["unmutechannel", "unlock", "unlockdown", "unchannelmute"])
    @commands.has_permissions(manage_guild=True)
    async def channelunmute(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        prevPerms = channel.overwrites_for(ctx.guild.default_role)
        prevPerms.send_messages = self.everyoneStatus[str(channel.id)]
        await channel.set_permissions(ctx.guild.default_role, overwrite=prevPerms)
        for role in ctx.guild.roles:
            perms = channel.overwrites_for(role)
            if role.id in self.editList[str(channel.id)]:
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
    async def serverInfo(self, ctx, *, server=None):
        if server is not None:
            guild = discord.utils.get(self.bot.guilds, name=server)
        else:
            guild = ctx.guild
        embed = discord.Embed(color=random.choice(embedColors))

        embed.add_field(name="<:owner:779163811172319232>  Server owner", value=guild.owner.mention)
        if guild.premium_subscription_count != 0:
            embed.add_field(name="<a:boost:779165947361624087>  Server Boost Level",
                            value=f"Level {guild.premium_tier} with {guild.premium_subscription_count} Boosts")  # 3

        embed.add_field(
            name=f":speech_balloon:  {len(guild.text_channels) + len(guild.voice_channels)} Channels",
            value=f"<:textchannel:779163783712342017> {len(guild.text_channels)} text channels\n<:voicechannel:779163754931552306> {len(guild.voice_channels)} voice channels")  # 5
        embed.add_field(name=f"<:members:779163840201621534>  {len(guild.members)} Members",
                        value=f"👨 Humans: {len([str(member) for member in guild.members if not member.bot])}\n🤖 Bots: {len([str(member) for member in guild.members if member.bot])}")

        embed.add_field(name=f"<a:emojis:779163904592445461>  {len(guild.emojis)} Emojis",
                        value=f"**<a:catroll:779406198935781376>  {len(guild.roles)} Roles**")
        embed.add_field(name=f"🗓️ Date Created", value=self.calcDate(guild))
        embed.set_author(name=f"{guild} Info", icon_url=guild.icon_url)
        await ctx.send(embed=embed)

    def calcDate(self, guild):
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
        with open("servers.json") as f:
            storage = json.load(f)
        if "autoroles" not in storage[str(ctx.guild.id)].keys():
            storage[str(ctx.guild.id)]["autoroles"] = []
        storage[str(ctx.guild.id)]["autoroles"].append(str(role.id))
        with open("servers.json",
                  "w") as f:
            json.dump(storage, f, indent=4)

        await ctx.send(embed=discord.Embed(
            description=f"{role.mention} has been set as an autorole for this server {ctx.author.mention}!"))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removeautorole(self, ctx, *, role: discord.Role):
        with open("servers.json") as f:
            storage = json.load(f)
        autoroles = storage[str(ctx.guild.id)]["autoroles"]
        for i in range(len(autoroles[str(ctx.guild.id)])):
            if str(i).lower() == str(role).lower():
                autoroles[str(ctx.guild.id)].pop(i)
        storage[str(ctx.guild.id)]["autoroles"] = autoroles
        with open("servers.json", "w") as f:
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

    @commands.command(aliases=["membercount"])
    async def memcount(self, ctx):
        members = [str(member) for member in ctx.guild.members if not member.bot]
        bots = [str(member) for member in ctx.guild.members if member.bot]
        Members = [str(member) for member in ctx.guild.members]
        embed = discord.Embed()
        embed.add_field(name="Members:", value=f"**{len(Members)}\nHumans: {len(members)}\nBots: {len(bots)}**")
        await ctx.send(embed=embed)

    @commands.command()
    async def role(self, ctx, role: discord.Role):
        members_with_role = []
        for member in ctx.guild.members:
            if role in member.roles:
                members_with_role.append(member)
        await ctx.send(
            f"Members with the {role.mention} role:\n{' '.join([member.mention for member in members_with_role])}")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        with open("servers.json") as f:
            storage = json.load(f)

        if "commandCount" not in storage[str(ctx.guild.id)].keys():
            storage[str(ctx.guild.id)]["commandCount"] = 0
        storage[str(ctx.guild.id)]["commandCount"] += 1
        json.dump(storage, open("servers.json", "w"), indent=4)

    @commands.command()
    async def Commands(self, ctx, condition=None):
        if condition is None:
            storage = json.load(open("servers.json"))
            await ctx.send(
                f"`{storage[str(ctx.guild.id)]['commandCount']}` commands have been sent in `{ctx.guild.name}`.")
        elif condition.lower() == "all":
            storage = json.load(open("servers.json"))
            totalCommands = 0
            for value in storage.values():
                try:
                    totalCommands += value["commandCount"]
                except:
                    pass
            await ctx.send(f"{totalCommands} commands have been sent.")

    @commands.command()
    async def commandCount(self, ctx):
        await ctx.send(len(self.bot.commands))




def setup(bot):
    bot.add_cog(ServerCog(bot))
