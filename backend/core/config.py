from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
USUARIOS_FILE = BASE_DIR / "usuarios.txt"
RESERVAS_FILE = BASE_DIR / "reservas.json"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

SALAS_BASE = ["Sala 101", "Sala 102", "Sala 201"]
HORAS = ["08:00", "09:00", "10:00", "11:00", "12:00"]