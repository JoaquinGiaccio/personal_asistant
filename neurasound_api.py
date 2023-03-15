import requests

def neura_speak(text):

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJzdHJpbmciLCJleHBpcnkiOjE2NjYzMDY5MDYuNDU5NjU5OH0.W2jSyRnkMOSdw7MSWL3N2ig4QNJS9OxC_jpfGwQ2PcE',
        'Content-Type': 'application/json',
    }

    json_data = {
        'text': text,
    }

    response = requests.post('https://fb6f-157-92-27-254.sa.ngrok.io/get-file', headers=headers, json=json_data)

    with open('neura_tts.wav', 'wb') as f:
        f.write(response.content)