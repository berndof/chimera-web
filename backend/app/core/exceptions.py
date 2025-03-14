
class DbNotInitializedError(Exception):
    def __init__(self):
        message = "Database engine is not initialized"
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


