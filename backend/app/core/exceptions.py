from fastapi import HTTPException, status


class DbNotInitializedError(Exception):
    def __init__(self):
        message = "Database engine is not initialized"
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

class InvalidCredentialsException(HTTPException):
    def __init__(self, detail:str = "Invalid Credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="",
        )
