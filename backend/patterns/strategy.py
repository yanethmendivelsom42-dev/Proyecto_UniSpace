from abc import ABC, abstractmethod

from database import SessionLocal
from services.auth_service import AuthService


class EstrategiaAutenticacion(ABC):

    @abstractmethod
    def autenticar(self, correo: str, contrasena: str):
        pass


class AutenticacionBaseDatos(EstrategiaAutenticacion):

    def autenticar(self, correo: str, contrasena: str):

        db = SessionLocal()

        try:
            auth_service = AuthService(db)
            return auth_service.autenticar(correo, contrasena)

        finally:
            db.close()


class ContextoAutenticacion:

    def __init__(self, estrategia: EstrategiaAutenticacion):
        self.estrategia = estrategia

    def autenticar(self, correo: str, contrasena: str):
        return self.estrategia.autenticar(correo, contrasena)


def obtener_contexto_auth():

    return ContextoAutenticacion(
        AutenticacionBaseDatos()
    )