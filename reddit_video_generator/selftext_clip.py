# selftext_clip.py
from moviepy.editor import TextClip, CompositeVideoClip

class SelfTextClip:
    @classmethod
    def create(cls, selftext):
        # Your logic to create a TextClip from selftext
        # Make sure to return an instance of SelfTextClip or None if selftext is empty
        if selftext:
            return cls(selftext)
        else:
            return None

    def __init__(self, selftext):
        # Initialize with necessary attributes based on selftext
        self.text_clip = TextClip(selftext, fontsize=24, color='white', bg_color='black', size=(1920, 1080))

    def overlay_on_background(self, background_clip):
        # Your logic to overlay self.text_clip on the background_clip
        return CompositeVideoClip([background_clip, self.text_clip])
