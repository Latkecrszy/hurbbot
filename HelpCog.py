import discord
from discord.ext import commands
import random

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

    @commands.command()
    async def help(self, ctx, command=None):
        if command is None:
            serverEmbed = discord.Embed(title="Help command for server management features of Hurb Bot:",
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
            await ctx.author.send(embed=funEmbed)
        elif command.lower() == "blackjack" or command.lower() == "bj":
            blackjackEmbed = discord.Embed(title="BlackJack Help:", color=random.choice(embedColors))
            blackjackEmbed.add_field(name="blackjack <bet>", value="Starts a game of blackjack with your bet. Example: `%blackjack 30` would start a game of blackjack with a bet of $30.")
            blackjackEmbed.add_field(name="hit", value="Draws another card for you in a game of blackjack.")
            blackjackEmbed.add_field(name="stand", value="Tells me not to draw another card for you in a game of blackjack.")
            await ctx.send(embed=blackjackEmbed)
        elif command.lower() == "roulette" or command.lower() == "r":
            rouletteEmbed = discord.Embed(title="Roulette Help:", color=random.choice(embedColors))
            rouletteEmbed.add_field(name="roulette <space> <bet>", value="Starts a game of roulette on the space you choose, with the bet you choose.")
            await ctx.send(embed=rouletteEmbed)
        elif command.lower() == "mute":
            muteEmbed = discord.Embed(title="Mute help:", color=random.choice(embedColors))
            muteEmbed.add_field(name="Mute <member> <reason>", value=f"Applies a mute to someone. If some of the channels are not being muted for the person, make sure that if they are locked, the role locking them is lower than the muted role. Preferably, ")


def setup(bot):
    bot.add_cog(HelpCog(bot))
