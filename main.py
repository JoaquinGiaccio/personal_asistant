#!/usr/bin/python3

import argparse
import transcriber
import record_audio
import gpt_api
import json
import neurasound_api
from playsound import playsound

def main(model, language, gpt_model, tts_voice, tts_accent):

    whisper_model = model
    loaded_model = transcriber.load_model(whisper_model)
    print("ASR model loaded")

    detected_language = ""

    while detected_language != str(language):
        audio = record_audio.record_audio_sr()
        print("Finish recording")
        record_audio.audio_to_wav(audio)
        detected_language, mel = transcriber.get_language(loaded_model, 'microphone-results.wav')
        print("##################################### ",language)

    print("Transcribing...")
    transcription = transcriber.transcriber(loaded_model, mel)
    print("Transcription: ",transcription)

    print("Sending Transcriptioon to openai API")
    chat_answer = gpt_api.send_request(transcription, gpt_model)
    chat_answer = json.loads(chat_answer)
    print("Chat answer: ", chat_answer)

    print(chat_answer['choices'])
    message_dict = dict(chat_answer['choices'][0])
    print(message_dict['message']['content'])
    gpt_message = message_dict['message']['content']

    #ssml_message = format_message(message_dict['message']['content'], tts_voice, tts_accent)
    ssml_message = format_message(gpt_message, tts_voice, tts_accent)
    print("\nFormated text: ",ssml_message)

    #tts_status = neurasound_api.neura_speak(message_dict['message']['content'])
    tts_status = neurasound_api.neura_speak(ssml_message)

    if tts_status != 'ERROR':
        playsound('neura_tts.wav')
    else:
        print("Error: Error in TTS message.")


def format_message(text, voice, accent):

    text = text.replace('.', ' <break time=\'1.5s\'/>')
    text = text.replace(',',' ,')
    words = text.split()
    formated_text = ""

    for word in words:
        x = word.isdigit()
        if x == True:
            ssml_tag = "<say-as interpret-as='cardinal'>" + word + "</say-as>"
            formated_text = formated_text + " " + ssml_tag
        else:
            formated_text = formated_text + " " + word

    formated_text = "<speak> <voice name='" + voice + "' lang='" + accent + "'>" + formated_text + "</voice> </speak>"

    return formated_text


def parseInputArguments():
    
    parser = argparse.ArgumentParser(description='Process to create a transcription while sending the audio')
    parser.add_argument("-m","--asrmodel", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large", "large-v2"])
    parser.add_argument("-l","--language", default="es", help="language",
                        choices=["en", "es"])
    parser.add_argument("-g","--gptmodel", default="gpt-3.5-turbo", help="openai gpt model to be used",
                        choices=["gpt-3.5-turbo", "text-davinci-003"])
    parser.add_argument("--tts_voice", default="m3", help="neurasound tts voice",
                        choices=["f1", "f2","f3", "m1", "m2", "m3"])
    parser.add_argument("--tts_accent", default="arg", help="neurasound tts accent",
                        choices=["arg", "col", "ven"])                     

    args = parser.parse_args()
    model = args.asrmodel
    language = args.language
    gpt_model = args.gptmodel
    tts_voice = args.tts_voice
    tts_accent = args.tts_accent

    return model, language, gpt_model, tts_voice, tts_accent

if __name__ == "__main__":
    model, language, gpt_model, tts_voice, tts_accent = parseInputArguments()
    main(model, language, gpt_model, tts_voice, tts_accent)