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
    chat_answer = gpt_api.send_request(transcription,gpt_model)
    chat_answer = json.loads(chat_answer)

    print(chat_answer['choices'])
    message_dict = dict(chat_answer['choices'][0])
    print(message_dict['message']['content'])

    tts_status = neurasound_api.neura_speak(message_dict['message']['content'])

    if tts_status != 'ERROR':
        playsound('neura_tts.wav')
    else:
        print("Error: Error in TTS message.")


def parseInputArguments():
    
    parser = argparse.ArgumentParser(description='Process to create a transcription while sending the audio')
    parser.add_argument("-m","--asrmodel", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large", "large-v2"])
    parser.add_argument("-l","--language", default="es", help="language",
                        choices=["en", "es"])
    parser.add_argument("-g","--gptmodel", default="gpt-3.5-turbo", help="language",
                        choices=["gpt-3.5-turbo", "text-davinci-003"])                    

    args = parser.parse_args()
    model = args.asrmodel
    gpt_model = args.gptmodel

    return model, gpt_model

if __name__ == "__main__":
    model, gpt_model = parseInputArguments()
    main(model)