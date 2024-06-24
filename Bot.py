import discord
from discord.ext import commands
import subprocess
import sys

# Remplacez 'YOUR_BOT_TOKEN' par le token de votre bot
TOKEN = 'Token-ID'

# ID de l'utilisateur "Owner" (remplacez par l'ID réel)
OWNER_ID = OwnerID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionnaire pour stocker le dernier message du OWNER par canal
last_owner_message = {}

# Variable pour indiquer si la réécriture est activée ou non
rewriting_enabled = True

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    global last_owner_message, rewriting_enabled

    # Vérifie si la réécriture est activée
    if not rewriting_enabled:
        return

    # Vérifie si l'auteur du message est l'utilisateur "Owner"
    if message.author.id == OWNER_ID:
        # Récupère le canal où le message a été envoyé
        channel_id = message.channel.id

        # Vérifie s'il existe un message précédent à supprimer
        if channel_id in last_owner_message:
            # Vérifie si le message précédent est toujours présent et non envoyé par le bot
            if last_owner_message[channel_id].author.id == OWNER_ID:
                await last_owner_message[channel_id].delete()

        # Envoie le nouveau message au nom de l'utilisateur "Owner"
        sent_message = await message.channel.send(f"{message.content} (envoyé par {message.author.name})")
        # Stocke le nouveau message du OWNER pour ce canal
        last_owner_message[channel_id] = sent_message

        # Supprime le message original de l'utilisateur "Owner"
        await message.delete()

    await bot.process_commands(message)

@bot.command(name='STP')
async def stop_rewriting(ctx):
    global rewriting_enabled
    rewriting_enabled = False
    await ctx.send("La réécriture des messages a été arrêtée temporairement.")

@bot.command(name='STRT')
async def start_rewriting(ctx):
    global rewriting_enabled
    rewriting_enabled = True
    await ctx.send("Redémarrage du bot...")
    await restart_bot()

async def restart_bot():
    """Fonction pour redémarrer le bot en utilisant subprocess."""
    python = sys.executable
    subprocess.Popen([python, 'bot.py'])
    await bot.close()

bot.run(TOKEN)
