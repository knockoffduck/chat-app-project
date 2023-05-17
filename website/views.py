from flask import request, jsonify, Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from website import db
from .__init__ import login
from website.forms import EditProfileForm
import json
import openai
import os
from dotenv import load_dotenv

# Import the add_data and get_response functions from the utilities module
from .utilities import (
    add_data,
    get_response,
    is_json_empty,
    get_chat_history,
    delete_conversations,
)

# Set up the Flask blueprint for the views
views = Blueprint("views", __name__)

# Load the OpenAI API key from the environment variables
openai.api_key = os.environ.get("API_KEY")


@views.errorhandler(500)
def handle_error(error):
    print("STATUS CODE 500")
    return error


# Route for the home page
@views.route("/")
def home():
    return render_template("home.html")


@views.route("/clear_chat", methods=["POST"])
def clear_chat():
    email = request.form.get("email")
    delete_conversations(email)
    return jsonify({"message": "Chat cleared successfully!"})


# Route for the chat page
@views.route("/chat", methods=["GET", "POST"])
@login_required
def chat_route():
    if request.method == "POST":
        email = request.json["email"]
        return jsonify(get_chat_history(email))
    user_email = current_user.email
    chat_history = json.dumps(get_chat_history(user_email))
    return render_template("chat.html", email=user_email, chat_history=chat_history)


@views.route("/user", methods=["POST"])
def user():
    email = request.form["email"]
    chatFile = "chats/history.json"

    chatHistory = []
    try:
        if is_json_empty(chatFile) == False:
            with open(chatFile, "r") as readJson:
                chatHistory = json.load(readJson)
            for user in chatHistory:
                if email == user["email"]:
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
        last_messages.append({"email": message["email"], "last_message": last_message})

    print(page_messages)  # Check if it prints to the console
    return render_template(
        "history.html", messages=page_messages, page=page, page_size=page_size
    )


# Route for generating text
@views.route("/api/prompt", methods=["POST"])
@login_required
def generate_text():
    # Get the email and input from the request form
    email = request.form["email"]
    prompt = request.form["input"]
    chatFile = "chats/history.json"

    # Load the chat history from the JSON file
    chatHistory = []
    try:
        # Add the user's input to the chat history and get a response
        add_data(
            email,
            {
                "role": "user",
                "content": prompt,
            },
        )
        reply = get_response(email)

        # Save the updated chat history to the JSON file
        with open(chatFile, "w") as writeJson:
            # Convert the chat history to a JSON string and write it to the file
            jsonExport = json.dumps(chatHistory)
            writeJson.write(jsonExport)

        # Return the assistant's response as a JSON object
        return jsonify({"generated_text": reply})
    except Exception as e:
        print(handle_error(e))
        return handle_error(e)


@views.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.dob = form.dob.data
        current_user.country = form.country.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("views.account"))
    elif request.method == "GET":
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.dob.data = current_user.dob
        form.country.data = current_user.country
        form.gender.data = current_user.gender
    return render_template("account.html", title="Account", form=form)
