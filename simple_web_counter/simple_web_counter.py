import os
from datetime import datetime, timedelta, timezone

from simple_web_counter import config
from simple_web_counter.utils import cgi
from simple_web_counter.utils.counter_helper import (
    generate_counter_image_as_mime,
    get_host_info_from_request,
)
from simple_web_counter.utils.file import add_row_to_tsv, read_last_row_from_tsv


def main() -> None:
    cfg = config.load()

    req = cgi.Request(env=dict(os.environ))

    if req != cgi.RequestMethod.GET:
        raise  # TODO: raise a proper exception

    host = get_host_info_from_request(req)
    client = req.headers["User-Agent"]

    datafile = req.params["datafile"]
    height = req.params["height"]

    last_row = read_last_row_from_tsv(path=cfg.data.out_dir / datafile)

    if last_row:
        last_count_str, _, last_host, last_client, _ = last_row
        last_count = int(last_count_str)
    else:
        last_count = 0
        last_host = ""
        last_client = ""

    # To prevent to count an access from the same host or client
    if host == last_host and client == last_client:
        count = last_count
    else:
        count = last_count + 1

        dt = datetime.now(
            tz=timezone(offset=timedelta(hours=9))
        )  # FIXME: fix to avoid hard-coding timezone
        referer = req.headers["Referer"]

        add_row_to_tsv(
            path=cfg.data.out_dir / datafile,
            row=[count, dt.isoformat(), host, client, referer],
        )

    image_mime = generate_counter_image_as_mime(
        images_base_dir=cfg.images.base_dir,
        images_filename=cfg.images.filename,
        height=height,
        count=count,
    )

    print(image_mime)
