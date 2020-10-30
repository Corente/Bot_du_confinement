import discord, os, asyncio, schedule
from datetime import date, time, datetime
from discord.ext import commands

TOKEN = 'Ton token ici'

description = '''Le bot du reconfinement'''
bot = commands.Bot(command_prefix='?')

#Les Chans textuels ou ils faut envoyer les messages auto
channels = ['tes channels ici']
#La date de fin du confinement
fin = datetime("fin format : yyyy, mm, dd")
#Le lien pour avoir l'attestation de sortie:
attestation_link = "https://media.interieur.gouv.fr/deplacement-covid-19/"

#La fonction qui creer un msg pour le confinement lié au weekend
def message_du_weekend(commence):
    if (commence):
        m = "Le confinement du weekend commence !"
    else:
        m = "Le confinement du weekend est fini !"
    return m

#La fonction qui creer un msg pour le couvre feu
def message_du_couvre_feu(commence):
    if (commence):
        m = "C'est le couvre feu !"
    else:
        m = "C'est la fin du couvre feu !"
    return m

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#La fonction qui envoit le message du confinement du weekend sur les channels
async def confinement_weekend():
    await bot.wait_until_ready()
    while not bot.is_closed():
        jour = datetime.now().weekday()
        heure = datetime.strftime(datetime.now(),'%H:%M')
        if (jour == 4 and heure == '19:00'):
            for i in channels:
                sender = bot.get_channel(i)
                m = message_du_weekend(True)
                await sender.send(m)
            t = 90
        elif (jour == 0 and heure == '6:00'):
            for i in channels:
                sender = bot.get_channel(i)
                m = message_du_weekend(False)
                await sender.send(m)
            t = 90
        else:
            t = 1
        await asyncio.sleep(t)

#La fonction qui envoit le message du couvre feu sur les channels
async def couvre_feu():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.strftime(datetime.now(),'%H:%M')
        jour = datetime.now().weekday()
        if (now == '19:00' and jour != 6 and jour != 5 and jour != 4):
            for i in channels:
                sender = bot.get_channel(i)
                m = message_du_couvre_feu(True)
                await sender.send(m)
            t = 90
        elif (now == '6:00' and jour != 0 and jour != 6 and jour != 5):
            for i in channels:
                sender = bot.get_channel(i)
                m = message_du_couvre_feu(False)
                await sender.send(m)
            t = 90
        else:
            t = 1
        await asyncio.sleep(t)

@bot.command()
async def timer(ctx):
    """Affiche le temps restant des mesures sanitaires"""
    mtn = datetime.now()
    ret = fin - mtn
    if (ret.days > 0):
        m = "Il reste " + str(ret.days) + " jours avant la des mesures sanitaires."
    elif (ret.days == 0):
        m = "C'est le dernier des mesures sanitaires." 
    else:
        m = "des mesures sanitaires sont finis !"    
    await ctx.send(m)

@bot.command()
async def que_faire(ctx):
    """Vous indique la procdure à suivre"""
    jour = datetime.now().weekday()
    mtn = datetime.strftime(datetime.now(),'%H:%M')
    if ((mtn >= '19:00' and mtn <= '6:00' and jour >= 0 and jour <= 4) or jour == 5 or jour == 6 ):
        await ctx.send("Reste chez toi batard !")
    else:   
        await ctx.send("Va travailer connard !")

@bot.command()
async def attestation(ctx):
    """Donne le lien pour l'attestation de deplacement"""
    await ctx.send(attestation_link)

bot.loop.create_task(confinement_weekend())
bot.loop.create_task(couvre_feu())
bot.run(TOKEN)
