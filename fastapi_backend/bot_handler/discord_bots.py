import os
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../.env")

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

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

# Create and run the client
client = Client(intents=intents)
client.run(os.getenv("DISCORD_TOKEN"))
