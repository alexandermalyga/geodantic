import pydantic
import pytest

from geodantic import GeoJSONObjectType, Polygon


def test_parse_polygon_with_zero_rings() -> None:
    # given
    data = {
        "type": "Polygon",
        "coordinates": [],
    }

    # when
    polygon = Polygon(**data)

    # then
    assert polygon.type is GeoJSONObjectType.POLYGON
    assert polygon.coordinates == []


def test_parse_polygon_with_one_ring() -> None:
    # given
    data = {
        "type": "Polygon",
        "coordinates": [[[1, 2], [3, 4], [5, 6], [1, 2]]],
    }

    # when
    polygon = Polygon(**data)

    # then
    assert polygon.type is GeoJSONObjectType.POLYGON
    assert polygon.coordinates == [[(1, 2), (3, 4), (5, 6), (1, 2)]]


def test_parse_polygon_with_multiple_rings() -> None:
    # given
    data = {
        "type": "Polygon",
        "coordinates": [
            [[1, 2], [3, 4], [5, 6], [1, 2]],
            [[1, 2], [3, 4], [5, 6], [1, 2]],
        ],
    }

    # when
    polygon = Polygon(**data)

    # then
    assert polygon.type is GeoJSONObjectType.POLYGON
    assert polygon.coordinates == [
        [(1, 2), (3, 4), (5, 6), (1, 2)],
        [(1, 2), (3, 4), (5, 6), (1, 2)],
    ]


def test_parse_polygon_with_long_ring() -> None:
    # given
    data = {
        "type": "Polygon",
        "coordinates": [[[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [1, 2]]],
    }

    # when
    polygon = Polygon(**data)

    # then
    assert polygon.type is GeoJSONObjectType.POLYGON
    assert polygon.coordinates == [[(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (1, 2)]]


def test_parse_polygon_with_too_short_ring() -> None:
    # given
    data = {
        "type": "Polygon",
        "coordinates": [[[1, 2], [3, 4], [1, 2]]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Polygon(**data)


def test_parse_polygon_with_non_closed_ring() -> None:
    # given
    data = {
        "type": "Polygon",
        "coordinates": [[[1, 2], [3, 4], [5, 6], [1.11, 2.22]]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Polygon(**data)
