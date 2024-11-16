from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv('OPENAI_API_KEY')  # Get the OpenAI API key from .env

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

def generate_response(prompt, model="gpt-3.5-turbo", max_tokens=150, temperature=0.3):
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

def validate_and_replace_word(prompt, analysis_response, full_text):
    """
    Tries to replace a word in the text. Validates whether the replacement makes sense in the sentence.
    If the initial replacement doesn't make sense, it falls back to a short phrase.
    """
    def attempt_replacement(replacement):
        validation_prompt = f"""
        Given the following sentence:
        '{full_text}'

        Does the replacement '{replacement}' make sense for the highlighted word '{prompt}' when inserted into the sentence? 
        If yes, return 'VALID'. If no, return 'INVALID'.
        """
        validation_response = generate_response(validation_prompt, max_tokens=10).strip()
        return validation_response == "VALID"

    # Step 1: Generate initial replacement
    replacement_prompt = f"""
    Based on the analysis provided below:

    {analysis_response}

    The full text is provided for context:
    '{full_text}'

    The following word is highlighted for replacement:
    '{prompt}'

    Replace this word with another word that maintains the author's tone, voice, and specific characteristics. 
    Ensure the replacement is clear and fits seamlessly into the sentence.
    """
    initial_replacement = generate_response(replacement_prompt, max_tokens=20).strip()

    # Step 2: Validate the initial replacement
    if attempt_replacement(initial_replacement):
        return initial_replacement

    # Step 3: Try a short phrase if the initial replacement doesn't work
    phrase_prompt = f"""
    The initial replacement '{initial_replacement}' did not fit well. Provide a very short phrase (2-3 words) that works better in the context:
    """
    short_phrase = generate_response(phrase_prompt, max_tokens=30).strip()

    if attempt_replacement(short_phrase):
        return short_phrase

    # Step 4: Fallback to the initial replacement if no phrase works
    return initial_replacement

def rewrite_text(prompt, analysis_response, mode='sentence', full_text=None):
    """
    Rewrites the text based on the analysis, either replacing a word or rewriting a sentence.
    Includes the full text when in 'word' mode to provide better context.
    """
    if mode == 'word':
        return validate_and_replace_word(prompt, analysis_response, full_text)
    elif mode == 'sentence':
        rewrite_prompt = f"""
        Based on the analysis provided below:

        {analysis_response}

        Rewrite the following sentence while preserving its meaning and offering a fresh structure. Avoid simply replacing words with synonyms or making the sentence overly flowery (or too terse) compared to the original text. Maintain a clear, grounded tone consistent with the original:

        '{prompt}'

        Ensure the rewritten sentence fits the overall context of the text, preserves coherence, and is about the same length as the original. Very BRIEFLY explain your design choices. Make sure your sentence is structurally (different and) ORIGINAL but not over-the-top.
        """
        return generate_response(rewrite_prompt, max_tokens=150)

def creative_personalization(prompt, mode='sentence', full_text=None):
    """
    Combines analysis and rewriting functions for a chained output.
    """
    # Step 1: Analyze the full text or prompt
    analysis_response = analyze_text(full_text or prompt)
    
    # Step 2: Rewrite the specific part (word or sentence) using the analysis
    rewrite_response = rewrite_text(prompt, analysis_response, mode, full_text=full_text)
    
    # Step 3: Return the combined output
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
    response = creative_personalization(highlighted_text or story, mode, full_text=story)

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5001)  # Running on port 5001
