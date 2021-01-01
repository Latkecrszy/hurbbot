import discord
from discord.ext import commands
import json

oldColors = {discord.Color.blue(): "blue", discord.Color.blurple(): "blurple",
             discord.Color.dark_blue(): "dark_blue",
             discord.Color.dark_gold(): "dark_gold", discord.Color.dark_green(): "dark_green",
             discord.Color.dark_grey(): "dark_grey",
             discord.Color.dark_magenta(): "dark_magenta", discord.Color.blue(): "blue",
             discord.Color.dark_orange(): "dark_orange",
             discord.Color.dark_purple(): "dark_purple", discord.Color.dark_red(): "dark_red",
             discord.Color.dark_teal(): "dark_teal",
             discord.Color.darker_grey(): "darker_grey", discord.Color.default(): "black",
             discord.Color.gold(): "gold",
             discord.Color.green(): "green", discord.Color.greyple(): "greyple",
             discord.Color.light_grey(): "light_grey",
             discord.Color.magenta(): "magenta", discord.Color.orange(): "orange",
             discord.Color.purple(): "purple",
             discord.Color.teal(): "teal", discord.Color.red(): "red"}

colors = {value: key for key, value in oldColors.items()}


class BuyRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, color, *, name):
        color = colors[color.lower()]
        role = await ctx.guild.create_role(name=name, color=color, permissions=discord.Permissions(send_messages=True))
        await ctx.send(embed=discord.Embed(description=f"{role.mention} has been created {ctx.author.mention}.",
                                           color=discord.Color.green()))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, *, role: discord.Role):
        await role.delete()
        await ctx.send(f"{str(role)} has been deleted.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def roleprice(self, ctx, role: discord.Role, price):
        with open("../Bots/roleprice.json", "r") as f:
            roles = json.load(f)

        if str(ctx.guild) not in roles.keys():
            roles[str(ctx.guild)] = {}
        if price == "none" or price == "None" or price == "NONE":
            roles[str(ctx.guild)].pop(str(role))
        else:
            roles[str(ctx.guild)][str(role)] = int(price)
        with open("../Bots/roleprice.json", "w") as f:
            json.dump(roles, f, indent=4)

        await ctx.send(embed=discord.Embed(description=f"The price for {str(role)} has been set to {price}.",
                                           color=discord.Color.green()))

    @commands.command()
    async def buyrole(self, ctx, *, role: discord.Role):
        with open("../Bots/roleprice.json", "r") as f:
            roles = json.load(f)

        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"][str(ctx.author.id)]
        money = players[str(ctx.author.id)]['money']

        if role in ctx.author.roles:
            embed = discord.Embed(description=f"You already have this role {ctx.author.mention}!",
                                  color=discord.Color.red())
        else:
            if str(role) not in roles[str(ctx.guild)].keys():
                embed = discord.Embed(description=f"You cannot buy this role {ctx.author.mention}!",
                                      color=discord.Color.red())
            else:
                if int(money) <= roles[str(ctx.guild)][str(role)]:
                    embed = discord.Embed(
                        description=f"You do not have enough money to buy this role {ctx.author.mention}!",
                        color=discord.Color.red())
                else:
                    money -= int(roles[str(ctx.guild)][str(role)])
                    embed = discord.Embed(
                        description=f"You have purchased the {role} role for ${roles[str(ctx.guild)][str(role)]}.")
                    await ctx.author.add_roles(role)
        with open("../Bots/roleprice.json", "w") as f:
            json.dump(roles, f, indent=4)

        players[str(ctx.author.id)]['money'] = money
        storage["players"] = players
        json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
        await ctx.send(embed=embed)

    @commands.command()
    async def roleshop(self, ctx):
        with open("../Bots/roleprice.json", "r") as f:
            roles = json.load(f)

        embed = discord.Embed(title=f"Role shop for {ctx.guild}:")
        for role, price in roles[str(ctx.guild)].items():
            role = discord.utils.get(ctx.guild.roles, name=str(role))
            if role is not None:
                embed.add_field(name=f"Price: ${price}", value=f"Role: {role.mention}")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BuyRoleCog(bot))
