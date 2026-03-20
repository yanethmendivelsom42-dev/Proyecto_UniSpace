from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
import json

app = FastAPI(title="UniSpace API")

BASE_DIR = Path(__file__).parent
RUTA_USUARIOS = BASE_DIR / "usuarios.txt"
RUTA_RESERVAS = BASE_DIR / "reservas.json"
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

HORAS = ["08:00", "09:00", "10:00", "11:00", "12:00"]
SALAS_BASE = ["Sala 101", "Sala 102", "Sala 201"]
class Reserva(BaseModel):
    id: int
    usuario: str
    sala: str
    activa: bool
    valor: float
reservas_api_db = []


def cargar_usuarios():
    usuarios = {}

    if not RUTA_USUARIOS.exists():
        return usuarios

    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            partes = linea.split(":")

            if len(partes) != 2:
                continue

            correo = partes[0].strip()
            clave = partes[1].strip()

            usuarios[correo] = clave

    return usuarios


def crear_reservas_iniciales():
    reservas = []

    for sala in SALAS_BASE:
        item = {"sala": sala}
        for hora in HORAS:
            item[hora] = "Libre"
        reservas.append(item)

    with open(RUTA_RESERVAS, "w", encoding="utf-8") as archivo:
        json.dump(reservas, archivo, ensure_ascii=False, indent=4)


def cargar_reservas():
    if not RUTA_RESERVAS.exists():
        crear_reservas_iniciales()

    with open(RUTA_RESERVAS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_reservas(reservas):
    with open(RUTA_RESERVAS, "w", encoding="utf-8") as archivo:
        json.dump(reservas, archivo, ensure_ascii=False, indent=4)


@app.get("/", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "mensaje": ""
        }
    )


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, usuario: str = Form(...), contrasena: str = Form(...)):
    usuarios = cargar_usuarios()

    if usuario in usuarios and usuarios[usuario] == contrasena:
        return RedirectResponse(url=f"/dashboard?usuario={usuario}", status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "mensaje": "Usuario o contraseña incorrectos"
        }
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, usuario: str = "", mensaje: str = ""):
    salas = cargar_reservas()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "salas": salas,
            "horas": HORAS,
            "mensaje": mensaje
        }
    )


@app.post("/reservar", response_class=HTMLResponse)
def reservar(
    request: Request,
    usuario: str = Form(...),
    sala: str = Form(...),
    hora: str = Form(...)
):
    reservas = cargar_reservas()
    mensaje = ""

    for item in reservas:
        if item["sala"] == sala:
            if item.get(hora) == "Libre":
                item[hora] = f"Ocupado por {usuario}"
                mensaje = f"Reserva realizada en {sala} a las {hora}"
            else:
                mensaje = f"La {sala} a las {hora} ya está ocupada"
            break

    guardar_reservas(reservas)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "salas": reservas,
            "horas": HORAS,
            "mensaje": mensaje
        }
    )


@app.post("/cancelar", response_class=HTMLResponse)
def cancelar(
    request: Request,
    usuario: str = Form(...),
    sala: str = Form(...),
    hora: str = Form(...)
):
    reservas = cargar_reservas()
    mensaje = ""

    for item in reservas:
        if item["sala"] == sala:
            if item.get(hora) != "Libre":
                item[hora] = "Libre"
                mensaje = f"Reserva cancelada en {sala} a las {hora}"
            else:
                mensaje = f"La {sala} a las {hora} ya estaba libre"
            break

    guardar_reservas(reservas)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "salas": reservas,
            "horas": HORAS,
            "mensaje": mensaje
        }
    )


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/reservas")
def obtener_reservas():
    return reservas_api_db


@app.post("/api/reservas")
def crear_reserva(reserva: Reserva):
    for item in reservas_api_db:
        if item["id"] == reserva.id:
            raise HTTPException(status_code=400, detail="Ya existe una reserva con ese ID")

    nueva_reserva = reserva.dict()
    reservas_api_db.append(nueva_reserva)

    return {
        "mensaje": "Reserva creada correctamente",
        "reserva": nueva_reserva
    }


@app.get("/api/reservas/{reserva_id}")
def obtener_reserva_por_id(reserva_id: int):
    for reserva in reservas_api_db:
        if reserva["id"] == reserva_id:
            return reserva

    raise HTTPException(status_code=404, detail="Reserva no encontrada")


@app.get("/api/reservas/filtro/")
def filtrar_reservas(
    usuario: Optional[str] = Query(default=None),
    sala: Optional[str] = Query(default=None),
    activa: Optional[bool] = Query(default=None)
):
    resultados = reservas_api_db

    if usuario is not None:
        resultados = [r for r in resultados if r["usuario"].lower() == usuario.lower()]

    if sala is not None:
        resultados = [r for r in resultados if r["sala"].lower() == sala.lower()]

    if activa is not None:
        resultados = [r for r in resultados if r["activa"] == activa]

    return resultados