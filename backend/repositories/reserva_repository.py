from datetime import date, time

from models.database_models import Reserva, Sala


class ReservaRepository:

    def __init__(self, db):
        self.db = db

    def obtener_salas_disponibles(self):
        return self.db.query(Sala).filter(
            Sala.estado == "Disponible"
        ).all()

    def obtener_sala_por_nombre(self, nombre_sala: str):
        return self.db.query(Sala).filter(
            Sala.nombre_sala == nombre_sala
        ).first()

    def obtener_reservas_activas(self):
        return self.db.query(Reserva).filter(
            Reserva.estado_reserva == "Activa"
        ).all()

    def obtener_reserva_activa(self, id_sala: int, hora: time):
        return self.db.query(Reserva).filter(
            Reserva.id_sala == id_sala,
            Reserva.hora == hora,
            Reserva.estado_reserva == "Activa"
        ).first()

    def crear_reserva(
        self,
        codigo_usuario: str,
        id_sala: int,
        hora: time
    ):
        reserva = Reserva(
            fecha=date.today(),
            hora=hora,
            estado_reserva="Activa",
            codigo_usuario=codigo_usuario,
            id_sala=id_sala
        )

        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)

        return reserva

    def cancelar_reserva(self, reserva: Reserva):
        reserva.estado_reserva = "Cancelada"

        self.db.commit()
        self.db.refresh(reserva)

        return reserva