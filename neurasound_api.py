import requests
import os

neura_tts_url = 'https://7d07-157-92-27-254.sa.ngrok.io/get-file'

def neura_speak(text):

    neura_api_key = os.getenv('NEURA_API_KEY')

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + neura_api_key,
        'Content-Type': 'application/json',
    }

    json_data = {
        'ssml_string': "<speak> <voice name='m3' lang='arg'>" + text + "</voice> </speak>",
    }

    response = requests.post(neura_tts_url, headers=headers, json=json_data)

    # TTS API result validation
    if str(response) == '<Response [200]>':
        with open('neura_tts.wav', 'wb') as f:
            f.write(response.content)
    else:
        return "ERROR"