from abc import ABC, abstractmethod
from pathlib import Path


class EstrategiaAutenticacion(ABC):
    @abstractmethod
    def autenticar(self, correo: str, contrasena: str) -> dict:
        pass


class AutenticacionArchivo(EstrategiaAutenticacion):
    def __init__(self, ruta: Path):
        self._ruta = ruta

    def autenticar(self, correo: str, contrasena: str) -> dict:
        if not self._ruta.exists():
            return {"ok": False, "mensaje": "Archivo de usuarios no encontrado."}
        with open(self._ruta, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) >= 2 and partes[0].strip() == correo and partes[1].strip() == contrasena:
                    return {"ok": True, "correo": correo}
        return {"ok": False, "mensaje": "Credenciales invalidas."}


class AutenticacionBaseDatos(EstrategiaAutenticacion):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def autenticar(self, correo: str, contrasena: str) -> dict:
        from models.database_models import Usuario
        db = self._session_factory()
        try:
            usuario = db.query(Usuario).filter(
                Usuario.correo == correo,
                Usuario.contrasena == contrasena,
                Usuario.estado == "Activo"
            ).first()
            if usuario:
                return {"ok": True, "correo": correo}
            return {"ok": False, "mensaje": "Credenciales invalidas."}
        finally:
            db.close()


class ContextoAutenticacion:
    def __init__(self, estrategia: EstrategiaAutenticacion):
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaAutenticacion) -> None:
        self._estrategia = estrategia

    def autenticar(self, correo: str, contrasena: str) -> dict:
        return self._estrategia.autenticar(correo, contrasena)


def obtener_contexto_auth() -> ContextoAutenticacion:
    from core.config import USUARIOS_FILE
    return ContextoAutenticacion(AutenticacionArchivo(USUARIOS_FILE))