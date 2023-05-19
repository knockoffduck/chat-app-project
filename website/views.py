from flask import request, jsonify, Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from website import db
from .__init__ import login
from website.forms import EditProfileForm
import json
import openai
import os
from dotenv import load_dotenv
import traceback
from PIL import Image

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


# sets the profile picture
@views.context_processor
def get_avatar_path():
    if not current_user.is_authenticated:
        return dict(profile_pic="default-avatar")
    hash_id = current_user.email_hash_id
    img_path = f"website/static/images/profile-pictures/{hash_id}.webp"

    if os.path.isfile(img_path):
        return dict(profile_pic=hash_id)
    else:
        return dict(profile_pic="default-avatar")
    # Check if the image file exists


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
    return render_template(
        "chat.html",
        email=user_email,
        chat_history=chat_history,
    )


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


@views.route("/search/<int:page>")
@login_required
def search(page=1):
    try:
        messages = get_chat_history(current_user.email)
        search_term = "how are you"

        for message in messages:
            if search_term in message["body"]["content"]:
                print(message)
        # Check if it prints to the console
        return render_template("search.html")

    # Prints an error message on the web page when there are no stored messages
    except Exception as e:
        traceback.print_exc()
        return (
            "An error occurred while loading the search page - no messages to display."
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
        username = current_user.firstname

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
            jsonExport = json.dumps(
                chatHistory, indent=4
            )  # Formatting of history.json file
            writeJson.write(jsonExport)

        # Return the assistant's response as a JSON object
        return jsonify({"generated_text": reply})
    except Exception as e:
        print(handle_error(e))
        return handle_error(e)


@views.route("/api/avatar_upload", methods=["POST"])
def upload():
    try:
        # Grab the file from the request
        file = request.files["avatar"]
        # Open the image file with Pillow
        image = Image.open(file)

        # Get the current user's hashed email ID
        email_hash_id = current_user.email_hash_id

        # Convert the image to RGB (necessary for the WebP format)
        converted_image = image.convert("RGB")

        # Save the converted image in the 'website/static/images/profile-pictures' directory
        # with a filename based on the user's hashed email ID, and in the WebP format
        converted_image.save(
            f"website/static/images/profile-pictures/{email_hash_id}.webp", "WEBP"
        )
        # Return a success message
        return jsonify({"message": "File uploaded successfully!"})
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
    return render_template(
        "account.html",
        title="Account",
        form=form,
    )
