import time
import openai


# Function to get the current timestamp
def get_time():
    # Get the current time in seconds since the epoch
    timestamp = time.time()

    # Convert the timestamp to a string with the specified format
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    # Return the timestamp string
    return timestamp_str


# Function to add new data to the data list for a given username
def add_data(username, new_data, data_list):
    # Add the current timestamp to the new data
    new_data["datetime"] = get_time()

    # Search for the username in the list
    for item in data_list:
        if item["username"] == username:
            # Append the new data to the existing data list
            item["data"].append(new_data)
            return data_list

    # If the username is not found, create a new dictionary and append it to the list
    new_item = {"username": username, "data": [new_data]}
    data_list.append(new_item)
    return data_list


# Function to get a response from the chatbot API
def get_response(username, data_list):
    print("getting response")
    # Search for the username in the list
    for users in data_list:
        if users["username"] == username:
            # Extract the messages for the user from the data list, removing any timestamps
            message = [
                {k: v for k, v in d.items() if k != "datetime"}
                if "datetime" in d
                else d
                for d in users["data"]
            ]

            # Insert a system message at the beginning of the message list
            """
            message.insert(0, {
                    "role": "system",
                    "content": "I want you to act as a therapist. I will present you with various prompts, questions, and scenarios on my mental well being and you will provide guidance on how to overcome, solve and help. Your responses should be conversational like a real therapist, which means that the responses should be short but also provide additional questions to ask the user. Do not ask whether I have spoken to a professional or a therapist, instead I would like you to be my therapist. So that means getting deep into the roots of the problem of where the problem occurs so that it can be solved.",
                })
            """

            # Call the chatbot API to get a response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=message
            )

            # Extract the response message from the API response
            reply = response["choices"][0]["message"]["content"]

            # Add the assistant's response to the user's data list with a timestamp
            users["data"].append(
                {"role": "assistant", "content": reply, "datetime": get_time()}
            )

            # Print the message list for debugging purposes
            print(message)

            # Return the assistant's response
            return reply
