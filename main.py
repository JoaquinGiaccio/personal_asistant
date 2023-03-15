#!/usr/bin/python3

import argparse
import transcriber
import record_audio
import gpt_api
import json
import neurasound_api
from playsound import playsound

def main(model):

    whisper_model = model
    loaded_model = transcriber.load_model(whisper_model)

    #record_audio.record_audio()
    audio = record_audio.record_audio_sr()
    record_audio.audio_to_wav(audio)
    transcription = transcriber.transcriber(loaded_model,'microphone-results.wav')

    print(transcription)
    chat_answer = gpt_api.send_request(transcription)

    chat_answer = json.loads(chat_answer)

    print(chat_answer['choices'])
    message_dict = dict(chat_answer['choices'][0])
    print(message_dict['message']['content'])

    neurasound_api.neura_speak(message_dict['message']['content'])

    playsound('neura_tts.wav')


def parseInputArguments():
    
    parser = argparse.ArgumentParser(description='Process to create a transcription while sending the audio')
    parser.add_argument("-m","--model", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large", "large-v2"])
    parser.add_argument("-l","--language", default="es", help="language",
                        choices=["tiny", "base", "small", "medium", "large", "large-v2"])                    

    args = parser.parse_args()
    model = args.model

    return model

if __name__ == "__main__":
    model = parseInputArguments()
    main(model)