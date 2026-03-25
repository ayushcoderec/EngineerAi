from google import genai
import sys

# 1. YOUR API KEY
# Go to https://aistudio.google.com/app/apikey to get your key
API_KEY = Az

# 2. Initialize the Gemini Client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"Configuration Error: {e}")
    sys.exit()

# 3. Create a chat session with the 2026 Flash model
# This session automatically remembers your conversation history
# Option A: Use the latest 2.5 Flash (very smart)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        'system_instruction': 'You are a friendly, wise bird named Meethu. You speak Hindi and English. Your goal is to help Ayush write scripts for kids’ animated videos. You are creative, funny, and use simple language.'
    }
)
# OR Option B: Use the most stable version (very reliable)
# chat = client.chats.create(model="gemini-flash-latest")

print("\n" + "="*40)
print("  GEMINI CHATBOT IS LIVE!")
print("  (Type 'exit' to stop the chat)")
print("="*40 + "\n")

# 4. The Chat Loop
while True:
    try:
        user_input = input("You: ")
        
        # Exit conditions
        if user_input.lower() in ["exit", "quit", "bye", "stop"]:
            print("\nBot: Goodbye! Have a great day.")
            break

        if not user_input.strip():
            continue

        # Send message to Gemini
        response = chat.send_message(user_input)
        
        # Print the bot's response
        print(f"\nBot: {response.text}\n")
        print("-" * 30)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        break