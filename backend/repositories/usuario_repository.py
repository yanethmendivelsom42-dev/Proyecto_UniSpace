from models.database_models import Usuario


class UsuarioRepository:

    def __init__(self, db):
        self.db = db

    def obtener_por_correo_y_contrasena(
        self,
        correo: str,
        contrasena: str
    ):

        return self.db.query(Usuario).filter(
            Usuario.correo == correo,
            Usuario.contrasena == contrasena,
            Usuario.estado == "Activo"
        ).first()

    def obtener_por_codigo(
        self,
        codigo_usuario: str
    ):

        return self.db.query(Usuario).filter(
            Usuario.codigo_usuario == codigo_usuario
        ).first()