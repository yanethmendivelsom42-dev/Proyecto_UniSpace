from abc import ABC, abstractmethod


class FabricaRepositorios(ABC):

    @abstractmethod
    def crear_repositorio_reservas(self):
        pass


class FabricaPostgreSQL(FabricaRepositorios):

    def __init__(self, db):
        self.db = db

    def crear_repositorio_reservas(self):
        from repositories.reserva_repository import ReservaRepository

        return ReservaRepository(self.db)