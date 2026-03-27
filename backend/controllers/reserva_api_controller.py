from fastapi import HTTPException
from models.reserva import Reserva

reservas_db = [
    Reserva(id=1, usuario="ana@ucatolica.edu.co", sala="Sala 101", activa=True, valor=15000),
    Reserva(id=2, usuario="juan@ucatolica.edu.co", sala="Sala 102", activa=False, valor=12000),
]

def obtener_reservas():
    return reservas_db

def obtener_reserva_por_id(reserva_id: int):
    for reserva in reservas_db:
        if reserva.id == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

def crear_reserva(reserva: Reserva):
    reservas_db.append(reserva)
    return reserva

def filtrar_reservas_por_estado(activa: bool):
    return [r for r in reservas_db if r.activa == activa]