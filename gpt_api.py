import requests

def send_request(text):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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',
    }

    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': text,
            },
        ],
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)

    print(response.content)

    return response.content