# comment_clip.py
import os
from moviepy.editor import (AudioFileClip,
                            CompositeVideoClip,
                            concatenate_videoclips,
                            ImageClip,
                            TextClip,
                            VideoFileClip)
from moviepy.video.fx import all as vfx
from .speech_engine import generate_audio
from settings import COMMENT_CONFIG


class CommentClip:
    @classmethod
    def create_comment_clips(cls, comments, comment_limit, slugified_title, background_clip):
        comment_clips = []

        for i, comment_text in enumerate(comments, start=1):
            if i > comment_limit:
                break

            # Skip comments with [removed]
            if "[removed]" in comment_text.body:
                print(f"Skipping comment {i} as it contains [removed]")
                continue

            # Skip comments exceeding the maximum length
            if len(comment_text.body) > COMMENT_CONFIG['max_comment_length']:
                print(f"Skipping comment {i} as it exceeds the maximum length")
                continue

            if comment_text.body:
                print(f"Generating Comment Clip {i}: {comment_text.body}")
                comment_audio_path = os.path.join("comments_audio", f"{slugified_title[:25]}_comment_{i}.mp3")

                if not os.path.exists(comment_audio_path):
                    generate_audio(comment_text.body, comment_audio_path)

                comment_audio_clip = AudioFileClip(comment_audio_path)

                image_path = os.path.join(COMMENT_CONFIG['output_directory'], f"{comment_text.name}.png")

                comment_image_clip: ImageClip = (
                    ImageClip(image_path)
                    .set_duration(comment_audio_clip.duration)
                    .set_audio(comment_audio_clip)
                    .resize(width=background_clip.size[0] * 0.8)
                )

                comment_clips.append(comment_image_clip)

            # Break the loop if the number of comments reaches the maximum
            if i + 1 >= COMMENT_CONFIG['max_comments']:
                print(f"Reached the maximum number of comments ({COMMENT_CONFIG['max_comments']}). Stopping.")
                break

        return comment_clips

    # @classmethod
    # def overlay_comments(cls, concatenated_comments, background_clip):
    #     if concatenated_comments.duration > background_clip.duration:
    #         # Loop the background video to match the duration of the concatenated comments
    #         loop_factor = int(concatenated_comments.duration / background_clip.duration) + 1
    #         background_clip = background_clip.fx(vfx.loop, n=loop_factor)

    #     return CompositeVideoClip([background_clip, concatenated_comments])

    def overlay_comments(cls, concatenated_comments, background_clip_path):
        background_clip = VideoFileClip(background_clip_path)

        if concatenated_comments.duration > background_clip.duration:
            print("Looping Video Background")
            background_clip = vfx.loop(
                background_clip, duration=concatenated_comments.duration
            ).without_audio()

        # Resize concatenated_comments to match the size of the background clip
        concatenated_comments = concatenated_comments.resize(background_clip.size)

        # Overlay the comments on the background video
        video = CompositeVideoClip([background_clip, concatenated_comments])

        return video