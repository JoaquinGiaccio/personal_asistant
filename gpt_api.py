import requests
import os

def send_request(text,model):

    openai_key = os.getenv('OPENAI_API_KEY')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai_key,
    }

    json_data = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': text,
            },
        ],
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)

    return response.content