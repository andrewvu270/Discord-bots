# from asyncio import tasks
from nextcord.ext import tasks, commands
from datetime import datetime

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "hello":
            await msg.channel.send("Hi!")

    @commands.command()
    async def black(self, ctx):
        await ctx.send("White!")
    
    @commands.command()
    async def ayo(self, ctx):
        await ctx.send("ayo!")

    @tasks.loop(seconds=5)
    async def hello(self, ctx):
        await ctx.send("task")

    @commands.command()
    async def start(self, ctx):
        self.hello.start(ctx)
        
    @commands.command()
    async def stop(self, ctx):
        self.hello.stop()

    @tasks.loop(seconds = 1)
    async def alarm (self, ctx, hour, minute):
        now = datetime.now().time()
        if now.hour == hour and now.minute == minute:
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send("Its time now!!")
            self.alarm.stop()

    @commands.command()
    async def startalarm(self, ctx,date):
        hour, minute = date.split(":")
        hour = int(hour)
        minute = int(minute)
        self.alarm.start(ctx, hour, minute)
        


def setup(bot):
    bot.add_cog(MyCog(bot))