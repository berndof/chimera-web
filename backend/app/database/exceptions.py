class DuplicateEntryError(Exception):
    """Exceção para indicar que o registro já existe (violação de unicidade)."""

    def __init__(self, message: str = "Registro duplicado."):
        super().__init__(message)
