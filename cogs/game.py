import discord
import random
import datetime
from discord.ext import commands , tasks
import sqlite3
import subprocess 


db = sqlite3.connect('./database/rps.db')
cur = db.cursor()

def win(author_id, guild_id):
    cur.execute(f'select user_id,wins from rps where guild_id="{guild_id}" and user_id="{author_id}"')
    result = cur.fetchall()
    if not result:
        cur.execute(f'insert into rps values("{author_id}","{guild_id}",1,0,0)')
        db.commit()
        return
    cur.execute(f'UPDATE rps SET wins={result[0][1] + 1} WHERE user_id="{author_id}" and guild_id="{guild_id}"')
    db.commit()


def lose(author_id, guild_id):
    cur.execute(f'select user_id,losses from rps where guild_id="{guild_id}" and user_id="{author_id}"')
    result = cur.fetchall()
    if not result:
        cur.execute(f'insert into rps values("{author_id}","{guild_id}",0,1,0)')
        db.commit()
        return
    cur.execute(f'UPDATE rps SET losses={result[0][1] + 1} WHERE user_id="{author_id}" and guild_id="{guild_id}"')
    db.commit()


def tie(author_id, guild_id):
    cur.execute(f'select user_id,ties from rps where guild_id="{guild_id}" and user_id="{author_id}"')
    result = cur.fetchall()
    if not result:
        cur.execute(f'insert into rps values("{author_id}","{guild_id}",0,0,1)')
        db.commit()
        return
    cur.execute(f'UPDATE rps SET ties={result[0][1] + 1} WHERE user_id="{author_id}" and guild_id="{guild_id}"')
    db.commit()


