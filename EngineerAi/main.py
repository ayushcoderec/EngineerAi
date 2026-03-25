import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Initialize Gemini Client
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.route('/')
def index():
    # Serves your custom HTML file from the /templates folder
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    file_content = data.get('file_context', "")

    # Construct the prompt for the Engineer AI
    if file_content:
        full_prompt = f"FILE CONTEXT:\n---\n{file_content}\n---\nUSER QUESTION: {user_message}"
    else:
        full_prompt = user_message

    try:
        # Generate response using the 2026 Gemini 2.5 Flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config={
                'system_instruction': 'You are a Senior Lead Engineer. Use Markdown for code blocks. Provide precise technical answers.'
            }
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "⚠️ AI Engine Error. Check terminal for details."}), 500

if __name__ == '__main__':
    print("\n🚀 ENGINEER HUB IS STARTING...")
    print("Go to: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)