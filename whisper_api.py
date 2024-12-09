import os
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, pipeline
from pydub import AudioSegment

def convert_ogg_2_wav(ogg_path):
    audio = AudioSegment.from_file(ogg_path, format="ogg")
    wav_path =  ogg_path + '.wav'
    audio.export(wav_path, format="wav")
    return wav_path

import subprocess

def normalize_audio(input_file: str, output_file: str) -> None:
    """
    Normalize an audio file using `sox`.

    Parameters:
    - input_file (str): Path to the input `.wav` file.
    - output_file (str): Path to save the normalized `.wav` file.
    """
    try:
        # Sox command to normalize audio
        command = [
            "sox", input_file, output_file,
            "norm", "-0.5", "compand", "0.3,1",
            "-90,-90,-70,-70,-60,-20,0,0", "-5", "0", "0.2"
        ]
        
        # Run the command
        subprocess.run(command, check=True)
        print(f"Audio normalized successfully: {output_file}")
    except FileNotFoundError:
        print("Error: `sox` is not installed or not found in PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Sox process failed with error:\n{e}")

def transcribe_russian(ogg_path):
    torch_dtype = torch.float32 # set your preferred type here 

    device = 'cpu'
    if torch.cuda.is_available():
        device = 'cuda'
    elif torch.backends.mps.is_available():
        device = 'mps'
        setattr(torch.distributed, "is_initialized", lambda : False) # monkey patching
    device = torch.device(device)

    whisper = WhisperForConditionalGeneration.from_pretrained(
        "antony66/whisper-large-v3-russian", torch_dtype=torch_dtype, use_safetensors=True,
        # add attn_implementation="flash_attention_2" if your GPU supports it
    )

    processor = WhisperProcessor.from_pretrained("antony66/whisper-large-v3-russian")

    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model=whisper,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=256,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    wav = convert_ogg_2_wav(ogg_path)
    wav_normalized = wav + '.normalized.wav'
    normalize_audio(wav, wav_normalized)

    # get the transcription
    asr = asr_pipeline(wav_normalized, generate_kwargs={"language": "russian", "max_new_tokens": 256}, return_timestamps=False)

    print(asr['text'])

    return asr['text']
