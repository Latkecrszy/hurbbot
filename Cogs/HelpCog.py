import discord
from discord.ext import commands
import random
import asyncio
import json

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def embed(self, commands, page, title, thumbnail):
        keys = list(commands.keys())
        embed = discord.Embed(title=title)
        for x in range(0, 4):
            try:
                active_key = keys[page * 4 + (x - 4)]
                embed.add_field(name="\u200b",
                                value=f"[`{active_key}`](https://hurb.gg/commands)\n**Parameters:** *{commands[active_key][0]}*\n**What it does:** *{commands[active_key][1]}*\n**Example:** `{commands[active_key][2]}`",
                                inline=False)
            except IndexError:
                pass
        embed.set_thumbnail(url=thumbnail)
        if round(len(commands)/4) < len(commands)/4:
            maxPage = round(len(commands)/4)+1
        else:
            maxPage = round(len(commands)/4)
        embed.set_footer(text=f"______________________________________\nUse ⬅️ and ️➡️ to switch pages | Page {page} / {maxPage}")
        return embed

    @commands.command()
    async def help(self, ctx, command=None):
        if command is None:
            embed = discord.Embed(title=f"Commands Overview:", color=random.choice(embedColors))
            embed.add_field(name=f"High level moderation",
                            value=f"Hurb is equipped with advanced moderation commands such as muting, tempmuting, modmuting (allows even admins to be muted), and channelmuting.\n\n*Use `%help moderation` to see all the commands*")
            embed.add_field(name=f"Bustling economy",
                            value=f"With gambling, donating, robbing, pets,buying roles, and much much more, Hurb has one of the best economy systems of any bot out there.\n\n*Use `%help economy` to see all the commands*")
            embed.add_field(name=f"Great random stuff I made for no reason",
                            value=f"Hurb also has lots of random, quirky but fun commands such as searching for gifs, playing hangman, and killing other users.\n\n*Use `%help fun` to see all the commands*")
            embed.add_field(name=f"Auto features",
                            value=f"Hurb can scan every message for potential things you don't want, such as invites, links, or even bad words, not to mention the ability to search and react to certain words within messsages.\n\n*Use `%help auto` to see all the commands*")
            embed.add_field(name=f"Animated emojis",
                            value=f"Emojis in any server that Hurb is in can be used anywhere, regardless of if you have nitro or not! Hurb detects failed emojis, and converts them into regular ones!\n\n*This one doesn't really need more explanation! It's that simple to use!*")
            embed.add_field(name=f"Advanced ranking system",
                            value=f"Want a ranking system with built in antispam? Like to be able to customize your person rank card? Even wanted to set your progress bar to a bunch of walking ducks? Well, Hurb can do that all and more with its leveling system!\n\n*Use `%help ranking` to see all the commands*")
            embed.add_field(name=f"Configuration Options", value=f"Hurb has many great customizable features like a changeable prefix, a blacklist to shoot bad words out of the server, and even autoroles to give to members when they join!\n\n*Use `%help config` to see all the commands*")
            embed.add_field(name=f"Seamless ModMail", value=f"With the latest and greatest in ModMail technology, you can now easily communicate with your server's moderators by just DMing Hurb! Use `%modmail setup` if you are a server admin to set it up in your server!\n\n*Use `%help modmail` to see all the commands*")
            embed.add_field(name=f"Coming soon!",
                            value=f"Hurb is still a work in progress, and will be receiving many new commands in features in the near future!", inline=False)
            await ctx.send(embed=embed)
            return
        Commands = json.load(open("Cogs/help_commands.json"))
        command = command.lower()
        title = None
        urls = {"Moderation": "https://cdn.discordapp.com/attachments/716377034728931331/796249453073924147/moderation.png",
                "Fun": "https://cdn.discordapp.com/attachments/716377034728931331/796249393283203102/fun.png",
                "Economy": "https://cdn.discordapp.com/attachments/716377034728931331/796249432080646174/economy.png",
                "Auto": "https://cdn.discordapp.com/attachments/716377034728931331/796249414196264977/auto.png",
                "Ranking": "https://cdn.discordapp.com/attachments/716377034728931331/796249376161923082/ranking.png",
                "Config": "https://cdn.discordapp.com/avatars/736283988628602960/b558212e5a66f7b25192116c212c381c.webp?size=1024",
                "ModMail": "https://cdn.discordapp.com/avatars/736283988628602960/b558212e5a66f7b25192116c212c381c.webp?size=1024"}
        if "modmail" in command:
            title = "ModMail"
        elif "eco" in command:
            title = "Economy"
        elif "fun" in command or "random" in command:
            title = "Fun"
        elif "feature" in command or "toggle" in command or "auto" in command:
            title = "Auto"
        elif 'rank' in command:
            title = "Ranking"
        elif 'mod' in command:
            title = "Moderation"
        elif 'config' in command:
            title = "Config"
        if title is None:
            return await self.help(ctx)
        message = await ctx.send(embed=self.embed(Commands[title.lower()], 1, f"{title} Help", urls[title]))
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(m, member):
            return not member.bot
        page = 1
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=check)
            except asyncio.TimeoutError:
                break
            if str(reaction) in ["▶️", "▶", "➡️"]:
                if page < len(Commands[title.lower()])/4:
                    page += 1
                await message.remove_reaction(str(reaction), user)
            elif str(reaction) in ["◀️", "️️️◀", "⬅️"]:
                if page > 1:
                    page -= 1
                await message.remove_reaction(str(reaction), user)
            await message.edit(embed=self.embed(Commands[title.lower()], page, f"{title} Help", urls[title]))
            await asyncio.sleep(.5)
            """elif command == "blackjack" or command.lower() == "bj":
                blackjackEmbed = discord.Embed(title="BlackJack Help:", color=random.choice(embedColors))
                blackjackEmbed.add_field(name=f"`%blackjack`",
                                         value=f"**Parameters**: *bet*\n**What it does**: *Play a game of blackjack against Hurb*\n**Example**: `%blackjack 1000`")
                blackjackEmbed.add_field(name=f"`%hit`",
                                         value=f"**Parameters**: *None*\n**What it does**: *Draw another card, but risk busting.*\n**Example**: `%hit`")
                blackjackEmbed.add_field(name=f"`%stand`",
                                         value=f"**Parameters**: *None*\n**What it does**: *End the game and hope that you have a higher value than the dealer.*\n**Example**: `%stand`")
                blackjackEmbed.add_field(name=f"`%doubledown`",
                                         value=f"**Parameters**: *None*\n**What it does**: *End the game, but double your bet.*\n**Example:** `%doubledown`")
                await ctx.send(embed=blackjackEmbed)
            else:
                await self.help(ctx)"""


def setup(bot):
    bot.add_cog(HelpCog(bot))
