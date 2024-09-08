from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/music", StaticFiles(directory="music"), name="music")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
app.mount("/images", StaticFiles(directory="images"), name="images")

# Constants
url = "http://localhost:3000/api/generate"
api_key = os.environ.get("GROQ_KEY")
openai_api_key = os.environ.get("OPEN_AI_KEY")
ele_ids = []

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)


class MusicPrompt(BaseModel):
    prompt: str


def create_music(prompt: str):
    print("PORMPTT:!!", prompt)
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
        audio_urls = [item['audio_url']
                      for item in data if 'audio_url' in item]

        if not os.path.exists('music'):
            os.makedirs('music')

        for idx, audio_url in enumerate([audio_urls[0]]):
            print(f"Downloading {audio_url}")
            item_id = audio_url.split('=')[-1]
            ele_ids.append(item_id)
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                file_path = os.path.join('music', f'audio_{idx}.mp3')
                with open(file_path, 'wb') as audio_file:
                    audio_file.write(audio_response.content)
                print(f"Accessed: {file_path}")
                l.append(file_path)
            else:
                print(f"Failed to download {audio_url}")
    else:
        print("Error:", response.status_code)
        print(response.text)

    return l


def get_req():
    global lyric
    global video_url
    print(ele_ids)
    if ele_ids:
        req_url = f"http://localhost:3000/api/get?ids={ele_ids[0]}"
        response = requests.get(req_url, verify=False)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data and isinstance(data, list):
                if 'video_url' in data[0]:
                    video_url = f"https://cdn1.suno.ai/{ele_ids[0]}.mp4"
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
    else:
        print("No audio files were generated.")


def get_image_prompts(lyrics: str):
    print("lyrics: ", lyrics)
    prompt = f"Generate a list of one image prompts each, for each verse in the following lyrics: {lyrics}, (prefix every image prompt with 'IMAGE_PROMPT')"
    prompts = []
    client = Groq(api_key=api_key)

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

    for line in output.split('\n'):
        if 'IMAGE_PROMPT' in line:
            prompts.append(line)

    return prompts


def genImage(prompt: str):
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="512x512",
        quality="standard",
        n=1,
    )
    return response.data[0].url


@app.post("/generate")
def generate(music_prompt: MusicPrompt):
    print("triggered")
    prompt = music_prompt.prompt

    # Step 1: Create music
    create_music(prompt)

    # Step 2: Get lyrics
    get_req()

    # Step 3: Generate image prompts
    prompts = get_image_prompts(lyric)
    print("Extracted Prompts:", prompts)

    # Step 4: Generate images
    image_urls = []
    for prompt in prompts:
        image_urls.append(genImage(prompt))
        # image_urls.append("ads")

    os.makedirs('images', exist_ok=True)
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        with open(f'images/image_{i}.jpg', 'wb') as f:
            f.write(response.content)
    print("Completed!")
    return {
        "audio_files": [f'music/audio_{i}.mp3' for i in range(len(ele_ids))],
        "video_files": [video_url],
        "image_files": [f'images/image_{i}.jpg' for i in range(len(image_urls))]
    }


@app.get('/')
def hellow():
    return {"response": "Hello World"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
