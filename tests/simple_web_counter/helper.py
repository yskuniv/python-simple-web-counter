from datetime import datetime
from typing import Tuple
from unittest.mock import Mock

from pytest_mock import MockFixture


def mock_counter_helper_functions_with_datafile_return_value(
    mocker: MockFixture,
    date_time_now: datetime,
    last_count: int,
    last_datetime: datetime,
    last_host: str,
    last_client: str,
    last_referer: str,
) -> Tuple[Mock, Mock]:
    get_datetime_now_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.get_datetime_now"
    )
    get_datetime_now_mock.return_value = date_time_now

    read_last_row_from_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.read_last_row_from_datafile"
    )
    read_last_row_from_datafile_mock.return_value = [
        last_count,
        last_datetime,
        last_host,
        last_client,
        last_referer,
    ]

    write_row_to_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.write_row_to_datafile"
    )

    return (read_last_row_from_datafile_mock, write_row_to_datafile_mock)


def mock_counter_helper_functions_without_datafile_return_value(
    mocker: MockFixture,
    date_time_now: datetime,
) -> Tuple[Mock, Mock]:
    get_datetime_now_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.get_datetime_now"
    )
    get_datetime_now_mock.return_value = date_time_now

    read_last_row_from_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.read_last_row_from_datafile"
    )
    read_last_row_from_datafile_mock.return_value = None

    write_row_to_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.write_row_to_datafile"
    )

    return (read_last_row_from_datafile_mock, write_row_to_datafile_mock)
