from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
from settings import YouTubeChannelConfig

def bark_speech(text: str, output_path: str, config: YouTubeChannelConfig) -> Audio:
    """
    Generate speech audio from text using Bark and save it to a WAV file.

    Parameters:
    - text (str): The input text for speech generation.
    - output_path (str): The path to save the generated audio as a WAV file.

    Returns:
    - Audio: An IPython.display.Audio object for playing the generated audio in
             a Jupyter notebook.
    """

    # download and load all models,
    # First time will take a while to complete
    preload_models()

    # generate audio from text
    audio_array = generate_audio(text,
                                 history_prompt=config.barkvoice)

    # save audio to disk
    write_wav(output_path, SAMPLE_RATE, audio_array)

    # play audio in notebook
    return Audio(audio_array, rate=SAMPLE_RATE)


# Example usage:
if __name__ == "__main__":
    text_prompt = """
         Hello, my name is Suno. And, uh — and I like pizza. [laughs]
         But I also have other interests such as playing tic tac toe.
    """
    output_path = "bark_generation.wav"

    audio_display = bark_speech(text_prompt, output_path)
    audio_display
