from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), nullable=False)


class Usuario(Base):
    __tablename__ = "usuario"

    codigo_usuario = Column(String(20), primary_key=True, index=True)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    estado = Column(String(20), default="Activo")


class Sala(Base):
    __tablename__ = "sala"

    id_sala = Column(Integer, primary_key=True, index=True)
    nombre_sala = Column(String(50), nullable=False)
    ubicacion = Column(String(100))
    capacidad = Column(Integer)
    estado = Column(String(20), default="Disponible")


class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    estado_reserva = Column(String(20), default="Activa")
    codigo_usuario = Column(String(20), ForeignKey("usuario.codigo_usuario"), nullable=False)
    id_sala = Column(Integer, ForeignKey("sala.id_sala"), nullable=False)


class Historial(Base):
    __tablename__ = "historial"

    id_historial = Column(Integer, primary_key=True, index=True)
    codigo_usuario = Column(String(20), ForeignKey("usuario.codigo_usuario"), nullable=False)
    id_reserva = Column(Integer, ForeignKey("reserva.id_reserva"), nullable=False)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())
    estado = Column(String(20))
    detalle = Column(Text)