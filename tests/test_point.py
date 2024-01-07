import pydantic
import pytest

from geodantic import GeoJSONObjectType, Point


def test_parse_point_with_two_coordinates() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
    }

    # when
    point = Point(**data)

    # then
    assert point.type is GeoJSONObjectType.POINT
    assert point.coordinates == (100.1, 80.2)


def test_parse_point_with_three_coordinates() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2, 900.3],
    }

    # when
    point = Point(**data)

    # then
    assert point.type is GeoJSONObjectType.POINT
    assert point.coordinates == (100.1, 80.2, 900.3)


def test_parse_point_with_one_coordinate() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


def test_parse_point_with_four_coordinates() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2, 900.3, 123.123],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


def test_parse_point_with_zero_coordinates() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


def test_parse_point_with_out_of_range_longitude() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [190, 90],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


def test_parse_point_with_out_of_range_latitude() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [180, 100],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)
