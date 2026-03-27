from fastapi import APIRouter
from models.reserva import Reserva
from controllers.reserva_api_controller import (
    obtener_reservas,
    obtener_reserva_por_id,
    crear_reserva,
    filtrar_reservas_por_estado,
)

router = APIRouter(prefix="/api/reservas", tags=["Reservas API"])

@router.get("/")
def listar_reservas():
    return obtener_reservas()

@router.get("/{reserva_id}")
def buscar_reserva(reserva_id: int):
    return obtener_reserva_por_id(reserva_id)

@router.post("/")
def agregar_reserva(reserva: Reserva):
    return crear_reserva(reserva)

@router.get("/estado/{activa}")
def reservas_por_estado(activa: bool):
    return filtrar_reservas_por_estado(activa)