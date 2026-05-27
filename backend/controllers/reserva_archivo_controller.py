import json

from core.config import RESERVAS_FILE, SALAS_BASE, HORAS
from patterns.abstract_factory import obtener_fabrica
from patterns.decorator import construir_servicio_reservas

_fabrica = obtener_fabrica("produccion")
_repo_reservas = _fabrica.crear_repositorio_reservas()
_servicio = construir_servicio_reservas(_repo_reservas)


def _estructura_base() -> dict:
    return {sala: {hora: "Libre" for hora in HORAS} for sala in SALAS_BASE}


def inicializar_reservas() -> None:
    if not RESERVAS_FILE.exists() or RESERVAS_FILE.stat().st_size == 0:
        _repo_reservas.guardar(_estructura_base())
        return
    try:
        datos = _repo_reservas.obtener_todas()
        if not isinstance(datos, dict):
            _repo_reservas.guardar(_estructura_base())
            return
        for sala in SALAS_BASE:
            if sala not in datos:
                _repo_reservas.guardar(_estructura_base())
                return
    except Exception:
        _repo_reservas.guardar(_estructura_base())


def obtener_reservas_dashboard() -> dict:
    inicializar_reservas()
    return _repo_reservas.obtener_todas()


def reservar_sala(sala: str, hora: str, usuario: str) -> dict:
    inicializar_reservas()
    return _servicio.reservar(sala, hora, usuario)


def cancelar_reserva_individual(usuario: str, sala: str, hora: str) -> dict:
    inicializar_reservas()
    return _servicio.cancelar(sala, hora, usuario)


def construir_historial_usuario(reservas: dict, usuario: str) -> list[dict]:
    historial = []
    for sala, horas in reservas.items():
        for hora, valor in horas.items():
            if valor == usuario:
                historial.append({"sala": sala, "hora": hora, "estado": "Activa"})
    historial.sort(key=lambda item: (item["hora"], item["sala"]))
    return historial    