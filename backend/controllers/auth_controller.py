from patterns.strategy import obtener_contexto_auth

_contexto = obtener_contexto_auth()


def validar_usuario(correo: str, contrasena: str) -> dict:
    correo = correo.strip()
    contrasena = contrasena.strip()

    if not correo or not contrasena:
        return {"ok": False, "mensaje": "Correo y contrasena son obligatorios."}

    return _contexto.autenticar(correo, contrasena)