from datetime import UTC, datetime

import pytest

from app.core.date_utils import normalize_iso_date, parse_iso8601_utc


def test_normalize_appends_z_to_naive_t_date():
    assert normalize_iso_date("2026-01-01T12:00:00") == "2026-01-01T12:00:00Z"


def test_normalize_leaves_offset_and_z_dates_untouched():
    assert normalize_iso_date("2026-01-01T12:00:00Z") == "2026-01-01T12:00:00Z"
    assert normalize_iso_date("2026-01-01T12:00:00+02:00") == "2026-01-01T12:00:00+02:00"


def test_normalize_passes_through_non_strings():
    assert normalize_iso_date(None) is None
    assert normalize_iso_date(123) == 123
    assert normalize_iso_date("") == ""


def test_parse_iso8601_utc_handles_z_suffix():
    dt = parse_iso8601_utc("2026-01-01T00:00:00Z")
    assert dt == datetime(2026, 1, 1, tzinfo=UTC)


def test_parse_iso8601_utc_rejects_garbage():
    with pytest.raises(ValueError):
        parse_iso8601_utc("not-a-date")
