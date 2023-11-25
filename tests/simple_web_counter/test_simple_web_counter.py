from datetime import datetime
from pathlib import Path

import helper
import pytest
from pytest_mock import MockFixture

from simple_web_counter.errors import Http400Error
from simple_web_counter.simple_web_counter import count_and_record_access, parse_request
from simple_web_counter.utils import cgi

DUMMY_URI = "DUMMY_URI"
DUMMY_USER_AGENT = "DUMMY_USER_AGENT"
DUMMY_REFERER = "DUMMY_REFERER"
DUMMY_HOST = "DUMMY_HOST"
DUMMY_DATETIME = datetime.fromisoformat("1970-01-01T00:00:00+09:00")
DUMMY_DATAFILE_PATH = Path("DUMMY_DATAFILE_PATH")


def test_parse_request_in_case_of_request_correctly() -> None:
    datafile = "dummy.txt"
    height = 24

    req = cgi.Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_URI,
            "QUERY_STRING": f"datafile={datafile}&height={height}",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_HOST,
        }
    )

    assert parse_request(req=req) == (
        DUMMY_HOST,
        DUMMY_USER_AGENT,
        DUMMY_REFERER,
        datafile,
        height,
    )


def test_parse_request_in_case_of_request_method_is_invalid() -> None:
    datafile = "dummy.txt"
    height = 24

    req = cgi.Request(
        env={
            "REQUEST_METHOD": "POST",
            "REQUEST_URI": DUMMY_URI,
            "QUERY_STRING": f"datafile={datafile}&height={height}",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_HOST,
        }
    )

    with pytest.raises(Http400Error):
        parse_request(req=req)


def test_parse_request_in_case_of_height_in_query_string_is_invalid() -> None:
    datafile = "dummy.txt"
    height = "INVALID_HEIGHT"

    req = cgi.Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_URI,
            "QUERY_STRING": f"datafile={datafile}&height={height}",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_HOST,
        }
    )

    with pytest.raises(Http400Error):
        parse_request(req=req)


def test_parse_request_in_case_of_query_string_missing() -> None:
    req = cgi.Request(
        env={
            "REQUEST_METHOD": "GET",
            "REQUEST_URI": DUMMY_URI,
            "QUERY_STRING": "",
            "HTTP_USER_AGENT": DUMMY_USER_AGENT,
            "HTTP_REFERER": DUMMY_REFERER,
            "REMOTE_HOST": DUMMY_HOST,
        }
    )

    with pytest.raises(Http400Error):
        parse_request(req=req)


def test_count_and_record_access_in_case_of_datafile_exists_and_the_access_is_from_new_host_and_client(
    mocker: MockFixture,
) -> None:
    (
        _,
        write_row_to_datafile_mock,
    ) = helper.mock_counter_helper_functions_with_datafile_return_value(
        mocker=mocker,
        date_time_now=DUMMY_DATETIME,
        last_count=1,
        last_datetime=DUMMY_DATETIME,
        last_host="DUMMY_HOST1",
        last_client="DUMMY_CLIENT1",
        last_referer=DUMMY_REFERER,
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
    (
        _,
        write_row_to_datafile_mock,
    ) = helper.mock_counter_helper_functions_with_datafile_return_value(
        mocker=mocker,
        date_time_now=DUMMY_DATETIME,
        last_count=1,
        last_datetime=DUMMY_DATETIME,
        last_host="DUMMY_HOST1",
        last_client="DUMMY_CLIENT1",
        last_referer=DUMMY_REFERER,
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


def test_count_and_record_access_in_case_of_datafile_exists_but_the_content_is_blank(
    mocker: MockFixture,
) -> None:
    (
        _,
        write_row_to_datafile_mock,
    ) = helper.mock_counter_helper_functions_without_datafile_return_value(
        mocker=mocker,
        date_time_now=DUMMY_DATETIME,
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
