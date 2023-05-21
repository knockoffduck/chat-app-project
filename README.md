## Introduction to CITS3403 Project
### Purpose of the web application, design and use explanation

This is a Flask web application that uses the OpenAI API to create a chatbot. The chatbot interacts with users and provides therapy-like conversation in response to prompts from the user. The chat history is stored in a JSON file and is loaded and saved to the database table to allow for continuous conversations with the chatbot.
The purpose of this web application is to provide users with a version of an online therapist, which they can chat with at anytime, anywhere. This aims to provide people with an accessible and helpful 'therapist', which they can talk to about their day, any issues they are having, their mental health or relationships. The login feature of the application allows a person's conversation history to be recorded and saved, so that when a user logs back in, they can begin a conversation where they left off. A user's account also ensures that their chats are not accessible to others, keeping conversations private.
When a person opens this application, they are greeted with the homepage for 'MindMate', the name of our app. This homepage explains the features of the app and how it can provide support for individuals. On clicking 'Chat Now', a user is prompted to login, or create an account to access the chat service. On logging in, the chat page appears, where a user can start chatting with the therapy chat assistant. Responses will be provided based on what a user talks about. Conversation history is stored within the 'Chat' page, and can be searched through using the 'Search' page, accessible from the navigation menu. Here, a user can search for keywords in their previous chat history, and can see questions and responses at that point in time. A user is also able to view and change their account details in the 'Account' page if they need to. There is also a dropdown menu to allow users to choose a 'darkmode' option for the application. If a user logs out, on their next login, they are able to continue their conversation with the therapy chat assistant, who remembers all previous interactions.
The purpose of MindMate is to provide support and advice for individuals, tailored to them, so that people have a place where they can freely and confidently talk about whatever is on their mind.

## Architecture of the Web Application
#### Database Schema
In our database, there are 2 tables: User and Chat. The schema definition for these are below:

-----------------------------
Table Name: User
Columns:
        id - INTEGER
        firstname - VARCHAR(30)
        lastname - VARCHAR(40)
        email - VARCHAR(120)
        email_hash_id - INTEGER
        password_hash - VARCHAR(128)
        dob - DATETIME
        country - VARCHAR(20)
        gender - VARCHAR(10)
Primary Key: ['id']
-----------------------------
Table Name: Chat
Columns:
        id - INTEGER
        body - VARCHAR(140)
        timestamp - DATETIME
        user_email_hash_id - INTEGER
Primary Key: ['id']
Foreign Key: email_hash_id -> user.email_hash_id

#### Chat
Our website contains a chat feature, where we use OpenAI API to create a chatbot. The /api/prompt endpoint is designed to interact with the OpenAI API and simulate a therapist. 
The user will send a message via the chat interface, causing the client to send a HTTP request to the /api/prompt endpoint. The server receives the request and uses it to interact with the OpenAI API. The OpenAI API will send a response back to the server which contains the generated response based on the user's prompt. Then, the server sends the generated response back to the client as a HTTP response. Finally, the client receives the response from the server and displays it in the chat interface. This process is done multiple times as the user inputs more messages in the chat, creating a conversation with the therapist.

#### Search
The search page is responsible for storing a user's chat history. The user is able to interact with the web application by accessing the search page and entering a search query. The client captures the search query and sends it to the server. The search page is handled by a Flask view function called 'search'. This view function is responsible for processing the user's search query and generating a response to be sent back to the client. The view function retrieves the search query and attempts to load the stored messages from a JSON file. The loaded messages are filtered based on the current user and the inputted search query. The client receives the response and updates the page accordingly with the search results.

#### Account 
The account page allows users to make changes to their personal details by interacting with the form elements and customise their profile by uploading a profile picture. The client is responsible for rendering the account page template, including the form elements that capture the user's input and send it to the server for processing. The server processes the form submissions, updates the user's personal details, and saves the changes to the database. If the account page is accessed via a GET request, the form elements are pre-populated with the user's existing personal details. This ensures that the forms displays the user's current data before any modifications are made. If modifications have been made by the user, the rendered template is sent as a HTTP response to the client. The client receives the response and updates the page accordingly.

## Steps to Launch the Web Application Using `app.py`

1. Unzip the project folder

2. Open a virtual environment within the project folder. Ensure that you have python downloaded.

   ```
   python -m venv venv
   ```

   ```
   source venv/bin/activate
   ```


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

11. The chat history is stored in the `chats/history.json` file, which is loaded and saved automatically by the `generate_text` function. You can view the chat history by opening the file in a text editor or by reading the contents of the file in your Python code. The chat history can be filtered and displayed by navigating to `http://127.0.0.1:5000/search/1` and entering a keyword in the search bar.   

12. The user account page is located at `http://127.0.0.1:5000/account`, which can be reached by clicking the "Account" navigation on the navigation menu. This page allows a user to make and save changes to their profile, which is saved to the database.

13. The drop-down menu (down arrow next to your username) allows you to toggle dark mode OFF/ON, clear the conversations displayed on the chat page, view your profile (navigates you to `http://127.0.0.1:5000/account`) and logout of the application. 

## Testing
Tests for the web application include: tests to ensure eaach flask route can be accessed successfully, correct password hashing, valid registration and login, handling for invalid registration and login, and successful profile changes.
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

   ```
   python tests/test_selenium.py
   ```

The selenium tests are designed to run in Chrome and use chromedriver to do so. Ensure that the lastest version of Chrome is installed. The selenium tests include tests for registering in the application, logging in, and using the chat functionality.

## Commit Logs
...

## Created By:
⁠
Daffa Fathurohman (23454661), Elise Panicciari (23088805), Tom Truong ⁠(23067483), Zarif ⁠Solaiman(23640056)
