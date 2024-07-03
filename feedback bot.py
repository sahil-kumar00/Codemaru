import discord
from discord.ext import commands
import os
from datetime import datetime

# Define the intents your bot needs
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Enable access to message content

# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot token (replace with your actual token)
TOKEN ='your bot token'
# Event handler for when the bot has connected to Discord
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

# Command to handle feedback submissions
@bot.command(name='feedback')
async def feedback(ctx, date: str = None, *, message: str):
    username = ctx.message.author.name

    # Use provided date or default to the current date
    if date is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = date

    feedback_message = f"{username}: {message}\n"

    # Debugging message to confirm the command is being triggered
    print(f'Received feedback from {username} on {date_str}: {message}')

    # Define the feedback file name based on the provided or current date
    feedback_file = f"feedback_{date_str}.txt"

    # Write the feedback to the date-specific file
    with open(feedback_file, "a") as file:
        file.write(feedback_message)

    # Confirm to the user that their feedback was received
    await ctx.send(f"Thank you for your feedback on {date_str}!")

# Command to read the stored feedback
@bot.command(name='readfeedback')
async def read_feedback(ctx, date: str = None):
    if date is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = date

    feedback_file = f"feedback_{date_str}.txt"

    if not os.path.exists(feedback_file):
        await ctx.send(f"No feedback available for {date_str}.")
        return

    # Read feedback from the date-specific file
    with open(feedback_file, "r") as file:
        feedbacks = file.readlines()

    if not feedbacks:
        await ctx.send(f"No feedback available for {date_str}.")
        return

    # Chunk feedback into messages of up to 2000 characters (Discord message limit)
    feedback_message = ''.join(feedbacks)
    chunks = [feedback_message[i:i + 2000] for i in range(0, len(feedback_message), 2000)]

    # Send each chunk as a separate message
    for chunk in chunks:
        await ctx.send(chunk)

# Run the bot
bot.run(TOKEN)

