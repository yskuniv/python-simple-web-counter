import os
from pathlib import Path

from simple_web_counter import config
from simple_web_counter.utils import cgi
from simple_web_counter.utils.counter_helper import (
    generate_counter_image_as_mime,
    get_datetime_now,
    get_host_info_from_request,
    read_last_row_from_datafile,
    write_row_to_datafile,
)


def count_access_and_output_image_as_mime(cfg: config.Config, req: cgi.Request) -> None:
    if req.method != cgi.RequestMethod.GET:
        raise  # TODO: raise a proper exception

    host = get_host_info_from_request(req)
    client = req.headers["User-Agent"]
    referer = req.headers["Referer"]

    datafile = req.params["datafile"][0]
    height = int(req.params["height"][0])

    last_row = read_last_row_from_datafile(path=Path(cfg.data.out_dir) / datafile)

    if last_row:
        last_count, _, last_host, last_client, _ = last_row
    else:
        last_count = 0
        last_host = None
        last_client = None

    # To prevent to count or record accesses from the same host or client
    if host == last_host and client == last_client:
        count = last_count
    else:
        count = last_count + 1

        dt = get_datetime_now(zone=cfg.datetime.timezone)

        write_row_to_datafile(
            path=Path(cfg.data.out_dir) / datafile,
            count=count,
            dt=dt,
            host=host,
            client=client or "",
            referer=referer or "",
        )

    image_mime = generate_counter_image_as_mime(
        images_base_dir=Path(cfg.images.base_dir),
        images_filename=cfg.images.filename,
        height=height,
        mode="RGB",
        format="PNG",
        count=count,
    )

    print(image_mime)


def main() -> None:
    cfg = config.load()
    req = cgi.Request(env=dict(os.environ))

    count_access_and_output_image_as_mime(cfg, req)
