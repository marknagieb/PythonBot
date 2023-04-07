import discord
from discord import app_commands
from discord.ext import commands
import requests
from requests import get
import asyncio
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


# Trivia

# Define a function to retrieve a random trivia question and answer
def get_trivia_question():
    response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
    question_data = response.json()["results"][0]
    question = question_data["question"]
    correct_answer = question_data["correct_answer"]
    incorrect_answers = question_data["incorrect_answers"]
    answers = [correct_answer] + incorrect_answers
    return question, answers, correct_answer

# Define the trivia game command
@client.tree.command()
async def trivia(interaction: discord.Interaction):
    if interaction.channel.name != 'trivia':
        await interaction.response.send_message(content="This command can only be used in the #trivia channel.", ephemeral=True)
        return
    question, answers, correct_answer = get_trivia_question()
    answer_choices = "\n".join([f"{i+1}. {answer}" for i, answer in enumerate(answers)])
    await interaction.response.send_message(content=f"**Trivia Question:**\n{question}\n\n**Answer Choices:**\n{answer_choices}", ephemeral=False)

    # Define a function to check the user's answer
    def check_answer(message):
        return message.author == interaction.user and message.channel == interaction.channel

    # Wait for the user's answer
    try:
        message = await client.wait_for("message", check=check_answer, timeout=20)
    except asyncio.TimeoutError:
        await interaction.followup.send("Time's up! The correct answer is: " + correct_answer, ephemeral=False)
    else:
        user_answer = message.content.lower()
        if user_answer == correct_answer.lower():
            await interaction.followup.send("You got it right!", ephemeral=False)
        else:
            await interaction.followup.send("Sorry, the correct answer is: " + correct_answer, ephemeral=False)

# Trivia end    

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
