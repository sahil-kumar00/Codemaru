import discord
import os
from discord.ext import commands
from discord.utils import get

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True  # Enable reaction related intents

# Create bot instance
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='poll')
async def poll(ctx, question: str, *options: str):
    """
    Create a poll with a question and options.
    Usage: /poll "Your Question" "Option1" "Option2" ...
    """
    if len(options) < 2:
        await ctx.send("A poll must have at least two options.")
        return
    if len(options) > 10:
        await ctx.send("A poll can have a maximum of 10 options.")
        return

    options_text = ""
    emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for i, option in enumerate(options):
        options_text += f"{emoji_numbers[i]} {option}\n"

    embed = discord.Embed(title=question, description=options_text, color=discord.Color.blue())
    poll_message = await ctx.send(embed=embed)

    for i in range(len(options)):
        await poll_message.add_reaction(emoji_numbers[i])

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
