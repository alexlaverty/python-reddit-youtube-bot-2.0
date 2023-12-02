# speech_engine.py
from gtts import gTTS
import subprocess
from settings import (
    SPEECH_CONFIG
)
from .speech_bark import bark_speech


def generate_audio(text, output_path):
    speech_engine = SPEECH_CONFIG['engine']

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
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    elif speech_engine == 'bark':
        bark_speech(text, output_path)
    else:
        raise ValueError(f"Unsupported speech engine: {speech_engine}")
