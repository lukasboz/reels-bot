import praw
import os
from config.secrets import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


def get_top_reddit_posts(subreddit="AskReddit", limit=5):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    print(f"[+] Fetching top {limit} posts from r/{subreddit} (excluding NSFW)...\n")
    
    # Get top posts of the day
    raw_posts = reddit.subreddit(subreddit).top(time_filter="day", limit=limit + 5)  # Extra to filter safely

    # Filter out NSFW posts
    safe_posts = [post for post in raw_posts if not post.over_18]

    # Limit again after filtering
    selected_posts = safe_posts[:limit]

    if not selected_posts:
        raise Exception("No safe (non-NSFW) posts found. Try another subreddit or time period.")

    return selected_posts


def choose_post(posts):
    for idx, post in enumerate(posts, 1):
        print(f"{idx}. {post.title}")
    
    while True:
        try:
            choice = int(input(f"\nEnter number (1-{len(posts)}): "))
            if 1 <= choice <= len(posts):
                return posts[choice - 1]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def get_top_comments(post, limit=3):
    print("[+] Expanding comment sections...")
    post.comments.replace_more(limit=10)

    print("[+] Collecting and sorting comments by length...")
    comments = post.comments.list()

    # Filter valid comments (not deleted, has a body)
    valid_comments = [
        comment for comment in comments
        if hasattr(comment, 'body') and comment.author != '[deleted]'
    ]

    # Sort comments by length descending and take top `limit`
    longest_comments = sorted(valid_comments, key=lambda c: len(c.body), reverse=True)[:limit]

    return longest_comments



def export_to_file(title, comments, filename="assets/output/reddit_script.txt"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n\n")
        for i, comment in enumerate(comments, 1):
            f.write(f"Comment {i}: {comment}\n\n")
    
    print(f"\n✅ Exported to {filename}")


if __name__ == "__main__":
    # Step 1: Get top posts
    try:
        posts = get_top_reddit_posts(subreddit="AskReddit")

        # Step 2: Let user pick one
        chosen_post = choose_post(posts)

        # Step 3: Get top 5 comments
        print(f"\n[+] Loading top comments for:\n{chosen_post.title}")
        comments = get_top_comments(chosen_post, limit=5)

        print('[+] Done!')

        # Step 4: Export to text file
        export_to_file(chosen_post.title, [c.body for c in comments])

    except Exception as e:
        print(f"[!] Error: {e}")