from discord.ext import commands

class SurpressOff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user:
            if after.channel == None:
                channel = await self.bot.fetch_channel(self.bot.channel)
                try:
                    await channel.connect()
                except:
                    pass
            if after.suppress:
                me = await after.channel.guild.fetch_member(self.bot.user.id)
                await me.edit(suppress = False)

def setup(bot):
    bot.add_cog(SurpressOff(bot))