from database import SessionLocal
from models.database_models import Sala, Reserva


def obtener_salas_db():
    db = SessionLocal()
    try:
        salas = db.query(Sala).all()

        resultado = []
        for sala in salas:
            resultado.append({
                "id_sala": sala.id_sala,
                "nombre_sala": sala.nombre_sala,
                "ubicacion": sala.ubicacion,
                "capacidad": sala.capacidad,
                "estado": sala.estado
            })

        return resultado
    finally:
        db.close()


def obtener_reservas_db():
    db = SessionLocal()
    try:
        reservas = db.query(Reserva).all()

        resultado = []
        for reserva in reservas:
            resultado.append({
                "id_reserva": reserva.id_reserva,
                "fecha": str(reserva.fecha),
                "hora": str(reserva.hora),
                "estado_reserva": reserva.estado_reserva,
                "codigo_usuario": reserva.codigo_usuario,
                "id_sala": reserva.id_sala
            })

        return resultado
    finally:
        db.close()