from database import SessionLocal
from services.reserva_service import ReservaService


def obtener_reservas_dashboard() -> dict:
    db = SessionLocal()

    try:
        servicio = ReservaService(db)
        return servicio.obtener_reservas_dashboard()

    finally:
        db.close()


def reservar_sala(
    sala: str,
    hora: str,
    usuario: str
) -> dict:
    db = SessionLocal()

    try:
        servicio = ReservaService(db)

        codigo_usuario = _obtener_codigo_usuario_por_correo(
            db,
            usuario
        )

        if not codigo_usuario:
            return {
                "ok": False,
                "mensaje": "Usuario no encontrado en la base de datos."
            }

        return servicio.reservar_sala(
            sala,
            hora,
            codigo_usuario
        )

    finally:
        db.close()


def cancelar_reserva_individual(
    usuario: str,
    sala: str,
    hora: str
) -> dict:
    db = SessionLocal()

    try:
        servicio = ReservaService(db)

        return servicio.cancelar_reserva_individual(
            usuario,
            sala,
            hora
        )

    finally:
        db.close()


def construir_historial_usuario(
    reservas: dict,
    usuario: str
) -> list[dict]:
    db = SessionLocal()

    try:
        servicio = ReservaService(db)

        historial = servicio.construir_historial_usuario(
            reservas,
            usuario
        )

        historial.sort(
            key=lambda item: (
                item["hora"],
                item["sala"]
            )
        )

        return historial

    finally:
        db.close()


def _obtener_codigo_usuario_por_correo(
    db,
    correo: str
) -> str | None:
    from models.database_models import Usuario

    usuario = db.query(Usuario).filter(
        Usuario.correo == correo
    ).first()

    if not usuario:
        return None

    return usuario.codigo_usuario