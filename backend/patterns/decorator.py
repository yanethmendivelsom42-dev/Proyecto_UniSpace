from abc import ABC, abstractmethod
from datetime import datetime


class ServicioReservas(ABC):
    @abstractmethod
    def reservar(self, sala: str, hora: str, usuario: str) -> dict:
        pass

    @abstractmethod
    def cancelar(self, sala: str, hora: str, usuario: str) -> dict:
        pass


class ServicioReservasBase(ServicioReservas):
    def __init__(self, repositorio):
        self._repo = repositorio

    def reservar(self, sala: str, hora: str, usuario: str) -> dict:
        datos = self._repo.obtener_todas()
        if sala not in datos:
            return {"ok": False, "mensaje": "Sala no encontrada."}
        if hora not in datos[sala]:
            return {"ok": False, "mensaje": "Hora no valida."}
        if datos[sala][hora] != "Libre":
            return {"ok": False, "mensaje": "La sala ya esta reservada."}
        datos[sala][hora] = usuario
        self._repo.guardar(datos)
        return {"ok": True, "mensaje": f"Tu reserva para {sala} a las {hora} se ha guardado correctamente."}

    def cancelar(self, sala: str, hora: str, usuario: str) -> dict:
        datos = self._repo.obtener_todas()
        if sala not in datos:
            return {"ok": False, "mensaje": "Sala no encontrada."}
        if hora not in datos[sala]:
            return {"ok": False, "mensaje": "Hora no valida."}
        valor = datos[sala][hora]
        if valor == "Libre":
            return {"ok": False, "mensaje": "Esa reserva ya se encuentra libre."}
        if valor != usuario:
            return {"ok": False, "mensaje": "Solo puedes cancelar tus propias reservas."}
        datos[sala][hora] = "Libre"
        self._repo.guardar(datos)
        return {"ok": True, "mensaje": f"La reserva de {sala} a las {hora} fue cancelada correctamente."}


class DecoradorReservas(ServicioReservas):
    def __init__(self, servicio: ServicioReservas):
        self._servicio = servicio

    def reservar(self, sala: str, hora: str, usuario: str) -> dict:
        return self._servicio.reservar(sala, hora, usuario)

    def cancelar(self, sala: str, hora: str, usuario: str) -> dict:
        return self._servicio.cancelar(sala, hora, usuario)


class DecoradorValidacion(DecoradorReservas):
    HORAS_VALIDAS = {"08:00", "09:00", "10:00", "11:00", "12:00"}
    SALAS_VALIDAS = {"Sala 101", "Sala 102", "Sala 201"}

    def reservar(self, sala: str, hora: str, usuario: str) -> dict:
        if not usuario or "@" not in usuario:
            return {"ok": False, "mensaje": "El correo del usuario no es valido."}
        if sala not in self.SALAS_VALIDAS:
            return {"ok": False, "mensaje": f"La sala '{sala}' no existe."}
        if hora not in self.HORAS_VALIDAS:
            return {"ok": False, "mensaje": f"El horario '{hora}' no esta disponible."}
        return super().reservar(sala, hora, usuario)

    def cancelar(self, sala: str, hora: str, usuario: str) -> dict:
        if not usuario or "@" not in usuario:
            return {"ok": False, "mensaje": "El correo del usuario no es valido."}
        return super().cancelar(sala, hora, usuario)


class DecoradorLog(DecoradorReservas):
    def reservar(self, sala: str, hora: str, usuario: str) -> dict:
        print(f"[LOG {datetime.now()}] RESERVAR | {usuario} | {sala} | {hora}")
        resultado = super().reservar(sala, hora, usuario)
        print(f"[LOG] Resultado: {resultado}")
        return resultado

    def cancelar(self, sala: str, hora: str, usuario: str) -> dict:
        print(f"[LOG {datetime.now()}] CANCELAR | {usuario} | {sala} | {hora}")
        resultado = super().cancelar(sala, hora, usuario)
        print(f"[LOG] Resultado: {resultado}")
        return resultado


def construir_servicio_reservas(repositorio) -> ServicioReservas:
    base = ServicioReservasBase(repositorio)
    con_validacion = DecoradorValidacion(base)
    con_log = DecoradorLog(con_validacion)
    return con_log