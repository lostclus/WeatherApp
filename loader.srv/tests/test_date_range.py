from datetime import date, timedelta

from weatherapp_loader.date_range import DateRange


def test_split_to_chunks():
    d_range = DateRange(date(2024, 1, 1), date(2025, 1, 1))
    d_chunks = d_range.split_to_chunks(timedelta(days=92))

    assert d_chunks == [
        DateRange(date(2024, 1, 1), date(2024, 4, 2)),
        DateRange(date(2024, 4, 2), date(2024, 7, 3)),
        DateRange(date(2024, 7, 3), date(2024, 10, 3)),
        DateRange(date(2024, 10, 3), date(2025, 1, 1)),
    ]
