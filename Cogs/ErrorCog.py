import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import CommandNotFound, BadArgument, CommandOnCooldown
from discord.ext.commands.errors import CommandInvokeError


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            print("Error: Command not found.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''Error: Missing one or more required argument.''')
            pass
        elif isinstance(error, BadArgument):
            await ctx.send("Please enter a proper argument for this command.")
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send(embed=discord.Embed(
                title=f"<a:no:771786741312782346> This command is currently disabled for you, {ctx.author.display_name}!",
                description=None, color=discord.Color.red()))
        elif isinstance(error, CommandOnCooldown):
            await ctx.send(embed=discord.Embed(
                title=f"Whoa there buddy, a little too quick on the commands. You still need to wait {int(error.retry_after)} seconds!",
                color=discord.Color.red()))
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send(embed=discord.Embed(
                title=f"<a:no:771786741312782346> Sorry, I don't have adequate permissions to accomplish that task. Try dragging my role higher in server settings to fix this.",
                color=discord.Color.red()))
        elif isinstance(error, CommandInvokeError):
            error = getattr(error, "original", error)
            if isinstance(error, ValueError):
                await ctx.send(embed=discord.Embed(
                    description=f"Please input a valid number into the command {ctx.author.mention}!",
                    color=discord.Color.red()))
            elif isinstance(error, IndexError):
                pass
            elif str(ctx.command) == "blackjack" or str(ctx.command) == "bj" or str(ctx.command) == "search" or str(
                    ctx.command) == "beg" or str(ctx.command) == "roulette" or str(ctx.command) == "r" or str(
                ctx.command) == "slots" or str(ctx.command) == "b" or str(ctx.command) == "balance" or str(
                ctx.command) == "hourly" or str(ctx.command) == "daily" or str(ctx.command) == "weekly" or str(
                ctx.command) == "monthly" or str(ctx.command) == "yearly" or str(ctx.command) == "rob":
                await ctx.send(embed=discord.Embed(
                    description=f"You do not yet have an account with this bot {ctx.author.mention}! To start one, just say `%start`, and an account will be made for you. Or, if you think that this was a mistake, or that your account has been deleted, please submit a bug report with the `%bug <message>` command.",
                    color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(
                title=f"<a:no:771786741312782346> Sorry, something went wrong in the command. Please check that you are inputting correct arguments, and try again!",
                color=discord.Color.red()))
            channel = self.bot.get_channel(755174796530155550)
            await channel.send(embed=discord.Embed(description=f"```py\n{error.original}```"))
            await channel.send("<@670493561921208320>")
            raise error.original

    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def bug(self, ctx, *, bug):
        channel = self.bot.get_channel(755174796530155550)
        embed = discord.Embed(title=f"{ctx.author} has found a bug in {ctx.guild}. It is:",
                              description=f"**{bug}**")
        await channel.send(embed=embed)
        await ctx.send(f"Thank you, {ctx.author.mention}, your bug report has been submitted successfully!")
        await channel.send("<@670493561921208320>")

    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        channel = self.bot.get_channel(755174796530155550)
        embed = discord.Embed(title=f"{ctx.author} has made a suggestion in {ctx.guild}. It is:",
                              description=f"**{suggestion}**")
        await channel.send(embed=embed)
        await ctx.send(f"Thank you for the suggestion {ctx.author.mention}! We'll look into it!")
        await channel.send("<@670493561921208320>")


def setup(bot):
    bot.add_cog(ErrorCog(bot))
