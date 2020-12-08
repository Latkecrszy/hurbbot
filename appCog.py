from flask import make_response, jsonify, Flask, render_template
import os
import discord
from discord.ext import commands
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<id>')
def todo(id):
    data = id
    return data


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _leaderboard(self, ID):
        with open("/Users/sethraphael/PycharmProject/REST/templates/index.html", "r") as f:
            file = f.read()
        file.split("f")
        file[0] = file[0] + "\n<div>THIS IS A TEST</div>"
        file = file[0] + file[1]
        with open("/Users/sethraphael/PycharmProject/REST/templates/index.html", "w") as f:
            f.write(file)
        with open("/Users/sethraphael/PycharmProject/REST/templates/index.html", "r") as f:
            print(f.read())
        memberOrder = {}
        newMemberOrder = {}
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json") as f:
            messages = json.load(f)
        members = messages[str(ID)]
        for member in members.keys():
            guild = self.bot.get_guild(ID)
            member = guild.get_member(int(member))
            if member is not None and not member.bot:
                memberOrder[self.position(member)] = member

        for x in range(len(memberOrder.keys())):
            newMemberOrder[min(memberOrder.keys())] = memberOrder[min(memberOrder.keys())]
            memberOrder.pop(min(memberOrder.keys()))
        num = 1

    @commands.command()
    async def leaderboard(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"Leaderboard for {ctx.guild}",
                                           description=f"[Click here to see the leaderboard](http://0.0.0.0:5000/{ctx.guild.id})"))

    def position(self, member):
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json") as f:
            messages = json.load(f)
        messages = messages[str(member.guild.id)]
        XPs = {int(Member["xp"] + Member["level"] * (Member["level"] * 200)): ID for ID, Member in messages.items()}
        newXPs = XPs
        highs = {}
        for x in range(len(newXPs.keys())):
            highs[max(newXPs.keys())] = XPs[max(newXPs.keys())]
            newXPs.pop(max(newXPs.keys()))
        for key, value in highs.items():
            newXPs[value] = key

        numCount = 1
        for key, value in newXPs.items():
            if key != str(member.id):
                numCount += 1
            else:
                break
        return numCount

    def calcspot(self, member):
        with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json") as f:
            messages = json.load(f)
        messages = messages[str(member.guild.id)]
        xp = messages[str(member.id)]["xp"]
        newXp = int(xp / messages[str(member.id)]["level"] * 10)
        fullList = ["🟦" for x in range(int(newXp / 100))]
        for x in range(20 - int(newXp / 100)):
            fullList.append("⬛")
        return fullList


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)


def setup(bot):
    bot.add_cog(Leaderboard(bot))

# https://hurbsite.herokuapp.com/todo
# https://discord.com/oauth2/authorize?access_type=online&client_id=204255083083333633&redirect_uri=https%3A%2F%2Fyagpdb.xyz%2Fconfirm_login&response_type=code&scope=identify+guilds&state=n0kCQj0D80GANM22xDLQBgTFpljgF311CruMY7uksEY%3D&prompt=none
