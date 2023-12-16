# settings.py

REDDIT_CONFIG = {
    'subreddit_name': 'AskReddit',  # Replace with your desired subreddit
    'post_limit': 30, # Number of Reddit posts to retrieve
}

VIDEO_CONFIG = {
    'background_video_path': 'video_background.mp4',
    'background_music_path': 'video_music.mp3',
    'desired_video_length': 180,  # Desired Video Length in Seconds
    'EnableNSFW': False, # Allow NSFW Posts
    'desired_video_count': 1,  # Replace with the desired number of videos
    'output_directory': 'final'
}

COMMENT_CONFIG = {
    'comment_limit': 10,  # Number of comments to include in the video
    'max_comment_length': 500,  # Maximum character limit for comments
    'output_directory': "cache",
    'width': 0.9  # Comment image width
}

SPEECH_CONFIG = {
    'engine': 'edge-tts',
    'barkvoice' : 'en_speaker_5'
}
