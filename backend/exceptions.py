class ArchivoUsuariosNoEncontradoError(Exception):
    """Se lanza cuando no existe usuarios.txt"""
    pass


class FormatoUsuarioInvalidoError(Exception):
    """Se lanza cuando una línea no cumple usuario:clave"""
    pass


class UsuarioVacioError(Exception):
    """Se lanza cuando el usuario está vacío"""
    pass


class ContrasenaVaciaError(Exception):
    """Se lanza cuando la contraseña está vacía"""
    pass


class CredencialesInvalidasError(Exception):
    """Se lanza cuando las credenciales son incorrectas"""
    pass
