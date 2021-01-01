import discord
from discord.ext import commands
import json
from pytube import YouTube
import youtube_dl
import asyncio
import os
import random


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["connect"])
    async def join(self, ctx):
        if ctx.author.voice is not None:
            channel = ctx.author.voice.channel
            if ctx.guild.voice_client is None:
                client = await channel.connect()
            else:
                await ctx.guild.voice_client.move_to(channel)
            await ctx.send(embed=discord.Embed(description=f"\U0001f44d Connected to {channel}", color=discord.Color.green()))
        else:
            await ctx.send(embed=discord.Embed(description=f"Please connect to a voice channel to use this command.", color=discord.Color.red()))

    @commands.command(aliases=["disconnect"])
    async def leave(self, ctx):
        client = ctx.guild.voice_client
        if client is not None:
            await client.disconnect()
            await ctx.send(embed=discord.Embed(description=f"\U0001f44d Disconnected from {client.channel}", color=discord.Color.green()))
        else:
            await ctx.send(embed=discord.Embed(description=f"I am not connected to a voice channel!", color=discord.Color.red()))

    @commands.command()
    async def play(self, ctx, *, song):
        songFile = os.path.isfile("song.mp4")
        if songFile:
            try:
                os.remove("song.mp4")
            except PermissionError:
                await ctx.send(f"Please pause or stop the current song before playing another.")
                return
        yt = YouTube('https://www.youtube.com/watch?v=xWOoBJUqlbI')
        yt.streams.filter(only_audio=True).all()
        stream = yt.streams.first()
        stream.download(filename="song")
        songFile = os.path.isfile("song.mp4")
        # video.streams.filter(file_extension="mp4").all()
        # video.streams.get_by_itag(18).download()
        vc = ctx.guild.voice_client
        vc.play(discord.FFmpegPCMAudio("song.mp4"), after=lambda e: print("Finished playing the song"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.07
        await ctx.send(f"Playing {songFile}.")


def setup(bot):
    bot.add_cog(VoiceCog(bot))
