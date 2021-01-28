import discord
from discord.ext import commands
import random
from discord.ext.commands.cooldowns import BucketType



class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 30.0, commands.BucketType.user)

    async def cog_check(self, message):
        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return False
        else:
            return True


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            storage = await self.bot.cluster.find_one({"id": str(message.guild.id)})
            if message.author.bot:
                return
            if "rank" not in storage:
                storage["rank"] = {}
                await self.bot.cluster.find_one_and_replace({"id": str(message.guild.id)}, storage)
            messages = storage["rank"]

            if str(message.author.id) not in messages.keys():
                messages[str(message.author.id)] = {"messages": 1, "xp": random.randint(1, 5),
                                                    "level": 1}
            messages[str(message.author.id)]["messages"] += 1
            await self.levelupcheck(message, messages, storage)
            storage["rank"] = messages
            if await self.cog_check(message):
                messages = storage["rank"]
                if "xpspeed" not in storage:
                    storage['xpspeed'] = 1.0
                messages[str(message.author.id)]["xp"] += random.randint(5, 20)*float(storage['xpspeed'])
                messages[str(message.author.id)]["color"] = "🟦" if "color" not in messages[str(message.author.id)].keys() else messages[str(message.author.id)]["color"]
                await self.levelupcheck(message, messages, storage)
            await self.bot.cluster.find_one_and_replace({"id": str(message.guild.id)}, storage)

    async def levelupcheck(self, message, messages, storage):
        if storage["commands"]["ranking"] != "True":
            return
        if "levelups" in storage.keys():
            channel = discord.utils.get(message.guild.channels, name=str(storage["levelups"]))
            channel = message.channel if channel is None else channel
        else:
            channel = message.channel
        level = int(messages[str(message.author.id)]["level"])
        xp = messages[str(message.author.id)]["xp"]
        maxXP = level * 200 + (200 * (int(level / 5) if int(level / 5) >= 1 else 0))
        if xp >= maxXP:
            storage['levelroles'] = {} if "levelroles" not in storage else storage['levelroles']
            next_level = str(messages[str(message.author.id)]['level'] + 1)
            if str(next_level) in storage["levelroles"].keys():
                role = message.guild.get_role(int(storage['levelroles'][str(next_level)]))
                await message.author.add_roles(role)
            content = storage["levelupmessage"].format(member=message.author.mention, level=next_level)
            try:
                await channel.send(content)
            except discord.errors.Forbidden:
                pass
            messages[str(message.author.id)]["level"] += 1
            messages[str(message.author.id)]["xp"] = 0
            storage["rank"] = messages
        storage["rank"] = messages
        await self.bot.cluster.find_one_and_replace({"id": str(message.guild.id)}, storage)


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.resetting = {}

    @commands.command(aliases=["level"])
    @commands.cooldown(1, 10, BucketType.user)
    async def rank(self, ctx, member: discord.Member = None):
        member = ctx.author if member is None else member
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        messages = storage["rank"]
        level = int(messages[str(member.id)]["level"])
        xp = messages[str(member.id)]["xp"]
        maxXP = level * 200 + (200 * (int(level / 5) if int(level / 5) >= 1 else 0))
        embed = discord.Embed()
        embed.set_author(name=f"{member.display_name}'s rank in {ctx.guild}", icon_url=member.avatar_url)
        field_parts = {"Position": await self.position(member, storage), 'Level': str(level), 'Messages': f'{messages[str(member.id)]["messages"]} messages'}
        for key, value in field_parts.items():
            embed.add_field(name=key, value=value)
        myList = ['\u200b' for _ in range(92)]
        embed.add_field(
            name=f"{' '.join(myList)}{int(xp)}/{int(maxXP)} XP",
            value="".join(await self.calcspot(member)))
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def levelupchannel(self, ctx, *, channel):
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        storage["levelups"] = "" if 'levelups' not in storage else storage['levelups']
        if str(channel).lower() == "none" or str(channel).lower() == "off" or str(channel).lower() == "current":
            storage.pop("levelups")
            await ctx.send(f"The level up channel has been set to the user's active channel.")
        else:
            converter = commands.TextChannelConverter()
            channel = await converter.convert(ctx, channel)
            if channel not in ctx.guild.text_channels:
                await ctx.send(f"I could not find that channel {ctx.author.mention}!")
            else:
                storage["levelups"] = channel.id
                await ctx.send(f"The level up channel for this guild has been set to {channel.mention}!")
        await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)

    async def position(self, member, storage):
        messages = storage["rank"]
        level = int(messages[str(member.id)]["level"])
        maxXP = level * 200 + (200 * (int(level / 5) if int(level / 5) >= 1 else 0))
        XPs = {int(Member["xp"] + Member["level"] * maxXP): ID for ID, Member in messages.items()}
        sortedXP = {}
        for x in range(len(XPs.keys())):
            sortedXP[max(XPs.keys())] = XPs[max(XPs.keys())]
            XPs.pop(max(XPs.keys()))
        pos = 1
        for key, value in sortedXP.items():
            if str(value) != str(member.id):
                pos += 1
            else:
                break
        return pos

    async def calcspot(self, member):
        storage = await self.bot.cluster.find_one({"id": str(member.guild.id)})
        messages = storage["rank"]
        xp = messages[str(member.id)]["xp"]
        level = messages[str(member.id)]["level"]
        maxXP = level * 200 + (200 * (int(level / 5) if int(level / 5) >= 1 else 0))
        percent = int(xp) / int(maxXP)
        percent = str(percent).split(".")
        percent = [char for char in percent[1]]
        if len(percent) >= 2:
            percent = str(percent[0]) + str(percent[1])
        else:
            percent = str(percent[0])
        percent = int(percent)
        percent = int(percent / 5)
        fullList = [messages[str(member.id)]["color"] for x in range(percent)]
        for x in range(20 - percent):
            fullList.append("⬛")
        return fullList

    @commands.command()
    async def rankcolor(self, ctx, color):
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        storage["rank"][str(ctx.author.id)]["color"] = color
        await ctx.send(f"Your rank color has been updated to {color}!")
        await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)

    @commands.command(aliases=["lb"])
    @commands.cooldown(1, 10, BucketType.user)
    async def leaderboard(self, ctx, condition=None):
        if condition == "local" or condition is None:
            guild = ctx.guild
            embed = discord.Embed(title=f"{guild}'s leaderboard:")
            memberOrder = {}
            newMemberOrder = {}
            storage = await self.bot.cluster.find_one({"id": str(guild.id)})
            messages = storage["rank"]
            members = messages
            for member in members.keys():
                member = guild.get_member(int(member))
                if member is not None and not member.bot:
                    memberOrder[await self.position(member, storage)] = member

            for x in range(len(memberOrder.keys())):
                newMemberOrder[min(memberOrder.keys())] = memberOrder[min(memberOrder.keys())]
                memberOrder.pop(min(memberOrder.keys()))
            num = 1
            for key, value in newMemberOrder.items():
                if num > 50:
                    break
                else:
                    embed.add_field(name=f"**#{num}** - {value.display_name}",
                                    value=f"**XP:** {int(members[str(value.id)]['xp'])}\n**Messages:** {members[str(value.id)]['messages']}\n**Level:** {members[str(value.id)]['level']}")
                    num += 1
            embed.set_thumbnail(url=guild.icon_url)
            embed.set_footer(text=f"Your Position: {await self.position(ctx.author, storage)}")
            await ctx.send(embed=embed)
        elif condition == "global":
            pass

    @commands.command(aliases=["levelroles"])
    @commands.has_permissions(administrator=True)
    async def levelrole(self, ctx, condition=None, level=None, *, role: discord.Role = None):
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        if condition == "view" or condition is None:
            embed = discord.Embed(title=f"Level Roles in {ctx.guild}")
            if not storage['levelroles']:
                await ctx.send(embed=discord.Embed(description=f"There are no levelroles in this server yet {ctx.author.mention}!", color=discord.Color.red()))
                return
            for key, value in storage['levelroles'].items():
                role = ctx.guild.get_role(value)
                embed.add_field(name='\u200b', value=f"**At level {key}, users will receive the {role.mention} role.**")
            await ctx.send(embed=embed)
        elif condition.lower() == "remove":
            if str(level) in storage["levelroles"]:
                storage["levelroles"].pop(str(level))
                await ctx.send(embed=discord.Embed(
                    description=f"Ok {ctx.author.mention}, {role.mention} has been removed from the level roles.",
                    color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(
                    description=f"You do not have a role set for level {level} {ctx.author.mention}!",
                    color=discord.Color.red()))
            await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)
        elif condition.lower() == "add" or condition.lower() == "set":
            if role < self.maxrole(ctx):
                if "levelroles" not in storage:
                    storage["levelroles"] = {}
                storage["levelroles"][str(level)] = role.id
                await ctx.send(embed=discord.Embed(
                    description=f"Ok {ctx.author.mention}, when users reach level {level}, they will receive the {role.mention} role!",
                    color=discord.Color.green()))
                await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)
            else:
                await ctx.send(
                    f"I do not have the permissions to assign that role {ctx.author.mention}! Please move my role above the role to allow me to assign it!")

        else:
            await ctx.send(embed=discord.Embed(
                description=f"Please use the correct format for this command {ctx.author.mention}! Here's an example: \n`%levelrole add 3 @Cool Dude` would make me give the role `@Cool Dude` when someone reached level 3!"))

    def maxrole(self, ctx):
        role = random.choice(ctx.guild.me.roles)
        for Role in ctx.guild.me.roles:
            if Role > role:
                role = Role
        return role

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, member: discord.Member):
        self.resetting[str(ctx.author.id)] = {"member": member}
        await ctx.send(
            f"Are you sure that you want to reset {member.mention}'s XP? This cannot be undone, and they're probably going to hate you from now on. Reply with `yes` to reset, and with anything else to cancel.")

    @commands.Cog.listener()
    @commands.has_permissions(administrator=True)
    async def on_message(self, message):
        if str(message.author.id) in self.resetting:
            if message.guild == self.resetting[str(message.author.id)]['member'].guild:
                if str(message.content).lower() == "yes":
                    storage = await self.bot.cluster.find_one({"id": str(message.guild.id)})
                    storage["rank"].pop(str(self.resetting[str(message.author.id)]['member'].id))
                    await self.bot.cluster.find_one_and_replace({"id": str(message.guild.id)}, storage)
                    await message.channel.send(f"{self.resetting[str(message.author.id)]['member'].mention}'s XP has been reset.")
                elif str(message.content).lower() == "no":
                    await message.channel.send(f"{self.resetting['member'].mention} has been spared :pray:")
                self.resetting.pop(str(message.author.id))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def levelupmessage(self, ctx, *, message):
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        storage["levelupmessage"] = message
        await ctx.send(embed=discord.Embed(description=f"Your level up message has been set to:\n\n**{message}**"))
        await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def xpspeed(self, ctx, num: float):
        if num > 2.0 or num <= 0:
            await ctx.send(embed=discord.Embed(description=f"Please choose a speed between 0 and 2 {ctx.author.mention}!", color=discord.Color.red()))
            return
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        storage["xpspeed"] = float(num)
        await ctx.send(embed=discord.Embed(description=f"Your server will now gain xp at a rate of {num}", color=discord.Color.green()))
        await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)




def setup(bot):
    bot.add_cog(MessageCog(bot))
    bot.add_cog(Rank(bot))
