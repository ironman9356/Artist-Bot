import os
import subprocess

try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
    subprocess.run('pip install -U git+https://github.com/ironman9356/discord.py',shell=True)
    import discord
    from discord.ext import commands

from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.all()


class ArtistBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(">"),
            owner_ids={
                548530397034577930,
                580385287297957888,
                732143432998322267
            },
            case_insensitive=True,
            intents=intents,
            strip_after_prefix=True,
            self_bot=False,
            activity=discord.Activity(type=discord.ActivityType.watching, name='kristian lose his mind ')
        )

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'discord version {discord.__version__}')
        print('------')


bot = ArtistBot()


@bot.command(help="To load a Cog")
@commands.is_owner()
async def load(ctx, cog):
    try:
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded {cog}')
    except commands.ExtensionNotLoaded:
        await ctx.send('That extention is already loaded')


@bot.command(help="To unload a Cog")
@commands.is_owner()
async def unload(ctx, cog):
    try:
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded {cog}')
    except commands.ExtensionNotLoaded:
        await ctx.send('That extention is already unloaded')


@bot.command(help="To reload a Cog")
@commands.is_owner()
async def reload(ctx, cog):
    bot.reload_extension(f"cogs.{cog}")
    await ctx.send(f"{cog} was reloaded")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
# bot.load_extension("jishaku")

bot.run(os.getenv("TOKEN"))
