from core.models.response import Response


class SuccessResponse(Response):
    def __init__(self, data) -> None:
        super().__init__(status="success")
        self.data = data
