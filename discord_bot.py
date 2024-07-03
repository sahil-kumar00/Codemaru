import discord
from discord.ext import commands,tasks
import os
import requests
import random
import json
from discord.utils import get
from discord import asyncio
from datetime import datetime
import aiohttp
TOKEN = os.getenv("DISCORD_TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))
guildServerId = 1225853236775227432

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True 
flag = 0


client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    scheduled_meme.start()
    scheduled_quote.start()
    print(f"Logged in as {client.user} (ID: {client.user.id})")



async def get_meme():
    url = 'https://www.reddit.com/r/memes/hot.json?limit=100'
    headers = {'User-Agent': 'discord-meme-bot'}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return None

            memes = await response.json()
            memes = memes['data']['children']
            meme = random.choice(memes)['data']

            meme_url = meme['url']
            meme_title = meme['title']

            return meme_title, meme_url

@client.slash_command(name="meme", description="Get a random meme",guild_ids=[guildServerId])
async def meme(ctx):
    meme = await get_meme()
    if meme:
        title, url = meme
        embed = discord.Embed(title=title)
        embed.set_image(url=url)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond('Could not fetch a meme at the moment. Please try again later.')

# Add a task to post a meme every 24 hours
@tasks.loop(hours=24)
async def scheduled_meme():
    channel = client.get_channel(channel_id)  # Replace with your channel ID
    meme = await get_meme()
    if meme:
        title, url = meme
        embed = discord.Embed(title=title)
        embed.set_image(url=url)
        await channel.send(embed=embed)
    else:
        await channel.send('Could not fetch a meme at the moment. Please try again later.')

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


@client.slash_command(name='quote',description="get a random quote!!",guild_ids=[guildServerId])
async def quote(ctx):
    quote = get_quote()
    await ctx.respond(quote)

@tasks.loop(hours=24)
async def scheduled_quote():
    global flag
    if flag ==0 | flag == 1:
        flag+=1
        print("hi")
    else:

        quote = get_quote()
        await client.get_channel(channel_id).send(quote) 




def fetch_ctfd_events():
    url = 'https://ctftime.org/api/v1/events/'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching CTF events: HTTP {response.status_code}")
        return []

# Function to format CTF events as a string message
def format_ctf_events(ctfs):
    if not ctfs:
        return "No CTF events found."

    formatted_message = ""
    for ctf in ctfs:
        title = ctf.get('title', 'N/A')
        description = ctf.get('description', 'N/A')
        start = ctf.get('start', 'N/A')
        end = ctf.get('end', 'N/A')
        url = ctf.get('url', 'N/A')

        formatted_message += f"**Title:** {title}\n"
        formatted_message += f"**Description:** {description}\n"
        formatted_message += f"**Start:** {start}\n"
        formatted_message += f"**Finish:** {end}\n"
        formatted_message += f"**URL:** {url}\n\n"
    return formatted_message

# Function to split message into chunks of 2000 characters or less
def split_message(message, limit=2000):
    chunks = []
    while len(message) > limit:
        # Find the last newline within the limit
        split_index = message.rfind('\n', 0, limit)
        if split_index == -1:
            split_index = limit
        chunks.append(message[:split_index])
        message = message[split_index:]
    chunks.append(message)
    return chunks


@client.slash_command(name="ctf",description="get information about ctfs",guild_ids=[guildServerId])
async def ctf(ctx):
        ctf_events = fetch_ctfd_events()

        # Format CTF events as a message
        ctf_message = format_ctf_events(ctf_events)

        # Split the message into chunks of 2000 characters or less
        chunks = split_message(ctf_message)
        for chunk in chunks:
            await ctx.respond(chunk)


@client.slash_command(name='poll',description="Create a poll(Seperate your option by commas)",guild_ids=[guildServerId])
async def poll(ctx, question: str, options_list: str):
    """
    Create a poll with a question and options.
    Usage: /poll "Your Question" "Option1" "Option2" ...
    """
    options = options_list.split(",")
    if len(options) < 2:
        await ctx.respond("A poll must have at least two options.")
        return
    if len(options) > 10:
        await ctx.respond("A poll can have a maximum of 10 options.")
        return

    # await ctx.respond("Poll created!")
    options_text = ""
    emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for i, option in enumerate(options):
        options_text += f"{emoji_numbers[i]} {option}\n"

    embed = discord.Embed(title=question, description=options_text, color=discord.Color.blue())
    # await ctx.respond(embed=embed,ephemeral=True).defer()
    poll_message = await ctx.send(embed=embed)

    for i in range(len(options)):
        await poll_message.add_reaction(emoji_numbers[i])




@client.slash_command(name='feedback',description="Provide feedback for a data",guild_ids=[guildServerId])
async def feedback(ctx, date: str, *, message: str):
    username = ctx.author.name

    # Use provided date or default to the current date
    if date is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = date

    feedback_message = f"{username}: {message}\n"

    # Debugging message to confirm the command is being triggered
    # print(f'Received feedback from {username} on {date_str}: {message}')

    # Define the feedback file name based on the provided or current date
    feedback_file = f"feedback_{date_str}.txt"

    # Write the feedback to the date-specific file
    with open(feedback_file, "a") as file:
        file.write(feedback_message)

    # Confirm to the user that their feedback was received
    await ctx.send(f"Thank you for your feedback on {date_str}!")

# Command to read the stored feedback
@client.slash_command(name='readfeedback',description="Read feedback for a particular data",guild_ids=[guildServerId])
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


client.run(TOKEN)
