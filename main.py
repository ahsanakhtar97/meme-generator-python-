from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.schemas import GenerateRequest
from app.sd_engine import generate_ai_image

from PIL import ImageDraw, ImageFont, Image
import uuid, os
from dotenv import load_dotenv

# ---- CORRECT GOOGLE GENAI IMPORTS FOR VERSION 1.52.0 ----
from google import genai
from google.genai import types


# ----------------------------------------------------
# 📌 ENV SETUP + GEMINI CLIENT
# ----------------------------------------------------
load_dotenv()

client = None
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print("Gemini client initialized successfully.")
except Exception as e:
    print(f"WARNING: Gemini client failed to initialize: {e}")


FONT_PATH = "impact/impact.ttf"

app = FastAPI(title="AI Meme Generator")
app.mount("/generated", StaticFiles(directory="generated"), name="generated")


# ----------------------------------------------------
# 📌 GEMINI CAPTION (NON-ASYNC, WORKS 100%)
# ----------------------------------------------------
def generate_ai_caption(prompt: str):
    if not client:
        return None, None

    system_instruction = (
        "You are an expert meme caption generator. "
        "Output ONLY in this format: TOP_TEXT | BOTTOM_TEXT"
    )

    full_prompt = f"Image Prompt: '{prompt}'. Create meme captions."

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.8,
            )
        )

        text = response.text or ""

        if "|" in text:
            top, bottom = text.split("|", 1)
            return top.strip().upper(), bottom.strip().upper()

        print("Unexpected Gemini output:", text)
        return None, None

    except Exception as e:
        print("Gemini caption error:", e)
        return None, None


# ----------------------------------------------------
# 📌 DRAW TEXT ON IMAGE
# ----------------------------------------------------
def draw_meme(image: Image.Image, top: str, bottom: str):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    font_size = int(height * 0.1)

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except:
        print("Impact font missing. Using default.")
        font = ImageFont.load_default()
        font_size = 20

    stroke_width = max(2, int(font_size * 0.05))

    def draw_text(text, y):
        if not text:
            return
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) / 2

        draw.text(
            (x, y),
            text,
            fill="white",
            stroke_fill="black",
            stroke_width=stroke_width,
            font=font
        )

    draw_text(top, 10)

    if bottom:
        bbox = draw.textbbox((0, 0), bottom, font=font)
        text_h = bbox[3] - bbox[1]
        draw_text(bottom, height - text_h - 10)

    return image


# ----------------------------------------------------
# 📌 ENDPOINTS
# ----------------------------------------------------
@app.get("/")
def root():
    return FileResponse("index.html")


@app.post("/generate-meme")
def generate_meme(req: GenerateRequest):
    try:
        # 1 - Generate image
        img = generate_ai_image(req.prompt)

        # 2 - Get captions
        if req.top_text and req.bottom_text:
            top = req.top_text.upper()
            bottom = req.bottom_text.upper()
        else:
            top, bottom = generate_ai_caption(req.prompt)
            if not top:
                top = "AI FAILED"
                bottom = "TO GENERATE CAPTION"

        # 3 - Draw text
        final = draw_meme(img, top, bottom)

        # 4 - Save result
        os.makedirs("generated", exist_ok=True)
        filename = f"{uuid.uuid4().hex}.jpg"
        path = f"generated/{filename}"

        final.save(path)

        return {"image_url": f"/{path}"}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Meme generation failed.")
