import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


def _generate(prompt: str) -> str:
    models = [
        "models/gemini-3.8-flash",
        "models/gemini-3.7-flash",
        "models/gemini-3.6-flash",
        "models/gemini-3.5-flash",
    ]

    last_error = ""

    for model in models:
        for _ in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                return response.text

            except Exception as e:
                last_error = str(e)

                # Retry only for temporary 503 errors
                if "503" in last_error or "UNAVAILABLE" in last_error:
                    time.sleep(3)
                    continue

                break

    return f"Error: {last_error}"


def generate_outline(topic: str) -> str:
    prompt = f"""
Create a short comic story outline.

Topic:
{topic}

Return:
1. Title
2. Characters
3. Scene-wise outline (5 scenes)
"""

    return _generate(prompt)


def generate_script(outline: str) -> str:
    prompt = f"""
Convert the following comic outline into a detailed comic script.

Outline:
{outline}

For each scene include:
- Scene Number
- Description
- Dialogue
"""

    return _generate(prompt)


def generate_image_prompt(scene_description: str) -> str:
    prompt = f"""
Create a detailed AI image prompt.

Scene:
{scene_description}

Make it cinematic, colorful, comic-book style.
"""

    return _generate(prompt)