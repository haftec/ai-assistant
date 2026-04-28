import os
from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def home():
    """
    Serves the main HTML interface.
    """
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """
    Handles AI chat requests.
    """
    try:
        data = request.get_json()
        user_question = data.get("question")
        
        # Request completion from Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_question}]
        )
        
        # Return the AI response as JSON
        return jsonify({"answer": completion.choices[0].message.content})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# This part allows manual running for development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
