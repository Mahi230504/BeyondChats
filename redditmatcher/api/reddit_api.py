import os
import praw
from dotenv import load_dotenv

load_dotenv()

def get_reddit_instance():
    """Initializes and returns a PRAW instance for interacting with the Reddit API."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not all([client_id, client_secret, user_agent]):
        raise ValueError("Reddit API credentials not found in .env file.")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    return reddit
