class AuthError(Exception):
    pass


class UserAlreadyExistsError(AuthError):
    pass


class LoginError(AuthError):
    pass


class UserError(Exception):
    pass


class CantBeUpdatedError(UserError):
    pass


class NoSuchUser(UserError):
    pass


class TokenError(Exception):
    pass


class NotAccessTokenError(TokenError):
    pass


class NotValidValue(Exception):
    pass


class NotValidPrice(NotValidValue):
    pass
