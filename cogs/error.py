from discord.ext import commands



def convert(seconds:int):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if hour!=0 :
        if hour <= 10 and minutes <=10 :
            return f'{hour} hours {minutes} minutes {round(seconds)} seconds'
    elif hour==0 and minutes !=0 :
        return f'{minutes} minutes {round(seconds)} seconds'
    else:
        return f'{round(seconds)} seconds'

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(":warning: You are not permitted to use this command :warning:")
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown try after {convert(error.retry_after)}")
        else:
            print(error)

def setup(bot):
    print("Loaded Error")
    bot.add_cog(error(bot))
