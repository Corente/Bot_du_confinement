import discord, os, asyncio, schedule
from datetime import date, time, datetime
from discord.ext import commands

TOKEN = 'YOUR TOKEN HERE'

description = '''ConfinnementBot in Python'''
bot = commands.Bot(command_prefix='?')

channels = ['Chanels id you want to have automatic message every day']

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
        if (now == '12:00'):
            for i in channels:
                sender = bot.get_channel(i)
                fin = datetime('END DATE yyyy, mm, dd')
                mtn = datetime.now()
                ret = fin - mtn
                if (ret.days > 0):
                    m = "Il reste " + str(ret.days) + " jours avant la fin du confinement."
                elif (ret.days == 0):
                    m = "C'est le dernier jour du confinement." 
                else:
                    m = "Le confinement est fini !"
                await sender.send(m)
            t = 90
        else:
            t = 1
        await asyncio.sleep(t)

@bot.command()
async def timer(ctx):
    """Affiche le temps restant en confinnement"""
    fin = datetime('END DATE yyyy, mm, dd')
    mtn = datetime.now()
    ret = fin - mtn
    if (ret.days > 0):
        m = "Il reste " + str(ret.days) + " jours avant la fin du confinement."
    elif (ret.days == 0):
        m = "C'est le dernier jour du confinement." 
    else:
        m = "Le confinement est fini !"    
    await ctx.send(m)

@bot.command()
async def que_faire(ctx):
    """Vous indique la procdure à suivre"""
    await ctx.send("Restez chez vous !")

bot.loop.create_task(time_check())
bot.run(TOKEN)
