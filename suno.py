import requests
import json
from dotenv import load_dotenv

import os
from groq import Groq
from openai import OpenAI

url = "http://localhost:3000/api/generate"
api_key = "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"
ele_ids = ["2a1adcb4-f14b-40b5-9ef0-3547f481b55b"]

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))

def genImage(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

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


lyric = ""
if ele_ids:
    req_url = f"http://localhost:3000/api/get?ids={ele_ids[0]}"

    def get_req():
        global lyric
        response = requests.get(req_url, verify=False)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data and isinstance(data, list):
                if 'video_url' in data[0]:
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

                if 'lyric' in data[0]:
                    lyric = data[0]['lyric']
                    print("Lyric:", lyric)
                else:
                    print("Lyric not found in the response.")
            else:
                print("Unexpected data format.")
        else:
            print("Error:", response.status_code)
            print(response.text)

    get_req()


else:
    print("No audio files were generated.")


def get_image_prompts(lyrics):
    # Define the prompt
    print("lyrics: ", lyrics)
    prompt = f"Generate a list of one image prompts each, for each verse in the following lyrics: {lyrics}, (prefix every image prompt with 'IMAGE_PROMPT')"
    prompts = []
    client = Groq(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
    )
    output = chat_completion.choices[0].message.content
    print(output)

    # Extract IMAGE_PROMPT lines and add them to the prompts list
    for line in output.split('\n'):
        if 'IMAGE_PROMPT' in line:
            prompts.append(line)

    return prompts


prompts = get_image_prompts(lyric)
print("Extracted Prompts:", prompts)
image_urls = []

for prompt in prompts:
    image_urls.append(genImage(prompt))

os.makedirs('images', exist_ok=True)

for i, url in enumerate(image_urls):
    response = requests.get(url)

    # Open a file in write mode and write the content of the image
    with open(f'images/image_{i}.jpg', 'wb') as f:
        f.write(response.content)