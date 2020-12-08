import discord
from discord.ext import commands
import json
import asyncio


class NQNCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def NQNCheck(self, message):
        if message.content.find(":") != -1:
            guild = message.guild
            everyone = guild.default_role
            channel = message.channel
            if channel.overwrites_for(everyone) != discord.PermissionOverwrite(send_messages=False) and channel.overwrites_for(everyone) != discord.PermissionOverwrite(read_messages=False):
                prevWrite = channel.overwrites_for(everyone)
                prevWrite.update(use_external_emojis=True)
                await channel.set_permissions(everyone, overwrite=prevWrite)
            EmojisList = str(message.content).split(":")
            Emojis = EmojisList[1]
            emojiList = [":"]
            for char in Emojis:
                emojiList.append(char)
            emojiList.append(":")
            emoji = "".join(emojiList)
            if await message.channel.webhooks() is None or not await message.channel.webhooks():
                await message.channel.create_webhook(name=str(message.author.display_name))
            for webhook in await message.channel.webhooks():
                await webhook.edit(name=str(message.author.display_name))
                mutualGuilds = []
                myGuilds = []
                for guild in self.bot.guilds:
                    if guild.get_member(message.author.id) is not None:
                        mutualGuilds.append(guild)
                    myGuilds.append(guild)

                for guild in myGuilds:
                    for emojis in guild.emojis:
                        emojiList = [char for char in str(emojis)]
                        del emojiList[0]
                        del emojiList[-1]
                        if emojiList[0] == "a":
                            del emojiList[0]
                        Emoji = "".join(emojiList)
                        emojiList = []
                        for char in Emoji:
                            numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
                            if char not in numbers:
                                emojiList.append(char)
                        Emoji = "".join(emojiList)
                        if Emoji.lower() == str(emoji).lower():
                            if EmojisList[0] != "<" and EmojisList[0] != "<a" and not EmojisList[2].find(">") != -1:
                                await message.delete()
                                content = EmojisList[0]+""+str(emojis)+""+EmojisList[2]
                                await webhook.send(avatar_url=message.author.avatar_url, content=content)
                                await asyncio.sleep(1)
                break

    @commands.command()
    async def alt(self, ctx, altName, *, message):
        if await ctx.channel.webhooks() is None or not await ctx.channel.webhooks():
            await ctx.channel.create_webhook(name=str(altName))
        for webhook in await ctx.channel.webhooks():
            await ctx.channel.purge(limit=1)
            with open("/Users/robraphael/Library/Application Support/JetBrains/PyCharmCE2020.2/scratches/alts.json", "r") as f:
                alts = json.load(f)
            alt = alts[str(ctx.author)]
            found = False
            for Alt in alt:
                for key, value in Alt.items():
                    if key.lower() == altName.lower():
                        alt = [key, value]
                        found = True
                        break
            if found:
                await webhook.edit(name=str(alt[0]))
                await webhook.send(content=message, avatar_url=alt[1])
            else:
                await ctx.send(f"I could not find that alt, {ctx.author.mention}! Try creating it with the `createalt` command.")

    @commands.command()
    async def createalt(self, ctx, avatar_url, altName):
        with open("/Users/robraphael/Library/Application Support/JetBrains/PyCharmCE2020.2/scratches/alts.json", "r") as f:
            alts = json.load(f)
        if str(ctx.author) in alts.keys():

            alts[str(ctx.author)].append({str(altName).lower(), str(avatar_url)})
        else:
            alts[str(ctx.author)] = []
            alts[str(ctx.author)].append({str(altName).lower(), str(avatar_url)})
        with open("/Users/robraphael/Library/Application Support/JetBrains/PyCharmCE2020.2/scratches/alts.json", "w") as f:
            json.dump(alts, f, indent=4)
        await ctx.send(f"Ok, I've created an alt by the name of {altName}!")

    @commands.command()
    async def delalt(self, ctx, *, altName):
        with open("/Users/robraphael/Library/Application Support/JetBrains/PyCharmCE2020.2/scratches/alts.json", "r") as f:
            alts = json.load(f)
        alt = alts[str(ctx.author)]
        for Alt in alt:
            for key, value in Alt.items():
                if key.lower() == altName.lower():
                    alt = [key, value]
                    found = True
                    break
        alts.pop(str(ctx.author))
        with open("/Users/robraphael/Library/Application Support/JetBrains/PyCharmCE2020.2/scratches/alts.json", "w") as f:
            json.dump(alts, f, indent=4)

    async def NQNTest(self, message):
        if message.content.find(":") != -1:
            guild = message.guild
            everyone = discord.utils.get(guild.roles, name="@everyone")
            channel = message.channel
            if channel.overwrites_for(everyone) != discord.PermissionOverwrite(
                    send_messages=False) and channel.overwrites_for(everyone) != discord.PermissionOverwrite(
                    read_messages=False):
                prevWrite = channel.overwrites_for(everyone)
                prevWrite.update(use_external_emojis=True)
                await channel.set_permissions(everyone, overwrite=prevWrite)
            EmojisList = str(message.content).split(":")
            start = EmojisList[0]
            end = EmojisList[-1]
            sendEmojis = []
            for theEmojis in EmojisList:
                if await message.channel.webhooks() is None or not await message.channel.webhooks():
                    await message.channel.create_webhook(name=str(message.author.display_name))
                for webhook in await message.channel.webhooks():
                    await webhook.edit(name=str(message.author.display_name))
                    myGuilds = []
                    for guild in self.bot.guilds:
                        myGuilds.append(guild)
                    for guild in myGuilds:
                        for emojis in guild.emojis:
                            emojiList = [char for char in str(emojis)]
                            del emojiList[0]
                            del emojiList[-1]
                            if emojiList[0] == "a":
                                del emojiList[0]
                            Emoji = "".join(emojiList)
                            emojiList = []
                            for char in Emoji:
                                numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
                                if char not in numbers:
                                    emojiList.append(char)
                            Emoji = "".join(emojiList)
                            if Emoji.lower() == str(theEmojis).lower():
                                if start != "<" and start != "<a" and not end.find(">") != -1 and not message.author.bot:
                                    await message.channel.purge(limit=1)
                                    sendEmojis.append(str(emojis))
                    sendStuff = "".join(sendEmojis)
                    content = str(sendStuff)
                    await webhook.send(avatar_url=message.author.avatar_url, content=content)
                    await asyncio.sleep(1)
                break


def setup(bot):
    bot.add_cog(NQNCog(bot))
