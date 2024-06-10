import discord
import requests
import random
import os

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_meme():
    url = 'https://www.reddit.com/r/memes/hot.json?limit=100'
    headers = {'User-Agent': 'discord-meme-bot'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    memes = response.json()['data']['children']
    meme = random.choice(memes)['data']

    meme_url = meme['url']
    meme_title = meme['title']

    return meme_title, meme_url

@client.event
async def on_ready():
    print(f'{client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$meme'):
        meme = get_meme()
        if meme:
            title, url = meme
            embed = discord.Embed(title=title)
            embed.set_image(url=url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Could not fetch a meme at the moment. Please try again later.')

client.run(TOKEN)
