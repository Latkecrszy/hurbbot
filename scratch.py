import discord
from discord.ext import commands
import json

class HelpMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def channelstuff(self, ctx):
        for channel in ctx.guild.text_channels:
            id = channel.id
            myChannel = ctx.guild.get_channel(int(id))
            for role in ctx.guild.roles:
                if str(role) == "unverified":
                    Role1 = role
            overwrites = {
                Role1: discord.PermissionOverwrite(
                    read_messages=False,
                    send_messages=False,
                )
            }
            await myChannel.edit(overwrites=overwrites)
        await ctx.send("Channel stuff has happened.")


class AddCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addcommand(self, ctx, name, *, output):
        with open("/Users/sethraphael/Library/Application Support/JetBrains/PyCharmCE2020.1/scratches/customcommands.json", "r") as f:
            customCommands = json.load(f)
        if name in customCommands.keys():
            await ctx.send(f"You already have a command by that name registered, {ctx.author.mention}!")



def setup(bot):
    bot.add_cog(HelpMe(bot))
