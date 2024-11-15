import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from Chatbot.chatbot import Chatbot

async def main():
    chatbot = Chatbot()
    conversation = []  # List to store plain text messages

    print("Chatbot Test - Type 'exit' to end the test.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Append user input to conversation
        conversation.append(f"You: {user_input}")

        # Get chatbot response
        try:
            response = await chatbot.ainvoke(user_input, "1")
            conversation.append(f"Chatbot: {response}")
            print(f"Chatbot: {response}")
        except Exception as e:
            print(f"Error: {e}")
            break

    # Save the conversation to a text file
    file_path = "conversation_log.txt"
    with open(file_path, "w") as file:
        file.write("\n".join(conversation))

    print(f"\nConversation saved to {file_path}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
