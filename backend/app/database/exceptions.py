class DuplicateEntryError(Exception):
    def __init__(self, model: type, message: str | None = None) -> None:
        if message is None:
            message = f"{model.__name__} already exists, skiping"
        super().__init__(message)
