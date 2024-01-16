from typing import Any

import pydantic
import pytest

from geodantic import (
    Feature,
    FeatureCollection,
    GeoJSONObjectType,
    GeometryCollection,
    Point,
)


def test_parse_feature_collection_with_zero_features() -> None:
    # given
    data = {
        "type": "FeatureCollection",
        "features": [],
    }

    # when
    feature_collection = FeatureCollection(**data)

    # then
    assert feature_collection.type is GeoJSONObjectType.FEATURE_COLLECTION
    assert feature_collection.features == []


def test_parse_feature_collection() -> None:
    # given
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1, 2]},
                "properties": None,
            },
            {
                "type": "Feature",
                "geometry": {
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
                },
                "properties": {"some_key": "some_value"},
            },
            {
                "type": "Feature",
                "geometry": None,
                "properties": None,
            },
        ],
    }

    # when
    feature_collection = FeatureCollection(**data)

    # then
    assert feature_collection.type is GeoJSONObjectType.FEATURE_COLLECTION
    assert feature_collection.features == [
        Feature(
            type=GeoJSONObjectType.FEATURE,
            geometry=Point(type=GeoJSONObjectType.POINT, coordinates=[1, 2]),
            properties=None,
        ),
        Feature(
            type=GeoJSONObjectType.FEATURE,
            geometry=GeometryCollection(
                type=GeoJSONObjectType.GEOMETRY_COLLECTION,
                geometries=[
                    Point(type=GeoJSONObjectType.POINT, coordinates=(100.1, 80.2)),
                    GeometryCollection(
                        type=GeoJSONObjectType.GEOMETRY_COLLECTION,
                        geometries=[
                            Point(
                                type=GeoJSONObjectType.POINT,
                                coordinates=(100.1, 80.2),
                            )
                        ],
                    ),
                ],
            ),
            properties={"some_key": "some_value"},
        ),
        Feature(
            type=GeoJSONObjectType.FEATURE,
            geometry=None,
            properties=None,
        ),
    ]


def test_parse_bounded_feature_collection() -> None:
    # given
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {
                            "type": "Point",
                            "coordinates": [100.1, 80.2],
                        }
                    ],
                },
                "properties": {"some_key": "some_value"},
            },
        ],
    }

    # when
    feature_collection = FeatureCollection[
        Feature[GeometryCollection[Point], dict[str, Any]]
    ](**data)

    # then
    assert feature_collection.type is GeoJSONObjectType.FEATURE_COLLECTION
    assert feature_collection.features == [
        Feature(
            type=GeoJSONObjectType.FEATURE,
            geometry=GeometryCollection(
                type=GeoJSONObjectType.GEOMETRY_COLLECTION,
                geometries=[
                    Point(
                        type=GeoJSONObjectType.POINT,
                        coordinates=(100.1, 80.2),
                    )
                ],
            ),
            properties={"some_key": "some_value"},
        ),
    ]


def test_parse_invalid_bounded_feature_collection() -> None:
    # given
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [100.1, 80.2],
                },
                "properties": None,
            },
        ],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        FeatureCollection[Feature[GeometryCollection[Point], dict[str, Any]]](**data)
