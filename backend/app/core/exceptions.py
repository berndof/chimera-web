from fastapi import HTTPException, status


class DbNotInitializedError(Exception):
    def __init__(self):
        message = "Database engine is not initialized"
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class EmptyPage(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This page is empty",
        )
