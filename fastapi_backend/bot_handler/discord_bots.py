import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../.env")

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

        try:

            synced = await self.tree.sync(guild=GUILD_ID)
            print(f"Synced {len(synced)} command(s)")

        except Exception as e:
            print(e)

    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        # useful when the bot sends messages for user activity
        if message.author == self.user:
            return

        print(f"message.author: {message.author}")
        print(f"message.content: {message.content}")

        # Respond to messages starting with 'hello'
        if message.content.startswith("hello"):
            await message.channel.send(
                f"Hello {message.author.mention}!"
            )

        # Respond if the bot is mentioned at the start of the message
        if message.content.startswith(self.user.mention):
            await message.channel.send(
                f"Hello, {message.author.mention} mentioned me!"
            )

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(
            f"You reacted with {reaction.emoji}"
        )
        print(f"reaction: {reaction}")
        print(f"user: {user}")

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

GUILD_ID = discord.Object(id=os.getenv("SERVER_GUILD_ID"))


# Create and run the client
client = Client(command_prefix="!", intents=intents) # ! was used to call functions in discord. Now, it is replaced with / command, but initiated with !

@client.tree.command(name="hallo", description="Say Hello!", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hi, {interaction.user.mention}!")

@client.tree.command(name="drueck", description="I print what you say!", guild=GUILD_ID)
async def druecker(interaction: discord.Interaction, printer: str, year: int):
    await interaction.response.send_message(f"Hi, {interaction.user.mention}!. You said: {printer} in {year}!")

client.run(os.getenv("DISCORD_TOKEN"))
