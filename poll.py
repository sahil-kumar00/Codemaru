import discord
import os
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True  # Enable reaction related intents

# Create bot instance
bot = commands.Bot(command_prefix='/', intents=intents)

class PollModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Create a Poll")
        self.question = discord.ui.TextInput(label="Question", placeholder="Enter your poll question", max_length=100)
        self.add_item(self.question)
        self.options = discord.ui.TextInput(label="Options", placeholder="Enter options separated by commas", style=discord.TextStyle.long)
        self.add_item(self.options)

    async def on_submit(self, interaction: discord.Interaction):
        question = self.question.value
        options = self.options.value.split(',')
        if len(options) < 2:
            await interaction.response.send_message("A poll must have at least two options.", ephemeral=True)
            return
        if len(options) > 10:
            await interaction.response.send_message("A poll can have a maximum of 10 options.", ephemeral=True)
            return

        options_text = ""
        emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for i, option in enumerate(options):
            options_text += f"{emoji_numbers[i]} {option.strip()}\n"

        embed = discord.Embed(title=question, description=options_text, color=discord.Color.blue())
        poll_message = await interaction.channel.send(embed=embed)

        for i in range(len(options)):
            await poll_message.add_reaction(emoji_numbers[i])

        await interaction.response.send_message("Poll created!", ephemeral=True)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='poll')
async def poll(ctx):
    """
    Create a poll using a modal dialog.
    Usage: /poll
    """
    await ctx.send_modal(PollModal())

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
