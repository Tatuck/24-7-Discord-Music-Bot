from discord.ext import commands
import discord

class SurpressOff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user:
            if after.channel == None:
                channel = await self.bot.fetch_channel(self.bot.channelID)
                try:
                    await channel.connect()
                except Exception as e:
                    if "Already connected to a voice channel." in str(e):
                        pass
                    else:
                        raise e
            if after.suppress and channel.type == discord.ChannelType.stage_voice:
                me = await after.channel.guild.fetch_member(self.bot.user.id)
                await me.edit(suppress = False)

def setup(bot):
    bot.add_cog(SurpressOff(bot))