from repositories.usuario_repository import UsuarioRepository


class AuthService:

    def __init__(self, db):

        self.usuario_repository = UsuarioRepository(db)

    def autenticar(
        self,
        correo: str,
        contrasena: str
    ):

        usuario = self.usuario_repository.obtener_por_correo_y_contrasena(
            correo,
            contrasena
        )

        if not usuario:

            return {
                "ok": False,
                "mensaje": "Correo o contraseña incorrectos"
            }

        return {
            "ok": True,
            "correo": usuario.correo,
            "codigo_usuario": usuario.codigo_usuario,
            "rol": usuario.id_rol
        }