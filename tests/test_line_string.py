import pydantic
import pytest

from geodantic import GeoJSONObjectType, LineString


def test_parse_line_string_with_zero_positions() -> None:
    # given
    data = {
        "type": "LineString",
        "coordinates": [],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        LineString(**data)


def test_parse_line_string_with_one_position() -> None:
    # given
    data = {
        "type": "LineString",
        "coordinates": [[1, 2]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        LineString(**data)


def test_parse_line_string_with_multiple_positions() -> None:
    # given
    data = {
        "type": "LineString",
        "coordinates": [[1, 2], [3, 4]],
    }

    # when
    line_string = LineString(**data)

    # then
    assert line_string.type is GeoJSONObjectType.LINE_STRING
    assert line_string.coordinates == [(1.0, 2.0), (3.0, 4.0)]
