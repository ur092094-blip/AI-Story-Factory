
import os
import json
import urllib.request
from pathlib import Path

API_KEY = os.environ["GEMINI_API_KEY"]

PROMPT = """
Write one original animated story for YouTube Shorts.

Requirements:
- English language
- 45 to 60 seconds
- Family friendly
- Strong opening hook
- Emotional or surprising ending
- 5 animated scenes
- Consistent characters

Include:
1. Catchy title
2. Complete narration
3. Character descriptions
4. Five scene descriptions
5. Visual prompts for every scene
6. Dialogue and sound effects

Return a complete, original story.
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

with urllib.request.urlopen(request, timeout=120) as response:
    result = json.loads(response.read().decode("utf-8"))

story = result["candidates"][0]["content"]["parts"][0]["text"]

Path("output").mkdir(exist_ok=True)
Path("output/story.md").write_text(story, encoding="utf-8")

print("SUCCESS! AI STORY CREATED!")
print(story)
