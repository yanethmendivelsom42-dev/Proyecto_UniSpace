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
            return

        estructura_valida = True
        for sala in SALAS_BASE:
            if sala not in datos or not isinstance(datos[sala], dict):
                estructura_valida = False
                break
            for hora in HORAS:
                if hora not in datos[sala]:
                    estructura_valida = False
                    break

        if not estructura_valida:
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

    return {"ok": True, "mensaje": f"Tu reserva para {sala} a las {hora} se ha guardado correctamente."}


def cancelar_reserva_individual(usuario: str, sala: str, hora: str) -> dict:
    reservas = cargar_reservas()

    if sala not in reservas:
        return {"ok": False, "mensaje": "Sala no encontrada."}

    if hora not in reservas[sala]:
        return {"ok": False, "mensaje": "Hora no válida."}

    valor_actual = reservas[sala][hora]

    if valor_actual == "Libre":
        return {"ok": False, "mensaje": "Esa reserva ya se encuentra libre."}

    if valor_actual != usuario:
        return {"ok": False, "mensaje": "Solo puedes cancelar tus propias reservas."}

    reservas[sala][hora] = "Libre"
    guardar_reservas(reservas)

    return {"ok": True, "mensaje": f"La reserva de {sala} a las {hora} fue cancelada correctamente."}


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

    historial.sort(key=lambda item: (item["hora"], item["sala"]))
    return historial