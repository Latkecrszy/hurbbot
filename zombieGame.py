import discord
from discord.ext import commands
import asyncio


class ZombieGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gotocar = False
        self.callpolice = False
        self.downstairs = False
        self.takeelevator = False
        self.gasstation = False
        self.pizzashop = False
        self.policestation = False
        self.canleave = False
        self.caneatchips = False
        self.canaccept = False
        self.candecline = False
        self.actions = [self.gotocar, self.callpolice, self.downstairs,
                        self.takeelevator, self.gasstation,
                        self.pizzashop, self.policestation, self.canleave, self.caneatchips, self.canaccept,
                        self.candecline]
        self.availableActions = []

    @commands.command()
    async def zombiegame(self, ctx):
        embed = discord.Embed(description='''This game is a text adventure game made to test your general knowledge, critical thinking,
        and problem solving abilities. You can use cash to buy items like ammo and weapons.
        If you tak risky choices and succeed, you will be rewarded greatly with prestige levels. You gain cash every
        time you level up. If there are any problems with this game, please email the makers of this
        game at akronnie55@gmail.com or setharaphael7@gmail.com.\n\nGreetings! You live in an apartment building near Toronto, Canada. You work as a mechanic,
        you're skilled at rock climbing, and your hobby is racing. Your life has been amazing until August 17, during
        the night, at around 11 PM...\n\nYou feel tired, so you decide to go to bed. After an hour, you wake up in your bed, deprived of sleep.
        Everything is quiet, so you think everything is normal, but you are awfully wrong. You open the fridge to grab a drink of juice, but you hear a disturbing
        retching sound outside. You open the window and you see a man walking around on the street. You close the window
        just in time to hear a scream outside. You open the window again, and the first man is grabbing another person
        by the head and ripping his head off. You start to feel dizzy. You think you're imagining things, but you hear
        a chorus of howling nearby. You step into the balcony of your home, bathed in
        moonlight, just in time to see a horde of zombies running down the road towards your apartment building. You
        see them enter the lobby, and you hear another scream. The lady at the front desk has mutated into a zombie as
        well. What do you do?\n\nDo you:
        Call 911 -> type `call911`
        Run downstairs to investigate -> type `stairs`
        Climb down to your car -> type `car`
        Call the respective command in the chat below.''', color=discord.Color.green())
        await ctx.send(embed=embed)
        self.revert(self.callpolice, self.gotocar, self.downstairs)

    @commands.command()
    async def car(self, ctx):
        if self.gotocar in self.availableActions:
            await ctx.send('''
            You gather your valuables, grab your family photos (you don't feel like leaving them behind), open your
            apartment window and casually climb down to the first floor. The zombies can't see you leave, but they
            smell flesh, so you quickly open your car door, hop in the driver seat, and drive away.
            15 minutes later, you come across an abandoned gas station. A sign up ahead says that there is a pizza shop
            1 mile away, and there is a police station 3.5 miles away. Where do want to go?
            Do you:
            1) Visit the gas station -> type `gasstation`
            2) Go to the pizza shop -> type `pizzashop`
            3) Go to the police station -> type `policestation`
            Call the respective command in the chat below.''')
            self.revert(self.gasstation, self.pizzashop, self.policestation)
        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def stairs(self, ctx):
        if self.downstairs in self.availableActions:
            await ctx.send('''You try to climb down the stairs, but the zombies rush up the stairs at eye-blurring speed. You are ambushed by a horde of hungry, bloodthirsty
            zombies, and you die a quick, painless death.''')
            self.revert()
        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def elevator(self, ctx):
        if self.takeelevator in self.availableActions:
            await ctx.send('''
            You press the elevator button, but nothing works, because the zombies cut out the power. What do you do?
            Do you:
            1) Go down via the stairs -> type `stairs`
            2) Get to the car instead -> type `car`
            Call the respective command in the chat below.''')
            self.revert(self.downstairs, self.gotocar)
        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def call911(self, ctx):
        if self.callpolice in self.availableActions:
            await ctx.send('''
            You grab your phone to call 911, but the phone battery is dead. You look for your charger, but the
            electricity stops working. The zombies must have switched off the power generator. Isn't that a little
            too smart for a zombie to behave? What do you do now?
            Do you:
            1) Run downstairs -> type `stairs`
            2) Get to your car ASAP -> type `car`
            3) Take the elevator -> type `elevator`
            Call the respective command in the chat below.''')
            self.takeelevator = True
            self.gotocar = True
            self.downstairs = True
            self.revert(self.takeelevator, self.gotocar, self.downstairs)
        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def gasstation(self, ctx):
        if self.gasstation in self.availableActions:
            await ctx.send('''You fill up your car with gas, and walk around. You see a small shop, so ou open the door, and you hear a
            dinging noise. You flinch, but you realize that it's the bell on the door.
            The shop is empty, but you see some snack bags on the ground, and you pick them up.
            It looks like someone has messed with the bag, because there are blood marks on the bag and it has been
            opened. You look inside, and it smells weird. You take a chip, and examine it.

            Do you:
            1) Eat it -> type `eatchips`
            2) Leave -> type `leave`
            Call the respective command in the chat below.''')
            self.revert(self.caneatchips, self.canleave)
        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def eatchips(self, ctx):
        if self.caneatchips in self.availableActions:
            await ctx.send('''
                You take a nibble on the chip, and you realize too late what is going to happen next. You start to leak blood everywhere.
                You start to wonder how this happened, but too late; You are welcomed into the arms of death.''')
            self.revert()
        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def leave(self, ctx):
        if self.canleave in self.availableActions:
            await ctx.send('''You decide that since you filled up your car with gas, you can visit the pizza shop or the police station.
            Where do you choose to go?
            Do you:
            1) Drive to the pizza shop -> type `pizzashop`
            2) Drive to the police station -> type `policestation`
            Call the respective command in the chat below.''')
            self.revert(self.pizzashop, self.policestation)
        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def pizzashop(self, ctx):
        if self.pizzashop in self.availableActions:
            await ctx.send('''
                You decide to go to the pizza shop, because you were starving. On the way there, you see a zombie, no wait,
                its another survivor! You drive over to him, and he thinks you're a zombie, so he yells, "Back off, stinky
                citizen!", and shoots your tire.
                    "Dude, i'm just another survivor, like you!", you shout.
                Relieved, the guy walks over to you, apoligizes for shooting your tire, and shakes hands with you.
                    "I'm terribly sorry for shooting your tire. How can I repay you?"
                    "No thanks, i'm a mechanic, so I always carry a tool kit.", you say.
                    After talking for a few minutes, the guy asks you,
                    "I have a gang of 3 survivors and a dog a little south of here. I can help you survive if you join me...
                    do you wanna join us?"

                    Do you:
                    1) Accept his offer -> type `accept`
                    2) Decline his offer, you're going to go solo -> type `decline`
                    Call the respective command in the chat below.''')
            self.revert(self.canaccept, self.candecline)

        else:
            await self.cannotUse(ctx)

    @commands.command()
    async def policeStation(self, ctx):
        if self.policestation in self.availableActions:
            await ctx.send('''
            You decide to go to the police station, because you think its safe there. On the way there, you see a zombie,
            no wait,its another survivor! You drive over to him, and he thinks you're a zombie, so he yells,
                "Back off, stinky citizen!", and shoots your tire.
                "Dude, i'm just another survivor, like you!", you shout.
            Relieved, the guy walks over to you, apoligizes for shooting your tire, and shakes hands with you.
                "I'm terribly sorry for shooting your tire. How can I repay you?"
                "No thanks, i'm a mechanic, so I always carry a tool kit.", you say.
                After talking for a few minutes, the guy asks you,
                "I have a gang of 3 survivors and a dog a little south of here. I can help you survive if you join me...
                do you wanna join us?"

                Do you:
                1) Accept his offer -> type `accept`
                2) Decline his offer, you're going to go solo -> type `decline`
                Call the respective command in the chat below.''')
            self.revert()
        else:
            await self.cannotUse(ctx)

    def revert(self, command1=None, command2=None, command3=None, command4=None, command5=None):
        for x in range(len(self.availableActions)):
            del self.availableActions[x]
        for command in self.actions:
            if command == command1 or command == command2 or command == command3 or command == command4 or command == command5:
                self.availableActions.append(command)

    async def cannotUse(self, ctx):
        embed = discord.Embed(title=f"You cannot use this command at this time, {ctx.author.display_name}!",
                              color=discord.Color.red())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ZombieGame(bot))
