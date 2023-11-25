from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from simple_web_counter.utils.file import add_row_to_tsv, read_last_row_from_tsv


def read_last_row_from_datafile(
    path: Path,
) -> Optional[Tuple[int, datetime, str, str, str]]:
    row = read_last_row_from_tsv(path=path)
    if row is None:
        return None
    else:
        count_str, dt_str, host, client, referer = row

        return (int(count_str), datetime.fromisoformat(dt_str), host, client, referer)


def write_row_to_datafile(
    path: Path,
    count: int,
    dt: datetime,
    host: str,
    client: str,
    referer: str,
    timespec: str = "seconds",
) -> None:
    add_row_to_tsv(
        path=path,
        row=[str(count), dt.isoformat(timespec=timespec), host, client, referer],
    )
