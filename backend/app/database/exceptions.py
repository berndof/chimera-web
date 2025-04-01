class DbNotInitializedError(Exception):
    def __init__(self):
        message = "Database engine is not initialized"
        super().__init__(message)


class DuplicateEntryError(Exception):
    def __init__(self, model: type, message: str | None = None) -> None:
        if message is None:
            message = f"{model.__name__} already exists, skiping"
        super().__init__(message)


class RelationAlreadyExistsError(Exception):
    def __init__(self, models: list[type | object], message: str | None = None) -> None:
        # Determina se o item é uma classe ou instância e ajusta a mensagem
        participants = [
            repr(model) if not isinstance(model, type) else model.__name__
            for model in models
        ]

        if message is None:
            message = (
                f"Relation already exists between: {', '.join(participants)}, skipping"
            )

        super().__init__(message)
