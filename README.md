# PythonBot

This code represents a highly functional and versatile chatbot that can seamlessly integrate with any Discord server. Using the powerful combination of the discord.py library and OpenAI's GPT-3 language model, this chatbot is capable of generating highly intelligent and coherent responses to any user's message. Additionally, the chatbot comes equipped with a trivia feature that is guaranteed to keep users engaged and entertained for hours. The bot fetches random questions from the Open Trivia Database API and prompts users to provide answers. If that's not enough, the chatbot can also fetch memes from the GIPHY API and display them in the chat. With its seamless integration, sophisticated features, and user-friendly interface, this chatbot is a must-have for any Discord community.
![image](https://user-images.githubusercontent.com/64073594/233247527-a821a2b6-1db9-488d-b72e-71c950f37a9f.png)

![image](https://user-images.githubusercontent.com/64073594/233247649-21749590-dd09-4f1a-861b-e372067d030c.png)

![image](https://user-images.githubusercontent.com/64073594/233248025-af293c48-c052-42d4-b447-82b00c0d6d5e.png)



# Prerequisites

Before running the bot, you need to have the following:

A Discord account
A Discord server where you have permission to add bots
An OpenAI API key
A GIPHY API key

# Installation
1. Clone the repository:
```git clone https://github.com/marknagieb/PythonBot.git```
2. Create a .env file in the project directory and add the following:
``` 
token=<your Discord bot token>
openai.api_key=<your OpenAI API key>
api_key=<your GIPHY API key>
```

3. Start the bot:
```python bot.py```

# Usage

Once the bot is running and added to your Discord server, you can use the following commands:

!hello: Sends a greeting message to the user who triggered the command.<br><br>
/say <message>: Echoes the provided message back to the user who triggered the command.<br><br>
/trivia: Starts a trivia game by fetching a random question from the Open Trivia Database API and prompting the user to provide an answer.<br><br>
/meme: Fetches a random meme from the GIPHY API and displays it in the chat. The user can click the "Next Meme" button to fetch another meme.<br><br>
send a message to the ai channel, the chatbot uses OpenAI's GPT-3 language model to generate a response. The chatbot can also use the previous message from the user to generate a more coherent and relevant response.
