from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from controllers.auth_controller import validar_usuario
from controllers.reserva_archivo_controller import obtener_reservas_dashboard, reservar_sala
from core.config import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, correo: str = Form(...), contrasena: str = Form(...)):
    validar_usuario(correo, contrasena)
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    reservas = obtener_reservas_dashboard()
    return templates.TemplateResponse("dashboard.html", {"request": request, "reservas": reservas})

@router.post("/reservar")
def reservar(request: Request, sala: str = Form(...), hora: str = Form(...), usuario: str = Form(...)):
    resultado = reservar_sala(sala, hora, usuario)
    if resultado["ok"]:
        return RedirectResponse(url="/dashboard", status_code=303)
    return {"mensaje": resultado["mensaje"]}