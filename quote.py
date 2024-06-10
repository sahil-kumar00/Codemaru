import discord
import os
import requests
import json
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable message related intents

# Create bot instance
bot = commands.Bot(command_prefix='/', intents=intents)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='quote')
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
