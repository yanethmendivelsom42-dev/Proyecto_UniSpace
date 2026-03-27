from fastapi import HTTPException
from core.config import USUARIOS_FILE

def validar_usuario(correo: str, contrasena: str):
    if not correo or not contrasena:
        raise HTTPException(status_code=400, detail="Correo y contraseña son obligatorios")

    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            usuarios = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

    for usuario in usuarios:
        if len(usuario) >= 2 and usuario[0] == correo and usuario[1] == contrasena:
            return {"correo": correo}

    raise HTTPException(status_code=401, detail="Credenciales inválidas")