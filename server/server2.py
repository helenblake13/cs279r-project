# server/server2.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv('OPENAI_API_KEY')  # Get the OpenAI API key from .env

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

def generate_response(prompt, model="gpt-3.5-turbo", max_tokens=150, temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']

def rewrite_text(prompt, mode='sentence'):
    """
    Rewrites the text directly, either replacing a word or rewriting a sentence.
    """
    if mode == 'word':
        rewrite_prompt = f"""
        Replace the word with a suitable alternative. Explain your choice:

        '{prompt}'
        """
    elif mode == 'sentence':
        rewrite_prompt = f"""
        Rewrite the following sentence. Explain your choices:

        '{prompt}'
        """
    return generate_response(rewrite_prompt, max_tokens=150)

@app.route('/api/rewrite', methods=['POST'])
def rewrite():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    text = data.get("text", "")
    mode = data.get("mode", "sentence")

    if not text:
        return jsonify({"error": "No text provided for rewriting"}), 400

    # Generate a rewritten response
    rewrite_response = rewrite_text(text, mode)

    return jsonify({"rewrite": rewrite_response})

if __name__ == "__main__":
    app.run(port=5001)  # Running on port 5001
