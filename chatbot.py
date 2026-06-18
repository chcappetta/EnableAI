from openrouter import OpenRouter
import os
from tools.registry import TOOLS
from help import help
import json
from memory import load_history, save_history
from auth import login, register, load_users, save_users

def ai_response(client, messages):  
    response = client.chat.send(
        model="poolside/laguna-m.1:free",
        messages= messages)
    output = response.choices[0].message.content
    return output

def get_prompt(username):
    userinput= input(f"{username}: ")
    return userinput

def main():
    ai_name = "Ruby"
    user_name = logreg()
    if user_name is None:
        return
    if user_name != "captest":
        q1=input(f"{ai_name}: Hello {user_name}! Would you like to pick out a name for me? [y/n] ")
        if q1 == "y":
            ai_name = input("My New Name: ")
            print(f"{ai_name}: Awesome choice! I love my new name.")
        q3=input(f"{ai_name}: Would you like to continue our conversation where we left off? [y/n] ") 
        if q3 == "y":
            messages = load_history(user_name, ai_name)
        else:
            messages = [
                {
                "role": "system",
                "content": f"You are a helpful AI assistant named {ai_name}."
            }
            ]
    print(f"{ai_name}: What would you like to ask me? Type /help for list of tools and Quit to exit")
    print()
    client = OpenRouter(KEY)
    while True:
        prompt = get_prompt(user_name)
        if prompt.lower() == "quit":
            qexit = input(f"{ai_name}: Would you like to save today's conversation? [y/n] ")
            if qexit == "y":
                print(f"{ai_name}: Saving...")
                save_history(user_name, messages)
                print()
                print(f"{ai_name}: Saved.")
            print(f"{ai_name}: Thank you for using EnableAI. Have a nice day, {user_name}!")
            break
        if prompt == "/help":
            help(ai_name)
            continue
        if not prompt.strip():
            continue
        parts = prompt.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        if command in TOOLS:
            print(TOOLS[command](ai_name, user_name, args))
            continue
        messages.append({
            "role": "user",
            "content": prompt
        })
        print(f"{ai_name}: Thinking...")
        try:
            output = ai_response(client, messages)
        except Exception as e:
            output = f"Sorry, AI is unavailable: {e}. Other tools still available."
        print(f"{ai_name}:", output)
        messages.append({
            "role": "assistant",
            "content": output
        })

def logreg():
    ai_name = "Ruby"
    print("Welcome to EnableAI")
    print("Please select: ")
    print("1. Login")
    print("2. Register")
    choice = input("> ")
    if choice == "1":
        user_name = login()
    elif choice == "2":
        user_name = register()
    elif choice == "Captest":
        print()
        print("Welcome back Christopher :)")
        print()
        return "captest"
    else: 
        print("Invalid Input.")
        return
    if user_name is None:
        print("Login Failed.")
        return
    return user_name

main()
