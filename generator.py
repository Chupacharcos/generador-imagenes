import base64
import io
import os
import time

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", "")
MODEL = os.getenv("HF_MODEL", "black-forest-labs/FLUX.1-schnell")

# Estilos predefinidos — prefijos de prompt para card images
STYLES = {
    "ninguno": {
        "label": "Sin estilo (prompt libre)",
        "prefix": "",
    },
    "card_tech": {
        "label": "Card proyecto tech",
        "prefix": "Professional software project card image, dark navy background, neon cyan accents, futuristic UI elements, tech aesthetic, clean composition, ",
    },
    "card_educacion": {
        "label": "Card proyecto educación",
        "prefix": "Colorful educational illustration, friendly cartoon characters, children learning with technology, bright pastel colors, clean modern design, ",
    },
    "card_finanzas": {
        "label": "Card proyecto finanzas",
        "prefix": "Financial data visualization, dark professional background, glowing charts and graphs, gold and blue accents, wall street aesthetic, ",
    },
    "card_ia": {
        "label": "Card proyecto IA / ML",
        "prefix": "Artificial intelligence concept art, neural network visualization, glowing nodes and connections, dark background, purple and cyan gradient, ",
    },
    "card_api": {
        "label": "Card proyecto API",
        "prefix": "API integration concept, connected systems, code snippets, dark terminal aesthetic, green matrix-style accents, clean technical illustration, ",
    },
}


def get_client() -> InferenceClient:
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN no configurado en .env")
    return InferenceClient(provider="hf-inference", token=HF_TOKEN)


def generate_image(
    prompt: str,
    style: str = "ninguno",
    width: int = 1200,
    height: int = 900,
) -> dict:
    style_data = STYLES.get(style, STYLES["ninguno"])
    full_prompt = style_data["prefix"] + prompt

    client = get_client()

    t0 = time.time()
    image: Image.Image = client.text_to_image(
        full_prompt,
        model=MODEL,
        width=width,
        height=height,
    )
    elapsed = round(time.time() - t0, 2)

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "image_b64": b64,
        "prompt_used": full_prompt,
        "style": style,
        "width": width,
        "height": height,
        "elapsed_seconds": elapsed,
        "model": MODEL,
    }


def list_styles() -> list:
    return [
        {"id": k, "label": v["label"], "prefix": v["prefix"]}
        for k, v in STYLES.items()
    ]
