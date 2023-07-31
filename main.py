# Taken from https://discordpy.readthedocs.io/en/stable/quickstart.html

# This example requires the 'message_content' intent.
import logging
import discord
import os
from dotenv import load_dotenv
load_dotenv()

permissions = 294205271040
app_id = os.getenv('application_id')
server_id = os.getenv('server_id')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Set up logging
handler = logging.FileHandler(
    filename='logs/discord.log', encoding='utf-8', mode='w')

# discord.utils.oauth_url(app_id,
#                         discord.Permissions(permissions), server_id)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello!')

client.run(os.getenv('discord_token'),
           log_handler=handler, log_level=logging.DEBUG)
