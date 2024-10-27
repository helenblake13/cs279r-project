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

def creative_personalization(prompt):
    # Creating a structured analysis prompt for the OpenAI API
    analysis_prompt = f"""
    You are a personalized sentence replacement AI that is designed to work specifically with creative writers. Your job is to analyze the following story or portion of a story and provide a detailed analysis. You must output a very structured paragraph describing the design choices you observe, with explanations specifically in tune with the author's characters and their personalities, the cadence of their writing or style of vocabulary, the structure of their sentences, and any recurring objects or symbols used by the author. Focus on identifying these key elements in the text provided:

    '{prompt}'
    """
    analysis_response = generate_response(analysis_prompt, max_tokens=350)

    rewrite_prompt = f"""
    Based on the analysis provided below:

    {analysis_response}

    Now, please rewrite the following sentence in the context of the story, keeping the nuances, style, and structure intact. Explain your design choices for the rewritten sentence:

    '{prompt}'
    """
    final_rewrite = generate_response(rewrite_prompt, max_tokens=150)

    return {"analysis": analysis_response, "rewrite": final_rewrite}

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    story = data.get("story", "")
    highlighted_text = data.get("highlighted", "")

    # Using the creative_personalization function to analyze and rewrite
    response = creative_personalization(highlighted_text or story)

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5001)  # Running on port 5001
