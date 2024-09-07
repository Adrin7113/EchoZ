import requests
import json
import time
import os

url = "http://localhost:3000/api/generate"

ele_ids = []


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
        for idx, audio_url in enumerate([audio_urls[0]]):
            print(f"Downloading {audio_url}")
            item_id = audio_url.split('=')[-1]
            ele_ids.append(item_id)
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


prompt = "create me a song exapling the basics of Quantum physics, make it descriptive, try to incorporate rhymes "
# create_music(prompt)


# req_url = "http://localhost:3000/api/get?ids=2a1adcb4-f14b-40b5-9ef0-3547f481b55b"


if ele_ids:
    req_url = f"http://localhost:3000/api/get?ids={ele_ids[0]}"

    def get_req():
        response = requests.get(req_url, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and 'video_url' in data[0]:
                video_url = data[0]['video_url']
                print("Video URL:", video_url)

                # Create the videos directory if it doesn't exist
                if not os.path.exists('videos'):
                    os.makedirs('videos')

                # Download the video file
                video_response = requests.get(video_url)
                if video_response.status_code == 200:
                    file_path = os.path.join(
                        'videos', f'video_{ele_ids[0]}.mp4')
                    with open(file_path, 'wb') as video_file:
                        video_file.write(video_response.content)
                    print(f"Downloaded: {file_path}")
                else:
                    print(f"Failed to download {video_url}")
            else:
                print("Video URL not found in the response.")
        else:
            print("Error:", response.status_code)
            print(response.text)

    get_req()
else:
    print("No audio files were generated.")
