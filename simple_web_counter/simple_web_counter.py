import os
from pathlib import Path
from typing import Optional

from simple_web_counter import config
from simple_web_counter.utils import cgi
from simple_web_counter.utils.counter_helper import (
    generate_counter_image_as_mime,
    get_datetime_now,
    get_host_info_from_request,
    read_last_row_from_datafile,
    write_row_to_datafile,
)

from .errors import Http400Error, Http404Error


def count_and_record_access(
    datafile_path: Path,
    timezone: Optional[str],
    host: str,
    client: Optional[str],
    referer: Optional[str],
) -> int:
    try:
        last_row = read_last_row_from_datafile(path=datafile_path)
    except FileNotFoundError:
        raise Http404Error()

    if last_row:
        last_count, _, last_host, last_client, _ = last_row
    else:
        last_count = 0
        last_host = None
        last_client = None

    # To prevent to count or record accesses from the same host or client
    if host == last_host and client == last_client:
        return last_count
    else:
        new_count = last_count + 1

        dt = get_datetime_now(zone=timezone)

        write_row_to_datafile(
            path=datafile_path,
            count=new_count,
            dt=dt,
            host=host,
            client=client or "",
            referer=referer or "",
        )

        return new_count


def main() -> None:
    cfg = config.load()
    req = cgi.Request(env=dict(os.environ))

    if req.method != cgi.RequestMethod.GET:
        raise Http400Error()

    host = get_host_info_from_request(req)
    client = req.headers["User-Agent"]
    referer = req.headers["Referer"]

    try:
        datafile = req.params["datafile"][0]
        height = int(req.params["height"][0])
    except (IndexError, ValueError):
        raise Http400Error()

    count = count_and_record_access(
        datafile_path=Path(cfg.data.out_dir) / datafile,
        timezone=cfg.datetime.timezone,
        host=host,
        client=client,
        referer=referer,
    )

    image_mime = generate_counter_image_as_mime(
        images_base_dir=Path(cfg.images.base_dir),
        images_filename=cfg.images.filename,
        height=height,
        mode="RGB",
        format="PNG",
        count=count,
    )

    print(image_mime, end="")
