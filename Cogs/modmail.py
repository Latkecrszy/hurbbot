import discord
from discord.ext import commands
import datetime
from typing import Optional


class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_messengers = {}

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modmail(self, ctx, condition, id: Optional[int] = None, *, extra=None):
        condition = condition.lower()
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        if "modmail" not in storage:
            storage['modmail'] = {
                'message': "Thank you for contacting the staff! We'll get back to you as soon as we can!", 'users': {}}
        if condition == "setup" or condition == "help":
            embed = discord.Embed(title=f"Welcome to Hurb ModMail setup! We'll make this quick for you.")
            embed.add_field(name=f"1. Set a channel.",
                            value=f"The first step is to set a channel to send modmail messages to. Use the `%modmail channel <channel>` command to do this.\nExample: `%modmail channel #modmail-messages`",
                            inline=False)
            embed.add_field(name=f"2. Set a message.",
                            value=f"The next step is to set a message for me to send to the users in response for DMing me. Use the `%modmail message <message>` command to do this.\nExample: `%modmail message Thank you for contacting the mods! We'll get back to you soon!",
                            inline=False)
            embed.add_field(name=f"3. That's it! Once you've done that, you're all set up!",
                            value=f"Use the `%modmail reply <complaint id>` command to reply to modmail messages.",
                            inline=False)
            await ctx.send(embed=embed)
        elif condition == "channel":
            if extra is None:
                await ctx.send(f"The current ModMail channel is {ctx.guild.get_channel(int(storage['modmail']['channel']))}")
            else:
                converter = commands.TextChannelConverter()
                channel = await converter.convert(ctx, extra)
                storage['modmail']['channel'] = channel.id
                await ctx.send(embed=discord.Embed(description=f"ModMail messages will now be sent to {channel.mention}.",
                                                color=discord.Color.green()))
        elif condition == "message":
            if extra is None:
                await ctx.send(embed=discord.Embed(description=f"You need to specify a message {ctx.author.mention}!",
                                                   color=discord.Color.red()))
            storage['modmail']['message'] = extra
            await ctx.send(
                embed=discord.Embed(description=f"Whenever members DM me, they will receive this message:\n{extra}",
                                    color=discord.Color.green()))
        elif condition == "reply" or condition == "respond":
            if str(id) not in storage['modmail']['users']:
                await ctx.send(embed=discord.Embed(
                    description=f"There is no ModMail message with the ID of {id} {ctx.author.mention}!",
                    color=discord.Color.red()))
                return
            member = await ctx.guild.fetch_member(int(id))
            await member.send(f"**Mods:** {extra}")
            await ctx.message.add_reaction(self.bot.get_emoji(769340776340783115))
            storage['modmail']['users'][str(member.id)]['responded'] = "True"
        elif condition == "close":
            if str(id) not in storage['modmail']['users']:
                await ctx.send(embed=discord.Embed(
                    description=f"There is no ModMail message with the ID of {id} {ctx.author.mention}!",
                    color=discord.Color.red()))
                return
            member = await ctx.guild.fetch_member(int(id))
            await member.send(f"Your ModMail message with {ctx.guild} has been closed. If you would like to start a new ModMail message, just send me another message.")
            await ctx.send(embed=discord.Embed(description=f"{member}'s ModMail message has been closed."))
            storage['modmail']['users'].pop(str(member.id))
        print(storage)
        results = await self.bot.cluster.find_one_and_replace({"id": str(ctx.guild.id)}, storage)
        print(results)
        storage = await self.bot.cluster.find_one({"id": str(ctx.guild.id)})
        print(storage)

    @commands.Cog.listener()
    async def on_message(self, start_message):
        if start_message.guild is not None or start_message.author.bot or start_message.author in self.active_messengers:
            return
        await start_message.channel.send(
            f"Thank you for contacting Hurb ModMail! Please send me the ID or name of the server you would like to report to.")
        self.active_messengers[start_message.author] = "active"

        def check(m):
            return m.guild is None and m.author == start_message.author

        message = await self.bot.wait_for("message", check=check)
        if message.content.isnumeric():
            guild = self.bot.get_guild(int(message.content))
        else:
            guild = None
            for guild in self.bot.guilds:
                if str(guild).lower() == message.content.lower():
                    guild = guild
                    break
        if guild is None:
            await message.channel.send(
                f"Sorry, I couldn't find that server. Please make sure that you have the ID or name correct, and try again.")
            return
        if message.author not in guild.members:
            await message.channel.send(f"You are not in {guild} {message.author.mention}!")
        storage = await self.bot.cluster.find_one({"id": str(guild.id)})
        print(storage)
        if 'modmail' not in storage:
            await message.channel.send(
                f"Unfortunately, {guild} does not yet have ModMail set up through me. Feel free to ask them to set it up so you can contact them effortlessly!")
            return
        if 'channel' not in storage['modmail']:
            await message.channel.send(
                f"Unfortunately, {guild} does not yet have ModMail set up through me. Feel free to ask them to set it up so you can contact them effortlessly!")
            return
        if str(message.author.id) not in storage['modmail']['users']:
            await message.channel.send(
                f"What message would you like to send to {guild}? Please be concise and clear, and explain your problem or what you want so that they can understand you.")

            def send_check(m):
                return m.guild is None and m.author == message.author

            send = await self.bot.wait_for("message", check=send_check)
            await message.channel.send(storage['modmail']['message'])
            channel = guild.get_channel(int(storage['modmail']['channel']))
            embed = discord.Embed(title=send.content, description=f"Respond using `%modmail reply {message.author.id} <message>`")
            embed.set_footer(text=f"Message Author: {message.author} | ModMail message ID: {message.author.id}", icon_url=message.author.avatar_url)
            await channel.send(embed=embed)
            storage['modmail']['users'][str(message.author.id)] = {"message": send.content, "responded": "False"}
            await self.bot.cluster.find_one_and_replace({"id": str(guild.id)}, storage)
            self.active_messengers.pop(message.author)
        elif storage['modmail']['users'][str(message.author.id)]['responded'] == "False":
            await message.channel.send(
                f"Please wait until the mods respond to you to send them another message {message.author.mention}!")
            self.active_messengers.pop(message.author)
        else:
            def send_check(m):
                return m.guild is None and m.author == message.author
            await message.channel.send(f"You may now type your response to the moderators in {guild}.")
            send = await self.bot.wait_for("message", check=send_check)
            await send.add_reaction(self.bot.get_emoji(769340776340783115))
            channel = guild.get_channel(int(storage['modmail']['channel']))
            embed = discord.Embed(title=send.content, description=f"Respond using `%modmail reply {message.author.id} <message>`")
            embed.set_footer(text=f"Message Author: {message.author} | ModMail message ID: {message.author.id}", icon_url=message.author.avatar_url)
            await channel.send(embed=embed)
            self.active_messengers.pop(message.author)


def setup(bot):
    bot.add_cog(ModMail(bot))
