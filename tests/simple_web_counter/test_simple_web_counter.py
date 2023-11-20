from datetime import datetime
from pathlib import Path

import pytest
from pytest_mock import MockFixture

from simple_web_counter.errors import Http400Error
from simple_web_counter.simple_web_counter import count_and_record_access, parse_request
from simple_web_counter.utils import cgi

DUMMY_REQUEST_URI = "DUMMY_REQUEST_URI"
DUMMY_USER_AGENT = "DUMMY_USER_AGENT"
DUMMY_REMOTE_HOST = "DUMMY_REMOTE_HOST"
DUMMY_DATETIME = datetime.fromisoformat("1970-01-01T00:00:00+09:00")
DUMMY_REFERER = "DUMMY_REFERER"
DUMMY_DATAFILE_PATH = Path("DUMMY_DATAFILE_PATH")


def test_parse_request_in_case_of_request_correctly() -> None:
    datafile = "dummy.txt"
    height = 48

    req = cgi.Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_REQUEST_URI,
            "QUERY_STRING": f"datafile={datafile}&height={height}",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_REMOTE_HOST,
        }
    )

    assert parse_request(req=req) == (
        DUMMY_REMOTE_HOST,
        DUMMY_USER_AGENT,
        DUMMY_REFERER,
        datafile,
        height,
    )


def test_parse_request_in_case_of_request_method_is_invalid() -> None:
    datafile = "dummy.txt"
    height = 48

    req = cgi.Request(
        env={
            "REQUEST_METHOD": "POST",
            "REQUEST_URI": DUMMY_REQUEST_URI,
            "QUERY_STRING": f"datafile={datafile}&height={height}",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_REMOTE_HOST,
        }
    )

    with pytest.raises(Http400Error):
        parse_request(req=req)


def test_parse_request_in_case_of_height_in_query_string_is_invalid() -> None:
    datafile = "dummy.txt"
    height = "DUMMY_HEIGHT"

    req = cgi.Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_REQUEST_URI,
            "QUERY_STRING": f"datafile={datafile}&height={height}",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_REMOTE_HOST,
        }
    )

    with pytest.raises(Http400Error):
        parse_request(req=req)


def test_parse_request_in_case_of_query_string_missing() -> None:
    req = cgi.Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_REQUEST_URI,
            "QUERY_STRING": "",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_REMOTE_HOST,
        }
    )

    with pytest.raises(Http400Error):
        parse_request(req=req)


def test_count_and_record_access_in_case_of_datafile_exists_and_the_access_is_from_new_host_and_client(
    mocker: MockFixture,
) -> None:
    read_last_row_from_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.read_last_row_from_datafile"
    )
    read_last_row_from_datafile_mock.return_value = [
        1,
        DUMMY_DATETIME,
        "DUMMY_HOST1",
        "DUMMY_CLIENT1",
        DUMMY_REFERER,
    ]

    get_datetime_now_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.get_datetime_now"
    )
    get_datetime_now_mock.return_value = DUMMY_DATETIME

    write_row_to_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.write_row_to_datafile"
    )

    assert (
        count_and_record_access(
            datafile_path=DUMMY_DATAFILE_PATH,
            timezone=None,
            host="DUMMY_HOST2",
            client="DUMMY_CLIENT2",
            referer=DUMMY_REFERER,
        )
        == 2
    )

    write_row_to_datafile_mock.assert_called_once_with(
        path=DUMMY_DATAFILE_PATH,
        count=2,
        dt=DUMMY_DATETIME,
        host="DUMMY_HOST2",
        client="DUMMY_CLIENT2",
        referer=DUMMY_REFERER,
    )


def test_count_and_record_access_in_case_of_datafile_exists_and_the_access_is_from_the_same_host_and_client(
    mocker: MockFixture,
) -> None:
    read_last_row_from_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.read_last_row_from_datafile"
    )
    read_last_row_from_datafile_mock.return_value = [
        1,
        DUMMY_DATETIME,
        "DUMMY_HOST1",
        "DUMMY_CLIENT1",
        DUMMY_REFERER,
    ]

    get_datetime_now_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.get_datetime_now"
    )
    get_datetime_now_mock.return_value = DUMMY_DATETIME

    write_row_to_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.write_row_to_datafile"
    )

    assert (
        count_and_record_access(
            datafile_path=DUMMY_DATAFILE_PATH,
            timezone=None,
            host="DUMMY_HOST1",
            client="DUMMY_CLIENT1",
            referer=DUMMY_REFERER,
        )
        == 1
    )

    write_row_to_datafile_mock.assert_not_called()


def test_count_and_record_access_in_case_of_datafile_does_not_exist(
    mocker: MockFixture,
) -> None:
    read_last_row_from_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.read_last_row_from_datafile"
    )
    read_last_row_from_datafile_mock.return_value = None

    get_datetime_now_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.get_datetime_now"
    )
    get_datetime_now_mock.return_value = DUMMY_DATETIME

    write_row_to_datafile_mock = mocker.patch(
        target="simple_web_counter.simple_web_counter.write_row_to_datafile"
    )

    assert (
        count_and_record_access(
            datafile_path=DUMMY_DATAFILE_PATH,
            timezone=None,
            host="DUMMY_HOST1",
            client="DUMMY_CLIENT1",
            referer=DUMMY_REFERER,
        )
        == 1
    )

    write_row_to_datafile_mock.assert_called_once_with(
        path=DUMMY_DATAFILE_PATH,
        count=1,
        dt=DUMMY_DATETIME,
        host="DUMMY_HOST1",
        client="DUMMY_CLIENT1",
        referer=DUMMY_REFERER,
    )
