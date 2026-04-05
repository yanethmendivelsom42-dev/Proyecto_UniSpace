from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from controllers.auth_controller import validar_usuario
from controllers.reserva_archivo_controller import (
    cancelar_reserva_individual,
    construir_historial_usuario,
    obtener_reservas_dashboard,
    reservar_sala,
)
from core.config import HORAS, SALAS_BASE, templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def mostrar_login(request: Request, mensaje: str = ""):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "mensaje": mensaje
        }
    )


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    correo: str = Form(...),
    contrasena: str = Form(...)
):
    resultado = validar_usuario(correo, contrasena)

    if not resultado["ok"]:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "mensaje": resultado["mensaje"]
            },
            status_code=401
        )

    return RedirectResponse(url=f"/dashboard?usuario={correo}", status_code=303)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, usuario: str = "", mensaje: str = ""):
    reservas = obtener_reservas_dashboard()
    historial_reciente = construir_historial_usuario(reservas, usuario)

    total_salas = len(SALAS_BASE)
    total_slots = len(SALAS_BASE) * len(HORAS)

    ocupados = 0
    libres = 0
    mis_reservas = 0

    for sala in SALAS_BASE:
        for hora in HORAS:
            valor = reservas.get(sala, {}).get(hora, "Libre")
            if valor == "Libre":
                libres += 1
            else:
                ocupados += 1
                if valor == usuario:
                    mis_reservas += 1

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "reservas": reservas,
            "salas": SALAS_BASE,
            "horas": HORAS,
            "usuario": usuario,
            "mensaje": mensaje,
            "historial_reciente": historial_reciente,
            "total_salas": total_salas,
            "horarios_libres": libres,
            "horarios_ocupados": ocupados,
            "mis_reservas": mis_reservas,
            "total_slots": total_slots,
        }
    )


@router.post("/reservar")
def reservar(
    sala: str = Form(...),
    hora: str = Form(...),
    usuario: str = Form(...)
):
    resultado = reservar_sala(sala, hora, usuario)

    return RedirectResponse(
        url=f"/dashboard?usuario={usuario}&mensaje={resultado['mensaje']}",
        status_code=303
    )


@router.post("/cancelar")
def cancelar(
    usuario: str = Form(...),
    sala: str = Form(...),
    hora: str = Form(...)
):
    resultado = cancelar_reserva_individual(usuario, sala, hora)

    return RedirectResponse(
        url=f"/dashboard?usuario={usuario}&mensaje={resultado['mensaje']}",
        status_code=303
    )