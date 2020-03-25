import discord, os, asyncio, schedule
from datetime import date, time, datetime
from discord.ext import commands

TOKEN = 'Le token du bot'

description = '''ConfinnementBot in Python'''
bot = commands.Bot(command_prefix='?')

channels = ['Les channels id ou envoyer les msg']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def time_check():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.strftime(datetime.now(),'%H:%M')
        if (now == 'L heure du message journalier :  HH:MM'):
            for i in channels:
                sender = bot.get_channel(i)
                fin = datetime('la date de fin: yyyy, mm, dd')
                mtn = datetime.now()
                ret = fin - mtn
                m = "Il reste " + str(ret.days) + " jours avant la fin du confinement."
                await sender.send(m)
            t = 90
        else:
            t = 1
        await asyncio.sleep(t)

@bot.command()
async def timer(ctx):
    """Affiche le temps restant en confinnement"""
    fin = datetime('la date de fin: yyyy, mm, dd')
    mtn = datetime.now()
    ret = fin - mtn
    send = "Il reste " + str(ret.days) + " jours avant la fin du confinement."
    await ctx.send(send)

bot.loop.create_task(time_check())
bot.run(TOKEN)
