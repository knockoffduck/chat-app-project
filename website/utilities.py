import time
import openai
import json
import random
import datetime
from website.models import Chat, User

from website import db


def generate_unique_id(email):
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    random_num = random.randint(0, 1000000)  # Random number between 0 and 1,000,000
    username_hash = hash(email) & 0xFFFF  # Convert email to a 16-bit integer
    unique_id = f"{timestamp}_{random_num}_{username_hash}"
    return unique_id


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


def is_json_empty(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return not bool(data)


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
        "content": "I want you to act as a mental health adviser. I want you to act as though you are a real person, that means limiting the size of your responses. Try to keep it as conversational as possible, before providing solutions to the problems I would like you to carry on a conversation with me, make it seem like im talking to a friend. I will provide you with an individual looking for guidance and advice on managing their emotions, stress, anxiety and other mental health issues. You should use your knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods in order to create strategies that the individual can implement in order to improve their overall wellbeing. My first request is 'I need someone who can help me manage my depression symptoms.'",
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
