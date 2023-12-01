# speech_engine.py
import os
from gtts import gTTS
import subprocess
from settings import (
    SPEECH_ENGINE
)
def generate_audio(text, output_path):
    speech_engine = SPEECH_ENGINE

    if speech_engine == 'gTTS':
        # Use gTTS
        tts = gTTS(text, lang='en')
        tts.save(output_path)
    elif speech_engine == 'edge-tts':
        # Use edge-tts
        subprocess.run(
            [
                "edge-tts",
                "--voice",
                "en-GB-RyanNeural",
                "--text",
                f"'{text.strip()}'",
                "--write-media",
                output_path,
            ]
        )
    else:
        raise ValueError(f"Unsupported speech engine: {speech_engine}")
