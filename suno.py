import requests
import json
import time
import os

url = "http://localhost:3000/api/generate"


def create_music(prompt):
    # Define the payload
    l = []
    payload = {
        "prompt": prompt,
        "make_instrumental": False,
        "wait_audio": True
    }

    headers = {
        "Content-Type": "application/json"
    }
    print("Generating your tones, please wait for 30 seconds...")
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()

        # Extract the audio URLs
        audio_urls = [item['audio_url']
                      for item in data if 'audio_url' in item]

        # Create the music directory if it doesn't exist
        if not os.path.exists('music'):
            os.makedirs('music')

        # Download and save each audio file
        for idx, audio_url in enumerate(audio_urls):
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                file_path = os.path.join('music', f'audio_{idx}.mp3')
                with open(file_path, 'wb') as audio_file:
                    audio_file.write(audio_response.content)
                print(f"Downloaded: {file_path}")
                l.append(file_path)
            else:
                print(f"Failed to download {audio_url}")

    else:
        print("Error:", response.status_code)
        print(response.text)

    return l


prompt = "create me a song about the laws of thermodynamic, try to incorporate rhymes "
create_music(prompt)
