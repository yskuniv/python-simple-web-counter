import urllib.parse
from enum import Enum
from typing import Dict, List, Optional, Tuple, cast

import multipart  # type: ignore


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"


class Request:
    def __init__(self, environ: Dict[str, str]) -> None:
        self._method = RequestMethod(environ["REQUEST_METHOD"])
        self._path = environ["REQUEST_URI"]
        self._params = urllib.parse.parse_qs(environ["QUERY_STRING"])
        self._data = cast(Tuple[dict, dict], multipart.parse_form_data(environ))
        self._headers = {
            "User-Agent": environ.get("HTTP_USER_AGENT"),
            "Referer": environ.get("HTTP_REFERER"),
            "X-Forwarded-For": environ.get("HTTP_X_FORWARDED_FOR"),
        }
        self._options = {
            "REMOTE_HOST": environ.get("REMOTE_HOST"),
            "REMOTE_ADDR": environ.get("REMOTE_ADDR"),
        }

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    @property
    def params(self) -> Dict[str, List[str]]:
        return self._params

    @property
    def data(self) -> Tuple[dict, dict]:
        return self._data

    @property
    def headers(self) -> Dict[str, Optional[str]]:
        return self._headers

    @property
    def options(self) -> Dict[str, Optional[str]]:
        return self._options
