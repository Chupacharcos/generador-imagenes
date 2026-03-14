# Generador de Imágenes IA

Servicio FastAPI que genera imágenes de alta calidad a partir de texto mediante **FLUX.1-schnell** (Black Forest Labs) a través de la Inference API de HuggingFace. Incluye estilos predefinidos optimizados para card images de proyectos.

## Demo en vivo

[adrianmoreno-dev.com/demo/generador-imagenes](https://adrianmoreno-dev.com/demo/generador-imagenes)

## Características

- Prompt libre en lenguaje natural
- **6 estilos predefinidos** con prefijos de prompt optimizados:
  - `ninguno` — prompt libre
  - `card_tech` — proyecto tech (dark, neon, futurista)
  - `card_educacion` — educación (colorido, cartoon, amigable)
  - `card_finanzas` — finanzas (charts, profesional, dark)
  - `card_ia` — IA / ML (redes neuronales, nodos, gradiente)
  - `card_api` — API / backend (código, terminal, conexiones)
- Dimensiones personalizables: 256–1440 × 256–1024 px
- Respuesta en base64 (PNG) con tiempo de generación y prompt completo

## Endpoints

```
POST /generador/generate    Genera imagen desde texto
GET  /generador/styles      Lista estilos disponibles con prefijos
GET  /generador/health
```

### POST /generador/generate

```json
// Request
{
  "prompt": "robot chef en cocina futurista, colores vibrantes",
  "style": "card_ia",
  "width": 1200,
  "height": 900
}

// Response
{
  "image_b64": "iVBOR...",
  "prompt_used": "Artificial intelligence concept art... robot chef en cocina...",
  "style": "card_ia",
  "width": 1200,
  "height": 900,
  "elapsed_seconds": 8.3,
  "model": "black-forest-labs/FLUX.1-schnell"
}
```

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Modelo | FLUX.1-schnell (Black Forest Labs) |
| Inferencia | HuggingFace Inference API (serverless) |
| API | FastAPI + Uvicorn |
| Imágenes | Pillow (PIL) |
| Frontend | Laravel + Blade |

## Instalación

```bash
# Requiere el venv compartido con huggingface_hub instalado
pip install fastapi uvicorn huggingface_hub pillow python-dotenv

# Variables de entorno
cp .env.example .env
# HF_TOKEN=hf_xxxxx   ← token de huggingface.co/settings/tokens
# HF_MODEL=black-forest-labs/FLUX.1-schnell

# Desarrollo
uvicorn api:app --host 127.0.0.1 --port 8098 --reload

# Producción (systemd)
sudo systemctl start generador-imagenes
```

## Servicio systemd

```ini
[Unit]
Description=Generador de Imágenes IA (FastAPI - puerto 8098)
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/generador-imagenes
ExecStart=/var/www/chatbot/venv/bin/uvicorn api:app --host 127.0.0.1 --port 8098
Restart=on-failure
```

## HuggingFace token

1. Crear cuenta en [huggingface.co](https://huggingface.co)
2. Ir a **Settings → Access Tokens → New token** (tipo Read)
3. Añadir al `.env`: `HF_TOKEN=hf_tu_token`
4. `sudo systemctl restart generador-imagenes`
