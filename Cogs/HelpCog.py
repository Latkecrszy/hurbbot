import discord
from discord.ext import commands
import random
import asyncio

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

    async def moderation(self, ctx):
        embed = discord.Embed(title=f"Moderation Commands")
        Commands = {"1": {"`%purge`": [f"number of messages", "Deletes a selected number of messages.", "`%purge 20`"],
                          "`%kick`": ["member, optional: reason", "Kicks a member and dms them the reason and person who kicked them.", "`%kick @Latkecrszy#0947 Spamming in general.`"],
                            "`%ban`": ["member, optional: reason", "Bans a member and DMs them the reason and person who banned them.", "`%ban @Latkecrszy#0947 Insulting other members and generally being a meanie.`"],
                            "`%warn`": ["member, reason", "DMs a member the server they were warned in and the reason for the warning.", "`%warn @Latkecrszy#0947 Calling me a 'mean mod'. I'm not mean!`"],
                          "`%rename`": ["member, new name", "Renames a member.", "`%rename @Latkecrszy#0947 big bad meanie.`"]},
                    "2": {"`%mute`": ["member, optional: reason", "Mutes a member.", "`%mute @Latkecrszy#0947 Spamming repeatedly.`"],
                            "`%tempmute`": ["member, time, optional: reason", "Mutes a member for a select amount of time.", "`%tempmute @Latkecrszy#0947 10m take a break and cool down.`"],
                            "`%unmute`": ["member", "Unmutes a member.", "`%unmute @Latkecrszy#0947`"],
                            "`%lockdown`": ["channel", "Locks down a channel, allowing only admins to talk.", "`%lock #general`"],
                            "`%unlock`": ["channel", "Unlocks a channel, allowing the people that could talk previously to talk.", "`%unlock #general`"]},
                    "3": {"`%modmute`": ["member", "Mutes an admin.", "`%modmute @Latkecrszy#0947`"],
                            "`%modunmute`": ["member", "Unmutes an admin.", "`%modunmute @Latkecrszy#0947`"],
                          "`%slowmode`": ["time", "Sets a slowmode for the channel.", "`%slowmode 10`"],
                            "`%setwelcomechannel`": ["channel, message", "Sets a channel and message to welcome new members with; type the word `member` to have it mention the member.", "`%setwelcomechannel #welcome Hi member! Welcome to Hurb Central! We hope you enjoy your time here!`"],
                            "`%setgoodbyechannel`": ["channel, message", "Sets a channel and message to say goodbye to members with; type the word `member` to have it mention the member.", "`%setgoodbyechannel #goodbye Aww. member left. Can we get an f in the chat?`"]},
                    "4": {"`%createrole`": ["color, name", "Creates a role with a given color and name.", "`%createrole teal cool person`"],
                            "`%deleterole`": ["role", "Deletes a role.", "`%deleterole cool person`"],
                            "`%autorole`": ["role", "Sets a role to automatically assign to people when they join the server.", "`%autorole cool person`"],
                            "`%removeautorole`": ["role", "Removes one of the autoroles.", "`%removeautorole cool person`"],
                            "`%levelrole`": ["add/remove, level, role", "Sets a role to assign once a member reaches a certain level.", "`%levelrole add 5 cool person"],
                            "`%serverinfo`": ["None", "Shows you general info about the server.", "`%serverinfo`"],
                            "`%info`": ["Optional: member", "Shows general info about you or another member of the server.", "`%info @Latkecrszy#7777`"]}}
        for key, value in Commands["1"].items():
            embed.add_field(name="\u200b",
                            value=f"[{key}](https://google.com)\n**Parameters**: *{value[0]}*\n**What it does**: *{value[1]}*\n**Example**: {value[2]}",
                            inline=False)
        embed.set_footer(
            text=f"______________________________________________________\nUse the ⬅️ and ➡️ to navigate between pages | Page 1 of 4.")
        message = await ctx.send(embed=embed)
        page = 1
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=None)
            except asyncio.TimeoutError:
                break
            if str(reaction) == "▶️" or str(reaction) == "▶" or str(reaction) == "➡️" and user != ctx.guild.me:
                if page < 4:
                    page += 1
                await message.remove_reaction("➡️", user)
            elif str(reaction) == "◀️" or str(reaction) == "️️️◀" or str(reaction) == "⬅️" and user != ctx.guild.me:
                if page > 1:
                    page -= 1
                await message.remove_reaction("⬅️", user)
            await message.edit(embed=self.Embed(discord.Embed(title=f"Moderation Commands"), Commands, page, 4))

    async def economy(self, ctx):
        embed = discord.Embed(title=f"Economy commands")
        Commands = {"1": {"`%start`": ["None", "Starts an account for you with $1000-10000.", "`%start`"],
                          "`%balance`": ["optional: member", "See how much money you have, or ping another user to see their balance.", "`%balance @Latkecrszy#0947`"],
                          "`%donate`": ["member, amount", "Give money to another user.", "`%donate @Latkecrszy 100000`"],
                          "`%blackjack`": ["bet", "Play a game of blackjack; use `%help blackjack` to see more info.", "`%blackjack 2000`"],
                          "`%roulette`": ["bet, place", "Play a game of roulette.", "`%roulette 10000 black`"],
                          "`%buy`": ["item name", "Buy an item from the shop.", "`%buy pokemon card`"]},
                    "2": {"`%slots`": ["bet", "Play a game of slots; get two of the same icon to win your bet, and get all three the same for a whopping 1000 times your bet!", "`%slots 1000`"],
                          "`%coinflip`": ["bet, heads/tails", "Flip a coin.", "`%coinflip 10000 heads"],
                          "`%buyrole`": ["role name", "Buy a role, purchasable roles and prices are set by the admins; see more info with `%help roles`.", "`%buyrole cool person`"],
                          "`%roleprice`": ["role name, price", "Set the price of a role. Only usable by admins; see more info with `%help roles`.", "`%roleprice 100000 cool person`"],
                          "`%roleshop`": ["None", "Shows you the role shop for your server.", "`%roleshop`"],
                          "`%shop`": ["None", "See the item shop, along with how many of each item you have.", "`%shop`"]},
                    "3": {"`%hourly`": ["None", "Claim $100 every hour!", "`%hourly`"],
                          "`%daily`": ["None", "Claim $500 every day!", "`%daily`"],
                          "`%weekly`": ["None", "Claim $2500 every week!", "`%weekly`"],
                          "`%monthly`": ["None", "Claim $10000 every month!", "`%monthly`"],
                          "`%yearly`": ["None", "Claim $1000000000 every year!", "`%yearly`"],
                          "`%items`": ["None", "See your items.", "`%items`"]}}
        for key, value in Commands["1"].items():
            embed.add_field(name="\u200b",
                            value=f"[{key}](https://google.com)\n**Parameters**: *{value[0]}*\n**What it does**: *{value[1]}*\n**Example**: {value[2]}",
                            inline=False)
        embed.set_footer(
            text=f"______________________________________________________\nUse the ⬅️ and ➡️ to navigate between pages | Page 1 of 3.")
        message = await ctx.send(embed=embed)
        page = 1
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=None)
            except asyncio.TimeoutError:
                break
            if str(reaction) == "▶️" or str(reaction) == "▶" or str(reaction) == "➡️" and user != ctx.guild.me:
                if page < 3:
                    page += 1
                await message.remove_reaction("➡️", user)
            elif str(reaction) == "◀️" or str(reaction) == "️️️◀" or str(reaction) == "⬅️" and user != ctx.guild.me:
                if page > 1:
                    page -= 1
                await message.remove_reaction("⬅️", user)
            await message.edit(embed=self.Embed(discord.Embed(title=f"Economy Commands"), Commands, page, 3))

    async def fun(self, ctx):
        embed = discord.Embed(title=f"Fun Commands", color=random.choice(embedColors))
        Commands = {
            "1": {
                "`%gif`": ["result number, name", "Search giphy for your favorite gifs!", "`%gif 1 Hurb is cool`"],
                "`%rps`": ["rock/paper/scissors", "Play a game of rock paper scissors against hurb!", "`%rps rock`"],
                "`%roll`": ["die size", "Roll a die.", "`%roll 5`"],
                "`%kill`": ["person", "Kill someone in a fun and creative way!", "`%kill @Latkecrszy#7777"],
                "`%joke`": ["type", "Check out some jokes!", "`%joke programming`"]},
            "2": {
                "`%doggo`": ["None", "Look at some cute doggos!", "`%doggo`"],
                "`%catto`": ["None", "Look at some cute cattos!", "`%catto`"],
                "`%panda`": ["None", "Look at some cute pandas!", "`%panda`"],
                "`%duck`": ["None", "Look at some cute duckies!", "`%duck`"],
                "`%redpanda`": ["None", "Look at some cute red pandas!", "`%redpanda`"],
                "`%koala`": ["None", "Look at some cute koalas!", "`%koala"]},
            "3": {
                "`%birb`": ["None", "Look at some cute birbs!", "`%birb`"],
                "`%fox`": ["None", "Look at some foxxies!", "`%fox`"],
                "`%autodoggo`": ["None", "Look at a cute doggo every 7 seconds!", "`%autodoggo"],
                "`%stopautodoggo`": ["None", "Stop looking at cute doggos every 7 seconds. (But why would you ever want to do that though?).", "`%stopautodoggo`"],
                "`%autocatto`": ["None", "Look at a cute catto every 7 seconds!", "`%autocatto`"],
                "`%stopautocatto`": ["None", "Stop looking at cute cattos every 7 seconds. (Although this one is a crime to use).", "`%stopautocatto`"]},
            "4": {
                "`%topic`": ["None", "Start a conversation!", "`%topic`"],
                "`%hangman`": ["None", "Play hangman against Hurb! Note: only usable if you have purchased the hangman item from the shop.", "`%hangman`"],
                "`%chatbot`": ["Begin/End", "Chat with a chatbot!", "`%chatbot begin`"]}}
        for key, value in Commands["1"].items():
            embed.add_field(name="\u200b",
                            value=f"[{key}](https://google.com)\n**Parameters**: *{value[0]}*\n**What it does**: *{value[1]}*\n**Example**: {value[2]}",
                            inline=False)
        embed.set_footer(
            text=f"______________________________________________________\nUse the ⬅️ and ➡️ to navigate between pages | Page 1 of 4.")
        message = await ctx.send(embed=embed)
        page = 1
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=None)
            except asyncio.TimeoutError:
                break
            if str(reaction) == "▶️" or str(reaction) == "▶" or str(reaction) == "➡️" and user != ctx.guild.me:
                if page < 3:
                    page += 1
                await message.remove_reaction("➡️", user)
            elif str(reaction) == "◀️" or str(reaction) == "️️️◀" or str(reaction) == "⬅️" and user != ctx.guild.me:
                if page > 1:
                    page -= 1
                await message.remove_reaction("⬅️", user)
            await message.edit(embed=self.Embed(discord.Embed(title=f"Fun Commands"), Commands, page, 3))

    def Embed(self, embed, Commands, page, maxPage):
        for key, value in Commands[str(page)].items():
            embed.add_field(name="\u200b",
                            value=f"[{key}](https://google.com)\n**Parameters**: *{value[0]}*\n**What it does**: *{value[1]}*\n**Example**: {value[2]}",
                            inline=False)
        embed.set_footer(
            text=f"______________________________________________________\nUse the ⬅️ and ➡️ to navigate between pages | Page {page} of {maxPage}.")
        return embed

    @commands.command()
    async def help(self, ctx, command=None):
        if command is None:
            embed = discord.Embed(title=f"Commands Overview:", color=random.choice(embedColors))
            embed.add_field(name=f"High level moderation", value=f"Hurb is equipped with advanced moderation commands such as muting, tempmuting, modmuting (allows even admins to be muted), and channelmuting.\n\n*Use `%help moderation` to see all the commands*")
            embed.add_field(name=f"Bustling economy", value=f"With gambling, donating, and even buying roles, hurb has one of the best economy systems of any bot out there.\n\n*Use `%help economy` to see all the commands*")
            embed.add_field(name=f"Great random stuff I made for no reason", value=f"Hurb also has lots of random, quirky but fun commands such as searching for gifs, playing hangman, and killing other users.\n\n*Use `%help fun` to see all the commands*")
            embed.add_field(name=f"Auto features", value=f"Hurb can scan every message for potential things you don't want, such as invites, links, or even bad words, not to mention the ability to search and react to certain words within messsages.\n\n*Use `%help auto` to see all the commands*")
            embed.add_field(name=f"Animated emojis", value=f"If you send a failed emoji from any server that Hurb is in, whether it be an animated emoji from your current server or a regular one from a server you aren't even in, Hurb can send the message for you from a bot that looks exactly like yourself, essentially granting you nitro. All for free!\n\n*This one doesn't really need more explanation! It's that simple to use!*")
            embed.add_field(name=f"Advanced ranking system", value=f"Want a ranking system with built in antispam? Like to be able to customize your person rank card? Even wanted to set your progress bar to a bunch of walking ducks? Well, Hurb can do that all and more with its leveling system!\n\n*Use `%help ranking` to see all the commands*")
            embed.add_field(name=f"Coming soon!", value=f"Hurb is still a work in progress, and will be receiving many new commands in features in the near future!")
            await ctx.send(embed=embed)
        else:
            command = command.lower()
            if command.find("mod") != -1:
                await self.moderation(ctx)
            elif command.find("eco") != -1:
                await self.economy(ctx)
            elif command.find("random") != -1 or command.find("fun") != -1:
               await self.fun(ctx)
            elif command.find("feature") != -1 or command.find("toggle") != -1 or command.find("auto") != -1:
                embed = discord.Embed(title=f"Auto features:", description=f"**These are features that can be turned on or off with the `%enable <command>` or `%disable <command>` commands.**", color=random.choice(embedColors))
                autoFeatures = {"`%enable invitecheck`": "Turns on an invite blocker for the server.",
                                "`%disable invitecheck`": "Turns off an invite blocker for the server.",
                                "`%enable nonocheck`": "Turns on a swear word blocker for the server.",
                                "`%disable nonocheck`": "Turns off a swear word blocker for the server.",
                                "`%enable nitro`": "Turns on an emoji converter for the server; see more info with the `%help nitro` command.",
                                "`%disable nitro`": "Turns off an emoji converter for the server; see more info with the `%help nitro` command.",
                                "`%enable linkcheck`": "Turns on a link blocker for the server.",
                                "`%disable linkcheck`": "Turns off a link blocker for the server.",
                                "`%enable ranking`": "Turns on a ranking system for the server.",
                                "`%disable ranking`": "Turns off a ranking system for the server."}
                for key, value in autoFeatures.items():
                    embed.add_field(name=key, value=f"**What it does**: *{value}*", inline=False)
                await ctx.send(embed=embed)
            elif command.find("rank") != -1 or command.find("level") != -1 or command.find("leaderboard") != -1:
                rankEmbed = discord.Embed(title=f"Ranking Help:", color=random.choice(embedColors))
                rankFeatures = {"`%enable ranking`": ["None", "Turn on ranking in your server.", "`%enable ranking`"],
                                "`%disable ranking`": ["None", "Turn off ranking in your server.", "`%disable ranking`"],
                                "`%rank`": ["Optional: member", "See your (or someone else's) level, messages, and xp for the server.", "`%rank @Latkecrszy#7777`"],
                                "`%leaderboard`": ["None", "Take a look at the leaderboard for the server.", "`%leaderboard`"],
                                "`%levelupchannel`": ["channel name/none", "Set a message to send level up messages in, or set it to none to have them send in the user's active channel.", "`%levelupchannel #level-up`"],
                                "`%rankcolor`": ["emoji", "Set an emoji to display your rank as, or even set it to a word if you want!", "`%rankcolor ✨`"]}
                for key, value in rankFeatures.items():
                    rankEmbed.add_field(name=key, value=f"**Parameters**: *{value[0]}*\n**What it does**: *{value[1]}*\n**Example**: {value[2]}", inline=False)
                await ctx.send(embed=rankEmbed)
            elif command.find("help") != -1:
                helpEmbed = discord.Embed(title=f"Help help:", color=random.choice(embedColors))
                helpEmbed.add_field(name=f"All the help commands for Hurb: ", value=f"**`%help`\n`%help moderation`\n`%help economy`\n`%help fun`\n`%help ranking`**")
                await ctx.send(embed=helpEmbed)
            elif command == "blackjack" or command.lower() == "bj":
                blackjackEmbed = discord.Embed(title="BlackJack Help:", color=random.choice(embedColors))
                blackjackEmbed.add_field(name=f"`%blackjack`", value=f"**Parameters**: *bet*\n**What it does**: *Play a game of blackjack against Hurb*\n**Example**: `%blackjack 1000`")
                blackjackEmbed.add_field(name=f"`%hit`", value=f"**Parameters**: *None*\n**What it does**: *Draw another card, but risk busting.*\n**Example**: `%hit`")
                blackjackEmbed.add_field(name=f"`%stand`", value=f"**Parameters**: *None*\n**What it does**: *End the game and hope that you have a higher value than the dealer.*\n**Example**: `%stand`")
                blackjackEmbed.add_field(name=f"`%doubledown`", value=f"**Parameters**: *None*\n**What it does**: *End the game, but double your bet.*\n**Example:** `%doubledown`")
                await ctx.send(embed=blackjackEmbed)
            else:
                await self.help(ctx)



