from abc import ABC, abstractmethod


class ServicioNotificacion(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        pass


class NotificacionConsola(ServicioNotificacion):
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        print(f"[NOTIFICACION] Para: {destinatario} | {asunto} | {cuerpo}")
        return True


class SendGridClienteexterno:
    def send_email(self, to: str, subject: str, html: str) -> dict:
        print(f"[SendGrid] Enviando a {to}: {subject}")
        return {"status": "sent"}


class AdaptadorSendGrid(ServicioNotificacion):
    def __init__(self):
        self._cliente = SendGridClienteexterno()

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        resultado = self._cliente.send_email(
            to=destinatario,
            subject=asunto,
            html=f"<p>{cuerpo}</p>"
        )
        return resultado.get("status") == "sent"


class GestorNotificaciones:
    def __init__(self, servicio: ServicioNotificacion):
        self._servicio = servicio

    def notificar_reserva(self, correo: str, sala: str, hora: str) -> None:
        self._servicio.enviar(
            correo,
            "Confirmacion de reserva - UniSpace",
            f"Tu reserva en {sala} a las {hora} fue registrada."
        )

    def notificar_cancelacion(self, correo: str, sala: str, hora: str) -> None:
        self._servicio.enviar(
            correo,
            "Cancelacion de reserva - UniSpace",
            f"Tu reserva en {sala} a las {hora} fue cancelada."
        )


gestor_notificaciones = GestorNotificaciones(NotificacionConsola())