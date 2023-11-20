class HttpError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self._status_code = status_code
        self._message = message

    def __str__(self) -> str:
        return f"Status: {self._status_code} {self._message}"


class Http400Error(HttpError):
    def __init__(self) -> None:
        super().__init__(status_code=400, message="Bad Request")


class Http404Error(HttpError):
    def __init__(self) -> None:
        super().__init__(status_code=404, message="Not Found")
