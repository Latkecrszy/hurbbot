import discord
from discord.ext import commands
import json
import asyncio
import random
from discord.ext.commands.cooldowns import BucketType
import aiohttp


def is_me(command):
    def predicate(ctx):
        with open('../Bots/servers.json', 'r') as f:
            commandsList = json.load(f)
            commandsList = commandsList[str(ctx.guild.id)]["commands"]
            return commandsList[command] == "True"

    return commands.check(predicate)


class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 30.0, commands.BucketType.user)
        self._cd2 = commands.CooldownMapping.from_cooldown(5.0, 60.0, commands.BucketType.user)

    async def cog_check(self, message):
        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return False
        else:
            return True

    async def cog_check2(self, message):
        bucket = self._cd2.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return False
        else:
            return True

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('../Bots/servers.json', 'r') as f:
            storage = json.load(f)
        commandsList = storage[str(message.guild.id)]["commands"]
        if commandsList["ranking"] == "True":
            if not message.author.bot:
                if "rank" in storage[str(message.guild.id)].keys():
                    messages = storage[str(message.guild.id)]["rank"]
                    if str(message.author.id) in messages.keys():
                        messages[str(message.author.id)]["messages"] += 1
                        await self.levelupcheck(message, messages)
                    else:
                        messages[str(message.author.id)] = {"messages": 1, "xp": random.randint(1, 5),
                                                            "level": 1}
                        storage["rank"] = messages
                        with open("../Bots/servers.json", "w") as f:
                            json.dump(storage, f, indent=4)
                else:
                    storage[str(message.guild.id)]["rank"] = {}
                    with open("../Bots/servers.json", "w") as f:
                        json.dump(storage, f, indent=4)
                    await self.on_message(message)
                if await self.cog_check(message):
                    if "rank" in storage[str(message.guild.id)].keys():
                        messages = storage[str(message.guild.id)]["rank"]
                        if str(message.author.id) in messages.keys():
                            messages[str(message.author.id)]["xp"] += random.randint(5, 20)
                            if "color" not in messages[str(message.author.id)].keys():
                                messages[str(message.author.id)]["color"] = "🟦"
                            await self.levelupcheck(message, messages)
                        else:
                            messages[str(message.author.id)] = {"messages": 1, "xp": random.randint(1, 5), "level": 1}
                            storage[message.guild.id]["rank"] = messages
                            with open("../Bots/servers.json", "w") as f:
                                json.dump(storage, f, indent=4)
                    else:
                        storage[str(message.guild.id)]["rank"] = {}
                        with open("../Bots/servers.json", "w") as f:
                            json.dump(storage, f, indent=4)
                        await self.on_message(message)

    async def levelupcheck(self, message, messages):
        with open('../Bots/servers.json', 'r') as f:
            storage = json.load(f)
        commandsList = storage[str(message.guild.id)]["commands"]
        if "levelups" in storage[str(message.guild.id)].keys():
            channel = discord.utils.get(message.guild.channels, name=str(storage[str(message.guild.id)]["levelups"]))
            if channel is None:
                channel = message.channel
        else:
            channel = message.channel
        level = int(messages[str(message.author.id)]["level"])
        xp = messages[str(message.author.id)]["xp"]
        maxXP = level * 200 + (200*(int(level / 5) if int(level / 5) >= 1 else 0))
        if xp >= maxXP:
            if commandsList["ranking"] == "True":
                if "levelroles" in storage[str(message.guild.id)]:
                    if str(messages[str(message.author.id)]['level']+1) in str(storage[str(message.guild.id)]["levelroles"].keys()):
                        role = message.guild.get_role(int(storage[str(message.guild.id)]["levelroles"][str(messages[str(message.author.id)]['level']+1)]))
                        if role is not None:
                            await message.author.add_roles(role)
                            await channel.send(f"Congrats {message.author.mention}! You leveled up to level {messages[str(message.author.id)]['level']+1} and got the {role.name} role!")
                        else:
                            await channel.send(f"Congrats {message.author.mention}! You leveled up to level {messages[str(message.author.id)]['level']+1}!")
                    else:
                        await channel.send(
                            f"Congrats {message.author.mention}! You leveled up to level {messages[str(message.author.id)]['level'] + 1}!")
                else:
                    await channel.send(
                        f"Congrats {message.author.mention}! You leveled up to level {messages[str(message.author.id)]['level'] + 1}!")
            messages[str(message.author.id)]["level"] += 1
            messages[str(message.author.id)]["xp"] = 0
        storage[str(message.guild.id)]["rank"] = messages
        with open("../Bots/servers.json", "w") as f:
            json.dump(storage, f, indent=4)


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.resetting = None

    @commands.command()
    @is_me("ranking")
    @commands.cooldown(1, 10, BucketType.user)
    async def rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("../Bots/servers.json") as f:
            storage = json.load(f)
        messages = storage[str(ctx.guild.id)]["rank"]
        level = int(messages[str(member.id)]["level"])
        xp = messages[str(member.id)]["xp"]
        maxXP = level * 200 + (200*(int(level / 5) if int(level / 5) >= 1 else 0))
        embed = discord.Embed()
        embed.set_author(name=f"{member.display_name}'s rank in {ctx.guild}", icon_url=member.avatar_url)
        embed.add_field(name=f"Position:", value=f"#{self.position(member)}")
        embed.add_field(name="Level:", value=str(level))
        embed.add_field(name=f"Messages sent: ",
                        value=str(messages[str(member.id)]["messages"]) + " messages")
        myList = ['\u200b' for x in range(92)]
        embed.add_field(
            name=f"{' '.join(myList)}{xp}/{maxXP} XP",
            value="".join(self.calcspot(member)))
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def levelupchannel(self, ctx, *, channel):
        with open("../Bots/servers.json") as f:
            storage = json.load(f)
        if "levelups" not in storage[str(ctx.guild.id)]:
            storage[str(ctx.guild.id)]["levelups"] = ""
        if str(channel).lower() == "none" or str(channel).lower() == "off" or str(channel).lower() == "current":
            storage[str(ctx.guild.id)].pop("levelups")
            await ctx.send(f"The level up channel has been set to the user's active channel.")
        else:
            converter = commands.TextChannelConverter()
            channel = await converter.convert(ctx, channel)
            if channel not in ctx.guild.text_channels:
                await ctx.send(f"I could not find that channel {ctx.author.mention}!")
            else:
                storage[str(ctx.guild.id)]["levelups"] = channel.id
                await ctx.send(f"The level up channel for this guild has been set to {channel.mention}!")
        with open("../Bots/servers.json", "w") as f:
            json.dump(storage, f, indent=4)

    def convert(self, channel: discord.TextChannel):
        return str(channel)

    def position(self, member):
        with open("../Bots/servers.json") as f:
            storage = json.load(f)
        messages = storage[str(member.guild.id)]["rank"]
        level = int(messages[str(member.id)]["level"])
        maxXP = level * 200 + (200*(int(level / 5) if int(level / 5) >= 1 else 0))
        XPs = {int(Member["xp"] + Member["level"] * maxXP): ID for ID, Member in messages.items()}
        newXPs = XPs
        highs = {}
        for x in range(len(newXPs.keys())):
            highs[max(newXPs.keys())] = XPs[max(newXPs.keys())]
            newXPs.pop(max(newXPs.keys()))
        for key, value in highs.items():
            newXPs[value] = key

        numCount = 1
        for key, value in newXPs.items():
            if key != str(member.id):
                numCount += 1
            else:
                break
        return numCount

    def calcspot(self, member):
        with open("../Bots/servers.json") as f:
            storage = json.load(f)
        messages = storage[str(member.guild.id)]["rank"]
        xp = messages[str(member.id)]["xp"]
        level = messages[str(member.id)]["level"]
        maxXP = level * 200 + (200 * (int(level / 5) if int(level / 5) >= 1 else 0))
        percent = int(xp)/int(maxXP)
        percent = str(percent).split(".")
        percent = [char for char in percent[1]]
        if len(percent) >= 2:
            percent = str(percent[0])+str(percent[1])
        else:
            percent = str(percent[0])
        percent = int(percent)
        percent = int(percent/5)
        fullList = [messages[str(member.id)]["color"] for x in range(percent)]
        for x in range(20 - percent):
            fullList.append("⬛")
        return fullList

    @commands.command()
    async def rankcolor(self, ctx, color):
        with open("../Bots/servers.json") as f:
            storage = json.load(f)
        storage[str(ctx.guild.id)]["rank"][str(ctx.author.id)]["color"] = color
        await ctx.send(f"Your rank color has been updated to {color}!")
        with open("../Bots/servers.json", "w") as f:
            json.dump(storage, f, indent=4)

    @is_me("ranking")
    @commands.command(aliases=["lb"])
    @commands.cooldown(1, 10, BucketType.user)
    async def leaderboard(self, ctx, condition=None):
        if condition == "local" or condition is None:
            guild = ctx.guild
            embed = discord.Embed(title=f"{guild}'s leaderboard:")
            memberOrder = {}
            newMemberOrder = {}
            with open("../Bots/servers.json") as f:
                storage = json.load(f)
            messages = storage[str(ctx.guild.id)]["rank"]
            members = messages
            for member in members.keys():
                member = guild.get_member(int(member))
                if member is not None and not member.bot:
                    memberOrder[self.position(member)] = member

            for x in range(len(memberOrder.keys())):
                newMemberOrder[min(memberOrder.keys())] = memberOrder[min(memberOrder.keys())]
                memberOrder.pop(min(memberOrder.keys()))
            num = 1
            for key, value in newMemberOrder.items():
                if num > 50:
                    break
                else:
                    embed.add_field(name=f"**#{num}** - {value.display_name}",
                                    value=f"**XP:** {members[str(value.id)]['xp']}\n**Messages:** {members[str(value.id)]['messages']}\n**Level:** {members[str(value.id)]['level']}")
                    num += 1
            embed.set_thumbnail(url=guild.icon_url)
        elif condition == "global":
            pass
        await ctx.send(embed=embed)

    @commands.command()
    async def testleaderboard(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"Leaderboard for {ctx.guild}",
                                           description=f"[Click here to see the leaderboard](https://hurbsite.herokuapp.com/leaderboard/{ctx.guild.id})"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelrole(self, ctx, condition, level, *, role: discord.Role=None):
        if condition.lower() == "add" or condition.lower() == "set":
            if role < self.maxrole(ctx):
                storage = json.load(open("../Bots/servers.json"))
                if "levelroles" not in storage[str(ctx.guild.id)]:
                    storage[str(ctx.guild.id)]["levelroles"] = {}
                storage[str(ctx.guild.id)]["levelroles"][str(level)] = role.id
                await ctx.send(embed=discord.Embed(description=f"Ok {ctx.author.mention}, when users reach level {level}, they will receive the {role.mention} role!",
                                                   color=discord.Color.green()))
                json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
            else:
                await ctx.send(
                    f"I do not have the permissions to assign that role {ctx.author.mention}! Please move my role above the role to allow me to assign it!")
        elif condition.lower() == "remove":
            storage = json.load(open("../Bots/servers.json"))
            if str(level) in storage[str(ctx.guild.id)]["levelroles"]:
                storage[str(ctx.guild.id)]["levelroles"].pop(str(level))
                await ctx.send(embed=discord.Embed(description=f"Ok {ctx.author.mention}, {role.mention} has been removed from the level roles.", color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(description=f"You do not have a role set for level {level} {ctx.author.mention}!", color=discord.Color.red()))
            json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
        else:
            await ctx.send(embed=discord.Embed(description=f"Please use the correct format for this command {ctx.author.mention}! Here's an example: \n`%levelrole add 3 @Cool Dude` would make me give the role `@Cool Dude` when someone reached level 3!"))

    def maxrole(self, ctx):
        role = random.choice(ctx.guild.me.roles)
        for Role in ctx.guild.me.roles:
            if Role > role:
                role = Role
        return role

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, member: discord.Member):
        self.resetting = {"member": member, "guild": ctx.guild, "reseter": ctx.author}
        await ctx.send(f"Are you sure that you want to reset {member.mention}'s XP? This cannot be undone, and they're probably going to hate you from now on. Reply with `yes` to reset, and with anything else to cancel.")

    @commands.Cog.listener()
    @commands.has_permissions(administrator=True)
    async def on_message(self, message):
        if self.resetting is not None:
            if message.author == self.resetting["reseter"] and message.guild == self.resetting["guild"]:
                if str(message.content).lower() == "yes":
                    with open("../Bots/servers.json") as f:
                        storage = json.load(f)
                    storage[str(message.guild.id)]["rank"].pop(str(self.resetting["member"].id))

                    with open("../Bots/servers.json", "w") as f:
                        json.dump(storage, f, indent=4)
                    await message.channel.send(f"{self.resetting['member'].mention}'s XP has been reset.")
                    self.resetting = None
                elif str(message.content).lower() == "no":
                    await message.channel.send(f"{self.resetting['member'].mention} has been spared :pray:")
                    self.resetting = None





def setup(bot):
    bot.add_cog(MessageCog(bot))
    bot.add_cog(Rank(bot))
