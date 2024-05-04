import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/5C9aRoVQC8P7QCK4f7IH"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "84a4c6c5597ba45858a7ff3b05a66754"
}

data = {
  "text": "behavior",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
