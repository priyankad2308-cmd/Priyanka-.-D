from pathlib import Path
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

OUTPUT_DIR = Path("static/generated")
OUTPUT_DIR.mkdir(parents=True, 

def generate_panel_image(prompt: str, panel_number: int):
    """
    Creates a placeholder comic panel image.
    (Gemini Flash cannot generate images directly.)
    """

    width = 1024
    height = 1024

    image = Image.new("RGB", (width, height), color=(245, 245, 245))
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        body_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    draw.rectangle(
        [(20, 20), (width - 20, height - 20)],
        outline="black",
        width=5
    )

    draw.text(
        (40, 40),
        f"Panel {panel_number}",
        fill="black",
        font=title_font
    )

    wrapped = "\n".join(textwrap.wrap(prompt, width=45))

    draw.multiline_text(
        (40, 120),
        wrapped,
        fill="black",
        font=body_font,
        spacing=8
    )

    filename = OUTPUT_DIR / f"panel_{panel_number}.png"
    image.save(filename)

    return str(filename)


def generate_comic_images(outline: list):
    """
    Generate all comic panel placeholder images.
    """

    image_paths = []

    for index, panel in enumerate(outline, start=1):
        prompt = panel.get("image_prompt", panel.get("description", "Comic Panel"))
        path = generate_panel_image(prompt, index)
        image_paths.append(path)

    return image_paths