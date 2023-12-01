# settings.py

REDDIT_CONFIG = {
    'subreddit_name': 'AskReddit',  # Replace with your desired subreddit
}

VIDEO_CONFIG = {
    'background_video_path': 'video_background.mp4',
    'background_music_path': 'video_music.mp3',
    'desired_video_length': 180,  # Desired Video Length in Seconds
    'EnableNSFW': True # Allow NSFW Posts
}

COMMENT_CONFIG = {
    'comment_limit': 10,  # Number of comments to include in the video
    'max_comment_length': 600,  # Maximum character limit for comments
    'max_comments': 10,  # Maximum number of comments to add to video
    'output_directory': "cache",
    'width': 0.9  # Comment image width
}

VIDEO_OUTPUT_DIR = 'final'

# Add the desired_video_count setting
VIDEO_GENERATION_CONFIG = {
    'desired_video_count': 1,  # Replace with the desired number of videos
}

SPEECH_ENGINE = 'edge-tts'  # You can set this to 'edge-tts' to use the edge-tts engine
