import discord
import os
import requests
import json
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable message-related intents

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
    send_daily_quote.start()  # Start the task when the bot is ready

@bot.command(name='quote')
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)

@tasks.loop(hours=24)
async def send_daily_quote():
    now = datetime.now()
    target_time = now.replace(hour=6, minute=0, second=0, microsecond=0)  # 6 AM today

    if now > target_time:
        target_time += timedelta(days=1)  # If it's already past 6 PM, target 6 PM tomorrow

    await discord.utils.sleep_until(target_time)  # Sleep until the target time

    channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))  # Replace with your channel ID or use an environment variable
    channel = bot.get_channel(channel_id)
    if channel:
        quote = get_quote()
        await channel.send(quote)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
