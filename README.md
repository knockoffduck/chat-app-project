## Introduction
### Purpose of the web application, design and use explanation

This is a Flask web application that uses the OpenAI API to create a chatbot. The chatbot interacts with users and provides therapy-like conversation in response to prompts from the user. The chat history is stored in a JSON file and is loaded and saved to allow for continuous conversations with the chatbot.

## Steps to Launch the Web Application Using `app.py`

1. Unzip the project folder

2. Open a virtual environment:

3. Install the required Python packages by running the following command in the terminal:

   ```
   pip install -r requirements.txt
   ```

   This will install the necessary packages, including Flask, OpenAI, SQLAlchemy and the Python dotenv library.

4. Create a `.env` file in the root directory of the project and add your OpenAI API key using the format:

   ```
   API_KEY=your_api_key_here
   ```

   This will allow the web application to access the OpenAI API.

5. Run the following command in the terminal to start the Flask development server:

   ```
   python app.py
   ```

6. Open a web browser and navigate to `http://127.0.0.1:5000/` to view the home page of the web application.

7. On clicking "Chat Now", you will be prompted to login at `http://127.0.0.1:5000/auth/login` with an email and password to access the features of the website. 

8. If you are a new user, click on "Create New Account", where you will be promted to fill in the form for account creation at `http://127.0.0.1:5000/auth/signup`. The fields required are: first name, last name, email address, password, confirm password, date of birth, country and gender. On clicking register, you will then be prompted to login to access the chat page, where you can enter a username and start a conversation with the chatbot.

9. Logging in will direct you to `http://127.0.0.1:5000/chat/`, where you can access the chat page. Here you can start a conversation with the chatbot, who acts as a therapy assistant.

10. Enter a prompt in the chat input field and click the send button to get a response from the chatbot.

To be edited:
11. The chat history is stored in the `chats/history.json` file, which is loaded and saved automatically by the `generate_text` function. You can view the chat history by opening the file in a text editor or by reading the contents of the file in your Python code.

12. The user account page is located at `http://127.0.0.1:5000/account`, which can be reached by clicking the "Account" navigation on the navigation menu. This page allows a user to make and save changes to their profile, which is saved to the database.

## Database Schema
In our database, there are 2 tables: User and Chat. The schema definition for these are below:

## Testing
Tests for the web application include:
...

Run the following command in the terminal to run the tests:

   ```
   coverage run -m unittest tests/test.py
   ```
Then run the following command in the terminal to have a coverage report returned:

   ```
   coverage report
   ```

### Selenium Tests
Have the application running on local host `http://127.0.0.1:5000/` and open a new terminal.
In this new terminal, to run the Selenium Tests, run the following command:

## Commit Logs
...