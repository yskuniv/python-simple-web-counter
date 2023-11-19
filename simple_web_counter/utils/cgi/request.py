import urllib.parse
from enum import Enum
from typing import Dict, List, Optional, Tuple, cast

import multipart  # type: ignore


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"


class Request:
    def __init__(self, env: Dict[str, str]) -> None:
        self._method = RequestMethod(env["REQUEST_METHOD"])
        self._path = env["REQUEST_URI"]
        self._params = urllib.parse.parse_qs(env["QUERY_STRING"])
        self._data = cast(Tuple[dict, dict], multipart.parse_form_data(env))
        self._headers = {
            "User-Agent": env.get("HTTP_USER_AGENT"),
            "Referer": env.get("HTTP_REFERER"),
            "X-Forwarded-For": env.get("HTTP_X_FORWARDED_FOR"),
        }
        self._options = {
            "REMOTE_HOST": env.get("REMOTE_HOST"),
            "REMOTE_ADDR": env.get("REMOTE_ADDR"),
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
