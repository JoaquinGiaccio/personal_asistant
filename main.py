#!/usr/bin/python3

import argparse
import transcriber
import record_audio

def main(model):

    whisper_model = model
    loaded_model = transcriber.load_model(whisper_model)
    #record_audio.record_audio()
    audio = record_audio.record_audio_sr()
    record_audio.audio_to_wav(audio)
    transcription = transcriber.transcriber(loaded_model,'microphone-results.wav')

    print(transcription)
    

def parseInputArguments():
    
    parser = argparse.ArgumentParser(description='Process to create a transcription while sending the audio')
    parser.add_argument("-m","--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large", "large-v2"])

    args = parser.parse_args()
    model = args.model

    return model

if __name__ == "__main__":

    model = parseInputArguments()
    main(model)
