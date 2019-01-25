import discord, asyncio, requests, json, random; from discord.ext import commands

with open("databases/thesacredtexts.json") as f:
    config = json.load(f)
    
class AntiToxic():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def toxicity(self, ctx, *, msg):
        originalMsg = await ctx.send("**<a:artificialGenius:512314405313314846> Loading...**")
        msg = msg.replace('"', '').replace("'", '')
        msg = msg.encode("utf-8")
        data = '{comment: {text: ' + f'"{msg}"' + '}, \
                languages: ["en"], \
                requestedAttributes: {TOXICITY:{}} }'
        response = requests.post(f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={config['tokens']['toxickey']}", data=data)
        result = response.json()
        if result["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.70:
            await originalMsg.edit(content="**Likely** to be percieved as toxic. I'm **" + str(round(result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]*100)) +'%** sure.')
        else:
            await originalMsg.edit(content="**Unlikely** to be percieved as toxic. I'm **" + str(round(result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]*100)) +'%** sure.')
    
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.command()
    async def antitoxic(self, ctx):
        with open('databases/antitoxiclist.txt') as f:
            channels = f.read().split()
        
        intChannels = []

        for channel in channels:
            intChannels.append(int(channel))

        channels = intChannels
        print(channels)

        if ctx.channel.id in channels:
                channels.remove(ctx.channel.id)
                m = await ctx.send("**This channel is no longer in anti-toxic mode**")
        else:
            channels.append(ctx.channel.id)
            m = await ctx.send("**This channel is now in anti-toxic mode. Do `$antitoxic` to turn it off/toggle it**")

        print(channels)
        z = ''
        with open('databases/antitoxiclist.txt', 'w') as f:
            for i in channels:
                z+=f"{i} "
            f.write(z)
            f.close()
        
        await m.add_reaction("a:artificialGenius:512314405313314846")

    async def on_message(self, ctx):
        if ctx.author.bot == True:
            return
        with open('databases/antitoxiclist.txt') as f:
            result = f.read().split()
            channels = []
            for i in result:
                channels.append(int(i))
        if ctx.channel.id in channels:
            msg = ctx.content.replace('"', '').replace("'", '')
            msg = msg.encode("utf-8")
            data = '{comment: {text: ' + f'"{msg}"' + '}, \
                    languages: ["en"], \
                    requestedAttributes: {TOXICITY:{}} }'
            response = requests.post(f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={config['tokens']['toxickey']}", data=data)
            result = response.json()
            if result["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.70:
                await ctx.delete()

            else:
                pass
        else:
            pass

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.bot == True:
            return
        with open('databases/antitoxiclist.txt') as f:
            result = f.read().split()
            channels = []
            for i in result:
                channels.append(int(i))
        if after.channel.id in channels:
            msg = after.content.replace('"', '').replace("'", '')
            msg = msg.encode("utf-8")
            data = '{comment: {text: ' + f'"{msg}"' + '}, \
                    languages: ["en"], \
                    requestedAttributes: {TOXICITY:{}} }'
            response = requests.post(f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={config['tokens']['toxickey']}", data=data)
            result = response.json()
            if result["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.70:
                await after.delete()

            else:
                pass
        else:
            pass

def setup(bot):
    bot.add_cog(AntiToxic(bot))
