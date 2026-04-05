import json

from core.config import RESERVAS_FILE, SALAS_BASE, HORAS


def _estructura_base() -> dict:
    return {
        sala: {hora: "Libre" for hora in HORAS}
        for sala in SALAS_BASE
    }


def inicializar_reservas() -> None:
    if not RESERVAS_FILE.exists() or RESERVAS_FILE.stat().st_size == 0:
        guardar_reservas(_estructura_base())
        return

    try:
        with open(RESERVAS_FILE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            guardar_reservas(_estructura_base())
    except (json.JSONDecodeError, OSError):
        guardar_reservas(_estructura_base())


def cargar_reservas() -> dict:
    inicializar_reservas()
    with open(RESERVAS_FILE, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_reservas(datos: dict) -> None:
    with open(RESERVAS_FILE, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def obtener_reservas_dashboard() -> dict:
    return cargar_reservas()


def reservar_sala(sala: str, hora: str, usuario: str) -> dict:
    reservas = cargar_reservas()

    if sala not in reservas:
        return {"ok": False, "mensaje": "Sala no encontrada."}

    if hora not in reservas[sala]:
        return {"ok": False, "mensaje": "Hora no válida."}

    if reservas[sala][hora] != "Libre":
        return {"ok": False, "mensaje": "La sala ya está reservada."}

    reservas[sala][hora] = usuario
    guardar_reservas(reservas)

    return {"ok": True, "mensaje": "Tu reserva se ha guardado correctamente."}


def cancelar_reservas_usuario(usuario: str) -> dict:
    reservas = cargar_reservas()
    cambios = 0

    for sala, horas in reservas.items():
        for hora, valor in horas.items():
            if valor == usuario:
                reservas[sala][hora] = "Libre"
                cambios += 1

    guardar_reservas(reservas)

    if cambios == 0:
        return {"ok": False, "mensaje": "No tienes reservas activas para cancelar."}

    return {"ok": True, "mensaje": "Tus reservas fueron canceladas correctamente."}


def construir_historial_usuario(reservas: dict, usuario: str) -> list[dict]:
    historial = []

    for sala, horas in reservas.items():
        for hora, valor in horas.items():
            if valor == usuario:
                historial.append({
                    "sala": sala,
                    "hora": hora,
                    "estado": "Activa"
                })

    historial.sort(key=lambda item: item["hora"])
    return historial