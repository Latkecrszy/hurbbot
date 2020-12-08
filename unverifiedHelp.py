import discord
from discord.ext import commands
import json


class HelpMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def channelstuff(self, ctx):
        for channel in ctx.guild.text_channels:
            if str(channel) != "🌱welcome-and-goodbye" and str(channel) != "🌱rules" and str(channel) != "🌱choose-your-roles":
                id = channel.id
                myChannel = ctx.guild.get_channel(int(id))
                role = discord.utils.get(ctx.guild.roles, name="unverified")

                overwrites = {
                    role: discord.PermissionOverwrite(
                        read_messages=False,
                        send_messages=False,
                    )
                }
                await myChannel.edit(overwrites=overwrites)
                print(str(channel), "has been edited!")
            await ctx.send("Channel stuff has happened.")
        for channel in ctx.guild.voice_channels:
            id = channel.id
            myChannel = ctx.guild.get_channel(int(id))
            role = discord.utils.get(ctx.guild.roles, name="unverified")

            overwrites = {
                role: discord.PermissionOverwrite(
                    read_messages=False,
                    send_messages=False,
                )
            }
            await myChannel.edit(overwrites=overwrites)
            print(str(channel), "has been edited!")
            await ctx.send("Channel stuff has happened.")


def setup(bot):
    bot.add_cog(HelpMe(bot))
