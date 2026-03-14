from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from generator import generate_image, list_styles

router = APIRouter(prefix="/generador")


class GenerateRequest(BaseModel):
    prompt: str = Field(default="a futuristic AI project", min_length=1)
    style: str = Field(default="ninguno")
    width: int = Field(default=1200, ge=256, le=1440)
    height: int = Field(default=900, ge=256, le=1024)


@router.get("/health")
def health():
    return {"status": "ok", "service": "generador-imagenes"}


@router.get("/styles")
def styles():
    return {"styles": list_styles()}


@router.post("/generate")
def generate(body: Optional[GenerateRequest] = None):
    req = body or GenerateRequest()
    try:
        result = generate_image(
            prompt=req.prompt,
            style=req.style,
            width=req.width,
            height=req.height,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando imagen: {str(e)}")
