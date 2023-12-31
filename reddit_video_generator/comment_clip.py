# comment_clip.py
import os
from moviepy.editor import (AudioFileClip,
                            ImageClip)
from .speech_engine import generate_audio
#from settings import COMMENT_CONFIG


class CommentClip:
    @classmethod
    def create_comment_clips(cls,
                             comments,
                             comment_limit,
                             slugified_title,
                             background_clip,
                             config):
        comment_clips = []

        for i, comment_text in enumerate(comments, start=1):
            if i > comment_limit:
                break

            # Skip comments with [removed]
            if "[removed]" in comment_text.body:
                print(f"Skipping comment {i} as it contains [removed]")
                continue

            if comment_text.body:
                print(f"Generating Comment Clip {i}: {comment_text.body}")
                comment_audio_path = os.path.join(config.comment_output_directory,
                                                  f"{comment_text.name}.mp3")

                if not os.path.exists(comment_audio_path):
                    generate_audio(comment_text.body, comment_audio_path, config)

                comment_audio_clip = AudioFileClip(comment_audio_path)

                image_path = os.path.join(config.comment_output_directory,
                                          f"{comment_text.name}.png")

                comment_image_clip: ImageClip = (
                    ImageClip(image_path)
                    .set_duration(comment_audio_clip.duration)
                    .set_audio(comment_audio_clip)
                    .resize(width=background_clip.size[0]
                            * config.comment_width)
                )

                comment_clips.append(comment_image_clip)

            # Break the loop if the number of comments reaches the maximum
            if i + 1 > config.comment_limit:
                print(f"Reached the maximum number of comments ({config.comment_limit}). Stopping.")
                break

        return comment_clips
