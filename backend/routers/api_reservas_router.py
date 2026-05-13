from fastapi import APIRouter

from controllers.reserva_api_controller import (
    crear_reserva,
    filtrar_reservas_por_estado,
    obtener_reserva_por_id,
    obtener_reservas,
)

from controllers.reserva_db_controller import (
    obtener_salas_db,
    obtener_reservas_db,
)

from models.reserva import Reserva

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


# =========================
# RUTAS POSTGRESQL - NEON
# =========================

@router.get("/db/salas")
def listar_salas_db():
    return obtener_salas_db()


@router.get("/db/reservas")
def listar_reservas_db():
    return obtener_reservas_db()