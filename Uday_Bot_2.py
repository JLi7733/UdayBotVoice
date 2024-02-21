from elevenlabs import generate, stream, set_api_key, voices, play, save
import os, discord, asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio

#Set up the proper API keys

#THIS SHIT DON'T WORK AND I'M GOING TO KILL A BITCH
set_api_key(os.getenv('ELEVENLABS_API_KEY'))
discordKey = os.getenv('DISCORD_API_KEY')
voices = voices()

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

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

# Uday Bot Voice Modules
#
# Since we are doing more complicated things than just text we want to have commands
# Thus we use a bot which should take in variables and respond properly

@bot.event
async def on_ready():
    print(f'Voice module is ready as {bot.user.name}')

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
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

    else:
        await voiceGen("UH OH STINKY!.")
        await ctx.send("testing here")

bot.run(discordKey)