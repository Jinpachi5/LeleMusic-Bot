# Discord
import discord
from discord.ext import commands
from discord import app_commands

# API's
from youtubepy import AsyncVideo
from youtubepy import ExtractData

# System
import os
from dotenv import load_dotenv
load_dotenv()

getGuild = discord.Object(id=941945255618572319)
TOKEN = os.environ['DISCORD_TOKEN']


class musicBot(discord.Client):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all(),
                         activity=discord.Game(name='Vibes'), status=discord.Status.dnd)
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=getGuild)
        self.synced = True
        print("ready")


bot = musicBot()
tree = app_commands.CommandTree(bot)
voiceBool = False


def voice_Toggle():
    global voiceBool
    voiceBool = not voiceBool
    return voiceBool


async def link_Translate(link: str):
    if ("open.spotify" in link):
        # Use spotify api to get song title
        print("bruh")
    else:
        ytvid = AsyncVideo(f"{link}")
        result = await ytvid.search()

    return result


@tree.command(name="ping", description="Returns the ping to the user", guild=getGuild)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")


@tree.command(name="play", description="Plays the song", guild=getGuild)
async def self(interaction: discord.Interaction, song: str):
    video = AsyncVideo(f"{song}")
    result = await video.search()
    title = ExtractData(result).title()
    print(result)
    voice_client = interaction.user.voice
    global voiceBool
    if (voice_client and not voiceBool):
        channel = interaction.user.voice.channel
        voice_Toggle()
        await channel.connect()
        await interaction.response.send_message(f"Playing: {str(title)}")
    elif (voice_client and voiceBool):
        await interaction.response.send_message(f"Playing: {str(title)}")
    else:
        voice_Toggle()
        await interaction.response.send_message(f"You are not in a voice channel, you must be in a voice channel to run this command!")


@tree.command(name="leave", description="Disconnects Lele if you no longer need her.", guild=getGuild)
async def self(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message("Goodbye!")
    else:
        await interaction.response.send_message("Lele is not connected to a voice channel.")


bot.run(TOKEN)
