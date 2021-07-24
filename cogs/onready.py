import asyncio
from datetime import datetime
from discord.ext import commands
import discord
import youtube_dl
import requests
import datetime


ffmpeg_options = {
    'options': '-vn'
}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def _getStreamings(self):
        req = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?channelId={self.bot.youtubeID}&eventType=live&type=video&key={self.bot.youtubeApiKey}").json()
        try:
            return req["items"][0]["id"]["videoId"]
        except:
            print(req)
            return ""

    async def _playMusic(self, channel):
        while True:
            print("Getting music")
            url = f"https://www.youtube.com/watch?v={self._getStreamings()}"
            print(f"Got stream URL: {url}")
            if url == "":
                print("Waiting 10 seconds...")
                await asyncio.sleep(10)
                continue
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(url, download=False)
                streamUrl = info["url"]

            client = channel.guild.voice_client

            if client == None:
                await asyncio.sleep(10)
                break

            source = discord.FFmpegPCMAudio(streamUrl, **ffmpeg_options)
            client.play(source)

            while client.is_playing():
                await asyncio.sleep(0.1)
            break


    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            channel = await self.bot.fetch_channel(self.bot.channelID)
            try:
                await channel.connect()
            except Exception as e:
                if "Already connected to a voice channel." in str(e):
                    pass
                else:
                    raise e
            if channel.type == discord.ChannelType.stage_voice:
                me = await channel.guild.fetch_member(self.bot.user.id)
                await me.edit(suppress = False)
            await self._playMusic(channel)

def setup(bot):
    bot.add_cog(OnReady(bot))

