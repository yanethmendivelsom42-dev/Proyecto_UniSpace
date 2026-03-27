from pydantic import BaseModel

class Reserva(BaseModel):
    id: int
    usuario: str
    sala: str
    activa: bool
    valor: float