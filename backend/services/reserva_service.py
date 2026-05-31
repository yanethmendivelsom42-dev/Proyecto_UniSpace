from datetime import datetime

from core.config import HORAS

from repositories.reserva_repository import ReservaRepository


class ReservaService:

    def __init__(self, db):
        self.reserva_repository = ReservaRepository(db)

    def obtener_reservas_dashboard(self):

        salas = self.reserva_repository.obtener_salas_disponibles()

        reservas_activas = (
            self.reserva_repository.obtener_reservas_activas()
        )

        dashboard = {}

        for sala in salas:

            dashboard[sala.nombre_sala] = {
                hora: "Libre"
                for hora in HORAS
            }

        for reserva in reservas_activas:

            hora_texto = reserva.hora.strftime("%I:%M %p")

            dashboard[
                reserva.sala.nombre_sala
            ][hora_texto] = reserva.usuario.correo

        return dashboard

    def reservar_sala(
        self,
        nombre_sala: str,
        hora_texto: str,
        codigo_usuario: str
    ):

        sala = self.reserva_repository.obtener_sala_por_nombre(
            nombre_sala
        )

        if not sala:
            return {
                "ok": False,
                "mensaje": "La sala no existe."
            }

        hora = datetime.strptime(
            hora_texto,
            "%I:%M %p"
        ).time()

        reserva_existente = (
            self.reserva_repository.obtener_reserva_activa(
                sala.id_sala,
                hora
            )
        )

        if reserva_existente:
            return {
                "ok": False,
                "mensaje": "La sala ya está reservada en ese horario."
            }

        self.reserva_repository.crear_reserva(
            codigo_usuario,
            sala.id_sala,
            hora
        )

        return {
            "ok": True,
            "mensaje": "Reserva creada correctamente."
        }

    def cancelar_reserva_individual(
        self,
        correo_usuario: str,
        nombre_sala: str,
        hora_texto: str
    ):

        sala = self.reserva_repository.obtener_sala_por_nombre(
            nombre_sala
        )

        if not sala:
            return {
                "ok": False,
                "mensaje": "La sala no existe."
            }

        hora = datetime.strptime(
            hora_texto,
            "%I:%M %p"
        ).time()

        reserva = (
            self.reserva_repository.obtener_reserva_activa(
                sala.id_sala,
                hora
            )
        )

        if not reserva:
            return {
                "ok": False,
                "mensaje": "No existe una reserva activa para cancelar."
            }

        if reserva.usuario.correo != correo_usuario:
            return {
                "ok": False,
                "mensaje": "Solo puedes cancelar tus propias reservas."
            }

        self.reserva_repository.cancelar_reserva(
            reserva
        )

        return {
            "ok": True,
            "mensaje": "Reserva cancelada correctamente."
        }

    def construir_historial_usuario(
        self,
        reservas: dict,
        usuario: str
    ):

        historial = []

        for sala, horas in reservas.items():

            for hora, correo in horas.items():

                if correo == usuario:

                    historial.append(
                        {
                            "sala": sala,
                            "hora": hora,
                            "estado": "Activa"
                        }
                    )

        return historial