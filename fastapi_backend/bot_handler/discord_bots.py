import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.message import Message
from discord.ext.commands.hybrid import U
from dotenv import load_dotenv
from llm_manager import LLMManager

# Load environment variables from .env file
load_dotenv(".env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_GUILD_ID = os.getenv("SERVER_GUILD_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")


# Define LLM Manager
llm = LLMManager(api_key=GOOGLE_API_KEY, 
                model_name=GEMINI_MODEL_NAME)


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

        try:

            synced = await self.tree.sync(guild=GUILD_ID)
            print(f"Synced {len(synced)} command(s)")

        except Exception as e:
            print(e)

    async def on_message(self, message: Message):
        # Ignore messages sent by the bot itself
        # useful when the bot sends messages for user activity
        if message.author == self.user:
            return

        print(f"message: {message.author} -- {message.content}")

        # Respond to messages starting with 'hello'
        if message.content.startswith("hello"):
            await message.channel.send(
                f"Hello {message.author.mention}!"
            )

        mention = self.user.mention

        print(f"mention: {mention}")


        # Respond if the bot is mentioned at the start of the message
        if mention in message.content:

            # user_query = message.content[len(mention):].lstrip()
            user_query = message.content.replace(mention, "", 1).lstrip()

            print("user_query: ", user_query)

            llm_response = llm.infer(prompt=user_query)
            await message.reply(llm_response, mention_author=False)


    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(
            f"You reacted with {reaction.emoji}"
        )
        print(f"reaction: {reaction}")
        print(f"user: {user}")

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

GUILD_ID = discord.Object(id=SERVER_GUILD_ID)


# Create and run the client
client = Client(command_prefix="!", intents=intents) # ! was used to call functions in discord. Now, it is replaced with / command, but initiated with !

@client.tree.command(name="hallo", description="Say Hello!", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hi, {interaction.user.mention}!")

@client.tree.command(name="drueck", description="I print what you say!", guild=GUILD_ID)
async def druecker(interaction: discord.Interaction, printer: str, year: int):
    await interaction.response.send_message(f"Hi, {interaction.user.mention}!. You said: {printer} in {year}!")

client.run(DISCORD_TOKEN)
