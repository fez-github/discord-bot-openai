# Taken from https://discordpy.readthedocs.io/en/stable/quickstart.html

# This example requires the 'message_content' intent.
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import logging
import os
from random import randint
from testopenai import get_prompt, call_openai

load_dotenv()

permissions = 294205271040
app_id = os.getenv('application_id')
server_id = os.getenv('server_id')

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

client = disnake.Client(intents=intents)

bot = commands.InteractionBot(test_guilds=[1135675866714738718])

# Set up logging
# handler = logging.FileHandler(
#     filename='logs/discord.log', encoding='utf-8', mode='w')

# discord.utils.oauth_url(app_id,
#                         discord.Permissions(permissions), server_id)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await message.channel.send('Hello!')


@bot.slash_command(
    name="loveai",
    description="OpenAI generates a love story between two people.",
)
async def love(ctx: disnake.ApplicationCommandInteraction, user: disnake.Member):
    await ctx.response.defer()

    if user.name == bot.user.name:
        userEmbed = disnake.Embed(
            type="rich", description="B-but I'm not worthy of your love.", title="Test Embed")
        await ctx.send(embed=userEmbed)
        return
    if user.name == ctx.author.name:
        await ctx.send("Don't love yourself in here!")

    # generate random number
    love = randint(0, 100)

    # Call OpenAI and return message.
    prompt = await get_prompt(ctx.author.name, user.name, love)
    response = await call_openai(prompt)

    if (love < 50):
        heart = ":broken_heart:"
    else:
        heart = ":heart:"

    header = f"{love}% {heart}"

    loveEmbed = disnake.Embed(
        type="rich",
        description=f"{ctx.author.name} & {user.name}\n**{header}**\n\n{response}",
        title="LoveAI"
    )
    await ctx.send(embed=loveEmbed)

    # # create message with random number.
    # if love == 0:
    #     await ctx.send("Omae wa mou shindeiru.")
    # if love < 10:
    #     await ctx.send("I abhor you.")
    # if love >= 11 and love < 100:
    #     await ctx.send("Eh, you're OK.")
    # if love == 100:
    #     await ctx.send("I'm wearing your heart as a necklace.")


@bot.slash_command()
async def help(ctx):
    await ctx.send("I am a bot that connects to OpenAI to have it tell love stories!  Use `/love` and tell me two people who you want to see get it on!")

bot.run(os.getenv('discord_token'))
