from importlib.metadata import files
import nextcord, youtube_dl, os, asyncio
from nextcord.ext import commands
bot = commands.Bot(command_prefix = "!")
queuelist = []
filestodelete = []

@bot.command()
@commands.has_role("DJ")
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

@bot.command()
@commands.has_role("DJ")
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
@commands.has_role("DJ")
async def play(ctx, *, searchword):
    ydl_opts = {}
    voice = ctx.voice_client

    # Get the title
    if searchword[0:4] == 'http' or searchword[0:3] == 'www':
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(searchword, download = False)
            title = info["title"]
            url = searchword

    if searchword[0:4] != 'http' and searchword[0:3] != 'www':
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{searchword}", download = False)["entries"][0]
            title = info["title"]
            url = info["webpage_url"]

    ydl_opts = {
        "format" : "bestaudio/best",
        "outtmpl" : f"{title}.mp3",
        "postprocessors" : [{"key" : "FFmpegExtractAudio", "preferredcodec" : "mp3", "preferredquality" : "192"}]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    #Playing and Queueing Audio
    if voice.is_playing():
        queuelist.append(title)
        await ctx.send(f"Added to Queue: ** {title} **")
    else:
        voice.play(nextcord.FFmpegPCMAudio(f"{title}.mp3"), after = lambda e : check_queue())
        await ctx.send(f"Playing: ** {title} ** :musical_note:")
        filestodelete.append(title)
        await bot.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.listening, name=title))

    def check_queue():
        try:
            if queuelist[0] != None:
                voice.play(nextcord.FFmpegPCMAudio(f"{queuelist[0]}.mp3"), after = lambda e : check_queue())
                coro = bot.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.listening, name=title))
                fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                fut.result()
                filestodelete.append(queuelist[0])
                queuelist.pop(0)
        except IndexError:
            for file in filestodelete:
                os.remove(f"{file}.mp3")
            filestodelete.clear()

@bot.command()
@commands.has_role("DJ")
async def pause(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        voice.pause()
    else: 
        await ctx.send("Bot is not playing Audio!")

@bot.command(aliases = ["skip"])
@commands.has_role("DJ")
async def stop(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        voice.stop()
    else: 
        await ctx.send("Bot is not playing Audio!")

@bot.command()
@commands.has_role("DJ")
async def resume(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        await ctx.send("Bot is playing Audio!")
    else: 
        voice.resume()

@bot.command()
@commands.has_role("DJ")
async def viewqueue(ctx):
    await ctx.send(f"Queue: ** {str(queuelist)} ** ")

@join.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("You have to be connected to a Voice Channel to use this command.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@leave.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@play.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@stop.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@resume.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@pause.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

bot.run("OTY0NDE0MTkyMjYwMTAwMTU3.YlkStQ.ymXRzL5TnReidXgRMqwToNzKcLE")