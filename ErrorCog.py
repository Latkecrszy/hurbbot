import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import CommandNotFound, BadArgument, CommandOnCooldown
from discord.ext.commands.errors import CommandInvokeError


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, message, error):
        if isinstance(error, CommandNotFound):
            print("Error: Command not found.")
            # await ctx.send(f"I could not find that command, {ctx.author}")
        elif isinstance(error, commands.MissingRequiredArgument):
            await message.channel.send(f'''Error: Missing one or more required argument.''')
        elif isinstance(error, BadArgument):
            await message.channel.send("Please enter a proper argument for this command.")
        elif isinstance(error, commands.errors.CheckFailure):
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> This command is currently disabled for you, {message.author.display_name}!",
                description=None, color=discord.Color.red())
            await message.channel.send(embed=embed)
        elif isinstance(error, CommandOnCooldown):
            embed = discord.Embed(
                title=f"Whoa there buddy, a little too quick on the commands. You still need to wait {int(error.retry_after)} seconds!",
                color=discord.Color.red())
            await message.channel.send(embed=embed)
        elif isinstance(error, discord.errors.Forbidden):
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> Sorry, I don't have adequate permissions to accomplish that task. Try dragging my role higher in server settings to fix this.",
                color=discord.Color.red())
            await message.channel.send(embed=embed)
        elif isinstance(error, CommandInvokeError):
            if str(message.command) == "blackjack" or str(message.command) == "bj" or str(message.command) == "search" or str(message.command) == "beg" or str(message.command) == "roulette" or str(message.command) == "r" or str(message.command) == "slots" or str(message.command) == "b" or str(message.command) == "balance":
                embed = discord.Embed(description=f"You do not yet have an account with this bot {message.author.mention}! To start one, just say `%start`, and an account will be made for you. Or, if you think that this was a mistake, or that your account has been deleted, please submit a bug report with the `%bug <message>` command.",
                                      color=discord.Color.red())
            else:
                embed = discord.Embed(title=f"<:x_:742198871085678642> Sorry, something went wrong in the command. Please check that you are inputting correct arguments, and try again!",
                                    color=discord.Color.red())
            await message.channel.send(embed=embed)
            raise error
        else:
            raise error

    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def bug(self, ctx, *, bug):
        channel = self.bot.get_channel(755174796530155550)
        embed = discord.Embed(title=f"{ctx.author} has left a bug in {ctx.guild}. It is:",
                              description=f"**{bug}**")
        embed.add_field(name=f"You better come check this out!", value="<@670493561921208320>")
        await channel.send(embed=embed)
        await ctx.send(f"Thank you, {ctx.author.mention}, your bug report has been submitted successfully!")


def setup(bot):
    bot.add_cog(ErrorCog(bot))

