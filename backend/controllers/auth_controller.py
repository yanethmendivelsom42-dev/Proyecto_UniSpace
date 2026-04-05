from core.config import USUARIOS_FILE


def validar_usuario(correo: str, contrasena: str) -> dict:
    correo = correo.strip()
    contrasena = contrasena.strip()

    if not correo or not contrasena:
        return {
            "ok": False,
            "mensaje": "Correo y contraseña son obligatorios."
        }

    if not USUARIOS_FILE.exists():
        return {
            "ok": False,
            "mensaje": "No se encontró el archivo de usuarios."
        }

    with open(USUARIOS_FILE, "r", encoding="utf-8") as archivo:
        usuarios = [line.strip().split(",") for line in archivo if line.strip()]

    for usuario in usuarios:
        if len(usuario) >= 2 and usuario[0].strip() == correo and usuario[1].strip() == contrasena:
            return {
                "ok": True,
                "correo": correo
            }

    return {
        "ok": False,
        "mensaje": "Credenciales inválidas."
    }