import time
import openai
import json
import random
import datetime
from website.models import Chat, User
import os

from website import db


def delete_conversations(email):
    hash_id = get_hash_id(email)
    Chat.query.filter_by(user_email_hash_id=hash_id).delete()
    db.session.commit()


def get_hash_id(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.email_hash_id


def get_chat_history(email):
    hash_id = get_hash_id(email)
    chats = (
        Chat.query.filter_by(user_email_hash_id=hash_id).order_by(Chat.id.asc()).all()
    )
    result = [
        {
            "body": json.loads(chat.body),
            "timestamp": chat.timestamp.strftime("%H:%M %d/%m/%y"),
        }
        for chat in chats
    ]
    return result


# Function to get the current timestamp
def get_time():
    # Get the current time in seconds since the epoch
    timestamp = time.time()

    # Convert the timestamp to a string with the specified format
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    # Return the timestamp string
    return timestamp_str


# Function to add new data to the data list for a given email
def add_data(email, new_data):
    user = User.query.filter_by(email=email).first()
    if not user:
        return "User not found"

    new_data_string = json.dumps(new_data)
    new_message = Chat(body=new_data_string, user_email_hash_id=user.email_hash_id)
    db.session.add(new_message)
    db.session.commit()

    return new_message


# Function to get a response from the chatbot API
def get_response(email):
    therapy_context = {
        "role": "system",
        "content": "I want you to act as a therapist. I will present you with various prompts, questions, and scenarios on my mental well being and you will provide guidance on how to overcome, solve and help. Your responses should be conversational like a real therapist, which means that the responses should be short but also provide additional questions to ask the user. Do not ask whether I have spoken to a professional or a therapist, instead I would like you to be my therapist. So that means getting deep into the roots of the problem of where the problem occurs so that it can be solved.",
    }

    messages = [message["body"] for message in get_chat_history(email)]
    messages.insert(0, therapy_context)
    try:
        # Call the chatbot API to get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        # Extract the response message from the API response
        reply = response["choices"][0]["message"]["content"]
        add_data(
            email,
            {
                "role": "assistant",
                "content": reply,
            },
        )
        # Return the assistant's response
        return reply
    except Exception:
        print(Exception)
        return Exception
        # Add the assistant's response to the user's data list with a timestamp
