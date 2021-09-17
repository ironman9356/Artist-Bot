from discord.ext import commands
import pickle
import asyncio


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        if message.author.bot:
            return
        with open("./swearwords.dat", 'rb') as file:
            a = pickle.load(file)
            swear_words = []
            for word in a:
                swear_words.append(word.strip())
            for i in range(len(swear_words)):
                if swear_words[i] in msg.split(" "):
                    reply = await message.reply(
                        "No swearing please.\nThis message will be auto deleted in few seconds.")
                    await message.delete()
                    await asyncio.sleep(5)
                    await reply.delete()


def setup(bot):
    print("Loaded Moderation")
    bot.add_cog(moderation(bot))
