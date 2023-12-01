# reddit_video_generator.py
from typing import List
import os
from slugify import slugify
from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
from gtts import gTTS
from .comment_clip import CommentClip
from .selftext_clip import SelfTextClip
from .screenshot import capture_element_screenshot
import praw
from settings import (
    VIDEO_GENERATION_CONFIG,
    VIDEO_CONFIG
)

class RedditPost:
    def __init__(self, title: str, selftext: str, comments: List[str], id:str):
        """
        Represents a Reddit post with a title, selftext, and comments.

        :param title: The title of the post.
        :param selftext: The selftext of the post.
        :param comments: List of comments for the post.
        """
        self.title = title
        self.selftext = selftext
        self.comments = comments
        self.id = id
        self.slugified_title = slugify(title)


class RedditVideoGenerator:
    def __init__(self, subreddit_name: str, client_id: str, client_secret: str, user_agent: str,
                 background_video_path: str, background_music_path: str):
        self.subreddit_name = subreddit_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.background_video_path = background_video_path
        self.background_music_path = background_music_path

    def overlay_comments(self, final_clip, concatenated_comments):
        return CompositeVideoClip([final_clip, concatenated_comments])

    def authenticate(self) -> praw.Reddit:
        """
        Authenticate with the Reddit API.

        :return: Authenticated praw.Reddit instance.
        """
        return praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent=self.user_agent)

    def get_top_posts(self, limit: int = 10) -> List[RedditPost]:
        print(f"Getting Top {str(limit)} Reddit Posts")
        reddit = self.authenticate()
        subreddit = reddit.subreddit(self.subreddit_name)
        top_posts = subreddit.top(time_filter='day', limit=limit)

        reddit_posts = []
        for post in top_posts:

            # Skip NSFW posts
            if post.over_18:
                if not VIDEO_CONFIG['EnableNSFW']:
                    print(f"Skipping NSFW post: {post.title}")
                    continue

            reddit_posts.append(RedditPost(title=post.title,
                                           selftext=post.selftext,
                                           comments=post.comments,
                                           id=post.id))

        return reddit_posts

    def generate_video(self, post, output_path: str, comment_limit: int = 10):
        print(f"Generating Video : {post.title}")

        # Create a folder to store comment audio clips
        comments_folder = "comments_audio"
        os.makedirs(comments_folder, exist_ok=True)

        # Create a video clip with the specified background video
        background_clip = VideoFileClip(self.background_video_path)

        # Read out the selftext using text-to-speech if it's not empty
        selftext_clip = SelfTextClip.create(post.selftext)
        if selftext_clip:
            final_clip = selftext_clip.overlay_on_background(background_clip)
        else:
            # If selftext is empty, use only the background clip
            final_clip = background_clip

        # Retrieve top comments for each post
        comments = [comment if not isinstance(comment, praw.models.MoreComments) else ""
                    for comment in post.comments.list() if hasattr(comment, 'body')]

        capture_element_screenshot(comments)

        # Create a list to store comment clips
        comment_clips = CommentClip.create_comment_clips(comments,
                                                         comment_limit,
                                                         post.slugified_title,
                                                         background_clip)

        # Concatenate all comment clips
        if comment_clips:
            concatenated_comments = concatenate_videoclips(comment_clips).set_position(('center', 'center'))
            final_clip = self.overlay_comments(final_clip, concatenated_comments)

        # Write the final video to the specified output path
        print(f"Writing the final video to the specified output path: {output_path}")

        final_clip.write_videofile(output_path,
                                   codec='libx264',
                                   audio_codec='aac',
                                   threads=4)