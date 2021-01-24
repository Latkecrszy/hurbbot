import discord
from discord.ext import commands
import asyncio


class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def modmail(self, ctx, condition):
        condition = condition.lower()
        if condition == "setup":
            storage = self.bot.cluster.find_one({"id": str(ctx.guild.id)})
            if "modmail" not in storage:
                storage['modmail'] = {}
            embed = discord.Embed(title=f"Welcome to Hurb ModMail setup! We'll make this quick for you.")
            embed.add_field(name=f"1. Set a channel")
            await ctx.send()






def setup(bot):
    bot.add_cog(ModMail(bot))
