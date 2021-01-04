import discord
from discord.ext import commands
import asyncio
import json
import random


class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.petList = {"dog": 100000, "cat": 200000, "turtle": 300000, "monkey": 400000, "rock": 50000, "fish": 75000}
        self.play_cooldown = commands.CooldownMapping.from_cooldown(1.0, 30.0, commands.BucketType.user)

    async def cogCheck(self, message, cooldown):
        if cooldown == "play_cooldown":
            bucket = self.play_cooldown.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                return False
            else:
                return True

    @commands.command(aliases=["petlist", "petshop"])
    async def pets(self, ctx):
        embed = discord.Embed(title=f"Pet shop:")
        for pet, cost in self.petList.items():
            embed.add_field(name=pet.capitalize(), value=f"Cost: ${cost}")
        await ctx.send(embed=embed)

    # pet: {"123456789": {"pet": {"name": "billy", "species": "turtle", "level": 1, "xp": 0}}

    @commands.command()
    async def Pet(self, ctx, condition1=None, condition2=None, *, condition3=None):
        storage = json.load(open("servers.json"))
        if "pet" in storage["players"][str(ctx.author.id)].keys():
            pet = storage["players"][str(ctx.author.id)]["pet"]
        else:
            pet = None
        if condition1 is None:
            embed = discord.Embed(title=f"{pet['name'].capitalize()} the {pet['species']}")
            embed.add_field(name="Level:", value=pet['level'])
            embed.add_field(name="Experience", value=pet['xp'])
            await ctx.send(embed=embed)
        elif condition2 is None:
            condition1 = condition1.lower()
            if condition1 == "buy":
                await ctx.send(embed=discord.Embed(
                    description=f"Please specify a name and species for your pet {ctx.author.mention}! The format is: `%pet buy species name`",
                    color=discord.Color.red()))
            elif condition1 == "view":
                await self.Pet(ctx)
            elif condition1 == "play":
                if await self.cogCheck(ctx.message, "play_cooldown"):
                    maxXP = (pet['level']*200)+(20*pet['level'])
                    newXP = random.randint(pet['level'], pet['level']*10)
                    await ctx.send(f"You played with {pet['name']}, and it gained {newXP} xp.")
                    pet['xp'] += newXP
                    if newXP >= maxXP:
                        pet['level'] += 1
                        pet['xp'] = newXP - maxXP
                        await ctx.send(f"Congrats! {pet['name']} has leveled up to level {pet['level']}!")
        elif condition3 is None:
            if condition1 == "buy":
                await ctx.send(embed=discord.Embed(
                    description=f"Please specify a species for your pet {ctx.author.mention}! The format is: `%pet buy species name`",
                    color=discord.Color.red()))
        else:
            if condition1 == "buy":
                storage["players"][str(ctx.author.id)]["pet"] = {"name": condition3, "species": condition2, "level": 1, "xp": 0}
                await ctx.send(embed=discord.Embed(
                    description=f"You now own a pet {condition2} named {condition3}! Treat it with care, and play with it to level it up! Type `%pet` to see its info!",
                    color=discord.Color.green()))
        if pet is not None:
            storage["players"][str(ctx.author.id)]["pet"] = pet
        json.dump(storage, open("servers.json", "w"), indent=4)


def setup(bot):
    bot.add_cog(Pets(bot))
