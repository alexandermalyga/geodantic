import pydantic
import pytest

from geodantic import GeoJSONObjectType, MultiPolygon


def test_parse_multi_polygon_with_zero_polygons() -> None:
    # given
    data = {
        "type": "MultiPolygon",
        "coordinates": [],
    }

    # when
    multi_polygon = MultiPolygon(**data)

    # then
    assert multi_polygon.type is GeoJSONObjectType.MULTI_POLYGON
    assert multi_polygon.coordinates == []


def test_parse_multi_polygon_with_one_polygon() -> None:
    # given
    data = {
        "type": "MultiPolygon",
        "coordinates": [[[[1, 2], [3, 4], [5, 6], [1, 2]]]],
    }

    # when
    multi_polygon = MultiPolygon(**data)

    # then
    assert multi_polygon.type is GeoJSONObjectType.MULTI_POLYGON
    assert multi_polygon.coordinates == [[[(1, 2), (3, 4), (5, 6), (1, 2)]]]


def test_parse_multi_polygon_with_multiple_polygons() -> None:
    # given
    data = {
        "type": "MultiPolygon",
        "coordinates": [
            [[[1, 2], [3, 4], [5, 6], [1, 2]]],
            [
                [[1, 2], [3, 4], [5, 6], [1, 2]],
                [[1, 2], [3, 4], [5, 6], [1, 2]],
            ],
        ],
    }

    # when
    multi_polygon = MultiPolygon(**data)

    # then
    assert multi_polygon.type is GeoJSONObjectType.MULTI_POLYGON
    assert multi_polygon.coordinates == [
        [[(1, 2), (3, 4), (5, 6), (1, 2)]],
        [
            [(1, 2), (3, 4), (5, 6), (1, 2)],
            [(1, 2), (3, 4), (5, 6), (1, 2)],
        ],
    ]


def test_parse_multi_polygon_with_too_short_ring() -> None:
    # given
    data = {
        "type": "MultiPolygon",
        "coordinates": [[[[1, 2], [3, 4], [1, 2]]]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        MultiPolygon(**data)


def test_parse_multi_polygon_with_non_closed_ring() -> None:
    # given
    data = {
        "type": "MultiPolygon",
        "coordinates": [[[[1, 2], [3, 4], [5, 6], [1.11, 2.22]]]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        MultiPolygon(**data)
