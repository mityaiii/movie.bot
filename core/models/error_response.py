from core.models.response import Response


class ErrorResponse(Response):
    def __init__(self, error_message):
        super().__init__(status="error")
        self.error_message = error_message
