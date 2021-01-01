import discord
from discord.ext import commands
from discord.ext.commands import EmojiConverter
import json
import asyncio
import random


class ReactionRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojiConverter = EmojiConverter()

    @commands.command()
    async def reactionrole(self, ctx, emoji, role: discord.Role, *, message):
        if role < self.maxrole(ctx):
            await ctx.message.delete()
            with open("../Bots/servers.json") as f:
                storage = json.load(f)
            reactionroles = storage["reactionroles"]
            if str(emoji).startswith("<"):
                emoji = await self.emojiConverter.convert(ctx, str(emoji))
                embed = discord.Embed(description=message)
                embed.set_footer(text=f"React to get the {role.name} role!")
                message = await ctx.send(embed=embed)
                await message.add_reaction(emoji)
                reactionroles[str(message.id)] = [str(emoji.name), role.id]
            else:
                embed = discord.Embed(description=message)
                embed.set_footer(text=f"React with {emoji} to get the {role.name} role!")
                message = await ctx.send(embed=embed)
                await message.add_reaction(emoji)
                reactionroles[str(message.id)] = [str(emoji), role.id]
            storage["reactionroles"] = reactionroles
            with open("../Bots/servers.json", "w") as f:
                json.dump(storage, f, indent=4)
        else:
            await ctx.send(f"I do not have the permissions to assign that role {ctx.author.mention}! Please move my role above the role to allow me to assign it!")

    def maxrole(self, ctx):
        role = random.choice(ctx.guild.me.roles)
        for Role in ctx.guild.me.roles:
            if Role > role:
                role = Role
        return role


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.user_id) != "736283988628602960":
            with open("../Bots/servers.json") as f:
                storage = json.load(f)
            reactionroles = storage["reactionroles"]
            if str(payload.message_id) in reactionroles.keys():
                if str(payload.emoji).find(reactionroles[str(payload.message_id)][0]) != -1:
                    guild = self.bot.get_guild(int(payload.guild_id))
                    role = guild.get_role(reactionroles[str(payload.message_id)][1])
                    member = guild.get_member(int(payload.user_id))
                    await member.add_roles(role)
                    channel = self.bot.get_channel(int(payload.channel_id))
                    message = await channel.fetch_message(int(payload.message_id))
                    ctx = await self.bot.get_context(message)
                    try:
                        emoji = await self.emojiConverter.convert(ctx, reactionroles[str(payload.message_id)][0])
                    except:
                        emoji = reactionroles[str(payload.message_id)][0]
                    await member.send(embed=discord.Embed(description=f"**You now have the {role} role for reacting with {emoji} in {str(self.bot.get_guild(int(payload.guild_id)))}.**\n\n"))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open("../Bots/servers.json") as f:
            storage = json.load(f)
        reactionroles = storage["reactionroles"]
        if str(payload.message_id) in reactionroles.keys():
            if str(payload.emoji).find(reactionroles[str(payload.message_id)][0]) != -1:
                guild = self.bot.get_guild(int(payload.guild_id))
                role = guild.get_role(reactionroles[str(payload.message_id)][1])
                member = guild.get_member(int(payload.user_id))
                await member.remove_roles(role)





def setup(bot):
    bot.add_cog(ReactionRoleCog(bot))
