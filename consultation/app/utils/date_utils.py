from datetime import datetime

import dateutil.parser


def parse_date(date_text: str) -> datetime:
    return dateutil.parser.isoparse(date_text)


def hours_between(end_date, start_date) -> int:
    duration = end_date - start_date
    duration_in_seconds = duration.total_seconds()
    dm = divmod(duration_in_seconds, 3600)

    hours = dm[0]
    if dm[1] > (10 * 60):  # additional hour if over 10 minutes
        hours += 1
    return hours
