# speech_engine.py
from gtts import gTTS
import subprocess

from .speech_bark import bark_speech

from elevenlabs import generate, set_api_key, save
from auth import ELEVENLABS

def elevenlabs_speech(text, output_path, config):
    set_api_key(ELEVENLABS['api_key'])

    voice = generate(
        text=text,
        voice="Daniel"
    )

    save(voice, output_path)


def generate_audio(text, output_path, config):
    speech_engine = config.speech_engine

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
        bark_speech(text, output_path, config)
    elif speech_engine == 'elevenlabs':
        elevenlabs_speech(text, output_path, config)
    else:
        raise ValueError(f"Unsupported speech engine: {speech_engine}")
