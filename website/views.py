from flask import request, jsonify, Blueprint, render_template, url_for, redirect
import json
import openai
import os
import uuid
from dotenv import load_dotenv

# Import the add_data and get_response functions from the utilities module
from .utilities import add_data, get_response

# Set up the Flask blueprint for the views
views = Blueprint("views", __name__)

# Load the OpenAI API key from the environment variables
load_dotenv()
openai.api_key = os.getenv("API_KEY")


# Route for the home page
@views.route("/")
def home():
    return render_template("home.html")


# Route for the chat page
@views.route("/chat/")
def chat_route():
    return render_template("chat.html")


@views.route("/history/<int:page>")
def history(page=1):
    messages = []
    if os.path.exists("chats/history.json"):
        with open("chats/history.json", "r") as f:
            messages = json.load(f)

    page_size = 5
    start_index = (page - 1) * 5
    end_index = start_index + page_size
    page_messages = messages[start_index:end_index]

    last_messages = []
    for message in page_messages:
        last_message = message['data'][-1]['content']
        last_messages.append({'username': message['username'], 'last_message': last_message})


    print(page_messages) #Check if it prints to the console
    return render_template('history.html', messages=page_messages, page=page, page_size=page_size)


# Route for generating text
@views.route("/chat/prompt", methods=["POST"])
def generate_text():
    # Get the username and input from the request form
    username = request.form["username"]
    prompt = request.form["input"]

    # Load the chat history from the JSON file
    chatHistory = []
    if os.stat("chats/history.json").st_size > 0:
        with open("chats/history.json", "r") as readJson:
            chatHistory = json.load(readJson)

    # Add the user's input to the chat history and get a response
    add_data(username, {"role": "user", "content": prompt}, chatHistory)
    reply = get_response(username, chatHistory)

    # Save the updated chat history to the JSON file
    with open("chats/history.json", "w") as writeJson:
        # Convert the chat history to a JSON string and write it to the file
        jsonExport = json.dumps(chatHistory)
        writeJson.write(jsonExport)

    # Return the assistant's response as a JSON object
    return jsonify({"generated_text": reply})

@views.route("/account")
def account():
    return render_template("account.html")