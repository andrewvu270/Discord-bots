import nextcord
intents = nextcord.Intents.all()
bot = nextcord.Client(intents = intents)

@bot.event
async def on_ready():
    print("SIR BOT IS ONLINE")
    
@bot.event
async def on_message(msg):
    username = msg.author.display_name
    if msg.author == bot.user:
        return
    else:
        if msg.content == "hello":
            await msg.channel.send("hello " + username)

@bot.event
async def on_memeber_join(member):
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Welcome to {guildname}!")

@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    member = payload.member
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)

    if emoji == "🕸️" and message_id == 964601847908302888:
        role = nextcord.utils.get(guild.roles, name = "Marvel Fan")
        await member.add_roles(role)

    if emoji == "🦇" and message_id == 964601810935496744:
        role = nextcord.utils.get(guild.roles, name = "DC Fan")
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    user_id = payload.user_id
    emoji = payload.emoji.name
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)

    if emoji == "🕸️" and message_id == 964601847908302888:
        role = nextcord.utils.get(guild.roles, name = "Marvel Fan")
        await member.remove_roles(role)

    if emoji == "🦇" and message_id == 964601810935496744:
        role = nextcord.utils.get(guild.roles, name = "DC Fan")
        await member.remove_roles(role)

bot.run("OTY0NDE0MTkyMjYwMTAwMTU3.YlkStQ.ymXRzL5TnReidXgRMqwToNzKcLE")