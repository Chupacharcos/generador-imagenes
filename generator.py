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

# Estilos predefinidos — prefijos de prompt
STYLES = {
    "ninguno": {
        "label": "Sin estilo (prompt libre)",
        "prefix": "",
    },
    "card_tech": {
        "label": "Tech / Dark UI",
        "prefix": "Dark navy background, neon cyan accents, futuristic UI elements, tech aesthetic, clean digital composition, professional illustration, ",
    },
    "card_educacion": {
        "label": "Educación / Colorido",
        "prefix": "Colorful educational illustration, friendly cartoon characters, learning and technology, bright pastel colors, clean modern design, playful style, ",
    },
    "card_finanzas": {
        "label": "Finanzas / Wall St.",
        "prefix": "Financial data visualization, dark professional background, glowing charts and graphs, gold and blue accents, wall street aesthetic, dramatic lighting, ",
    },
    "card_ia": {
        "label": "IA / Neural",
        "prefix": "Artificial intelligence concept art, neural network visualization, glowing nodes and connections, dark background, purple and cyan gradient, abstract digital, ",
    },
    "card_api": {
        "label": "API / Backend",
        "prefix": "Connected systems concept, server infrastructure, code and data flow, dark terminal aesthetic, green matrix-style accents, clean technical illustration, ",
    },
    "card_naturaleza": {
        "label": "Naturaleza / Paisaje",
        "prefix": "Stunning natural landscape, vivid colors, dramatic lighting, photorealistic style, high detail, cinematic composition, ",
    },
    "card_retro": {
        "label": "Retro / Synthwave",
        "prefix": "Retro synthwave aesthetic, neon grid, sunset gradient, 80s vaporwave style, vivid pink and purple, detailed illustration, ",
    },
    "card_minimalista": {
        "label": "Minimalista",
        "prefix": "Minimalist clean illustration, simple shapes, limited color palette, white background, elegant modern design, geometric, ",
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
