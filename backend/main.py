from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="UniSpace API")

BASE_DIR = Path(__file__).parent
RUTA_USUARIOS = BASE_DIR / "usuarios.txt"
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def cargar_usuarios():
    usuarios = {}

    if not RUTA_USUARIOS.exists():
        return usuarios

    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            partes = linea.split(":")

            if len(partes) != 2:
                continue

            correo = partes[0].strip()
            clave = partes[1].strip()

            usuarios[correo] = clave

    return usuarios


@app.get("/", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "mensaje": ""
        }
    )


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, usuario: str = Form(...), contrasena: str = Form(...)):
    usuarios = cargar_usuarios()

    if usuario in usuarios and usuarios[usuario] == contrasena:
        mensaje = f"Bienvenido, {usuario}"
    else:
        mensaje = "Usuario o contraseña incorrectos"

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "mensaje": mensaje
        }
    )


@app.get("/health")
def health():
    return {"status": "ok"}