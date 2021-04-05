import asyncio
import discord
from discord.ext import commands


async def nonocheck(message):
    if str(message.author) != "Hurb#4980":
        for i in ["shit", "fuck", "bitch", "dick", "fuk", "dik", "sht", "btch", " ass "]:
            if message.content.lower().find(str(i)) != -1:
                await message.delete()
                sent = await message.channel.send(
                    embed=discord.Embed(description=f"Swearing is disabled in this server {message.author.mention}.",
                                        color=discord.Color.red()))
                await asyncio.sleep(5)
                await sent.delete()
                break


async def linkcheck(message):
    if message.content.find("https://") != -1 and message.content.find("discord.gg/") or message.content.find(
            "http://") != -1 and message.content.find("discord.gg/"):
        if message.content.find("https://cdn.discordapp.com") and message.content.find("https://tenor.com"):
            await message.delete()
            embed = discord.Embed(description=f"Link sharing is disabled in {message.guild} {message.author.mention}!",
                                  color=discord.Color.red())
            warning = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await warning.delete()


async def invitecheck(message):
    if not message.content.find("https://discord.gg/"):
        await message.delete()
        warning = await message.channel.send(embed=discord.Embed(
            description=f"You are not allowed to post invites in {message.guild.name} {message.author.mention}!",
            color=discord.Color.red()))
        await asyncio.sleep(5)
        await warning.delete()


async def modMuteCheck(message, storage):
    if "mutedmods" in storage.keys():
        if str(message.author.id) in storage["mutedmods"].keys():
            if storage["mutedmods"][str(message.author.id)] == str(message.guild.id):
                await message.delete()
                pass


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            storage = await self.bot.cluster.find_one({"id": str(message.guild.id)})
            commandsList = storage["commands"]
            if commandsList['nonocheck'] == "True":
                await nonocheck(message)
            if commandsList['linkcheck'] == "True":
                await linkcheck(message)
            if commandsList['invitecheck'] == "True":
                await invitecheck(message)
            await modMuteCheck(message, storage)


def setup(bot):
    bot.add_cog(MessageCommands(bot))
