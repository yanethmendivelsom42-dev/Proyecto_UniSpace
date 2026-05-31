from urllib.parse import quote_plus

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from patterns.strategy import obtener_contexto_auth
from patterns.observer import gestor_eventos

from controllers.reserva_archivo_controller import (
    cancelar_reserva_individual,
    construir_historial_usuario,
    obtener_reservas_dashboard,
    reservar_sala,
)

from core.config import HORAS, SALAS_BASE, templates

router = APIRouter()


def _obtener_usuario_activo(request: Request) -> str:
    return request.session.get("usuario", "")


def _validar_vista(view: str) -> str:
    return view if view in {"salas", "reservas", "historial"} else "salas"


@router.get("/", response_class=HTMLResponse)
def mostrar_login(request: Request, mensaje: str = ""):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "mensaje": mensaje
        }
    )


@router.get("/login", response_class=HTMLResponse)
def mostrar_login_page(request: Request, mensaje: str = ""):
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
    contexto_auth = obtener_contexto_auth()

    resultado = contexto_auth.autenticar(
        correo.strip(),
        contrasena.strip()
    )

    if not resultado["ok"]:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "mensaje": resultado["mensaje"]
            },
            status_code=401
        )

    request.session["usuario"] = resultado["correo"]
    request.session["codigo_usuario"] = resultado["codigo_usuario"]
    request.session["rol"] = resultado["rol"]

    return RedirectResponse(
        url="/dashboard?view=salas",
        status_code=303
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()

    mensaje = quote_plus("Sesión cerrada correctamente.")

    return RedirectResponse(
        url=f"/?mensaje={mensaje}",
        status_code=303
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    view: str = "salas",
    mensaje: str = ""
):
    usuario = _obtener_usuario_activo(request)
    vista = _validar_vista(view)

    reservas = obtener_reservas_dashboard()

    historial_reciente = (
        construir_historial_usuario(reservas, usuario)
        if usuario
        else []
    )

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
            "logueado": bool(usuario),
            "vista": vista,
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
    request: Request,
    sala: str = Form(...),
    hora: str = Form(...)
):
    usuario = _obtener_usuario_activo(request)

    if not usuario:
        mensaje = quote_plus("Debes iniciar sesión para reservar.")

        return RedirectResponse(
            url=f"/?mensaje={mensaje}",
            status_code=303
        )

    resultado = reservar_sala(sala, hora, usuario)

    if resultado["ok"]:
        gestor_eventos.publicar_reserva_creada(usuario, sala, hora)

    mensaje = quote_plus(resultado["mensaje"])

    return RedirectResponse(
        url=f"/dashboard?view=reservas&mensaje={mensaje}",
        status_code=303
    )


@router.post("/cancelar")
def cancelar(
    request: Request,
    sala: str = Form(...),
    hora: str = Form(...)
):
    usuario = _obtener_usuario_activo(request)

    if not usuario:
        mensaje = quote_plus("Debes iniciar sesión para cancelar reservas.")

        return RedirectResponse(
            url=f"/?mensaje={mensaje}",
            status_code=303
        )

    resultado = cancelar_reserva_individual(usuario, sala, hora)

    if resultado["ok"]:
        gestor_eventos.publicar_reserva_cancelada(usuario, sala, hora)

    mensaje = quote_plus(resultado["mensaje"])

    return RedirectResponse(
        url=f"/dashboard?view=historial&mensaje={mensaje}",
        status_code=303
    )