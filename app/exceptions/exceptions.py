class AuthError(Exception):
    pass


class UserAlreadyExistsError(AuthError):
    pass


class LoginError(AuthError):
    pass


class CantBeDeletedError(Exception):
    pass
