from abc import ABC, abstractmethod
from datetime import datetime


class ObservadorReserva(ABC):
    @abstractmethod
    def actualizar(self, evento: str, datos: dict) -> None:
        pass


class ObservadorNotificacion(ObservadorReserva):
    def actualizar(self, evento: str, datos: dict) -> None:
        usuario = datos.get("usuario", "")
        sala = datos.get("sala", "")
        hora = datos.get("hora", "")
        if evento == "reserva_creada":
            print(f"[NOTIF] Confirmacion enviada a {usuario}: {sala} a las {hora}")
        elif evento == "reserva_cancelada":
            print(f"[NOTIF] Cancelacion enviada a {usuario}: {sala} a las {hora}")


class ObservadorHistorial(ObservadorReserva):
    def __init__(self):
        self._registros = []

    def actualizar(self, evento: str, datos: dict) -> None:
        self._registros.append({
            "evento": evento,
            "fecha": datetime.now().isoformat(),
            "usuario": datos.get("usuario"),
            "sala": datos.get("sala"),
            "hora": datos.get("hora"),
        })
        print(f"[HISTORIAL] Evento registrado: {evento} | {datos.get('sala')} | {datos.get('hora')}")

    def obtener(self) -> list:
        return self._registros


class ObservadorEstadisticas(ObservadorReserva):
    def __init__(self):
        self._reservas = 0
        self._cancelaciones = 0

    def actualizar(self, evento: str, datos: dict) -> None:
        if evento == "reserva_creada":
            self._reservas += 1
        elif evento == "reserva_cancelada":
            self._cancelaciones += 1
        print(f"[STATS] Reservas: {self._reservas} | Cancelaciones: {self._cancelaciones}")


class GestorEventos:
    def __init__(self):
        self._observadores: list[ObservadorReserva] = []

    def suscribir(self, observador: ObservadorReserva) -> None:
        self._observadores.append(observador)

    def notificar(self, evento: str, datos: dict) -> None:
        for obs in self._observadores:
            obs.actualizar(evento, datos)

    def publicar_reserva_creada(self, usuario: str, sala: str, hora: str) -> None:
        self.notificar("reserva_creada", {"usuario": usuario, "sala": sala, "hora": hora})

    def publicar_reserva_cancelada(self, usuario: str, sala: str, hora: str) -> None:
        self.notificar("reserva_cancelada", {"usuario": usuario, "sala": sala, "hora": hora})


gestor_eventos = GestorEventos()
gestor_eventos.suscribir(ObservadorNotificacion())
gestor_eventos.suscribir(ObservadorHistorial())
gestor_eventos.suscribir(ObservadorEstadisticas())