from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

def generate_response(prompt, model="gpt-3.5-turbo", max_tokens=150, temperature=0.7):
    """
    Generate a direct response from OpenAI's ChatCompletion API.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    story = data.get("story", "")
    highlighted_text = data.get("highlighted", "")
    mode = data.get("mode", "sentence")

    if not highlighted_text:
        return jsonify({"error": "No highlighted text provided"}), 400

    if mode == "word":
        prompt = f"""
        Replace the word '{highlighted_text}' in the following text:
        '{story}'
        
        Provide a replacement word that fits seamlessly into the sentence and maintains its meaning and tone.
        """
        response = generate_response(prompt, max_tokens=20)
        return jsonify({"word_replacement": response.strip()})

    elif mode == "sentence":
        prompt = f"""
        Rewrite the sentence:
        '{highlighted_text}'

        Provide an alternative version that preserves the meaning but offers a fresh structure. Avoid flowery or terse language.
        """
        response = generate_response(prompt, max_tokens=150)
        return jsonify({"sentence_rewrite": response.strip()})

    return jsonify({"error": "Invalid mode specified"}), 400

if __name__ == "__main__":
    app.run(port=5001)  # Running on port 5001
