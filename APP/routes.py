from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from APP.ai.gemini_flash import generate_outline, generate_script

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate")
async def generate(
    request: Request,
    prompt: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    full_prompt = f"""
Story Idea: {prompt}

Main Character: {character}

Setting: {setting}

Tone: {tone}

Art Style: {style}
"""

    outline = generate_outline(full_prompt)   
    script = generate_script(outline)

    return templates.TemplateResponse(
    request=request,
    name="preview.html",
    context={
        "request": request,
        "outline": outline,
        "script": script,
        "download_url": None
    }
)