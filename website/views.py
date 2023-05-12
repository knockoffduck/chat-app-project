from flask import request, jsonify, Blueprint, render_template
import json
import openai
import os
from dotenv import load_dotenv

# Import the add_data and get_response functions from the utilities module
from .utilities import (
    add_data,
    get_response,
    is_json_empty,
    generate_unique_id,
    get_time,
)

# Set up the Flask blueprint for the views
views = Blueprint("views", __name__)

# Load the OpenAI API key from the environment variables
openai.api_key = os.environ.get("API_KEY")


@views.errorhandler(500)
def handle_error(error):
    response = jsonify({"error": error})
    response.status_code = 500
    return response


# Route for the home page
@views.route("/")
def home():
    return render_template("home.html")


# Route for the chat page
@views.route("/chat")
def chat_route():
    return render_template("chat.html")


@views.route("/user", methods=["POST"])
def user():
    username = request.form["username"]
    chatFile = "chats/history.json"

    chatHistory = []
    try:
        if is_json_empty(chatFile) == False:
            with open(chatFile, "r") as readJson:
                chatHistory = json.load(readJson)
            for user in chatHistory:
                if username == user["username"]:
                    chatHistory = user["data"]

        return jsonify({"conversation": chatHistory})
    except Exception:
        return Exception


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
        last_message = message["data"][-1]["content"]
        last_messages.append(
            {"username": message["username"], "last_message": last_message}
        )

    print(page_messages)  # Check if it prints to the console
    return render_template(
        "history.html", messages=page_messages, page=page, page_size=page_size
    )


# Route for generating text
@views.route("/api/prompt", methods=["POST"])
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
        add_data(
            username,
            {
                "role": "user",
                "content": prompt,
                "datetime": get_time(),
                "uuid": generate_unique_id(username),
            },
            chatHistory,
        )
        reply = get_response(username, chatHistory)

        # Save the updated chat history to the JSON file
        with open(chatFile, "w") as writeJson:
            # Convert the chat history to a JSON string and write it to the file
            jsonExport = json.dumps(chatHistory)
            writeJson.write(jsonExport)

        # Return the assistant's response as a JSON object
        return jsonify({"generated_text": reply})
    except Exception:
        return Exception


@views.route("/account")
def account():
    return render_template("login.html")
