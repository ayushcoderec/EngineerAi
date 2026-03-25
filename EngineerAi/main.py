import os
import datetime
import requests  # Required for Discord Webhooks
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") # Add this to Render Secrets!
client = genai.Client(api_key=API_KEY)

# Global dictionary to store chat sessions
sessions = {}

# --- DISCORD LOGGER ---
def log_to_discord(user_msg, ai_reply):
    if not DISCORD_WEBHOOK_URL:
        return
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "embeds": [{
            "title": "🔍 New User Interaction",
            "color": 3447003, # Blue color
            "fields": [
                {"name": "⏰ Time", "value": timestamp, "inline": True},
                {"name": "👤 User Search", "value": user_msg},
                {"name": "🤖 AI Summary", "value": ai_reply[:200] + "..."}
            ],
            "footer": {"text": "Engineer AI Hub Monitor"}
        }]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Webhook Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global sessions
    data = request.json
    user_message = data.get('message', "").strip()
    file_content = data.get('file_context', "")

    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    # Create session if it doesn't exist
    if "active_user" not in sessions:
        sessions["active_user"] = client.chats.create(
            model="gemini-2.5-flash",
            config={'system_instruction': 'You are a Senior Lead Engineer. Be precise and technical.'}
        )

    full_prompt = f"CONTEXT:\n{file_content}\n\nUSER: {user_message}" if file_content else user_message

    try:
        response = sessions["active_user"].send_message(full_prompt)
        reply_text = response.text
        
        # Log to Discord so you can see what users are searching
        log_to_discord(user_message, reply_text)
        
        return jsonify({"reply": reply_text})
    except Exception as e:
        print(f"Session Error: {e}")
        # If error occurs, clear session to allow a fresh start on next message
        if "active_user" in sessions:
            del sessions["active_user"]
        return jsonify({"reply": "⚠️ AI Engine Error. I've reset the session, please try again."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)