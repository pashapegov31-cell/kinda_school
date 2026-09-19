class AuthError(Exception):
    pass


class UserAlreadyExistsError(AuthError):
    pass


class LoginError(AuthError):
    pass


class CantBeUpdatedError(Exception):
    pass


class TokenError(Exception):
    pass


class NotAccessTokenError(TokenError):
    pass
