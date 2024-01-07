import pydantic
import pytest

from geodantic import GeoJSONObjectType, MultiLineString


def test_parse_multi_line_string_with_zero_line_strings() -> None:
    # given
    data = {
        "type": "MultiLineString",
        "coordinates": [],
    }

    # when
    multi_line_string = MultiLineString(**data)

    # then
    assert multi_line_string.type is GeoJSONObjectType.MULTI_LINE_STRING
    assert multi_line_string.coordinates == []


def test_parse_multi_line_string_with_one_line_string() -> None:
    # given
    data = {
        "type": "MultiLineString",
        "coordinates": [[[1, 2], [3, 4]]],
    }

    # when
    multi_line_string = MultiLineString(**data)

    # then
    assert multi_line_string.type is GeoJSONObjectType.MULTI_LINE_STRING
    assert multi_line_string.coordinates == [[(1, 2), (3, 4)]]


def test_parse_multi_line_string_with_multiple_line_strings() -> None:
    # given
    data = {
        "type": "MultiLineString",
        "coordinates": [[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
    }

    # when
    multi_line_string = MultiLineString(**data)

    # then
    assert multi_line_string.type is GeoJSONObjectType.MULTI_LINE_STRING
    assert multi_line_string.coordinates == [
        [(1.0, 2.0), (3.0, 4.0)],
        [(5.0, 6.0), (7.0, 8.0)],
    ]


def test_parse_multi_line_string_with_invalid_position() -> None:
    # given
    data = {
        "type": "MultiLineString",
        "coordinates": [[[1, 2], [3, 91]]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        MultiLineString(**data)


def test_parse_multi_line_string_with_invalid_line_string() -> None:
    # given
    data = {
        "type": "MultiLineString",
        "coordinates": [[[1, 2]]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        MultiLineString(**data)
