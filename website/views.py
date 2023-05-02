from flask import request, jsonify, Blueprint, render_template
import json
import openai
import os
from dotenv import load_dotenv
from flask_login import login_required

# Import the add_data and get_response functions from the utilities module
from .utilities import add_data, get_response

# Set up the Flask blueprint for the views
views = Blueprint("views", __name__)

# Load the OpenAI API key from the environment variables
load_dotenv()
openai.api_key = os.getenv("API_KEY")

#Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Route for the home page
@views.route("/")
def home():
    return render_template("home.html")


# Route for the chat page
@views.route("/chat/")
@login_required
def chat_route():
    return render_template("chat.html")


# Route for generating text
@views.route("/chat/prompt", methods=["POST"])
@login_required
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
@login_required
def account():
    return render_template("account.html")