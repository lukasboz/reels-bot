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


def choose_post(posts, subreddit="AskReddit", limit=5):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    seen_ids = set(post.id for post in posts)
    index = 0

    while True:
        current_batch = posts[index:index + limit]

        if not current_batch:
            print("\n⚠️ No more cached posts. Fetching new ones...")

            raw_new_posts = reddit.subreddit(subreddit).top(time_filter="day", limit=15)
            new_safe_posts = [
                post for post in raw_new_posts
                if not post.over_18 and post.id not in seen_ids
            ]

            if not new_safe_posts:
                print("😕 Couldn't find new unseen posts. Try again later.")
                continue

            posts.extend(new_safe_posts)
            seen_ids.update(post.id for post in new_safe_posts)
            continue  # Start loop again with newly added posts

        # Show current batch with local numbers (1–limit)
        print(f"\nTop posts from r/{subreddit} (batch {index // limit + 1}):")
        for i, post in enumerate(current_batch, 1):
            print(f"{i}. {post.title}")

        try:
            choice = input(f"\nEnter number (1-{len(current_batch)}) or 0 to get more posts: ").strip()
            if choice == "0":
                index += limit
                continue

            choice = int(choice)
            if 1 <= choice <= len(current_batch):
                return current_batch[choice - 1]
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
    subreddit = "AskReddit"
    try:
        # Step 1: Get initial top posts
        posts = get_top_reddit_posts(subreddit=subreddit)

        # Step 2: Let user pick one (with option to load more)
        chosen_post = choose_post(posts, subreddit=subreddit)

        # Step 3: Get top comments
        print(f"\n[+] Loading top comments for:\n{chosen_post.title}")
        comments = get_top_comments(chosen_post, limit=5)

        print('[+] Done!')

        # Step 4: Export to text file
        export_to_file(chosen_post.title, [c.body for c in comments])

    except Exception as e:
        print(f"[!] Error: {e}")