"""serverEmbed = discord.Embed(title="Help command for server management features of Hurb Bot:",
                                        color=random.choice(embedColors))
            funEmbed = discord.Embed(title="Help command for fun features of Hurb Bot:", color=random.choice(embedColors))
            funEmbed.add_field(name="Help <command>", value="Either displays this, or help for a specific command.")
            serverEmbed.add_field(name="Enable <command>", value="Enables a disabled command")
            serverEmbed.add_field(name="Disable <command>", value="Disables an enabled command")
            serverEmbed.add_field(name="Prefix <new prefix>", value="Changes your server prefix to whatever you want")
            funEmbed.add_field(name="BlackJack <bet>", value="Starts a blackjack game with a bet of your choice")
            funEmbed.add_field(name="beg", value="You beg for money")
            funEmbed.add_field(name="search <place>", value="You search for money")
            funEmbed.add_field(name="searchplaces", value="Shows you where you can search")
            funEmbed.add_field(name="roulette <bet> <number>",
                               value="Starts a game of roulette with a bet on a number of your choice")
            funEmbed.add_field(name="joke", value="Tells you a joke")
            funEmbed.add_field(name="multiply <number> <number2>", value="Multiplies two numbers for you")
            funEmbed.add_field(name="add <number> <number2>", value="Adds two numbers for you")
            funEmbed.add_field(name="subtract <number> <number2>", value="Subtracts two numbers for you")
            funEmbed.add_field(name="divide <number> <number2>", value="Divides two numbers for you")
            funEmbed.add_field(name="power <number> <number2>", value="Finds the power of two numbers for you")
            serverEmbed.add_field(name="mute <member> <optional: reason>",
                                  value="Mutes a memberYou must have admin privileges to do this.")
            serverEmbed.add_field(name="tempmute <member> <time> <optional: reason>", value="Mute a member for a specified amount of time.")
            serverEmbed.add_field(name="unmute <member>",
                                  value="Unmutes a member. Pretty self-explanatory. You must have admin privileges to do this.")
            serverEmbed.add_field(name="warn <member> <reason>",
                                  value="Warns a member, and sends them a dm with the warning. You must have admin privileges to do this.")
            serverEmbed.add_field(name="rename <member> <new name>",
                                  value="Renames a member. You must have admin privileges to do this.")
            serverEmbed.add_field(name="rall <new name>",
                                  value="renames everyone in your server to whatever you want. Use wisely. You must have admin privileges to do this.")
            serverEmbed.add_field(name="kick <member> <optional: reason>",
                                  value="kicks a member from your server. They will be able to rejoin. You must have admin privileges to do this.")
            serverEmbed.add_field(name="ban <member> <optional: reason>",
                                  value="bans a member from your server. You can undo this in server settings. You must have admin privileges to do this.")
            serverEmbed.add_field(name="enable <command>",
                                  value="Enables a given command and allows it to be used in your server.")
            serverEmbed.add_field(name="disable <command>",
                                  value="Disables a given command and does not allow it to be used in your server.")
            serverEmbed.add_field(name="invite", value="Creates an invite to your server.")
            funEmbed.add_field(name="gimme <color> <name>",
                               value="Creates a custom role for you with a desired color and name. You can only use this once per day.")
            serverEmbed.add_field(name="setwelcomechannel <channel> <message>",
                                  value="Sets the welcome channel for the server, and the message it displays. When you type member, it will put their name instead.")
            serverEmbed.add_field(name="setgoodbyechannel <channel> <message>",
                                  value="Sets the goodbye channel for the server, and the message it displays. When you type member, it will put their name instead.")
            serverEmbed.add_field(name="mutechannel <channel>", value="Mutes a specific channel so that only admins can talk. If the channel is not listed, mutes the channel it was called in.")
            serverEmbed.add_field(name="unmutechannel <channel>", value="Unmutes a specific channel so that everyone that could talk before can now talk. If the channel is not listed, unmutes the channel it was called in.")
            funEmbed.add_field(name="hangman", value="Starts a game of hangman for you to play! you get 8 lives, so choose carefully.")
            funEmbed.add_field(name="guess <letter>", value="Guesses a letter in hangman and continues the game.")
            await ctx.author.send(embed=serverEmbed)
            await ctx.author.send(embed=funEmbed)"""


