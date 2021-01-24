import discord
from discord.ext import commands
import asyncio


class Nitro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def nitro(self, message):
        if message.content.count(":") >= 2 and not message.author.bot:
            if message.channel.overwrites_for(message.guild.default_role) != discord.PermissionOverwrite(
                    send_messages=False) and message.channel.overwrites_for(
                    message.guild.default_role) != discord.PermissionOverwrite(read_messages=False):
                prevWrite = message.channel.overwrites_for(message.guild.default_role)
                prevWrite.update(use_external_emojis=True)
                try:
                    await message.channel.set_permissions(message.guild.default_role, overwrite=prevWrite)
                except:
                    pass
            EmojisList = message.content.split(":")
            emoji = "".join([char for char in EmojisList[1]])
            try:
                await message.channel.create_webhook(name=str(
                    message.author.display_name)) if await message.channel.webhooks() is None or not await message.channel.webhooks() else None
                webhook = (await message.channel.webhooks())[0]
                await webhook.edit(name=str(message.author.display_name)) if webhook.name != str(
                    message.author.display_name) else None
                for guild in self.bot.guilds:
                    for emojis in guild.emojis:
                        if f"{emojis.name.lower()}" == str(emoji).lower():
                            if EmojisList[0] != "<" and EmojisList[0] != "<a" and ">" not in EmojisList[2]:
                                await webhook.send(avatar_url=message.author.avatar_url,
                                                   content=f"{EmojisList[0]}{emojis}{EmojisList[2]}")
                                await message.delete()
                                await asyncio.sleep(1)
                                break
            except:
                pass

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.nitro(message)


def setup(bot):
    bot.add_cog(Nitro(bot))
