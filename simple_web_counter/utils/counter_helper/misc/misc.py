from simple_web_counter.utils.cgi import Request


def get_host_info_from_request(req: Request) -> str:
    if req.options["REMOTE_HOST"]:
        return req.options["REMOTE_HOST"]
    else:
        return f"{req.options['REMOTE_ADDR']}/{req.headers['X-Forwarded-For']}"
