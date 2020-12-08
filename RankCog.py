import discord
from discord.ext import commands
import json
import asyncio
import random
from discord.ext.commands.cooldowns import BucketType
import aiohttp


def is_me(command):
    def predicate(ctx):
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
            return commandsList[str(ctx.guild.id)][command] == "True"

    return commands.check(predicate)


async def getrank():
    async with aiohttp.ClientSession() as cs:
        link = "http://api.giphy.com/v1/gifs/search?q=" + img + "&api_key=HIxNUDiCJmENIyZimfquvn7g20ILt4Dc&limit=15"
        async with cs.get(link) as r:
            num -= 1
            res = await r.json()  # returns dict


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
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
        if commandsList[str(message.guild.id)]["ranking"] == "True":
            if not message.author.bot:
                with open("rank.json") as f:
                    messages = json.load(f)
                if str(message.guild.id) in messages.keys():
                    if str(message.author.id) in messages[str(message.guild.id)].keys():
                        messages[str(message.guild.id)][str(message.author.id)]["messages"] += 1
                        await self.levelupcheck(message, messages)
                    else:
                        messages[str(message.guild.id)][str(message.author.id)] = {"messages": 1, "xp": random.randint(1, 5),
                                                                                   "level": 1}
                        with open("rank.json", "w") as f:
                            json.dump(messages, f, indent=4)
                else:
                    messages[str(message.guild.id)] = {}
                    with open("rank.json", "w") as f:
                        json.dump(messages, f, indent=4)
                    await self.on_message(message)
                if await self.cog_check(message):
                    if str(message.guild.id) in messages.keys():
                        if str(message.author.id) in messages[str(message.guild.id)].keys():
                            messages[str(message.guild.id)][str(message.author.id)]["xp"] += random.randint(5, 20)
                            if "color" not in messages[str(message.guild.id)][str(message.author.id)].keys():
                                messages[str(message.guild.id)][str(message.author.id)]["color"] = "🟦"
                            await self.levelupcheck(message, messages)
                        else:
                            messages[str(message.guild.id)][str(message.author.id)] = {"messages": 1, "xp": random.randint(1, 5), "level": 1}
                            with open("rank.json", "w") as f:
                                json.dump(messages, f, indent=4)
                    else:
                        messages[str(message.guild.id)] = {}
                        with open("rank.json", "w") as f:
                            json.dump(messages, f, indent=4)
                        await self.on_message(message)

    async def levelupcheck(self, message, messages):
        with open('/Users/sethraphael/PycharmProject/Hurb/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/levelups.json") as f:
            channels = json.load(f)
        if str(message.guild.id) in channels.keys():
            channel = discord.utils.get(message.guild.channels, name=str(channels[str(message.guild.id)]))
            if channel is None:
                channel = message.channel
        else:
            channel = message.channel
        level = int(messages[str(message.guild.id)][str(message.author.id)]["level"])
        xp = messages[str(message.guild.id)][str(message.author.id)]["xp"]
        maxXP = level * 200 + (200*(int(level / 5) if int(level / 5) >= 1 else 0))
        if xp >= maxXP:
            if commandsList[str(message.guild.id)]["ranking"] == "True":
                await channel.send(f"Congrats {message.author.mention}! You leveled up to level {messages[str(message.guild.id)][str(message.author.id)]['level']+1}!")
            messages[str(message.guild.id)][str(message.author.id)]["level"] += 1
            messages[str(message.guild.id)][str(message.author.id)]["xp"] = 0
        with open("rank.json", "w") as f:
            json.dump(messages, f, indent=4)


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
        with open("rank.json") as f:

            messages = json.load(f)
        level = int(messages[str(ctx.guild.id)][str(member.id)]["level"])
        xp = messages[str(ctx.guild.id)][str(member.id)]["xp"]
        maxXP = level * 200 + (200*(int(level / 5) if int(level / 5) >= 1 else 0))
        embed = discord.Embed()
        embed.set_author(name=f"{member.display_name}'s rank in {ctx.guild}", icon_url=member.avatar_url)
        embed.add_field(name=f"Position:", value=f"#{self.position(member)}")
        embed.add_field(name="Level:", value=str(level))
        embed.add_field(name=f"Messages sent: ",
                        value=str(messages[str(ctx.guild.id)][str(member.id)]["messages"]) + " messages")
        myList = ['\u200b' for x in range(92)]
        embed.add_field(
            name=f"{' '.join(myList)}{xp}/{maxXP} XP",
            value="".join(self.calcspot(member)))
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def levelupchannel(self, ctx, *, channel):
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/levelups.json") as f:
            channels = json.load(f)
            if str(channel).lower() == "none" or str(channel).lower() == "off" or str(channel).lower() == "current":
                channels.pop(str(ctx.guild.id))
                await ctx.send(f"The level up channel has been set to the user's active channel.")
            else:
                converter = commands.TextChannelConverter()
                channel = await converter.convert(ctx, channel)
                print(channel)
                if channel not in ctx.guild.text_channels:
                    await ctx.send(f"I could not find that channel {ctx.author.mention}!")
                else:
                    channels[str(ctx.guild.id)] = str(channel)
                    await ctx.send(f"The level up channel for this guild has been set to {channel.mention}!")
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/levelups.json", "w") as f:
            json.dump(channels, f, indent=4)

    def convert(self, channel: discord.TextChannel):
        return str(channel)

    def position(self, member):
        with open("rank.json") as f:
            messages = json.load(f)
        level = int(messages[str(member.guild.id)][str(member.id)]["level"])
        maxXP = level * 200 + (200*(int(level / 5) if int(level / 5) >= 1 else 0))
        messages = messages[str(member.guild.id)]
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
        with open("rank.json") as f:
            messages = json.load(f)
        messages = messages[str(member.guild.id)]
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
        with open("rank.json") as f:
            messages = json.load(f)
        messages[str(ctx.guild.id)][str(ctx.author.id)]["color"] = color
        await ctx.send(f"Your rank color has been updated to {color}!")
        with open("rank.json", "w") as f:
            json.dump(messages, f, indent=4)

    @is_me("ranking")
    @commands.command(aliases=["lb", "Leaderboard", "LEADERBOARD", "Lb", "LB"])
    @commands.cooldown(1, 10, BucketType.user)
    async def leaderboard(self, ctx, condition=None):
        if condition == "local" or condition is None:
            guild = ctx.guild
            embed = discord.Embed(title=f"{guild}'s leaderboard:")
            memberOrder = {}
            newMemberOrder = {}
            with open("rank.json") as f:
                messages = json.load(f)
            members = messages[str(guild.id)]
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
    async def levelrole(self, role: discord.Role, level):
        pass

    @commands.command()
    async def highest(self, ctx):
        top = {"user": "", "level": 0, "xp": 0, "server": ""}
        with open("rank.json") as f:
            levels = json.load(f)

        for keys, value in levels.items():
            if self.bot.get_guild(int(keys)) is not None:
                for key, values in value.items():
                    if self.bot.get_user(int(key)) is not None:
                        if not self.bot.get_user(int(key)).bot:
                            if values["level"] == top["level"]:
                                if values["xp"] > top["xp"]:
                                    top["level"] = values["level"]
                                    top["user"] = self.bot.get_user(int(key))
                                    top["xp"] = values["xp"]
                                    top["server"] = self.bot.get_guild(int(keys))
                            elif values["level"] > top["level"]:
                                top["level"] = values["level"]
                                top["user"] = self.bot.get_user(int(key))
                                top["xp"] = values["xp"]
                                top["server"] = self.bot.get_guild(int(keys))

        await ctx.send(embed=discord.Embed(description=f"The highest level of any server is {top['user'].mention} in {top['server']} with a level of {top['level']} and {top['xp']} xp."))

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
                    with open("rank.json") as f:
                        levels = json.load(f)

                    levels[str(message.guild.id)].pop(str(self.resetting["member"].id))
                    with open("rank.json", "w") as f:
                        json.dump(levels, f, indent=4)
                    await message.channel.send(f"{self.resetting['member'].mention}'s XP has been reset.")
                    self.resetting = None
                elif str(message.content).lower() == "no":
                    await message.channel.send(f"{self.resetting['member'].mention} has been spared :pray:")
                    self.resetting = None





def setup(bot):
    bot.add_cog(MessageCog(bot))
    bot.add_cog(Rank(bot))
