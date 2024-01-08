import pydantic
import pytest

from geodantic import (
    GeoJSONObjectType,
    GeometryCollection,
    LineString,
    MultiPolygon,
    Point,
)


def test_parse_geometry_collection_with_zero_geometries() -> None:
    # given
    data = {
        "type": "GeometryCollection",
        "geometries": [],
    }

    # when
    geometry_collection = GeometryCollection(**data)

    # then
    assert geometry_collection.type is GeoJSONObjectType.GEOMETRY_COLLECTION
    assert geometry_collection.geometries == []


def test_parse_geometry_collection_with_multiple_geometries() -> None:
    # given
    data = {
        "type": "GeometryCollection",
        "geometries": [
            {
                "type": "Point",
                "coordinates": [100.1, 80.2],
            },
            {
                "type": "LineString",
                "coordinates": [[1, 2], [3, 4]],
            },
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[1, 2], [3, 4], [5, 6], [1, 2]]],
                    [
                        [[1, 2], [3, 4], [5, 6], [1, 2]],
                        [[1, 2], [3, 4], [5, 6], [1, 2]],
                    ],
                ],
            },
        ],
    }

    # when
    geometry_collection = GeometryCollection(**data)

    # then
    assert geometry_collection.type is GeoJSONObjectType.GEOMETRY_COLLECTION
    assert geometry_collection.geometries == [
        Point(type=GeoJSONObjectType.POINT, coordinates=(100.1, 80.2)),
        LineString(
            type=GeoJSONObjectType.LINE_STRING, coordinates=[(1.0, 2.0), (3.0, 4.0)]
        ),
        MultiPolygon(
            type=GeoJSONObjectType.MULTI_POLYGON,
            coordinates=[
                [[(1, 2), (3, 4), (5, 6), (1, 2)]],
                [
                    [(1, 2), (3, 4), (5, 6), (1, 2)],
                    [(1, 2), (3, 4), (5, 6), (1, 2)],
                ],
            ],
        ),
    ]


def test_parse_recursive_geometry_collection() -> None:
    # given
    data = {
        "type": "GeometryCollection",
        "geometries": [
            {
                "type": "Point",
                "coordinates": [100.1, 80.2],
            },
            {
                "type": "GeometryCollection",
                "geometries": [
                    {
                        "type": "Point",
                        "coordinates": [100.1, 80.2],
                    }
                ],
            },
        ],
    }

    # when
    geometry_collection = GeometryCollection(**data)

    # then
    assert geometry_collection.type is GeoJSONObjectType.GEOMETRY_COLLECTION
    assert geometry_collection.geometries == [
        Point(type=GeoJSONObjectType.POINT, coordinates=(100.1, 80.2)),
        GeometryCollection(
            type=GeoJSONObjectType.GEOMETRY_COLLECTION,
            geometries=[Point(type=GeoJSONObjectType.POINT, coordinates=(100.1, 80.2))],
        ),
    ]


def test_parse_bounded_geometry_collection() -> None:
    # given
    data = {
        "type": "GeometryCollection",
        "geometries": [
            {
                "type": "Point",
                "coordinates": [100.1, 80.2],
            },
        ],
    }

    # when
    geometry_collection = GeometryCollection[Point](**data)

    # then
    assert geometry_collection.type is GeoJSONObjectType.GEOMETRY_COLLECTION
    assert geometry_collection.geometries == [
        Point(type=GeoJSONObjectType.POINT, coordinates=(100.1, 80.2)),
    ]

    with pytest.raises(pydantic.ValidationError):
        GeometryCollection[Point](
            type=GeoJSONObjectType.GEOMETRY_COLLECTION,
            geometries=[
                {
                    "type": "LineString",
                    "coordinates": [[1, 2], [3, 4]],
                }
            ],
        )
