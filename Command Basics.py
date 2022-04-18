from nextcord import Interaction
import nextcord
import random
from nextcord.ext import commands
from datetime import datetime
bot = commands.Bot(command_prefix="!", help_command=None)

def is_me(ctx):
    return ctx.author.id == 355866770898157591

def starts_with_a(msg):
    return msg.content.startwith("a") #or msg.content.startswith("!purge")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)

    if num == 1:
        await ctx.send("Heads!")
    if num == 2:
        await ctx.send("Tails!")

@bot.command()
async def rps(ctx, hand):
    hands = ["✌️", "✋", "✊"]
    bothand = random.choice(hands)
    await ctx.send(bothand)
    if hand == bothand:
        await ctx.send("Its a draw!")
    elif hand == "✌️":
        if bothand == "✊":
            await ctx.send("I won!")
        if bothand == "✋":
            await ctx.send("You won..")
    elif hand == "✋":
        if bothand == "✌️":
            await ctx.send("I won!")
        if bothand == "✊":
            await ctx.send("You won..")
    elif hand == "✊":
        if bothand == "✋":
            await ctx.send("I won!")
        if bothand == "✌️":
            await ctx.send("You won..")

@bot.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = nextcord.Embed(title = "Commands", description = "These are the Commands that you can use for this bot", color = nextcord.Colour.dark_purple())
    MyEmbed.set_thumbnail(url = "https://images.gamebanana.com/img/ico/sprays/617466274d5c8.png")
    MyEmbed.add_field(name = "!ping", value = "This Command replies back with Pong whenever you write '!ping'", inline=False)
    MyEmbed.add_field(name = "!coinflip", value = "This Command lets you flip a coin whenever you write '!coinflip'", inline=False)
    MyEmbed.add_field(name = "!rps", value = "This Command allows you to play a game of rock paper scissor with the bot whenever you write '!rps' + hand emoji ':v:' for scissor, ':fist:' for rock and ':raised_hand:' for paper", inline=False)
    await ctx.send(embed = MyEmbed)

@bot.group()
async def edit(ctx):
    pass

@edit.command()
async def serverName(ctx, *, input):
    await ctx.guild.edit(name=input)

@edit.command()
async def region(ctx, *, input):
    await ctx.guild.edit(region=input)

@region.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Please enter a valid region name")

@edit.command()
async def createtextchannel(ctx, *, input):
    await ctx.guild.create_text_channel(name=input)

@edit.command()
async def createvoicechannel(ctx, *, input):
    await ctx.guild.create_voice_channel(name=input)

@edit.command()
async def createrole(ctx, *, input):
    await ctx.guild.create_role(name=input)

@bot.command()
@commands.has_role("Marvel Fan")
async def kick(ctx, member : nextcord.Member, *, reason=None):
    await ctx.guild.kick(member, reason = reason)

@kick.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have the Role for this command")

@bot.command()
@commands.has_role("Marvel Fan")
async def ban(ctx, member : nextcord.Member, *, reason=None):
    await ctx.guild.ban(member, reason = reason)

@ban.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have the Role for this command")


@bot.command()
@commands.has_role("Marvel Fan")
async def unban(ctx, *, input):
    name, discriminator = input.split("#")
    banned_members = await ctx.guild.bans()
    for bannedmember in banned_members:
        username = bannedmember.user.name
        disc = bannedmember.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(bannedmember.user)
 
@unban.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have the Role for this command")


@bot.command()
@commands.check(is_me) #check user
async def purge(ctx, amount, day:int=None, month:int=None, year:int=datetime.now().year):
    if amount == "/":
        if day == None or month == None:
            return
        else:
            await ctx.channel.purge(after = datetime(year, month, day))#, check=starts_with_a))#purg msg start with 'a'
    else:
        await ctx.channel.purge(limit = int(amount)+1)#, check=starts_with_a)

@purge.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify either a date or a number!") 
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You can only have a number or slash as the 1st input!")

    
@bot.command()
async def mute(ctx, user: nextcord.Member):
    await user.edit(mute=True)

@bot.command()
async def unmute(ctx, user: nextcord.Member):
    await user.edit(mute=False)

@bot.command()
async def deafen(ctx, user: nextcord.Member):
    await user.edit(deafen=True)

@bot.command()
async def undeafen(ctx, user: nextcord.Member):
    await user.edit(deafen=False)

@bot.command()
async def voicekick(ctx, user: nextcord.Member):
    await user.edit(voice_channel = None)

@bot.command()
async def unload(ctx):
    bot.unload_extension("Cogs")

@bot.command()
async def load(ctx):
    bot.load_extension("Cogs")

@bot.command()
async def reload(ctx):
    bot.reload_extension("Cogs")

@bot.slash_command(guild_ids = [400936246290939904], description="sends back yo when you type hello")
async def hello(interaction: Interaction, name):
    await interaction.response.send_message(f"Yo {name}!")

bot.load_extension("Cogs")
bot.run("OTY0NDE0MTkyMjYwMTAwMTU3.YlkStQ.ymXRzL5TnReidXgRMqwToNzKcLE")