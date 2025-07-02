import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

stations = {
    "eska": "http://n-04.eska.pl/eska48.aac",
    "rmf-fm": "http://stream3.rmf.fm:8000/rmf_fm",
    "rmf-maxx": "http://195.150.20.242:8000/rmf_maxxx",
    "vox-fm": "http://91.232.4.33:7340",
    "zet": "http://zdigitalstream.radiozet.pl/RadioZet",
    "melo-radio": "http://meloradio128.streaming.rspectrumnet.com.pl:8000/melo"
}

ffmpeg_options = {'options': '-vn'}

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}!")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Pauza.")
    else:
        await ctx.send("Nie ma nic do zatrzymania.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Wznowiono.")
    else:
        await ctx.send("Nie ma nic do wznowienia.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Zatrzymano radio.")
    else:
        await ctx.send("Bot nie jest na kanale głosowym.")

@bot.command()
async def play(ctx, *, name):
    name = name.lower()
    if name not in stations:
        await ctx.send("Nie znam takiej stacji.")
        return

    if ctx.author.voice is None:
        await ctx.send("Dołącz najpierw do kanału głosowego.")
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    ctx.voice_client.stop()
    source = discord.FFmpegPCMAudio(stations[name], **ffmpeg_options)
    ctx.voice_client.play(source)
    await ctx.send(f"▶️ Gra {name.capitalize()}")

@bot.command() async def eska(ctx): await play(ctx, name="eska")
@bot.command() async def rmf_fm(ctx): await play(ctx, name="rmf-fm")
@bot.command() async def rmf_maxx(ctx): await play(ctx, name="rmf-maxx")
@bot.command() async def vox_fm(ctx): await play(ctx, name="vox-fm")
@bot.command() async def zet(ctx): await play(ctx, name="zet")
@bot.command() async def melo_radio(ctx): await play(ctx, name="melo-radio")

bot.run(os.getenv("DISCORD_TOKEN"))
