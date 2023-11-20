from datetime import datetime
from pathlib import Path

from pytest_mock import MockFixture

from simple_web_counter.simple_web_counter import count_and_record_access

DUMMY_DATETIME = datetime.fromisoformat("1970-01-01T00:00:00+09:00")
DUMMY_REFERER = "DUMMY_REFERER"
DUMMY_DATAFILE_PATH = Path("DUMMY_DATAFILE_PATH")


def test_count_and_record_access_datafileにデータが存在して新たなホストandクライアントからのアクセスの場合(
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


def test_count_and_record_access_datafileにデータが存在して同一のホストandクライアントからのアクセスの場合(
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


def test_count_and_record_access_datafileにデータが存在しない場合(mocker: MockFixture) -> None:
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
