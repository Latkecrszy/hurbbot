import discord
from discord.ext import commands
import asyncio


class AppCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.applying = ""
        self.question = 0
        self.answers = []

    @commands.command(aliases=["APPLY", "Apply"])
    @commands.dm_only()
    async def apply(self, ctx):
        if self.applying == "":
            guild = self.bot.get_guild(751667811931390012)
            embed = discord.Embed(title=f"Hello aspiring mod! This is the application to carry you to your dreams of managing Art Gatherings! Fill out a survey answering the questions fully and understandably, and the mods will consider your application and get back to you within 2 days!",
                                  description=f"Please respond to these questions in full sentences. You may be funny, as the mods do have a sense of humor (except for layfa, don't worry about him), but please keep it appropriate.\nIf your application is denied, for whatever reason, don't think that all is lost! We still greatly value your contribution to our server, and there will be other opportunities to try again.\nNow, on to the application!")
            embed.add_field(name=f"How to respond:  ", value=f"Good news! Your application has already been started! Be warned, everything that you say in this DM will be in response to a question, so from here on out don't mess around. You will first type an answer to question 1, which will be listed below. Then, after you have sent it, your answer will be recorded, and the next question will be sent. Once everything is submitted, your submission will be immediately sent to the mods for approval. That's all! Good luck!")
            embed.add_field(name=f"Question 1: ", value=f"Why do you want to be a mod on this server? (4 sentence minimum)", inline=False)
            embed.set_footer(text=f"Created by Latkecrszy#0947")
            embed.set_author(name=f"Application for Manager role in {guild}", icon_url=guild.icon_url)
            await asyncio.sleep(1)
            self.applying = str(ctx.author)
            self.question = 1
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Someone is applying right now {ctx.author.mention}! Please try again in 5-10 minutes!")

    @commands.command()
    @commands.dm_only()
    async def form(self, ctx):
        await ctx.send(embed=discord.Embed(description=f"[Click here to fill our your application! Good luck!](https://docs.google.com/forms/d/e/1FAIpQLSc0yVliMSoswbvs_XsOByyXfZaKdf_xfs4XYwdMF44ZdRaE5A/viewform?usp=sf_link)",
                                           color=discord.Color.green()))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            if not message.author.bot:
                if self.applying == str(message.author):
                    if self.question == 1:
                        print(str(message.channel))
                        self.answers.append(str(message.content))
                        embed = discord.Embed(description=f"Your response for question one has been recorded {message.author.mention}! Now, on to question two!")
                        embed.add_field(name=f"Question 2: ", value=f"What do you think being a mod means? (4 sentence minimum)")
                        self.question = 2
                        await message.channel.send(embed=embed)
                    elif self.question == 2:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(description=f"Your response for question two has been recorded {message.author.mention}! Now, on to question three!")
                        embed.add_field(name=f"Question 3: ", value=f"Please rank your leadership abilities on a 1-10 scale, 1 being the worst, 10 being the best.")
                        self.question = 3
                        await message.channel.send(embed=embed)
                    elif self.question == 3:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(description=f"Your response for question three has been recorded {message.author.mention}! Now, on to question four!")
                        embed.add_field(name=f"Question 4: ", value=f"Please rank your assertiveness on a 1-10 scale, one being the worst, 10 being the best.")
                        self.question = 4
                        await message.channel.send(embed=embed)
                    elif self.question == 4:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(
                            description=f"Your response for question four has been recorded {message.author.mention}! Now, on to question five!")
                        embed.add_field(name=f"Question 5: ", value=f"Please tell us your strengths and weaknesses. (3 sentence minimum)")
                        self.question = 5
                        await message.channel.send(embed=embed)
                    elif self.question == 5:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(
                            description=f"Your response for question five has been recorded {message.author.mention}! Now, on to question six!")
                        embed.add_field(name=f"Question 6: ", value=f"Do you have previous modding experience? If so, tell us what.")
                        self.question = 6
                        await message.channel.send(embed=embed)
                    elif self.question == 6:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(
                            description=f"Your response for question six has been recorded {message.author.mention}! Now, on to question seven!")
                        embed.add_field(name=f"Question 7: ", value=f"Please explain why you'd be a good mod on this server. (3 sentence minimum)")
                        self.question = 7
                        await message.channel.send(embed=embed)
                    elif self.question == 7:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(
                            description=f"Your response for question seven has been recorded {message.author.mention}! Now, on to question eight!")
                        embed.add_field(name=f"Question 8: ", value=f"What would you do in the event of a spam raid? You don't need to be super specific, but please include some detail.")
                        self.question = 8
                        await message.channel.send(embed=embed)
                    elif self.question == 8:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(
                            description=f"Your response for question eight has been recorded {message.author.mention}! Now, on to question nine!")
                        embed.add_field(name=f"Question 9: ", value=f"What would you do if a mod was breaking the rules, eg. Layfa was randomly banning people.")
                        self.question = 9
                        await message.channel.send(embed=embed)
                    elif self.question == 9:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(
                            description=f"Your response for question nine has been recorded {message.author.mention}! Now, on to question ten!")
                        embed.add_field(name=f"Question 10: ", value=f"Lastly, what would you do in the event that someone was being rude on the server to others?")
                        self.question = 10
                        await message.channel.send(embed=embed)
                    elif self.question == 10:
                        self.answers.append(str(message.content))
                        embed = discord.Embed(
                            description=f"Your response for question ten has been recorded {message.author.mention}! WHOO! You're all done! Good job completing the application. You deserve a break!")
                        embed.add_field(name="If, for whatever reason, you have seconds doubts right now and DON'T want to submit, you can type anything other than submit in the chat.", value="If you do want to submit, type submit below, and your responses will be whisked away to the mods.")
                        self.question = 11
                        await message.channel.send(embed=embed)
                    elif self.question == 11:
                        if str(message.content).lower() == "submit":
                            self.question = 0
                            self.applying = ""
                            channel = self.bot.get_channel(751669703558168576)
                            embed = discord.Embed(title=f"Application from {message.author} for Mod: ")
                            embed.set_author(name=f"{message.author}", icon_url=message.author.avatar_url)
                            embed.add_field(name=f"Question: Why do you want to be a mod on this server? (4 sentence minimum)", value=f"Answer: **{self.answers[0]}**")
                            embed.add_field(name=f"Question: What do you think being a mod means? (4 sentence minimum)", value=f"Answer: **{self.answers[1]}**")
                            embed.add_field(name=f"Question: Please rank your leadership abilities on a 1-10 scale, 1 being the worst, 10 being the best.", value=f"Answer: **{self.answers[2]}**")
                            embed.add_field(name=f"Question: Please rank your assertiveness on a 1-10 scale, one being the worst, 10 being the best.", value=f"Answer: **{self.answers[3]}**")
                            embed.add_field(name=f"Question: Please tell us your strengths and weaknesses. (3 sentence minimum)", value=f"Answer: **{self.answers[4]}**")
                            embed.add_field(name=f"Question: Do you have previous modding experience? If so, tell us what.", value=f"Answer: **{self.answers[5]}**")
                            embed.add_field(name=f"Question: Please explain why you'd be a good mod on this server. (3 sentence minimum)", value=f"Answer: **{self.answers[6]}**")
                            embed.add_field(name=f"Question: What would you do in the event of a spam raid? You don't need to be super specific, but please include some detail.", value=f"Answer: **{self.answers[7]}**")
                            embed.add_field(name=f"Question: What would you do if a mod was breaking the rules, eg. Layfa was randomly banning people.", value=f"Answer: **{self.answers[8]}**")
                            embed.add_field(name=f"Question: Lastly, what would you do in the event that someone was being rude on the server to others?", value=f"Answer: **{self.answers[9]}**")
                            await channel.send(embed=embed)
                            role = discord.utils.get(channel.guild.roles, name="Artist Doggos")
                            await channel.send(f"{role.mention}, you guys should check this out! {message.author} just submitted this great application!")
                            embed = discord.Embed(description=f"Your application has been submitted {message.author.mention}! Good job! The mods will get back to you in 1-3 days. Sit tight, and don't worry about it! Enjoy the server!")
                            await message.channel.send(embed=embed)
                            self.answers = []
                        else:
                            embed = discord.Embed(description=f"Ok, your application submission has been cancelled. Feel free to try to submit again at any time. You've got this!")
                            await message.channel.send(embed=embed)
                            self.answers = []
                            self.question = 0
                            self.applying = ""

    @commands.command()
    async def startapp(self, ctx):
        channel = self.bot.get_channel(751668926148247674)
        await channel.send(ctx.guild.default_role)
        await channel.send(embed=discord.Embed(description=f"GREAT NEWS!!! WE JUST HIT 100 MEMBERS! NOW, AS A CELEBRATION, WERE ARE MAKING {discord.utils.get(ctx.guild.members, name='Titan#0415')} AN ARTIST DOGGO! WHOO!! WE ARE ALSO ACCEPTING APPLICATIONS FOR MODS ON THE SERVER! DM THE PHRASE `%apply` TO HURB TO GET THE APPLICATION VIA DISCORD, OR DM `%form` TO APPLY VIA GOOGLE FORM! GOOD LUCK TO YOU ALL, AND THANK YOU SO MUCH FOR 100 MEMBERS!!!!", color=discord.Color.green()))

    @commands.command()
    async def place(self, ctx, day):
        if day.lower() == "domingo":
            embed = discord.Embed(title=f"En domingo Bababooey va al cine ver películas.", color=discord.Color.green())
            embed.set_image(url='https://cdn.discordapp.com/attachments/716377034728931331/764247661833748510/Screen_Shot_2020-10-09_at_3.07.15_PM.png')
            embed.set_author(name=f"Domingo")
        elif day.lower() == "lunes":
            embed = discord.Embed(title=f"En lunes, yo voy a la esquela para estudiar.")
            embed.set_image(url='https://cdn.discordapp.com/attachments/716377034728931331/764247734274097192/Screen_Shot_2020-10-09_at_3.07.32_PM.png')
            embed.set_author(name=f"Lunes")
        elif day.lower() == "martes":
            embed = discord.Embed(title=f"En Martes, Charlito y yo vamos para las montañas hacer el deberes.")
            embed.set_image(url='https://cdn.discordapp.com/attachments/716377034728931331/764247787403083786/Screen_Shot_2020-10-09_at_3.07.43_PM.png')
            embed.set_author(name=f"Martes")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, *, message):
        message = message.split(",")
        while len(message) > 2:
            message[1] += message[2]
            del message[2]
        channel = self.bot.get_channel(751668926148247674)
        # 751668926148247674
        embed = discord.Embed(title=message[0], description=message[1], color=discord.Color.teal())
        embed.set_author(name=f"Announced by {ctx.author}", icon_url=ctx.author.avatar_url)
        role = discord.utils.get(ctx.guild.roles, name="Announcements")
        await channel.send(role.mention)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(AppCog(bot))
