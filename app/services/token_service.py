from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.exceptions.exceptions import NotAccessTokenError, TokenError


class TokenService:
    def __init__(self, secret_key: str, algorithm: str):
        self._secret_key = secret_key
        self._algorithm = algorithm

    def create_access_token(self, user_id: int, email: str) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=15)
        payload = {
            "sub": user_id,
            "email": email,
            "iat": now,
            "exp": exp,
            "typ": "access",
        }
        encoded_token = jwt.encode(payload, self._secret_key, self._algorithm)
        return encoded_token

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except JWTError:
            raise TokenError("Ошибка проверки токена")

    def verify_access_token(self, access_token: str) -> int:
        decoded_token = self.decode_token(access_token)
        if decoded_token.get("typ") != "access":
            raise NotAccessTokenError("Данный токен не является access токеном")
        user_id = decoded_token.get("sub")
        if not user_id:
            raise TokenError("В токене отсутствует user_id")
        return user_id
