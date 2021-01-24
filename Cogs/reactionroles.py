import discord
from discord.ext import commands
from discord.ext.commands import EmojiConverter
import random





class ReactionRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojiConverter = EmojiConverter()

    @commands.command()
    async def reactionrole(self, ctx, emoji, role: discord.Role, *, message):
        if role < self.maxrole(ctx):
            await ctx.message.delete()
            storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)}, "reaction_roles")
            if storage is None:
                await self.bot.cluster.insert_one({"id": str(ctx.guild.id), "roles": {}}, "reaction_roles")
                storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)}, "reaction_roles")
            if 'roles' not in storage:
                storage['roles'] = {}
                await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage, 'reaction_roles')
                storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)}, "reaction_roles")
            reactionroles = storage["roles"]
            if str(emoji).startswith("<"):
                emoji = await self.emojiConverter.convert(ctx, str(emoji))
                embed = discord.Embed(title=message)
                embed.set_footer(text=f"React to get the {role.name} role!")
                message = await ctx.send(embed=embed)
                await message.add_reaction(emoji)
                reactionroles[str(message.id)] = [str(emoji.name), role.id]
            else:
                embed = discord.Embed(title=message)
                embed.set_footer(text=f"React with {emoji} to get the {role.name} role!")
                message = await ctx.send(embed=embed)
                await message.add_reaction(emoji)
                reactionroles[str(message.id)] = [str(emoji), role.id]
            storage["roles"] = reactionroles
            await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage, "reaction_roles")
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
            storage = await self.bot.cluster.find_one({"id": str(payload.guild_id)}, "reaction_roles")
            if storage is not None:
                if 'roles' not in storage:
                    storage['roles'] = {}
                    await self.bot.cluster.find_one_and_replace({"id": str(payload.guild_id)}, storage, 'reaction_roles')
                    storage = await self.bot.cluster.find_one({"id": str(payload.guild_id)}, "reaction_roles")
                reactionroles = storage["roles"]
                if reactionroles is not None:
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
        storage = await self.bot.cluster.find_one({"id": str(payload.guild_id)}, "reaction_roles")
        if storage is not None:
            reactionroles = storage["roles"]
            if reactionroles is not None:
                if str(payload.message_id) in reactionroles.keys():
                    if str(payload.emoji).find(reactionroles[str(payload.message_id)][0]) != -1:
                        guild = self.bot.get_guild(int(payload.guild_id))
                        role = guild.get_role(reactionroles[str(payload.message_id)][1])
                        member = guild.get_member(int(payload.user_id))
                        await member.remove_roles(role)





def setup(bot):
    bot.add_cog(ReactionRoleCog(bot))
