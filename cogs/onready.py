import asyncio
from datetime import datetime
from discord.ext import commands
import discord
import youtube_dl
import requests
import datetime

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}

FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_delay_max 5'

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
            with youtube_dl.YoutubeDL(YTDL_OPTS) as ydl:
                info = ydl.extract_info(url, download=False)
                streamUrl = info["formats"][0]["url"]
            expireDate = streamUrl.split("expire/")[1].split("/")[0]
            expireDate = datetime.datetime.fromtimestamp(int(expireDate))
            print(f"STREAM EXPIRES: {expireDate}")
            client = channel.guild.voice_client
            if client == None:
                await asyncio.sleep(300)
                break
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(streamUrl, before_options=FFMPEG_BEFORE_OPTS), 1)
            client.play(source)
            while client.is_playing():
                await asyncio.sleep(0.1)
            break
            #times = 0
            #while client.is_playing():
            #    times = times + 1
            #    if datetime.datetime.utcnow()>=expireDate:
            #        break
            #    if times >= 3600:
            #        await me.edit(suppress = False)
            #        times = 0
            #    await asyncio.sleep(0.1)

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            channel = await self.bot.fetch_channel(self.bot.channelID)
            try:
                await channel.connect()
            except:
                pass
            me = await channel.guild.fetch_member(self.bot.user.id)
            await me.edit(suppress = False)
            await self._playMusic(channel)

def setup(bot):
    bot.add_cog(OnReady(bot))

