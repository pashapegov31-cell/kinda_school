class AuthError(Exception):
    pass


class UserAlreadyExistsError(AuthError):
    pass
