from datetime import datetime
from email.mime.image import MIMEImage
from functools import partial
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Union

from PIL import Image  # type: ignore

from simple_web_counter.utils.cgi import Request
from simple_web_counter.utils.file import add_row_to_tsv, read_last_row_from_tsv
from simple_web_counter.utils.image import concat_images, resize_image_to_height


def get_host_info_from_request(req: Request) -> str:
    if req.options["REMOTE_HOST"]:
        return req.options["REMOTE_HOST"]
    else:
        return f"{req.options['REMOTE_ADDR']}/{req.headers['X-Forwarded-For']}"


def read_last_row_from_datafile(
    path: Path,
) -> Optional[List[Union[int, datetime, str]]]:
    row = read_last_row_from_tsv(path=path)
    if row is None:
        return None
    else:
        count_str, dt_str, host, client, referer = row

        return [int(count_str), datetime.fromisoformat(dt_str), host, client, referer]


def write_row_to_datafile(
    path: Path, count: int, dt: datetime, host: str, client: str, referer: str
) -> None:
    add_row_to_tsv(path=path, row=[str(count), dt.isoformat(), host, client, referer])


def generate_counter_image_as_mime(
    images_base_dir: Path,
    images_filename: str,
    height: int,
    mode: str,
    format: str,
    count: int,
) -> str:
    count_str = str(count)

    image = concat_images(
        images=map(
            partial(get_image_of_number, images_base_dir, images_filename, height),
            count_str,
        ),
        mode=mode,
    )

    io = BytesIO()
    image.save(fp=io, format=format)
    image_mime = MIMEImage(io.getvalue())

    image_mime_str = str(image_mime)

    return image_mime_str


def get_image_of_number(
    images_base_dir: Path, images_filename: str, height: int, n: int
) -> Image:
    filename = images_filename.replace("%", f"{n}")
    image_path = images_base_dir / filename

    image = Image.open(image_path)
    resize_image_to_height(image=image_path, height=height)

    return image
