import discord
import requests
import os

# Your Discord bot token
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

# Function to fetch CTF events from the CTFTime API
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
        print("Response content:", response.content.decode('utf-8'))
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
        end = ctf.get('finish', 'N/A')
        url = ctf.get('url', 'N/A')

        formatted_message += f"**Title:** {title}\n"
        formatted_message += f"**Description:** {description}\n"
        formatted_message += f"**Start:** {start}\n"
        formatted_message += f"**Finish:** {end}\n"
        formatted_message += f"**URL:** {url}\n\n"

    # Ensure the message does not exceed Discord's character limit
    if len(formatted_message) > 2000:
        formatted_message = formatted_message[:1997] + '...'

    return formatted_message

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Check if the message starts with '!ctf'
    if message.content.startswith('!ctf'):
        # Fetch CTF events
        ctf_events = fetch_ctfd_events()

        # Format CTF events as a message
        ctf_message = format_ctf_events(ctf_events)

        # Send the message to the same channel or DM
        await message.channel.send(ctf_message)

# Run the bot
client.run(TOKEN)
