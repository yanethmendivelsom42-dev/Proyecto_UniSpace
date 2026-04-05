import json
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuración de carpetas
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

JSON_FILE = "reservas.json"

# Función para asegurar que el JSON exista y no esté vacío
def inicializar_json():
    if not os.path.exists(JSON_FILE) or os.stat(JSON_FILE).st_size == 0:
        with open(JSON_FILE, "w") as f:
            json.dump([], f)

def obtener_reservas():
    inicializar_json()
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def guardar_reserva_json(nueva):
    reservas = obtener_reservas()
    reservas.append(nueva)
    with open(JSON_FILE, "w") as f:
        json.dump(reservas, f, indent=4)

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request, mensaje: str = None):
    reservas = obtener_reservas()
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "reservas": reservas,
        "mensaje": mensaje
    })

@app.post("/reservar")
async def crear_reserva(sala: str = Form(...), hora: str = Form(...)):
    # Guardamos en el archivo
    guardar_reserva_json({"sala": sala, "hora": hora, "estado": "Activa"})
    # Redirigimos con un mensaje de éxito
    return RedirectResponse(url="/dashboard?mensaje=Reserva+exitosa", status_code=303)

@app.post("/cancelar")
async def cancelar_todas():
    # Limpiamos el JSON (Para el botón de cancelar)
    with open(JSON_FILE, "w") as f:
        json.dump([], f)
    return RedirectResponse(url="/dashboard", status_code=303)
