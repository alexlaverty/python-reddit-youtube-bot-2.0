# reddit_video_generator.py
from typing import List
import os
from slugify import slugify
from moviepy.editor import (VideoFileClip,
                            CompositeVideoClip,
                            concatenate_videoclips,
                            AudioFileClip,
                            TextClip)
from moviepy.video.fx import all as vfx
from .comment_clip import CommentClip
from .selftext_clip import SelfTextClip
from .screenshot import RedditScreenshotCapture
from .speech_engine import generate_audio
import praw
from settings import (YouTubeChannelConfig)
from auth import REDDIT_AUTH

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
    def __init__(self, channel_config: YouTubeChannelConfig):
        self.config = channel_config

    def overlay_comments(self, background_clip, concatenated_comments):

        print(f"final_clip.duration : {str(background_clip.duration)}")
        print(f"concatenated_comments.duration : {str(concatenated_comments.duration)}")

        # Loop the video background if required
        if concatenated_comments.duration > background_clip.duration:
            print("Looping Video Background")
            background_clip = vfx.loop(
                background_clip, duration=concatenated_comments.duration
            ).without_audio()
        else:
            # Trim background clip to duration of the comment clips
            print("Trimming background video to comments duration...")
            background_clip = background_clip.subclip(0, concatenated_comments.duration)

        # Overlay the comments on the background video
        video = CompositeVideoClip([background_clip, concatenated_comments])

        return video

    def authenticate(self) -> praw.Reddit:
        """
        Authenticate with the Reddit API.

        :return: Authenticated praw.Reddit instance.
        """
        return praw.Reddit(client_id=REDDIT_AUTH['client_id'],
                           client_secret=REDDIT_AUTH['client_secret'],
                           user_agent=REDDIT_AUTH['user_agent'])

    def get_top_posts(self, limit: int = 10) -> List[RedditPost]:
        print(f"Retrieving Top {str(limit)} Reddit Posts from {self.config.subreddit_name}")
        reddit = self.authenticate()
        subreddit = reddit.subreddit(self.config.subreddit_name)
        top_posts = subreddit.top(time_filter='day', limit=limit)

        reddit_posts = []
        for post in top_posts:

            # Skip NSFW posts
            if post.over_18:
                if not self.config.enable_nsfw:
                    print(f"Skipping NSFW post: {post.title}")
                    continue

            reddit_posts.append(RedditPost(title=post.title,
                                           selftext=post.selftext,
                                           comments=post.comments,
                                           id=post.id))

        return reddit_posts

    def generate_title_text_clip(self, post,
                                 background_clip: VideoFileClip) -> TextClip:
        title_audio_path = os.path.join(self.config.comment_output_directory, f"{post.id}.mp3")

        if not os.path.exists(title_audio_path):
            generate_audio(post.title, title_audio_path, self.config)

        title_audio_clip = AudioFileClip(title_audio_path)

        title_text_clip = (
            TextClip(post.title,
                     color='white',
                     font="Verdana-Bold",
                     fontsize=70,
                     method="caption",
                     size=background_clip.size,
                     stroke_color='black',
                     stroke_width=2)
            .set_audio(title_audio_clip)
            .set_duration(title_audio_clip.duration)
        )

        return title_text_clip

    def generate_video(self, post):
        print(f"Generating Video : {post.title}")

        # Create a folder to store comment audio clips
        os.makedirs(self.config.output_directory, exist_ok=True)

        # Create a video clip with the specified background video
        background_video_path = os.path.join("assets", self.config.background_video_path)
        background_clip = VideoFileClip(background_video_path).volumex(0)

        title_audio_path = os.path.join(self.config.comment_output_directory,
                                        f"{post.id}.mp3")

        if not os.path.exists(title_audio_path):
            generate_audio(post.title, title_audio_path, self.config)

        # title_audio_clip = AudioFileClip(title_audio_path)

        title_text_clip = self.generate_title_text_clip(post, background_clip)

        # # Read out the selftext using text-to-speech if it's not empty
        # selftext_clip = SelfTextClip.create(post.selftext)
        # if selftext_clip:
        #     final_clip = selftext_clip.overlay_on_background(background_clip)
        # else:
        #     # If selftext is empty, use only the background clip
        #     final_clip = background_clip

        # Retrieve top comments for each post, excluding comments exceeding
        # max_comment_length and those with [removed]

        final_clip = background_clip

        comments = [
            comment
            for i, comment in enumerate(post.comments.list())
            if hasattr(comment, 'body')
            and len(comment.body) <= self.config.max_comment_length
            and "[removed]" not in comment.body
        ]

        screenshot_capture = RedditScreenshotCapture(self.config)
        screenshot_capture.capture_element_screenshot(comments)

        # Create a list to store comment clips
        comment_clips = CommentClip.create_comment_clips(comments,
                                                         self.config.comment_limit,
                                                         post.slugified_title,
                                                         background_clip,
                                                         self.config)

        comment_clips.insert(0, title_text_clip)

        # Concatenate all comment clips
        if comment_clips:
            concatenated_comments = concatenate_videoclips(comment_clips)\
                                    .set_position(('center', 'center'))

            final_clip = self.overlay_comments(final_clip,
                                               concatenated_comments)

        output_path = os.path.join(self.config.output_directory, f"{post.slugified_title}.mp4")

        # Write the final video to the specified output path
        print(f"Writing the final video to the specified output path: {output_path}")

        final_clip.write_videofile(output_path,
                                   codec='libx264',
                                   audio_codec='aac',
                                   threads=4)
