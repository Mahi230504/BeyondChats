import os
import google.generativeai as genai
from dotenv import load_dotenv
from api.people_api import enrich_persona_with_pdl

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_persona(user_data):
    """
    Generates a structured user persona using Gemini API based on Reddit data.
    Returns a dictionary with persona fields for UI rendering.
    """
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not found."}

    model = genai.GenerativeModel("gemini-2.5-flash")

    # Read prompt from file
    try:
        script_dir = os.path.dirname(__file__)
        prompt_file_path = os.path.join(script_dir, "..", "persona_prompt.txt")
        with open(prompt_file_path, "r") as f:
            prompt_template = f.read()
        print(f"[DEBUG] prompt_template content: {prompt_template[:200]}...") # Print first 200 chars
    except FileNotFoundError:
        return {"error": "persona_prompt.txt not found."}

    # Escape backslashes and other special characters in user data
    for key in ['comments', 'submissions', 'top_comments', 'top_submissions']:
        if key in user_data and isinstance(user_data[key], list):
            user_data[key] = [str(item).encode('unicode_escape').decode() for item in user_data[key]]

    prompt = prompt_template.format(
        username=user_data['username'],
        comment_karma=user_data['comment_karma'],
        link_karma=user_data['link_karma'],
        posts_per_week_comments=user_data.get('posts_per_week', {}).get('comments', 0),
        posts_per_week_submissions=user_data.get('posts_per_week', {}).get('submissions', 0),
        top_comments=user_data.get('top_comments', []),
        top_submissions=user_data.get('top_submissions', []),
        comments=user_data['comments'],
        submissions=user_data['submissions']
    )

    try:
        response = model.generate_content(prompt)
        print(f"Raw Gemini API Response: {response.text}") # Add this line for debugging
        import json
        json_string = response.text.strip()
        if json_string.startswith('```json') and json_string.endswith('```'):
            json_string = json_string[len('```json'):-len('```')].strip()
        persona = json.loads(json_string)

        # Enrich persona with People Data Labs API
        enriched_persona = enrich_persona_with_pdl(persona)
        return enriched_persona
    except Exception as e:
        return {"error": str(e)}
