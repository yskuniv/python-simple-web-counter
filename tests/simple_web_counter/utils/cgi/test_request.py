from simple_web_counter.utils.cgi import Request, RequestMethod

DUMMY_URI = "DUMMY_URI"
DUMMY_USER_AGENT = "DUMMY_USER_AGENT"
DUMMY_REFERER = "DUMMY_REFERER"
DUMMY_X_FORWARDED_FOR = "DUMMY_X_FORWARDED_FOR"
DUMMY_HOST = "DUMMY_HOST"
DUMMY_ADDR = "DUMMY_ADDR"


def test_request1():
    req = Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_URI,
            "QUERY_STRING": "a=1&b=2",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "HTTP_X_FORWARDED_FOR": DUMMY_X_FORWARDED_FOR,
            "REMOTE_HOST": DUMMY_HOST,
            "REMOTE_ADDR": DUMMY_ADDR,
        }
    )

    assert req.method == RequestMethod.GET
    assert req.path == DUMMY_URI
    assert req.params == {"a": ["1"], "b": ["2"]}
    assert req.headers["User-Agent"] == DUMMY_USER_AGENT
    assert req.headers["Referer"] == DUMMY_REFERER
    assert req.headers["X-Forwarded-For"] == DUMMY_X_FORWARDED_FOR
    assert req.options["REMOTE_HOST"] == DUMMY_HOST
    assert req.options["REMOTE_ADDR"] == DUMMY_ADDR


def test_request2():
    req = Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_URI,
            "QUERY_STRING": "",
        }
    )

    assert req.method == RequestMethod.GET
    assert req.path == DUMMY_URI
    assert req.params == {}
    assert req.headers["User-Agent"] is None
    assert req.headers["Referer"] is None
    assert req.headers["X-Forwarded-For"] is None
    assert req.options["REMOTE_HOST"] is None
    assert req.options["REMOTE_ADDR"] is None
