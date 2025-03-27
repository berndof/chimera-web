class DuplicateEntryError(Exception):
    def __init__(self, model: type, message: str | None = None) -> None:
        if message is None:
            message = f"{model.__name__} already exists, skiping"
        super().__init__(message)


class RelationAlreadyExistsError(Exception):
    def __init__(self, models: list[type], message: str | None = None) -> None:
        if message is None:
            participants = [model.__name__ for model in models]
            message = f"Relation already exists between: {', '.join(participants)}"
        super().__init__(message)
