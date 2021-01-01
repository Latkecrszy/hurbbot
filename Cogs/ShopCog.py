import discord
import random
import time
import json
from discord.ext import commands


class Shop:
    def __init__(self, name, displayName, price, *, actions):
        self.name = name
        self.price = price
        self.displayName = displayName
        self.actions = actions


shopItems = [Shop(name="computer", displayName=":desktop:  **computer**", price=3000, actions="Game, code, amazon"),
             Shop(name="phone", displayName=":telephone:  **phone**", price=5000, actions="PrankCall, CopCall, MobileGame, amazon"),
             Shop(name="coke", displayName=":tropical_drink:  **coke**", price=1000, actions="sugarHigh"),
             Shop(name="airpods", displayName=":headphones:  **airpods**", price=1000, actions="music, flex")]
"""shopItems = []

computer = Shop(name="Computer", price=3000, actions="Become addicted to video games, create a bot")
shopItems.append(computer)
phone = Shop(name="Phone", price=5000, actions="Prank call people, call the cops, play shitty mobile games, search amazon")
shopItems.append(phone)
coke = Shop(name="Coke", price=1000, actions="Get a sugar high")
shopItems.append(coke)
airpods = Shop(name="Airpods", price=1000, actions="Act like an asshole and listen to music in class, flex on people")
shopItems.append(airpods)"""


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = None
        self.shopItems = shopItems
        with open("/Users/sethraphael/PycharmProject/Bots/items.json", "r") as f:
            self.items = json.load(f)
        with open("/Users/sethraphael/PycharmProject/Bots/money.json", "r") as r:
            self['money'] = json.load(r)

    @commands.command()
    async def buy(self, ctx, item):
        with open("/Users/sethraphael/PycharmProject/Bots/money.json", "r") as r:
            self['money'] = json.load(r)
        with open("/Users/sethraphael/PycharmProject/Bots/items.json", "r") as f:
            self.items = json.load(f)
        itemFound = False
        for i in self.shopItems:
            if i.name == item.lower():
                itemFound = True
        if itemFound:
            if str(ctx.author) in self['money'].keys():
                for x in range(len(self.shopItems)):
                    if self.shopItems[x].name == item:
                        value = self.shopItems[x].price
                        break
                if value <= self['money'][str(ctx.author)]:
                    if str(ctx.author) in self.items.keys():
                        self.name = str(ctx.author)
                        itemList = [item]
                        for i in self.items[str(self.name)]:
                            itemList.append(i)
                        self.items[str(ctx.author)] = itemList
                    elif str(ctx.author) not in self.items.keys():
                        self.name = str(ctx.author)
                        itemList = [item]
                        self.items[str(ctx.author)] = itemList
                    embed = discord.Embed(title=f"You have bought a(n) {item} for {value}. You now have ${self['money'][str(ctx.author)]}.", color=discord.Color.green())
                    await ctx.send(embed=embed)
                    userMoney = self['money'][str(ctx.author)]
                    userMoney -= value
                    self['money'][str(ctx.author)] = userMoney
                    with open("/Users/sethraphael/PycharmProject/Bots/money.json", "w") as f:
                        json.dump(self['money'], f, indent=4)
                    with open("/Users/sethraphael/PycharmProject/Bots/items.json", "w") as r:
                        json.dump(self.items, r, indent=4)
                elif value > self['money'][str(ctx.author)]:
                    embed = discord.Embed(
                        title=f"You do not have enough money to purchase this item, {ctx.author.display_name}!",
                        description=f"This item costs ${value}, and you only have {self['money'][str(ctx.author)]}!",
                        color=discord.Color.red())
                    await ctx.send(embed=embed)

        elif not itemFound:
            embed = discord.Embed(title="Bro wtf are you thinking that item isn't even in the shop.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx):
        with open("/Users/sethraphael/PycharmProject/Bots/money.json", "r") as r:
            self['money'] = json.load(r)
        with open("/Users/sethraphael/PycharmProject/Bots/items.json", "r") as f:
            self.items = json.load(f)

        inventory = self.items[str(ctx.author)]
        inventoryItems = []
        for i in inventory:
            for p in self.shopItems:
                if str(i) == p.name.lower():
                    inventoryItems.append(f"{p.displayName}\n{p.actions} \n\n")
        myInventory = "".join(inventoryItems)
        embed = discord.Embed(title=myInventory, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def use(self, ctx, item, action):
        with open("/Users/sethraphael/PycharmProject/Bots/money.json", "r") as r:
            self['money'] = json.load(r)
        with open("/Users/sethraphael/PycharmProject/Bots/items.json", "r") as f:
            self.items = json.load(f)
        itemFound = False
        inventory = self.items[str(ctx.author)]
        for i in inventory:
            if i.name == item.lower():
                itemFound = True
                for p in self.shopItems:
                    if item.lower() == p.name:
                        actions = p.actions.split(", ")
                        for a in actions:
                            if a.lower() == actions.lower():
                                pass

        for i in inventory:
            for p in self.shopItems:
                if str(i) == p.name.lower():
                    pass


def setup(bot):
    bot.add_cog(ShopCog(bot))
