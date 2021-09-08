from discord.ext import commands

class thread(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_thread_join(self,thread):
        x = await thread.fetch_members()
        if len(x) == 1  :
            await thread.send("Don't forget to follow rules even when you are in a thread :slight_smile: ")


def setup(bot):
    print('Loaded Thread')
    bot.add_cog(thread(bot))