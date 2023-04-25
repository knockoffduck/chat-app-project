with open('API_KEY.txt', 'r') as file:
    API_KEY = file.read().strip()
    
import openai
openai.api_key = API_KEY

messages = []
#This part of the code sets the initial context of what you want to be. (where you would paste the context prompt)
system_msg = input("What type of chatbot would you like to create?\n") 
messages.append({"role": "system", "content": system_msg}) 

print("Your new assistant is ready!")
while input != "quit()":
    message = input()
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")
    print(messages)