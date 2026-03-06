from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="UniSpace API")

RUTA_USUARIOS = Path(__file__).parent / "usuarios.txt"


class LoginRequest(BaseModel):
    usuario: str
    contrasena: str


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


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a UniSpace API",
        "descripcion": "API funcionando correctamente en Azure"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/usuarios")
def listar_usuarios():
    usuarios = cargar_usuarios()
    return {
        "total_usuarios": len(usuarios),
        "usuarios": list(usuarios.keys())
    }


@app.post("/login")
def login(datos: LoginRequest):
    usuarios = cargar_usuarios()

    if datos.usuario in usuarios and usuarios[datos.usuario] == datos.contrasena:
        return {
            "mensaje": "Inicio de sesión exitoso",
            "usuario": datos.usuario
        }

    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
