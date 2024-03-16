import discord
import requests
import html2text
import os
import google.generativeai as genai
genai.configure(api_key="AIzaSyCIvEgd0khhdZmwviOoT-OdXNVYrFNLj7g")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)

def ask(messages):
    history = []
    final_message = messages[len(messages) - 1]
    #remove the last message as it is the question
    messages.pop()

    #convert messages list to google api format
    for i in range(len(messages)):
        if i % 2 == 0:
            history.append(
                {
                    'role': 'user',
                    'parts': messages[i]
                }
            )
        elif i % 2 == 1:
            history.append(
                {
                    'role': 'model',
                    'parts': messages[i]
                }
        )
    convo = model.start_chat(history=history)
    convo.send_message(final_message)
    return convo.last.text

# function to read websites
def scrape(url):
    # check thoroughly if the link is valid
    if not url.startswith('http'):
        print(f"Invalid link: {url}")
        return
    
    # Set up the paths relative to the script location
    # Gets the directory where the script is located
    script_dir = os.path.dirname(__file__)
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')  # Path to the output directory

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Specify the path for the output file within the 'output' directory
    output_file_path = os.path.join(output_dir, "output.md")

    # Fetch the HTML
    url = url  # Change this URL to the one you're interested in
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    html_content = response.text

    # Convert HTML to Markdown
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    markdown_content = text_maker.handle(html_content)
    # Save to a Markdown file in the specified 'output' directory
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"Done! Your HTML has been converted and saved as a markdown file at {output_file_path}.")
    return markdown_content

#Discord code:

# Define bot's intents/permissions
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True

# Initialize the bot client with intents
client = discord.Client(intents=intents)

# Triggered when bot is ready
@client.event
async def on_ready():
    print(f'Bot logged in as: {client.user}')

context="" # The context of the conversation (all the websites read)
messages=[] # The messages sent by the user and model
chat=False # If the bot is in a conversation with the user

# Triggered when anyone sends a message
@client.event
async def on_message(message):
    global context, messages, chat
    # If sender is bot, ignore it
    if message.author == client.user:
        return
    
    # If message starts with 'hello', bot will respond:
    if message.content=='!help':
        await message.channel.send(f"""Hello {message.author.mention}! I'm Adapt, a wonderful Discord bot created to help you learn!

**Commands:**
!help - Displays this message
!read https://website1.com  https://website2.com, etc... - Reads websites seperated by spaces
!talk - Starts a conversation with me
!stop - Stops the conversation and clears the websites read""")

    # Any other message, bot will respond:
    elif message.content.startswith('!read'):
        # Split the message by spaces
        message_contents = message.content.split(' ')
        # Remove the first element (the command itself)
        message_contents.pop(0)
        # check if there are any links
        if len(message_contents) == 0:
            await message.channel.send(f'No links provided!!')
        
        # Loop through the links and read them
        await message.channel.send(f"Reading link(s)... Please wait until I'm done reading >-<")
        for link in message_contents:
            context+=scrape(link)
        await message.channel.send(f"Done reading! Use !start chat if you haven't already!")

    elif message.content=='!start':
        await message.channel.send(f"Hello! You can ask me anything about what I've read now (:")
        chat=True
    
    elif message.content=='!stop':
        context=""
        messages=[]
        chat=False
        await message.channel.send(f"Conversation stopped and context cleared!")
    else:
        if chat:
            messages.append(message.content)
            response=ask((["You are a helpful chatbot designed to answer questions given the context of the websites. Always respond in markdown. Say \"Okay!\" if you understand.\nContext:"+context, "Okay!"]+messages))
            messages.append(response)
            await message.channel.send(response)
        else:
            await message.channel.send(f"Sorry, I'm not programmed to understand that command :(")


    #Con
   import requests

def get_cod_info(url="https://cod.edu"):
  """Fetches information from the College of DuPage website."""
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise error for non-200 status codes
    # Process the response content (text or data) based on your needs
    print(f"Successfully retrieved content from {url}")
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

get_cod_info()  # Call the function
# Run the bot with your Discord bot token
client.run('MTIxNzIyMDcyNTQxMzUxMTI3OQ.GGraBf.lALO0KCRKpIjbo9GE1Th46spBKf2hy7PpMwOOs')