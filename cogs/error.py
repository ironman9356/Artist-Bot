from discord.ext import commands


class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(":warning: You are not permitted to use this command :warning:")


def setup(bot):
    print("Loaded Error")
    bot.add_cog(error(bot))
