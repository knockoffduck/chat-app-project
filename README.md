## Introduction

This is a Flask web application that uses the OpenAI API to create a chatbot. The chatbot interacts with users and provides therapy-like conversation in response to prompts from the user. The chat history is stored in a JSON file and is loaded and saved to allow for continuous conversations with the chatbot.

## Steps to Run the Web Application Using `main.py`

1. Install the required Python packages by running the following command in the terminal:

   ```
   pip install -r requirements.txt
   ```

   This will install Flask, OpenAI, and the Python dotenv library.

2. Create a `.env` file in the root directory of the project and add your OpenAI API key using the format:

   ```
   API_KEY=your_api_key_here
   ```

   This will allow the web application to access the OpenAI API.

3. Run the following command in the terminal to start the Flask development server:

   ```
   python main.py
   ```

4. Open a web browser and navigate to `http://127.0.0.1:5000/` to view the home page of the web application.

5. Navigate to `http://127.0.0.1:5000/chat/` to access the chat page, where you can enter a username and start a conversation with the chatbot.

6. Enter a prompt in the chat input field and click the send button to get a response from the chatbot.

7. The chat history is stored in the `chats/history.json` file, which is loaded and saved automatically by the `generate_text` function. You can view the chat history by opening the file in a text editor or by reading the contents of the file in your Python code.
