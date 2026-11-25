
import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

API_KEY = os.environ["GEMINI_API_KEY"]

PROMPT = """
Create one original animated story for YouTube Shorts.

Language: English
Duration: 45-60 seconds
Family friendly.
Strong opening hook.
Emotional or surprising ending.
Five animated scenes.
Consistent characters.

Include title, narration, character descriptions,
scene descriptions, visual prompts and dialogue.
"""

url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.8-flash:generateContent"
)

payload = {
    "contents": [{
        "parts": [{"text": PROMPT}]
    }]
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    },
    method="POST"
)

for attempt in range(5):
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        story = result["candidates"][0]["content"]["parts"][0]["text"]

        Path("output").mkdir(exist_ok=True)
        Path("output/story.md").write_text(
            story, encoding="utf-8"
        )

        print("SUCCESS! AI STORY CREATED!")
        print(story)
        break

    except urllib.error.HTTPError as error:
        print("API Error:", error.code)

        if error.code not in (429, 500, 502, 503, 504):
            raise

        if attempt == 4:
            raise

        wait = 10 * (2 ** attempt)
        print("Retrying after", wait, "seconds...")
        time.sleep(wait)
