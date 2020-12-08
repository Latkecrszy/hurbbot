from flask import make_response, jsonify, Flask, render_template
import os
import discord
from discord.ext import commands
import json
app = Flask(__name__)

bot = None


class Leaderboard(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot
        global bot
        bot = _bot

    @commands.command()
    async def leaderboard(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"Leaderboard for {ctx.guild}",
                                           description=f"[Click here to see the leaderboard](https://hurbsite.herokuapp.com/{ctx.guild.id})"))



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


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<id>')
def todo(id):
    data = _leaderboard(id)
    return data


def position(member):
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


def _leaderboard(ID):
    with open("/Users/sethraphael/PycharmProject/REST/templates/index.html", "r") as f:
        file = f.read()
    memberOrder = {}
    newMemberOrder = {}
    with open("/Users/sethraphael/PycharmProject/Hurb/Bots/rank.json") as f:
        messages = json.load(f)
    members = messages[str(ID)]
    for member in members.keys():
        guild = bot.get_guild(ID)
        member = guild.get_member(int(member))
        if member is not None and not member.bot:
            memberOrder[position(member)] = member

    for x in range(len(memberOrder.keys())):
        newMemberOrder[min(memberOrder.keys())] = memberOrder[min(memberOrder.keys())]
        memberOrder.pop(min(memberOrder.keys()))
    num = 1
    print(newMemberOrder)
    return newMemberOrder


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)


def setup(_bot):
    _bot.add_cog(Leaderboard(_bot))

# https://hurbsite.herokuapp.com/todo
# https://discord.com/oauth2/authorize?access_type=online&client_id=204255083083333633&redirect_uri=https%3A%2F%2Fyagpdb.xyz%2Fconfirm_login&response_type=code&scope=identify+guilds&state=n0kCQj0D80GANM22xDLQBgTFpljgF311CruMY7uksEY%3D&prompt=none
