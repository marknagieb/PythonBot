import discord
from discord import app_commands
from discord.ext import commands
import requests
from requests import get
import openai
import json
import os
from dotenv import load_dotenv

# Keys

load_dotenv()
token = os.environ.get('token')
openai.api_key = os.environ.get('openai.api_key')
api_key = os.getenv('api_key')

# Keys end

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))
    try:
        synced = await client.tree.sync()
        print (f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# AI 
   
previous_messages = {}

@client.event
async def on_message(message):
    user_id = message.author.id
    if message.author == client.user:
        return
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    
    if user_id in previous_messages:
        previous_message = previous_messages[user_id]
        # Use the previous message to generate a response
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{previous_message} {user_message}",
            max_tokens=3000,
            temperature=0.3
        )
    else:
        # If there are no previous messages, just use the user's current message to generate a response
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_message,
            max_tokens=3000,
            temperature=0.3
        )

    # Store the user's current message as the previous message
    previous_messages[user_id] = user_message


    # print(username + " said " + user_message.lower() + " in " + channel)

    if message.channel.name == client.user:
        return

    if message.channel.name == 'ai':
        response = openai.Completion.create(
                model="text-davinci-002",
                prompt=user_message,
                max_tokens=3000,
                temperature=0.3
            )

        output = response["choices"][0]["text"]
        if output:
            print(output)
            await message.channel.send(output)
        else:
            print("Empty response from OpenAI API")

# AI end    

# MEME
class NextButton(discord.ui.View):
    def __init__(self, nxt: str):
        super().__init__()
        self.nxt = nxt
    
    @discord.ui.button(label="Next Meme", style=discord.ButtonStyle.blurple)
    async def NextBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)  # defer the interaction response to avoid timing out
        url = self.nxt
        response = requests.get(url)
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON response")
            data = {}
        if 'data' in data and 'images' in data['data'] and 'original' in data['data']['images']:
            meme_url = data['data']['images']['original']['url']
            meme = discord.Embed(color=discord.Color.random()).set_image(url=meme_url)
            await interaction.followup.send(embed=meme, view=NextButton(nxt=url))
        else:
            await interaction.followup.send("Failed to fetch meme :(", ephemeral=True)

@client.tree.command(name="meme")
async def meme(interaction: discord.Interaction):
    url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag=&rating=g"
    response = requests.get(url)
    try:
        data = response.json()
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON response")
        data = {}
    if 'data' in data and 'images' in data['data'] and 'original' in data['data']['images']:
        meme_url = data['data']['images']['original']['url']
        meme = discord.Embed(color=discord.Color.random()).set_image(url=meme_url)
        nxt = await interaction.response.send_message(embed=meme, view=NextButton(nxt=url))
    else:
        await interaction.response.send_message("Failed to fetch meme :(")
# MEME end   



#Commands

@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(content=f"hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

@client.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say")
async def say(interaction: discord.Interaction, thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.name} said '{thing_to_say}'")

#Commands end  

client.run(token)