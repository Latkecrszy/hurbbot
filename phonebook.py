import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='&')


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

bot.run("NzE2Mzc2ODE4MDcyMDI3MTY3.XvJrIQ.hs_VjmYiEb2VumpaKCUzLnM2AdM")
