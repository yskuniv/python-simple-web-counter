from datetime import datetime
from typing import Optional

import pytz


def get_datetime_now(zone: Optional[str]) -> datetime:
    if zone:
        tz = pytz.timezone(zone)
    else:
        tz = pytz.utc

    return datetime.now(tz=tz)
