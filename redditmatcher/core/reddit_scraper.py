from api.reddit_api import get_reddit_instance

def get_user_data(username):
    """Scrapes a Reddit user's profile for their comments and submissions."""
    reddit = get_reddit_instance()
    try:
        redditor = reddit.redditor(username)

        

        data = {
            "username": redditor.name,
            "id": redditor.id,
            "comment_karma": redditor.comment_karma,
            "link_karma": redditor.link_karma,
            "created_utc": redditor.created_utc,
            "profile_img": redditor.icon_img if hasattr(redditor, 'icon_img') else None,
            "comments": [],
            "submissions": [],
            "posts_per_week": {"comments": 0, "submissions": 0},
            "top_comments": [],
            "top_submissions": [],
        }

        all_comments = []
        all_submissions = []

        # Fetch comments
        try:
            for comment in redditor.comments.new(limit=100):
                all_comments.append(
                    {
                        "body": comment.body,
                        "score": comment.score,
                        "subreddit": comment.subreddit.display_name,
                        "created_utc": comment.created_utc,
                    }
                )
        except Exception as e:
            print(f"Error fetching comments for u/{username}: {e}")

        # Fetch submissions
        try:
            for submission in redditor.submissions.new(limit=100):
                all_submissions.append(
                    {
                        "title": submission.title,
                        "score": submission.score,
                        "subreddit": submission.subreddit.display_name,
                        "created_utc": submission.created_utc,
                        "selftext": submission.selftext,
                        "url": submission.url,
                    }
                )
        except Exception as e:
            print(f"Error fetching submissions for u/{username}: {e}")

        data["comments"] = all_comments
        data["submissions"] = all_submissions

        # Calculate posts per week
        import time
        current_time = time.time()

        if all_comments:
            oldest_comment_time = min([c["created_utc"] for c in all_comments])
            time_span_seconds = current_time - oldest_comment_time
            time_span_weeks = time_span_seconds / (7 * 24 * 3600)
            if time_span_weeks > 0:
                data["posts_per_week"]["comments"] = len(all_comments) / time_span_weeks

        if all_submissions:
            oldest_submission_time = min([s["created_utc"] for s in all_submissions])
            time_span_seconds = current_time - oldest_submission_time
            time_span_weeks = time_span_seconds / (7 * 24 * 3600)
            if time_span_weeks > 0:
                data["posts_per_week"]["submissions"] = len(all_submissions) / time_span_weeks

        # Get top comments and submissions
        data["top_comments"] = sorted(all_comments, key=lambda x: x["score"], reverse=True)[:3]
        data["top_submissions"] = sorted(all_submissions, key=lambda x: x["score"], reverse=True)[:3]

        return data

    except Exception as e:
        print(f"An error occurred while scraping data for u/{username}: {e}")
        return None