class Roshambo(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=15.0)
        self.value = None
        self.user = None
        self.ctxuser= None
        self.gitupdate.start()
    
    @tasks.loop(minutes=10)
    async def gitupdate(self):
        print("Attempting to update database")
        try:
            subprocess.run("git add database/rps.db",shell=True)
            subprocess.run("git commit -m 'database update' ",shell=True)
            subprocess.run("git push origin master",shell=True)
        except Exception as e:
            print(e)
            print("Update failed")
            return
        print("GIT UPDATED")

    @discord.ui.button(label="Rock", emoji="🪨")
    async def rock(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.scissors.emoji = "<:scissor:888314061299810325>"
        self.value = "rock"
        self.user = interaction.user
        self.paper.style = discord.ButtonStyle.red
        self.rock.style = discord.ButtonStyle.green
        self.scissors.style = discord.ButtonStyle.red
        self.rock.disabled = True
        self.paper.disabled = True
        self.scissors.disabled = True
        self.stop()

    @discord.ui.button(label="Paper", emoji="📰")
    async def paper(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.scissors.emoji = "<:scissor:888314061299810325>"
        self.value = "paper"
        self.user = interaction.user
        self.paper.style = discord.ButtonStyle.green
        self.rock.style = discord.ButtonStyle.red
        self.scissors.style = discord.ButtonStyle.red
        self.rock.disabled = True
        self.paper.disabled = True
        self.scissors.disabled = True
        self.stop()

    @discord.ui.button(label="Scissors", emoji="✂")
    # @discord.ui.button(label="Scissors", emoji="<:scissor:888314061299810325>")
    async def scissors(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.scissors.emoji = "<:scissor:888314061299810325>"
        self.value = "scissors"
        self.user = interaction.user
        self.paper.style = discord.ButtonStyle.red
        self.rock.style = discord.ButtonStyle.red
        self.scissors.style = discord.ButtonStyle.green
        self.rock.disabled = True
        self.paper.disabled = True
        self.scissors.disabled = True
        self.stop()


class game(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.group(aliases=["roshambo"], invoke_without_command=True, case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def rps(self, ctx):
        """PLAY ROCK PAPER SCISSOORS (ROSHAMBO) WITH THE BOT"""
        rps = Roshambo()

        message = await ctx.reply("ROSHAMBO!", view=rps)
        await rps.wait()
        if not rps.value:
            rps.paper.style = discord.ButtonStyle.red
            rps.rock.style = discord.ButtonStyle.red
            rps.scissors.style = discord.ButtonStyle.red
            rps.rock.disabled = True
            rps.paper.disabled = True
            rps.scissors.disabled = True
            await message.edit(view=None)
            embed=discord.Embed(description="Time's up",color=discord.Color.red())
            await message.reply(view=rps, embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
        if rps.user.id != ctx.author.id:
            rps.paper.style = discord.ButtonStyle.red
            rps.rock.style = discord.ButtonStyle.red
            rps.scissors.style = discord.ButtonStyle.red
            rps.rock.disabled = True
            rps.paper.disabled = True
            rps.scissors.disabled = True
            await message.edit(view=None)
            await message.reply(view=rps, content=f"`{rps.user.name}` reacted before `{ctx.author.name}`\nSo I stopped")
            ctx.command.reset_cooldown(ctx)
            return

        options = ["rock", "paper", "scissors"]
        bot_choice = random.choice(options)
        author_choice = rps.value
        
        if bot_choice == author_choice:
            await message.edit(view=None)
            embed=discord.Embed(title="TIE",description=f"You and I chose {author_choice.title()}",color=discord.Color.yellow())
            tie(ctx.author.id, ctx.guild.id)
            await message.reply(embed=embed, view=rps)
            
            
        elif bot_choice == "rock" and author_choice == "paper":
            await message.edit(view=None)
            embed=discord.Embed(title="YOU WIN",description=f"My Choice: {bot_choice.title()}\nYour choice: {author_choice.title()}",color=discord.Color.green())
            win(ctx.author.id, ctx.guild.id)
            await message.reply(
                embed=embed, view=rps)
        elif bot_choice == "rock" and author_choice == "scissors":
            await message.edit(view=None)
            embed=discord.Embed(title="YOU LOSE",description=f"My Choice: {bot_choice.title()}\nYour choice: {author_choice.title()}",color=discord.Color.red())
            lose(ctx.author.id, ctx.guild.id)
            await message.reply(
               embed=embed, view=rps)

        elif bot_choice == "paper" and author_choice == "rock":
            await message.edit(view=None)
            embed=discord.Embed(title="YOU LOSE",description=f"My Choice: {bot_choice.title()}\nYour choice: {author_choice.title()}",color=discord.Color.red())
            lose(ctx.author.id, ctx.guild.id)
            await message.reply(
               embed=embed, view=rps)

        elif bot_choice == "paper" and author_choice == "scissors":
            await message.edit(view=None)
            embed=discord.Embed(title="YOU WIN",description=f"My Choice: {bot_choice.title()}\nYour choice: {author_choice.title()}",color=discord.Color.green())
            win(ctx.author.id, ctx.guild.id)
            await message.reply(
                embed=embed, view=rps)
            
        elif bot_choice == "scissors" and author_choice == "paper":
            await message.edit(view=None)
            embed=discord.Embed(title="YOU LOSE",description=f"My Choice: {bot_choice.title()}\nYour choice: {author_choice.title()}",color=discord.Color.red())
            lose(ctx.author.id, ctx.guild.id)
            await message.reply(
               embed=embed, view=rps)
            

        elif bot_choice == "scissors" and author_choice == "rock":
            await message.edit(view=None)
            embed=discord.Embed(title="YOU WIN",description=f"My Choice: {bot_choice.title()}\nYour choice: {author_choice.title()}",color=discord.Color.green())
            win(ctx.author.id, ctx.guild.id)
            await message.reply(
                embed=embed, view=rps)
            
    @rps.command(aliases=["stat"])
    async def stats(self, ctx, member: discord.Member = None):  # nunber:int
        """YOUR/THE PERSON YOU MENTIONED STATS"""
        if not member:
            member = ctx.author
        if member.id == self.client.user.id:
            return await ctx.send("Stats for the bot is not saved")
        cur.execute(f'select wins , losses , ties from rps where user_id="{member.id}" and guild_id="{ctx.guild.id}"')
        result = cur.fetchall()

        if not result:
            return await ctx.send(f"{member.name} has never played")
        embed = discord.Embed(title="Stats", description=f"Stats of {member.name}", timestamp=datetime.datetime.now(),
                              color=member.color)
        embed.add_field(name="Total Games Played", value=f"{result[0][0] + result[0][1] + result[0][2]} games",
                        inline=False)
        embed.add_field(name="Wins", value=f"{result[0][0]} Wins")
        embed.add_field(name="Losses", value=f"{result[0][1]} Losses")
        embed.add_field(name="Ties", value=f"{result[0][2]} Ties")
        if result[0][1] == 0:
            embed.add_field(name="W/L ratio", value=f"Ratio: {result[0][0]}.0")
            embed.add_field(name="Win %", value=f"{result[0][0]}00 %")
        elif result[0][1] != 0:
            embed.add_field(name="W/L ratio", value=f"Ratio: {round(result[0][0] / result[0][1], 2)}")
            embed.add_field(name="Win %", value=f"{round(result[0][0] / result[0][1], 4) * 100} %")
        embed.set_footer(text="Stats as of")
        embed.set_author(name=f"Stats of {member.name}")

        embed.set_thumbnail(url=member.avatar.with_format("png"))

        await ctx.send(embed=embed)

    @rps.command()
    async def wins(self, ctx, member: discord.Member = None):
        """YOUR/THE PERSON YOU MENTIONED WINS"""
        if not member:
            member = ctx.author
        if member.id == self.client.id:
            return await ctx.send("Wins for the bot is not saved")
        cur.execute(f'select wins , losses , ties from rps where user_id="{member.id}" and guild_id="{ctx.guild.id}"')
        result = cur.fetchall()
        if not result:
            return await ctx.send(f"{member.name} has never played")
        await ctx.send(f"{member.name} has {result[0][0]} wins")

    @rps.command(aliases=["loss"])
    async def losses(self, ctx, member: discord.Member = None):
        """YOUR/THE PERSON YOU MENTIONED LOSSES"""
        if not member:
            member = ctx.author
        if member.id == self.client.id:
            return await ctx.send("Losses for the bot is not saved")
        cur.execute(f'select wins , losses , tie from rps where user_id="{member.id}" and guild_id="{ctx.guild.id}"')
        result = cur.fetchall()
        if not result:
            return await ctx.send(f"{member.name} has never played")
        await ctx.send(f"{member.name} has {result[0][1]} losses")

    @rps.command(aliases=["tie"])
    async def ties(self, ctx, member: discord.Member = None):
        """YOUR/THE PERSON YOU MENTIONED TIES"""
        if not member:
            member = ctx.author
        if member.id == self.client.id:
            return await ctx.send("Ties for the bot is not saved")
        cur.execute(f'select wins , losses , ties from rps where user_id="{member.id}" and guild_id="{ctx.guild.id}"')
        result = cur.fetchall()
        if not result:
            return await ctx.send(f"{member.name} has never played")
        await ctx.send(f"{member.name} has {result[0][2]} ties")

    @rps.group(invoke_without_command=True, aliases=['lb'], case_insensitive=True)
    async def leaderboard(self, ctx):
        """SERVER LEADERBOARD"""
        cur.execute(
            f"select user_id,wins from rps where guild_id='{ctx.guild.id}' group by user_id order by wins DESC;")
        result = cur.fetchall()
        final = ""
        n = 0

        if not result:
            return await ctx.send("The leaderboard is empty")
        for i in result:
            n += 1
            if n == 11:
                break
            if i[1] == 0:
                continue
            try:
                final += f"**{n}.** {self.client.get_user(int(i[0])).name} :  {i[1]} wins\n"
            except Exception:
                continue

        embed = discord.Embed(title=":trophy: ROSHAMBO LEADERBOARD :trophy:", description=final.strip(), color=0x05ffd5,timestamp=datetime.datetime.now())
        embed.set_footer(text="Stats as of")
        try:
            embed.set_thumbnail(url=ctx.guild.icon.with_format("png"))
        except Exception:
            pass
        await ctx.send(embed=embed)

    @leaderboard.command()
    @commands.is_owner()
    async def reset(self, ctx):
        """TO RESET THE LEADER BOARD OF THE SERVER ( BOT OWNER ONLY )"""
        cur.execute(f"delete from rps where guild_id='{ctx.guild.id}';")
        db.commit()

        await ctx.send("Cleared the leaderboard")




def setup(bot):
    print("Loaded Game")
    bot.add_cog(game(bot))