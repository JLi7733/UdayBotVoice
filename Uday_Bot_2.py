from elevenlabs import generate, set_api_key, voices, save
import os, discord, asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
import json

#Set up the proper API keys

set_api_key(os.getenv('ELEVENLABS_API_KEY'))
discordKey = os.environ['DISCORD_API_KEY']
voices = voices()

#Function to generate the mp3 file we use
async def voiceGen(text):
    audio_stream = generate(
        text=text,
        stream=False,
        voice="Uday-Normal"
    )
    save(audio_stream, filename="line.mp3")

#Set up the discord client
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Uday Bot message modules
# Using a dictionary, we will respond to certain messages
# I use a json to store these messages as they are quite long. 

responseFile = "responses.json"
f = open(responseFile)
responses = json.load(f)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    
    # 3 ways we want messages to be sent
    # First is if they are just full words e.g. Hello responds hello
    # There is also the case of there being phrases, e.g. Hello world
    # and finally, just for this bot there is also the case of certain letters within a word
    # For example, there is a trigger for the construction for, which we purpousely want to send 
    # a message for even if it's a word like forever 

    full = message.content
    words = full.split()
    triggered = set()

    #Checking the first case
    for i in words:
        word = i.lower() 
        response = responses.get(word)
        if (response):
            triggered.add(word)
            await message.channel.send(response)
    
    #Checking for the second case
    for trigger in responses.keys():
        if trigger in full and trigger not in triggered:
            await message.channel.send(responses[trigger])


# Uday Bot Voice Modules
#
# Since we are doing more complicated things than just text we want to have commands
# Thus we use a bot which should take in variables and respond properly

@bot.event
async def on_ready():
    print(f'Voice module is ready as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Updating..."))

#Help commands
@bot.command()
async def help(ctx):
    await ctx.send("This is Uday Bot, designed by Jonathan Li written in python using the discord.py library and the Elevenlabs API")
    await ctx.send("If you want more information on what I can do type in !voice and !text")

@bot.command()
async def voice(ctx):
    await ctx.send("There are two commands, !say to generate a new line or !play to play an existing line")

@bot.command()
async def text(ctx):
    textHelp = "Here are the following trigger words for the bot: "
    for i in responses.keys():
        textHelp = textHelp + i + " "
    await ctx.send(textHelp)


#play pre-recorded voicelines
@bot.command()
async def play(ctx, *, file_name):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        if voice_client.is_playing():
            voice_client.stop()
        source = FFmpegPCMAudio("voicelines/" + file_name + ".mp3")
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

    else:
        await ctx.send("Go into a voice channel")

#Say whatever you want
@bot.command()
async def say(ctx, *, text):
    try:
        os.remove("line.mp3")
    except:
        print("line.mp3 doesn't exist yet")
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        await voiceGen(text + ".")
        source = FFmpegPCMAudio("line.mp3")
        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

    else:
        await ctx.send("Go into a voice channel")

bot.run(discordKey)