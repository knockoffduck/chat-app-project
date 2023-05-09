from flask import request, jsonify, Blueprint, render_template
import json
import openai
import os
from dotenv import load_dotenv

# Import the add_data and get_response functions from the utilities module
from .utilities import add_data, get_response, is_json_empty

# Set up the Flask blueprint for the views
views = Blueprint("views", __name__)

# Load the OpenAI API key from the environment variables
openai.api_key = os.environ.get("API_KEY")


@views.errorhandler(500)
def handle_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 500
    return response


# Route for the home page
@views.route("/")
def home():
    return render_template("home.html")


# Route for the chat page
@views.route("/chat/")
def chat_route():
    return render_template("chat.html")


# Route for generating text
@views.route("/chat/prompt", methods=["POST"])
def generate_text():
    # Get the username and input from the request form
    username = request.form["username"]
    prompt = request.form["input"]
    chatFile = "chats/history.json"

    # Load the chat history from the JSON file
    chatHistory = []
    try:
        if is_json_empty(chatFile) != False:
            with open(chatFile, "r") as readJson:
                chatHistory = json.load(readJson)

        # Add the user's input to the chat history and get a response
        add_data(username, {"role": "user", "content": prompt}, chatHistory)
        reply = get_response(username, chatHistory)

        # Save the updated chat history to the JSON file
        with open(chatFile, "w") as writeJson:
            # Convert the chat history to a JSON string and write it to the file
            jsonExport = json.dumps(chatHistory)
            writeJson.write(jsonExport)

        # Return the assistant's response as a JSON object
        return jsonify({"generated_text": reply})
    except Exception as e:
        return handle_error(e)


@views.route("/account")
def account():
    return render_template("account.html")
