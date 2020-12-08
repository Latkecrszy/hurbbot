import discord
import json
from discord.ext import commands
import random


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
        self.editList = []

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
                    embed = discord.Embed(title=f"<:check:742198670912651316> Command {command} has been disabled!",
                                          description=None, color=discord.Color.green())
                    await ctx.send(embed=embed)
                    commandsList[str(ctx.guild.id)] = activeList
                    disabled = False

        with open(commandsFile, 'w') as f:
            json.dump(commandsList, f, indent=4)

        if not found:
            await ctx.send(f"I could not find that command, {ctx.author.mention}!")

        if disabled and found:
            embed = discord.Embed(title=f"<:x_:742198871085678642> Command {command} is already disabled!",
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
                    embed = discord.Embed(title=f"<:check:742198670912651316> Command {command} has been enabled!",
                                          description=None, color=discord.Color.green())
                    await ctx.send(embed=embed)
                    commandsList[str(ctx.guild.id)] = activeList
                    enabled = False

        with open(commandsFile, 'w') as f:
            json.dump(commandsList, f, indent=4)

        if enabled and found:
            embed = discord.Embed(title=f"<:x_:742198871085678642> Command {command} is already enabled!",
                                  description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

        if not found:
            await ctx.send(f"I could not find that command, {ctx.author.mention}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel(self, ctx, channelName: discord.TextChannel, *, message=None):
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/welcome.json", "r") as f:
            welcomeChannels = json.load(f)
        if message is not None and str(channelName).lower() != "none":
            if discord.utils.get(ctx.guild.text_channels, name=str(channelName)):
                welcomeChannels.pop(str(ctx.guild.id))
                welcomeChannels[str(ctx.guild.id)] = {str(channelName): str(message)}
                with open("/Users/sethraphael/PycharmProject/Hurb/Bots/welcome.json", "w") as f:
                    json.dump(welcomeChannels, f, indent=4)
                await ctx.send(
                    f"Ok, {ctx.author.mention}, I've set the welcome channel for this server to {channelName}!")
            else:
                await ctx.send(
                    "Hmm, I couldn't find that channel on this server. Try checking the spelling, and making sure that you are using a text channel, and try again!")

        elif str(channelName).lower() == "none":
            await ctx.send(
                "Ok, I won't welcome people to this server.")
            welcomeChannels.pop(str(ctx.guild.id))
            welcomeChannels[ctx.guild.id] = "None"

        else:
            await ctx.send(f"Please specify a message to display when people arrive, {ctx.author.mention}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setgoodbyechannel(self, ctx, channelName: discord.TextChannel, *, message=None):
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/goodbye.json", "r") as f:
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

            with open("/Users/sethraphael/PycharmProject/Hurb/Bots/goodbye.json", "w") as f:
                json.dump(goodbyeChannels, f, indent=4)
        elif str(channelName).lower() == "none":
            goodbyeChannels.pop(str(ctx.guild.id))
            goodbyeChannels[str(ctx.guild.id)] = "None"
        else:
            await ctx.send(f"Please specify a message to display when people leave, {ctx.author.mention}!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/prefixes.json', 'r') as h:
            prefixes = json.load(h)

        prefixes[str(guild.id)] = '%'

        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/prefixes.json', 'w') as g:
            json.dump(prefixes, g, indent=4)

        for channel in guild.text_channels:
            everyone = guild.default_role
            if channel.overwrites_for(everyone).send_messages:
                embed = discord.Embed(title=f"Thank you so much for adding me to {guild.name}! You are server number {len(self.bot.guilds)} to add me!",
                                      description=f"To get started, you'll need to run a few commands to get all set up.")
                embed.add_field(name=f"First, you should use the command `%setwelcomechannel` to set the channel that you would like me to welcome people from, and the message you'd like to display!",
                                value=f"Here's an example: `%setwelcomechannel welcome Hello member! Welcome to Latkecrszy's server!` would tell me to send my welcome messages in a channel called welcome, to welcome them with that message every time, and to replace the word member with their name.")
                embed.add_field(name=f"Once you've done that, you can set the goodbye channel in the same way; with the command `%setgoodbyechannel` instead.",
                                value=f"Finally, once you've done all of that, you can change the server prefix to whatever you want using the `%prefix` command.\nJust say `%prefix !` to change your prefix to `!`. And once you've done that, you're all set! Enjoy the bot!")
                break
        with open(commandsFile, 'r') as f:
            commandsList = json.load(f)
        commandsList[str(guild.id)] = {"authorize": "True", "ban": "True", "gimme": "False", "goodbye": "True",
                                       "kick": "True", "mute": "True", "nitro": "True", "nonocheck": "False",
                                       "numcheck": "True",
                                       "purge": "True", "quiz": "True", "rall": "True", "rename": "True", "rps": "True",
                                       "testreaction": "True", "unmute": "True", "warn": "True", "welcome": "True",
                                       "mutechannel": "True", "invitecheck": "False", "unmutechannel": "True",
                                       "linkcheck": "False"}
        with open(commandsFile, 'w') as f:
            json.dump(commandsList, f, indent=4)

        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/welcome.json', 'r') as a:
            welcomeChannels = json.load(a)

        welcomeChannels[str(guild.id)] = "None"

        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/welcome.json', 'w') as b:
            json.dump(welcomeChannels, b, indent=4)

        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/goodbye.json', 'r') as c:
            goodbyeChannels = json.load(c)

        goodbyeChannels[str(guild.id)] = "None"

        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/goodbye.json', 'w') as d:
            json.dump(goodbyeChannels, d, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/prefixes.json', 'w') as a:
            json.dump(prefixes, a, indent=4)

        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/welcome.json", "r") as b:
            welcomeChannels = json.load(b)

        welcomeChannels.pop(str(guild.id))

        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/welcome.json", "w") as c:
            json.dump(welcomeChannels, c, indent=4)

        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/goodbye.json", "r") as d:
            goodbyeChannels = json.load(d)

        goodbyeChannels.pop(str(guild.id))

        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/goodbye.json", "w") as e:
            json.dump(goodbyeChannels, e, indent=4)

        with open(commandsFile, "r") as g:
            commandsList = json.load(g)

        commandsList.pop(str(guild.id))

        with open(commandsFile, "w") as h:
            json.dump(commandsList, h, indent=4)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        overwrite = discord.PermissionOverwrite(send_messages=False)
        role = discord.utils.get(channel.guild.roles, name="muted")
        if not role or role is None:
            role = discord.utils.get(channel.guild.roles, name="Muted")
        if not role or role is None:
            newRole = await channel.guild.create_role(name="muted", color=discord.Color.dark_grey())
            role = newRole
            await channel.set_permissions(role, overwrite=overwrite)

    @commands.command(aliases=["mutechannel"])
    @commands.has_permissions(manage_guild=True)
    async def channelmute(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        overwrite = discord.PermissionOverwrite(send_messages=False)
        await ctx.send(embed=discord.Embed(description=f"<:check:742198670912651316> {channel} has been muted.",
                                           color=discord.Color.green()))
        role = ctx.guild.default_role
        await channel.set_permissions(role, overwrite=overwrite)
        for role in ctx.guild.roles:
            if channel.overwrites_for(role) == discord.PermissionOverwrite(send_messages=True):
                await channel.set_permissions(role, overwrite=overwrite)
                self.editList.append(str(role))

    @commands.command(aliases=["unmutechannel"])
    @commands.has_permissions(manage_guild=True)
    async def channelunmute(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        overwrite = discord.PermissionOverwrite(send_messages=True)
        role = ctx.guild.default_role
        await channel.set_permissions(role, overwrite=overwrite)
        for role in ctx.guild.roles:
            if str(role) in self.editList:
                await channel.set_permissions(role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(description=f"<:check:742198670912651316> {channel} has been unmuted.",
                                           color=discord.Color.green()))

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(await ctx.message.channel.create_invite())

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f"Server Info for {ctx.guild}", color=random.choice(embedColors))
        embed.add_field(name="Server owner:", value=ctx.guild.owner.mention)  # 1
        admins = []
        for member in ctx.guild.members:
            if member.guild_permissions.administrator:
                if not member.bot:
                    admins.append(member.mention)
        if len(admins) != 0:
            embed.add_field(name="Administrators:", value="\n".join(admins))  # 2
        boosters = ctx.guild.premium_subscribers
        boosts = ctx.guild.premium_subscription_count
        level = ctx.guild.premium_tier
        members = []
        bots = []
        Members = []
        emojis = []
        for emoji in ctx.guild.emojis:
            emojis.append(str(emoji))
        for member in ctx.guild.members:
            if not member.bot:
                members.append(str(member))
            else:
                bots.append(str(member))
            Members.append(str(member))
        if boosts != 0:
            embed.add_field(name="Server Boost Level:", value=f"Level {level} with {boosts} Boosts")  # 3
        if boosters:
            embed.add_field(name=f"Server Boosters", value='\n'.join([Booster.mention for Booster in boosters]))  # 4
        embed.add_field(name="Channels:",
                        value=f"**#** {len(ctx.guild.text_channels)}\n:loud_sound: {len(ctx.guild.voice_channels)}\nTotal: {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)}")  # 5
        description = ctx.guild.description
        if description is not None:
            embed.add_field(name="Description: ", value=f"{description}")
        embed.add_field(name="Members:", value=f"{len(Members)}\nHumans: {len(members)}\nBots: {len(bots)}")  # 6
        guildRoles = ctx.guild.roles
        roles = []
        for role in guildRoles:
            roles.append(role.mention)
        roleString = " ".join(roles)
        extraRoles = []
        while len(roleString) > 1024:
            extraRoles.append(roles[-1])
            del roles[-1]

            roleString = " ".join(roles)
        roles = " ".join(roles)
        embed.add_field(name="Roles:", value=roles)
        if extraRoles:
            embed.add_field(name="Other roles:", value=" ".join(extraRoles))
        emojiString = " ".join(emojis)
        extraEmojis = []
        while len(emojiString) > 1024:
            extraEmojis.append(emojis[-1])
            del emojis[-1]
            emojiString = " ".join(emojis)
        if emojis:
            embed.add_field(name="Emojis:", value=emojiString)
        if extraEmojis:
            embed.add_field(name=f"More emojis:", value=f"{' '.join(extraEmojis)}")
        if ctx.guild.icon_url is not None:
            embed.set_thumbnail(url=ctx.guild.icon_url)
        onlineMembers = []
        invisibleMembers = []
        for member in ctx.guild.members:
            if member.status == discord.Status.online:
                onlineMembers.append(member.mention)
            elif member.status == discord.Status.invisible:
                invisibleMembers.append(member.mention)
        if onlineMembers:
            embed.add_field(name=f"Online members: ", value=" ".join(onlineMembers))
        if invisibleMembers:
            embed.add_field(name=f"Invisible members: ", value=" ".join(invisibleMembers))

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(str(message.content))
        print(str(message.author))
        print(str(message.channel))


def setup(bot):
    bot.add_cog(ServerCog(bot))
