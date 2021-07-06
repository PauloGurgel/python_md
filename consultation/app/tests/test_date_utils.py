import datetime

from dateutil.tz import tzutc
from app.utils import date_utils


def verify_date(hours, minutes, seconds):
    start_date = datetime.datetime(2021, 7, 6, 8, 0, 0, 0)
    end_date = datetime.datetime(2021, 7, 6, hours, minutes, seconds, 0)
    output_hours = date_utils.hours_between(end_date=end_date, start_date=start_date)
    return output_hours


def test_parsing_iso_format():
    expected_time = datetime.datetime(2021, 7, 6, 13, 1, 0, 0)
    input_str = "2021-07-06T13:01:00.000"
    date_time = date_utils.parse_date(date_text=input_str)
    assert expected_time == date_time


def test_parsing_zulu_format():
    expected_time = datetime.datetime(2021, 7, 6, 13, 1, 0, 0, tzutc())
    input_str = "2021-07-06T13:01:00.000Z"
    date_time = date_utils.parse_date(date_text=input_str)
    assert expected_time == date_time


def test_hours_between_single_hour():
    expected = 1
    assert expected == verify_date(9, 0, 0)


def test_hours_between_single_hour_within_tolerance():
    expected = 1
    assert expected == verify_date(9, 10, 0)


def test_hours_between_single_hour_outside_tolerance():
    expected = 2
    assert expected == verify_date(9, 11, 0)


def test_hours_between_four_hours():
    expected = 4
    assert expected == verify_date(12, 5, 0)







