import discord
from discord.ext import commands
from Bots.Cogs.players import saveMoney, refreshBalance
import random
import json


class RouletteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def allCheck(self, ctx, bet):
        if bet >= 2 ** 31:
            embed = discord.Embed(title="Bro, that number is WAY too big; come back to me when it's smaller.")
            await ctx.send(embed=embed)
            return True
        elif bet <= 0:
            await ctx.send(embed=discord.Embed(title=f"Don't try to bet less than 0 lol stealing money is not good."))
            return True

    async def tooMuchCheck(self, ctx, bet: int):
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]

        if int(bet) > int(players[str(ctx.author.id)]['money']):
            embed = discord.Embed(title=f"Bro, don't try to bet more than you have. I don't want to break ;(")
            await ctx.send(embed=embed)
            return False
        elif int(bet) <= 0:
            await ctx.send(embed=discord.Embed(title=f"Don't try to bet less than 0 LOL I don't want to break",
                           color=discord.Color.red()))

        else:
            return True

    @commands.command(aliases=["r", "R", "Roulette", "ROULETTE"])
    async def roulette(self, ctx, bet, number: str):
        validBets = ["black", "red", "high", "low", "row1", "row2", "row3", "1-12", "13-24", "25-36"]
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]

        playerMoney = int(players[str(ctx.author.id)]['money'])
        if bet.lower() == "all":
            bet = playerMoney
        bet = int(bet)
        if not await self.allCheck(ctx, bet):
            if await self.tooMuchCheck(ctx, bet):
                numbers = ["1", "2", "3", "4", "5", "6", '7', "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                           "18", "19", "20", "21", "22", "23", "24", "25",
                           "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "0", "00"]
                if number.lower() not in validBets and number not in numbers:
                    await ctx.send("Bro u frickin idiot that's not a valid thing to bet on")
                else:
                    numberHit = random.choice(numbers)
                    if int(numberHit) != 0 and int(numberHit) != 00:
                        if int(numberHit) % 2 == 1:
                            numberColor = "black"
                        else:
                            numberColor = "red"
                    else:
                        numberColor = ""
                    if int(numberHit) != 0 and int(numberHit) != 00:
                        if int(numberHit) < 18:
                            numberPlace = "low"
                        else:
                            numberPlace = "high"
                    else:
                        numberPlace = ""
                    if number in numbers:
                        if int(numberHit) == int(number):
                            playerMoney += int(bet) * 35
                            if int(numberHit) != 0 and int(numberHit) != 00:
                                embed = discord.Embed(
                                    title=f"Congrats, {ctx.author.display_name}! It was {numberColor} {numberHit}! You just won ${bet * 35}!",
                                    color=discord.Color.green())
                            else:
                                embed = discord.Embed(
                                    title=f"Congrats, {ctx.author.display_name}! It was {numberHit}! You just won ${bet * 35}!",
                                    color=discord.Color.green())

                        else:
                            playerMoney -= int(bet)
                            if int(numberHit) != 0 and int(numberHit) != 00:
                                embed = discord.Embed(
                                    title=f"Sorry, {ctx.author.display_name}. It was {numberColor} {numberHit}. You lost ${bet}.",
                                    color=discord.Color.red())
                            else:
                                embed = discord.Embed(
                                    title=f"Sorry, {ctx.author.display_name}. It was {numberHit}. You lost ${bet}.",
                                    color=discord.Color.red())

                    else:
                        if numberPlace == number or numberColor == number:
                            embed = discord.Embed(
                                title=f"Congrats, {ctx.author.display_name}! It was {number} {numberHit}! You won ${bet}!",
                                color=discord.Color.green())
                            playerMoney += int(bet)
                        else:
                            playerMoney -= int(bet)
                            if number.lower() == "black" or number.lower() == "red":
                                embed = discord.Embed(
                                    title=f"Sorry, {ctx.author.display_name}, it was {numberColor} {numberHit}. You lost ${bet}.",
                                    color=discord.Color.red())
                            else:
                                embed = discord.Embed(
                                    title=f"Sorry, {ctx.author.display_name}, it was {numberPlace} {numberHit}. You lost ${bet}.",
                                    color=discord.Color.red())
                    players[str(ctx.author.id)]['money'] = playerMoney
                    storage["players"][str(ctx.author.id)] = player
                    json.dump(storage, open("../Bots/servers.json", "w"), indent=4)
                    await ctx.send(embed=embed)

    @commands.command()
    async def slots(self, ctx, bet):
        bet = int(bet)
        storage = json.load(open("../Bots/servers.json"))
        players = storage["players"]


        playerMoney = int(players[str(ctx.author.id)]['money'])
        if await self.allCheck(ctx, bet) or not await self.tooMuchCheck(ctx, bet):
            pass
        else:
            slotsImages = [":poop: ", ":eye: ", ":microbe: ", ":peach: ", ":hot_pepper: ", ":eggplant:", ":middle_finger: ", ":gorilla: ", ":full_moon_with_face: "]
            slotsChoices = []
            for x in range(3):
                slotsChoices.append(random.choice(slotsImages))
            if slotsChoices[0] == slotsChoices[1] == slotsChoices[2]:
                embed = discord.Embed(title=f'**>** {"".join(slotsChoices)} **<**',
                                      description=f"WHOOOO! YOU WON THE F*CKIN JACKPOT BRO!!! Here's ${bet * 1000} my dude!",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                playerMoney += (bet * 100)
            elif slotsChoices[0] == slotsChoices[1] or slotsChoices[0] == slotsChoices[2] or slotsChoices[1] == slotsChoices[2]:
                embed = discord.Embed(title=f'**>** {"".join(slotsChoices)} **<**',
                                      description=f"Congrats! You won ${bet}!",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                playerMoney += int(bet)
            else:
                embed = discord.Embed(title=f'**>** {"".join(slotsChoices)} **<**',
                                      description=f"Oof, {ctx.author.mention}, you lost ${bet}.",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                playerMoney -= int(bet)
            players[str(ctx.author.id)]['money'] = playerMoney
            storage["players"] = players
            json.dump(storage, open("../Bots/servers.json", "w"), indent=4)


def setup(bot):
    bot.add_cog(RouletteCog(bot))