"""<html data-theme="dark">
<style>
button {
  border: none;
  color: red;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 5px;
  hover-text: green;
  background-color: black;
}

a {
	color: black !important;
    background-color: #4a4a4a !important;
    --text: black !important;
}
a.atag {
	color: black !important;
}
#bot-details-page {
	--background: #4a4a4a !important;
    background-color: #4a4a4a !important; 
}
p.bot-description {
	color: black !important;
}


</style>
<body data-theme="dark">

Hurb is a great general purpose/economy/moderation bot for your discord server! It has many, many features, but I'll list the highlights here.

<b>Moderation commands:</b>
<ul>
  <li>`%purge {amount}` ==> deletes messages</li>
  <li>`%kick {member} {optional: reason}` ==> kicks a member</li>
  <li>`%ban {member} {optional: reason}` ==> bans a member</li>
  <li>`%warn {member} {reason}` ==> warns a member</li>
  <li>`%mute {member} {optional: reason}` ==> mutes a member</li>
  <li>`%tempmute {member} {time} {optional: reason}` ==> mutes a member for a specified amount of time</li>
  <li>`%unmute {member}` ==> unmutes a member</li>
  <li>`%channelmute {channel}` ==> mutes a channel</li>
  <li>`%channelunmute {channel}` ==> unmutes a channel</li>
  <li>`%rename {member} {new name}` ==> renames a member</li>
  <li>`%setwelcomechannel {channel} {message}` ==> sets a channel to welcome members and a message to welcome them with</li>
  <li>`%setgoodbyechannel {channel} {message}` ==> sets a channel to send a goodbye message to members.</li>
  <li>`%disable {command}` ==> disables a command so that no one can use it</li>
  <li>`%enable {command}` ==> enables a command so that it can be used</li>
  <li>`%createrole {color} {name}` ==> creates a role</li>
  <li>`%deleterole {name}` ==> deletes a role</li>
</ul>

<b>Economy commands:</b>
<ul>
  <li>`%start` ==> starts an account for you with a random amount of money</li>
  <li>`%beg` ==> lets you beg for money</li>
  <li>`%search {place}` ==> searches a place for you; do `searchplaces` to see where you can search</li>
  <li>`%balance` ==> checks your balance</li>
  <li>`%donate {user} {amount}` ==> donates money to another user</li>
  <li>`%blackjack {bet}` ==> starts a game of blackjack</li>
  <li>`%roulette {bet} {place}` ==> starts a game of roulette</li>
  <li>`%slots {bet}` ==> starts a game of slots</li>
  <li>`%coinflip {bet} {heads/tails}` ==> flips a coin</li>
  <li>`%buyrole {role name}` ==> buys a role</li>
  <li>`%roleprice {price} {role name}` ==> sets the price for a role</li>
  <li>`%roleshop` ==> shows you the role shop for your server</li>
</ul>

<b>Fun commands:</b>
<ul>
  <li>`%joke` ==> sends a joke</li>
  <li>`meme` ==> sends a dank meme</li>
  <li>`%gif {result number} {name}` ==> searches giphy for a gif and sends it</li>
  <li>`%youtube {result number} {name}` ==> searches youtube for a video and sends it</li>
  <li>`%message {user} {message}` ==> sends a direct message to a user</li>
  <li>`%rps {rock/paper/scissors}` ==> plays a game of rock paper scissors against Hurb</li>
  <li>`%doggo` ==> shows you a cute doggo</li>
  <li> `%catto` ==> shows you a cute catto</li>
  <li>`%autodoggo` ==> shows you a new doggo every 5 seconds</li>
  <li>`%stopautodoggo` ==> stops showing you a doggo every 5 seconds</li>
  <li>`%autocatto` ==> shows you a new catto every 5 seconds</li>
  <li>`%stopautocatto` ==> stops showing you a new catto every 5 seconds</li>
  <li>`%automeme` ==> shows you a meme every 7 seconds</li>
  <li>`%stopautomeme` ==> stop showing you a meme every 7 seconds</li>
  <li>`%topic` ==> gives you a conversation topic to get people active on your server</li>
  <li>`%hangman` ==> starts a game of hangman</li>
  <li>`@offline` ==> pings all offline members</li>
</ul>
  

<b>Fun features:
These are features that can be turned on and off with the `%enable {command}` and `%disable {command}` commands</b>
<ul>
  <li>`nonocheck` ==> checks for swear words, deletes them, and warns the sender</li>
  <li>`linkcheck` ==> checks for links, deletes them, and warns the sender</li>
  <li>`invitecheck` ==> checks for invites, deletes them, and warns the sender</li>
  <li>`welcome` ==> welcomes people to the server; can be customized with `%setwelcomechannel {channel} {message}`</li>
  <li>`goodbye` ==> displays a message when a member leaves the server; can be customized with `%setgoodbyechannel {channel} {message}`</li>
  <li>`nitro` ==> auto-converts emoji format parts of messages; for example `:catblob:` could be auto-converted into a moving rainbow cat blob emoji, this will be elaborated on later</li>
</ul>
  
<b>Elaboation on the nitro command:</b>

<i><b>Whenever a failed emoji is sent, such as `:catblob:`, if that emoji is from a server that Hurb is in, it will delete the message and send it from a bot looking exactly like you, with the same profile picture and name. This is something that other bots dedicate their whole selves to, but Hurb integrates it seamlessly into the flow of the bot. You can even use emojis from other servers that Hurb is in, for that real 'nitro' feel. View all the emojis you can use with the `%emojis` command, and emojis from specific servers by using `%emojis {servername}`</b></i>

Hurb has many other great and unique features, but to see those you'll have to check it out for yourself! 


<a href="https://discord.com/api/oauth2/authorize?client_id=736283988628602960&permissions=2081418359&scope=bot"><button>Click here to add Hurb to your server!</button></a>
</body>
</html>"""

def setup(bot):
    bot.add_cog(HelpCog(bot))
