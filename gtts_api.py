from gtts import gTTS
from pydub import AudioSegment

def convert_mp3_2_ogg(mp3_path):
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    ogg_path =  mp3_path.replace('mp3', 'ogg')
    audio.export(ogg_path, format="ogg")
    return ogg_path

def text_to_speech_gtts(text: str) -> None:

    output_file = 'gtts_output.mp3'
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    output_file = convert_mp3_2_ogg(output_file)

    print(f"Audio saved to {output_file}")

    return output_file
