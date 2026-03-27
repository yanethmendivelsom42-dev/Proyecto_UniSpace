import json
from core.config import RESERVAS_FILE, SALAS_BASE, HORAS

def inicializar_reservas():
    if not RESERVAS_FILE.exists():
        datos = {sala: {hora: "Libre" for hora in HORAS} for sala in SALAS_BASE}
        guardar_reservas(datos)

def cargar_reservas():
    inicializar_reservas()
    with open(RESERVAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_reservas(datos):
    with open(RESERVAS_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def obtener_reservas_dashboard():
    return cargar_reservas()

def reservar_sala(sala: str, hora: str, usuario: str):
    reservas = cargar_reservas()

    if sala not in reservas:
        return {"ok": False, "mensaje": "Sala no encontrada"}

    if hora not in reservas[sala]:
        return {"ok": False, "mensaje": "Hora no válida"}

    if reservas[sala][hora] != "Libre":
        return {"ok": False, "mensaje": "La sala ya está reservada"}

    reservas[sala][hora] = usuario
    guardar_reservas(reservas)

    return {"ok": True, "mensaje": "Reserva realizada correctamente"}