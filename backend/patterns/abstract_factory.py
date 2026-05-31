from abc import ABC, abstractmethod
from pathlib import Path
import json


class RepositorioReservas(ABC):

    @abstractmethod
    def obtener_todas(self) -> dict:
        pass

    @abstractmethod
    def guardar(self, datos: dict) -> None:
        pass


class RepositorioReservasArchivo(RepositorioReservas):

    def __init__(self, ruta: Path):
        self._ruta = ruta

    def obtener_todas(self) -> dict:
        with open(self._ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar(self, datos: dict) -> None:
        with open(self._ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)


class RepositorioReservasMemoria(RepositorioReservas):

    def __init__(self):
        self._datos = {
            "Sala 101": {
                "08:00": "Libre"
            }
        }

    def obtener_todas(self) -> dict:
        return self._datos

    def guardar(self, datos: dict) -> None:
        self._datos = datos


class FabricaRepositorios(ABC):

    @abstractmethod
    def crear_repositorio_reservas(self) -> RepositorioReservas:
        pass


class FabricaArchivo(FabricaRepositorios):

    def __init__(self, ruta_reservas: Path):
        self._ruta_reservas = ruta_reservas

    def crear_repositorio_reservas(self) -> RepositorioReservas:
        return RepositorioReservasArchivo(self._ruta_reservas)


class FabricaMemoria(FabricaRepositorios):

    def crear_repositorio_reservas(self) -> RepositorioReservas:
        return RepositorioReservasMemoria()


def obtener_fabrica(entorno: str = "produccion") -> FabricaRepositorios:
    from core.config import RESERVAS_FILE

    if entorno == "produccion":
        return FabricaArchivo(RESERVAS_FILE)

    return FabricaMemoria()