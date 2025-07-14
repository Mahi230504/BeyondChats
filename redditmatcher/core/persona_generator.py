import os
import google.generativeai as genai
from dotenv import load_dotenv

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

    prompt = f"""
    Based on the following Reddit user data, create a detailed user persona in JSON format with these fields:
    - name: (username or best guess)
    - age: (estimated or range)
    - occupation: (likely job or field)
    - status: (relationship status if possible)
    - location: (if possible)
    - personality_traits: (array of objects, each with "trait" and "citations" - 1-3 short, direct quotes from user data that support the trait)
    - motivations: (array of objects, each with "motivation" and "citations" - 1-3 short, direct quotes from user data that support the motivation)
    - behaviour_habits: (array of objects, each with "habit" and "citations" - 1-3 short, direct quotes from user data that support the habit)
    - frustrations: (array of objects, each with "frustration" and "citations" - 1-3 short, direct quotes from user data that support the frustration)
    - goals_needs: (array of objects, each with "goal_need" and "citations" - 1-3 short, direct quotes from user data that support the goal/need)
    - summary_quote: (a first-person quote summarizing their approach to Reddit or life)
    - subreddits_active: (list of most active subreddits)
    - sentiment_tone: (summary of their typical sentiment/tone)
    - comment_karma: (from user_data)
    - link_karma: (from user_data)

    Ensure that for 'personality_traits', 'motivations', 'behaviour_habits', 'frustrations', and 'goals_needs', you provide 1-3 *short, direct quotes* from the user's comments or submissions in the 'citations' array that directly support the description. If no direct quote is available, provide an empty array for citations.

    User Data:
    - Username: {user_data['username']}
    - Comment Karma: {user_data['comment_karma']}
    - Link Karma: {user_data['link_karma']}
    - Most recent 100 comments: {user_data['comments']}
    - Most recent 100 submissions: {user_data['submissions']}
    """

    try:
        response = model.generate_content(prompt)
        print(f"Raw Gemini API Response: {response.text}") # Add this line for debugging
        import json
        json_string = response.text.strip()
        if json_string.startswith('```json') and json_string.endswith('```'):
            json_string = json_string[len('```json'):-len('```')].strip()
        persona = json.loads(json_string)
        return persona
    except Exception as e:
        return {"error": str(e)}
