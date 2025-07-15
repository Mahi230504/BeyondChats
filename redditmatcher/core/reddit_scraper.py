from api.reddit_api import get_reddit_instance

def get_user_data(username):
    """Scrapes a Reddit user's profile for their comments and submissions."""
    reddit = get_reddit_instance()
    redditor = reddit.redditor(username)

    data = {
        "username": redditor.name,
        "id": redditor.id,
        "comment_karma": redditor.comment_karma,
        "link_karma": redditor.link_karma,
        "created_utc": redditor.created_utc,
        "profile_img": redditor.icon_img, # Add profile image URL
        "comments": [],
        "submissions": [],
    }

    for comment in redditor.comments.new(limit=100):
        data["comments"].append(
            {
                "body": comment.body,
                "score": comment.score,
                "subreddit": comment.subreddit.display_name,
                "created_utc": comment.created_utc,
            }
        )

    for submission in redditor.submissions.new(limit=100):
        data["submissions"].append(
            {
                "title": submission.title,
                "score": submission.score,
                "subreddit": submission.subreddit.display_name,
                "created_utc": submission.created_utc,
                "selftext": submission.selftext,
                "url": submission.url,
            }
        )

    return data
