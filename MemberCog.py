import discord
from discord.ext import commands
import time
from datetime import datetime
import asyncio
import json
from typing import Optional


def is_it_me(ctx):
    return ctx.author.id == 670493561921208320


async def notvaliduserkick(ctx):
    t = time.localtime()
    the_time = time.strftime("%H:%M:%S", t)
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y")
    await ctx.guild.kick(ctx.author)
    await ctx.send(
        f'''On {current_time}, at {the_time}, {ctx.author} attempted to maliciously edit {ctx.guild.name}.''')
    await ctx.send(f'''They have promptly been kicked.''')


async def notvaliduserban(ctx):
    t = time.localtime()
    the_time = time.strftime("%H:%M:%S", t)
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y")
    await ctx.guild.ban(ctx.author)
    await ctx.send(
        f'''On {current_time}, at {the_time}, {ctx.author} attempted to maliciously edit {ctx.guild.name}.''')
    await ctx.send(f'''They have promptly been banned.''')


def is_me(command):
    def predicate(ctx):
        with open('/Users/sethraphael/PycharmProject/Bots/commands.json', 'r') as f:
            commandsList = json.load(f)
            return commandsList[command] == "True"

    return commands.check(predicate)


class MemberCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @is_me("mute")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, muteTime: Optional[int] = None, *,
                   reason="There was no reason for this muting."):
        alreadyMuted = False
        if member is not None:
            if member in list(ctx.guild.members):
                if not member.guild_permissions.administrator:
                    for roles in list(member.roles):
                        if str(roles).lower() == "muted":
                            alreadyMuted = True

                    role = discord.utils.get(ctx.guild.roles, name="muted")
                    if role is None:
                        role = discord.utils.get(ctx.guild.roles, name="Muted")
                    if role is None:
                        overwrite = discord.PermissionOverwrite(send_messages=False)
                        newRole = await ctx.guild.create_role(name="muted", color=discord.Color.dark_grey())
                        for channel in ctx.guild.text_channels:
                            await channel.set_permissions(newRole, overwrite=overwrite)
                        await ctx.send("New role has been created!")
                    if not alreadyMuted:
                        if muteTime is not None:
                            embed = discord.Embed(
                                title=f"<:check:742198670912651316>  {member.display_name} has been muted for {muteTime} seconds.",
                                description=f"Reason: {reason}",
                                colour=discord.Colour.green())
                            await ctx.send(embed=embed)
                            await member.add_roles(role, reason=reason)
                            await asyncio.sleep(int(muteTime))
                            for role in ctx.guild.roles:
                                if str(role).lower() == "muted":
                                    await member.remove_roles(role)
                            embed = discord.Embed(
                                title=f"<:check:742198670912651316>  {member.display_name} has been unmuted after {muteTime} seconds. Welcome them back!",
                                description=None,
                                colour=discord.Colour.green())

                            await ctx.send(embed=embed)
                            await member.add_roles(role, reason=reason)

                        elif muteTime is None:
                            embed = discord.Embed(
                                title=f"<:check:742198670912651316>  {member.display_name} has been muted.",
                                description=f"Reason: {reason}",
                                colour=discord.Colour.green())
                            await ctx.send(embed=embed)
                            await member.add_roles(role, reason=reason)

                    elif alreadyMuted:
                        if member.nick is None:
                            embed = discord.Embed(title=f"<:x_:742198871085678642>  {member} is already muted!",
                                                  description=None,
                                                  colour=discord.Colour.red())
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title=f"<:x_:742198871085678642>  {member.nick} is already muted!",
                                                  description=None,
                                                  colour=discord.Colour.red())
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title="error", description=None, color=discord.Color.red())
                        await ctx.send(embed=embed)
                elif member.guild_permissions.administrator:
                    embed = discord.Embed(
                        title=f"<:x_:742198871085678642>  I can't do that, as {member} is an administrator.",
                        description=None, colour=discord.Colour.red())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="error", description=None, color=discord.Color.red())
                    await ctx.send(embed=embed)
            elif member not in list(ctx.guild.members):
                embed = discord.Embed(
                    title=f"<:x_:742198871085678642>  I could not find a member by the name of {member} \U0001f914.",
                    description=None, colour=discord.Colour.red())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="error", description=None, color=discord.Color.red())
                await ctx.send(embed=embed)
        elif member is None:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642>  You need to specify a member to mute, {ctx.author} \U0001f914.",
                description=None, colour=discord.Colour.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="error", description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

    @is_me("unmute")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is not None:
            alreadyMuted = False
            if member in list(ctx.guild.members):
                if member in list(ctx.guild.members):
                    for roles in list(member.roles):
                        if str(roles).lower() == "muted":
                            alreadyMuted = True
                if alreadyMuted:
                    for role in ctx.guild.roles:
                        if str(role).lower() == "muted":
                            await member.remove_roles(role)
                            embed = discord.Embed(
                                title=f"<:check:742198670912651316>  Success! {member} has been unmuted! \U0001f44d",
                                description=None, colour=discord.Colour.green())
                elif not alreadyMuted:
                    embed = discord.Embed(title=f"<:x_:742198871085678642>  {member} is not muted!", description=None,
                                          colour=discord.Colour.red())
            elif member not in list(ctx.guild.members):
                embed = discord.Embed(
                    title=f"\U0000274c  I could not find a member by the name of {member} \U0001f914.",
                    description=None, colour=discord.Colour.red())

        elif member is None:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642>  You need to specify a member to mute, {ctx.author} \U0001f914.",
                description=None, colour=discord.Colour.red())
        await ctx.send(embed=embed)

    @is_me("kick")
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def kick(self, ctx, member: discord.Member, reason="There was no reason for this kicking."):
        if not member.guild_permissions.administrator:
            for user in list(ctx.guild.members):
                if user == member:
                    await ctx.guild.kick(user)
                    embed = discord.Embed(
                        title=f"<:check:742198670912651316> {member} has been kicked by {ctx.author.display_name}.",
                        description=f"Reason: {reason}", color=discord.Color.green())
                    await ctx.send(embed=embed)

        elif member.guild_permissions.administrator:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> {member} has failed to be kicked by {ctx.author.display_name} because they are an admin/mod.",
                description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

    @is_me("ban")
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, member: discord.Member):
        if not member.guild_permissions.administrator:
            for user in list(ctx.guild.members):
                if user == member:
                    await ctx.guild.ban(user)
        elif member.guild_permissions.administrator:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> {member} has failed to be kicked by {ctx.author.display_name} because they are an admin/mod.",
                description=None, color=discord.Color.red())
            await ctx.send(embed=embed)

    @is_me("rall")
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def rall(self, ctx, *, rename_to):
        validuser = False
        if is_it_me(ctx):
            validuser = True
        if validuser:
            for user in list(ctx.guild.members):
                try:
                    await user.edit(nick=rename_to)
                    print(f"{user.name} has been renamed to {rename_to} in {ctx.guild.name}")
                except:
                    print(f"{user.name} has NOT been renamed to {rename_to} in {ctx.guild.name}")
            print("Action Completed: rall")
        elif not validuser:
            await notvaliduserkick(ctx)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''Please specify who you would like to kick.''')
        else:
            raise error.original

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''Please specify who you would like to ban.''')
        else:
            raise error.original

    @is_me("rename")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rename(self, ctx, member: discord.Member = None, *, new_name):
        user_existing = False
        for user in list(ctx.guild.members):
            if str(user) == str(member):
                user_existing = True
                await user.edit(nick=new_name)
                print(f"{user.name} has been renamed to {new_name} in {ctx.guild.name}")
        if not user_existing:
            await ctx.send(f'''I could not find the member, {member} in {ctx.guild.name}.''')

    @is_me("warn")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member in list(ctx.guild.members) and reason is not None:
            await member.send(f"You have been warned in server {ctx.guild} by {ctx.author} for {reason}")
            embed = discord.Embed(
                title=f"<:check:742198670912651316>  Success! {member.display_name} has been warned for {reason}",
                description=None, colour=discord.Colour.green())
        elif member in list(ctx.guild.members) and reason is None:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642>  Why would you warn someone for no reason {ctx.author.display_name}? \U0001f914",
                description=None, color=discord.Color.red())
        else:
            embed = discord.Embed(
                title=f"<:x_:742198871085678642> I couldn't find that member {ctx.author.display_name} \U0001f914",
                description=None, color=discord.Color.red())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberCog(bot))
