import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Initialize Gemini Client
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- MEMORY SYSTEM ---
# We start a persistent chat session here
chat_session = client.chats.create(
    model="gemini-2.5-flash",
    config={
        'system_instruction': (
            "You are a versatile Expert Engineer. You handle both physical science "
            "(like physics/chemistry atoms) and software engineering (like the Atom editor). "
            "If a term is ambiguous, address the scientific meaning first, then the technical one. "
            "Always maintain context from previous messages in this conversation."
        )
    }
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    file_content = data.get('file_context', "")

    # Combine file and message for the prompt
    if file_content:
        full_prompt = f"FILE CONTEXT:\n{file_content}\n\nUSER QUESTION: {user_message}"
    else:
        full_prompt = user_message

    try:
        # We use chat_session.send_message instead of generate_content
        # This automatically keeps track of the history for us!
        response = chat_session.send_message(full_prompt)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "⚠️ AI Engine Error. The session might need a reset."}), 500

# Route to clear memory if you want to start fresh
@app.route('/reset', methods=['POST'])
def reset():
    global chat_session
    chat_session = client.chats.create(model="gemini-2.5-flash")
    return jsonify({"status": "History cleared"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)