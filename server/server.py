# server/server.py

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

def analyze_text(prompt):
    """
    Analyzes the text for design elements such as tone, character traits, and style.
    """
    analysis_prompt = f"""
    You are a personalized sentence replacement AI for creative writers. Your job is to analyze the following text for:
    - Tone and voice [KEY FOCUS], focusing on word choice frequency and grounded qualities.
    - Character traits and personalities.
    - Cadence, vocabulary style, and unique structures.
    - Recurring objects or symbols.

    Analyze the text and provide a structured paragraph describing these elements:

    '{prompt}'
    """
    return generate_response(analysis_prompt, max_tokens=350)

def rewrite_text(prompt, analysis_response, mode='sentence'):
    """
    Rewrites the text based on the analysis, either replacing a word or rewriting a sentence.
    """
    if mode == 'word':
        rewrite_prompt = f"""
        Based on the analysis provided below:

        {analysis_response}

        Replace a significant word in the sentence below with another word that maintains the author's tone, voice, and specific characteristics. Explain the choice briefly:

        '{prompt}'
        """
    elif mode == 'sentence':
        rewrite_prompt = f"""
        Based on the analysis provided below:

        {analysis_response}

        Rewrite the following sentence while maintaining the original author's tone and voice. Identify key features of their style and ensure these are preserved. Make sure your sentence is distinct from the original. Explain the design choices briefly:

        '{prompt}'
        """
    return generate_response(rewrite_prompt, max_tokens=150)

def creative_personalization(prompt, mode='sentence'):
    """
    Combines analysis and rewriting functions for a chained output.
    """
    analysis_response = analyze_text(prompt)
    rewrite_response = rewrite_text(prompt, analysis_response, mode)
    
    if mode == 'word':
        return {"analysis": analysis_response, "word_replacement": rewrite_response}
    else:
        return {"analysis": analysis_response, "sentence_rewrite": rewrite_response}

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    story = data.get("story", "")
    highlighted_text = data.get("highlighted", "")
    mode = data.get("mode", "sentence")

    # Using the creative_personalization function to analyze and rewrite
    response = creative_personalization(highlighted_text or story, mode)

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5001)  # Running on port 5001
