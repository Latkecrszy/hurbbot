import discord
import asyncio
from discord.ext import commands
import aiohttp


class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chatting = {}

    @commands.command()
    async def chatbot(self, ctx, parameter=None):
        if parameter is None:
            self.chatting[str(ctx.author.id)] = str(ctx.channel)
            await ctx.send(embed=discord.Embed(
                description=f"Your chatting session with Hurb has been started in this channel! Type `%chatbot end` to end the session."))
        elif parameter.lower() == "end":
            self.chatting.pop(str(ctx.author.id))
            await ctx.send(embed=discord.Embed(description=f"Your chat session with Hurb has ended."))
        else:
            self.chatting[str(ctx.author.id)] = str(ctx.channel)
            await ctx.send(embed=discord.Embed(description=f"Your chatting session with Hurb has been started in this channel! Type `%chatbot end` to end the session."))

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) in self.chatting.keys():
            if str(message.channel) == self.chatting[str(message.author.id)]:
                if not message.author.bot:
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(f'https://some-random-api.ml/chatbot?message="{str(message.content)}"') as r:
                            res = await r.json()
                    await message.channel.send(res["response"])

def setup(bot):
    bot.add_cog(ChatBot(bot))
