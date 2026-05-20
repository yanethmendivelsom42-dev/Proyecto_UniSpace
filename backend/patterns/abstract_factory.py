from abc import ABC, abstractmethod
from pathlib import Path
import json


class RepositorioUsuarios(ABC):
    @abstractmethod
    def buscar(self, correo: str, contrasena: str) -> bool:
        pass


class RepositorioReservas(ABC):
    @abstractmethod
    def obtener_todas(self) -> dict:
        pass

    @abstractmethod
    def guardar(self, datos: dict) -> None:
        pass


class RepositorioUsuariosArchivo(RepositorioUsuarios):
    def __init__(self, ruta: Path):
        self._ruta = ruta

    def buscar(self, correo: str, contrasena: str) -> bool:
        if not self._ruta.exists():
            return False
        with open(self._ruta, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) >= 2 and partes[0].strip() == correo and partes[1].strip() == contrasena:
                    return True
        return False


class RepositorioReservasArchivo(RepositorioReservas):
    def __init__(self, ruta: Path):
        self._ruta = ruta

    def obtener_todas(self) -> dict:
        with open(self._ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def guardar(self, datos: dict) -> None:
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)


class RepositorioUsuariosMemoria(RepositorioUsuarios):
    def __init__(self):
        self._usuarios = [("test@ucatolica.edu.co", "1234")]

    def buscar(self, correo: str, contrasena: str) -> bool:
        return (correo, contrasena) in self._usuarios


class RepositorioReservasMemoria(RepositorioReservas):
    def __init__(self):
        self._datos = {"Sala 101": {"08:00": "Libre"}}

    def obtener_todas(self) -> dict:
        return self._datos

    def guardar(self, datos: dict) -> None:
        self._datos = datos


class FabricaRepositorios(ABC):
    @abstractmethod
    def crear_repositorio_usuarios(self) -> RepositorioUsuarios:
        pass

    @abstractmethod
    def crear_repositorio_reservas(self) -> RepositorioReservas:
        pass


class FabricaArchivo(FabricaRepositorios):
    def __init__(self, ruta_usuarios: Path, ruta_reservas: Path):
        self._ruta_usuarios = ruta_usuarios
        self._ruta_reservas = ruta_reservas

    def crear_repositorio_usuarios(self) -> RepositorioUsuarios:
        return RepositorioUsuariosArchivo(self._ruta_usuarios)

    def crear_repositorio_reservas(self) -> RepositorioReservas:
        return RepositorioReservasArchivo(self._ruta_reservas)


class FabricaMemoria(FabricaRepositorios):
    def crear_repositorio_usuarios(self) -> RepositorioUsuarios:
        return RepositorioUsuariosMemoria()

    def crear_repositorio_reservas(self) -> RepositorioReservas:
        return RepositorioReservasMemoria()


def obtener_fabrica(entorno: str = "produccion") -> FabricaRepositorios:
    from core.config import USUARIOS_FILE, RESERVAS_FILE
    if entorno == "produccion":
        return FabricaArchivo(USUARIOS_FILE, RESERVAS_FILE)
    return FabricaMemoria()