from gtts import gTTS
from pydub import AudioSegment

def convert_mp3_2_ogg(mp3_path):
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    ogg_path =  mp3_path.replace('mp3', 'ogg')
    audio.export(ogg_path, format="ogg")
    return ogg_path

def remap_language(language: str):
    lang_map = {
        'Polish': 'pl',
        'English': 'en'
    }

    assert language in lang_map
    return lang_map[language]

def text_to_speech_gtts(text: str, language) -> None:

    language = remap_language(language)
    output_file = 'gtts_output.mp3'
    tts = gTTS(text=text, lang=language)
    tts.save(output_file)

    output_file = convert_mp3_2_ogg(output_file)

    print(f"Audio saved to {output_file}")

    return output_file
