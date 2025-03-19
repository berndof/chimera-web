from os import getenv

import bcrypt
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_secret_key() -> str:
    secret_key = getenv("SECRET_KEY")
    if secret_key is None:
        raise ValueError("EMPTY SECRET KEY ON .env")
    return secret_key


def get_password_hash(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def validate_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
