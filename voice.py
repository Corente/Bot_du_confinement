import discord, os, asyncio, schedule
from datetime import date, time, datetime
from discord.ext import commands

#Placer le token dans un fichier token.txt

f = open("token.txt", "r")
TOKEN = f.read()
f.close()

description = '''Le bot du reconfinement'''
bot = commands.Bot(command_prefix='?')

#Les Chans textuels ou ils faut envoyer les messages auto
channels = []
#La date de fin du confinement
fin = datetime(2080, 1, 1)
#Le lien pour avoir l'attestation de sortie:
attestation_link = "https://media.interieur.gouv.fr/deplacement-covid-19/"
#Le lien pour acceder au code source
github = "https://github.com/Corente/Bot_du_confinement"
#Le Dico Pour les sons marrant
dico = {
    "savon" : "sounds/avec-du-savon-macron.mp3",
    "marseillaise" : "sounds/la-marseillaise.mp3",
    "marsollaise" : "sounds/la-marsollaise.mp3",
    "etat" : "sounds/etat.mp3"
}

#Retourne le message de date avant la fin du confinement
def message_de_fin():
    mtn = datetime.now()
    jours = fin - mtn
    if (jours.days > 0):
        m = "Il reste " + str(jours.days + 1) + " jours avant la fin du confinement."
    elif (jours.days == 0):
        m = "C'est le dernier jour du confinement." 
    else:
        m = "Le confinement est fini !"
    return m

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='mettre des amendes de 135 euros'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
#Fonction qui envoit tt les jours a midi le nbre de jours avant la fin du confinement
async def time_check():
    await bot.wait_until_ready()
    while not bot.is_closed():
        mtn = datetime.strftime(datetime.now(),'%H:%M')
        if (mtn == '15:02'):
            for i in channels:
                sender = bot.get_channel(i)
                m = message_de_fin()
                await sender.send(m)
            t = 90
        else:
            t = 1
        await asyncio.sleep(t)

@bot.command()
async def timer(ctx):
    """Affiche le temps restant en confinnement"""
    await ctx.send(message_de_fin())

@bot.command()
async def attestation(ctx):
    """Donne le lien pour l'attestation de deplacement"""
    await ctx.send(attestation_link)

@bot.command()
async def que_faire(ctx):
    """Vous indique la procdure à suivre"""
    await ctx.send("Restez chez vous !")

@bot.command()
async def ajouter(ctx, message):
    """Ajoute un channel textuel a la liste des chans pour le message du jour"""
    try:
        sender = bot.get_channel(int(message))
        await sender.send("Le channel a été ajouté")
        channels.append(int(message))
    except :
        await ctx.send("Le channel n'a pas été ajouté, l'id est faux")

@bot.command()
async def list_sound(ctx):
    """liste tous les sons disponibles"""
    message = "```Les sons :\n"
    for key in dico:
        message = message + '\t'+ key + '\n'
    message += "```"
    await ctx.send(message) 

@bot.command()
async def sound(ctx, query):
    """Viens jouer un son dans le channel vocal ou tu est"""
    if ctx.message.author.voice != None:
        vc = await ctx.message.author.voice.channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(dico.get(query)))
        vc.play(source)
        while vc.is_playing():
            await asyncio.sleep(.1)
        await vc.disconnect()
    else:
        await ctx.send(" Tu dois etre dans un channel vocal.")

@bot.command()
async def stop(ctx):
    """Déconecte le bot du channel vocal"""
    await ctx.voice_client.disconnect()

@bot.command()
async def credits(ctx):
    """Lien du code source"""
    await ctx.send(github)


bot.loop.create_task(time_check())
bot.run(TOKEN)
