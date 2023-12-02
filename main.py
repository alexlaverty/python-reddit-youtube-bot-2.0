# main.py
import os
from reddit_video_generator.reddit_video_generator import RedditVideoGenerator
from auth import REDDIT_AUTH
from settings import (
    COMMENT_CONFIG,
    REDDIT_CONFIG,
    VIDEO_CONFIG,
    VIDEO_GENERATION_CONFIG,
    VIDEO_OUTPUT_DIR,
)


if __name__ == "__main__":
    # Extract Reddit credentials from auth
    subreddit_name = REDDIT_CONFIG['subreddit_name']

    # Extract video-related settings from settings
    background_video_path = VIDEO_CONFIG['background_video_path']
    background_music_path = VIDEO_CONFIG['background_music_path']

    # Extract comment-related settings from settings
    comment_limit = COMMENT_CONFIG['comment_limit']

    video_generator = RedditVideoGenerator(
        subreddit_name=subreddit_name,
        client_id=REDDIT_AUTH["client_id"],
        client_secret=REDDIT_AUTH["client_secret"],
        user_agent=REDDIT_AUTH["user_agent"],
        background_video_path=VIDEO_CONFIG["background_video_path"],
        background_music_path=VIDEO_CONFIG["background_music_path"],
    )

    # Specify the desired number of videos to generate
    desired_video_count = VIDEO_GENERATION_CONFIG['desired_video_count']

    # Retrieve a batch of posts
    top_posts = video_generator.get_top_posts(limit=10)  # Adjust the batch size as needed

    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

    # Loop until the desired number of videos is reached
    generated_video_count = 0

    print(f"Comment limit set to : {comment_limit}")

    for i, post in enumerate(top_posts, start=1):
        if generated_video_count >= desired_video_count:
            break  # Exit the loop if the desired number of videos is reached

        output_path = os.path.join(VIDEO_OUTPUT_DIR, f"{post.slugified_title}.mp4")

        if os.path.exists(output_path):
            print(f"Skipping Already Exists : {post.title}")
            continue
        else:
            video_generator.generate_video(post, output_path, comment_limit)
            generated_video_count += 1
