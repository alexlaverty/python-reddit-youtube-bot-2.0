from dataclasses import dataclass, field

@dataclass
class YouTubeChannelConfig:
    channel_name: str
    client_secret_file: str
    credentials_storage_file: str
    theme_background_color: str = "#ffffff"
    theme_font_color: str = "#000000"
    subreddit_name: str = "AskReddit"
    post_limit: int = 50
    # Additional fields from settings.py
    background_video_path: str = 'video_background.mp4'
    background_music_path: str = 'video_music.mp3'
    desired_video_length: int = 180
    enable_nsfw: bool = False
    desired_video_count: int = 1
    output_directory: str = 'final'
    comment_limit: int = 10
    max_comment_length: int = 500
    comment_output_directory: str = "cache"
    comment_width: float = 0.9
    speech_engine: str = 'edge-tts'
    barkvoice: str = 'en_speaker_5'

@dataclass
class Theme:
    background_color: str
    font_color: str

    def __str__(self):
        return f"Background Color: {self.background_color}\nFont Color: {self.font_color}"