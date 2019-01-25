import discord, asyncio, time, datetime, random, json, aiohttp, logging, os
from discord.ext import commands
from time import ctime
from os import listdir; from os.path import isfile, join

with open("databases/thesacredtexts.json") as f:
    config = json.load(f)

class AntiToxic(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(">"),
                         owner_id=276707898091110400,
                         case_insensitive=True)

    async def update_activity(self):
        await self.change_presence(
            activity=discord.Activity(
                name=f"idk",
                type=1,
                url="https://www.twitch.tv/SpectrixYT"))
        print("Updated presence")
        payload = {"server_count"  : len(self.guilds)}
        url = "https://discordbots.org/api/bots/320590882187247617/stats"
        headers = {"Authorization" : config["tokens"]["dbltoken"]}
        async with aiohttp.ClientSession() as aioclient:
                await aioclient.post(
                    url,
                    data=payload,
                    headers=headers)
        print(f"Posted payload to Discord Bot List:\n{payload}")

    async def on_ready(self):
        print("=======================\nConnected\n=========")
        await self.update_activity()
        
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_guild_join(self, guild):
        await self.update_activity()
        try:
           pass # TODO
        except:
            pass

    async def on_guild_remove(self):
        await self.update_activity()

    def initiate_start(self):
        self.remove_command("help")
        lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
        no_py = [s.replace('.py', '') for s in lst]
        startup_extensions = ["cogs." + no_py for no_py in no_py]
        try:
            for cogs in startup_extensions:
                self.load_extension(cogs)
                print(f"Loaded {cogs}")
            print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
            super().run(config['tokens']['token'])
        except Exception as e:
            print(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\n\n\
                    THIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")

if __name__ == '__main__':
    AntiToxic().initiate_start()
