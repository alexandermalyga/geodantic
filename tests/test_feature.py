from typing import Any

import pydantic
import pytest

from geodantic import (
    Feature,
    GeoJSONObjectType,
    Geometry,
    GeometryCollection,
    Point,
    Polygon,
)


def test_parse_feature_with_null_geometry() -> None:
    # given
    data = {
        "type": "Feature",
        "geometry": None,
        "properties": None,
    }

    # when
    feature = Feature(**data)

    # then
    assert feature.type is GeoJSONObjectType.FEATURE
    assert feature.geometry is None
    assert feature.properties is None
    assert feature.id is None


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {"type": "Point", "coordinates": [1, 2]},
            Point(type="Point", coordinates=[1, 2]),
        ),
        (
            {
                "type": "Polygon",
                "coordinates": [[[1, 2], [3, 4], [5, 6], [1, 2]]],
            },
            Polygon(
                type="Polygon",
                coordinates=[[[1, 2], [3, 4], [5, 6], [1, 2]]],
            ),
        ),
        (
            {
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
            GeometryCollection(
                type=GeoJSONObjectType.GEOMETRY_COLLECTION,
                geometries=[
                    Point(type=GeoJSONObjectType.POINT, coordinates=(100.1, 80.2)),
                    GeometryCollection(
                        type=GeoJSONObjectType.GEOMETRY_COLLECTION,
                        geometries=[
                            Point(
                                type=GeoJSONObjectType.POINT, coordinates=(100.1, 80.2)
                            )
                        ],
                    ),
                ],
            ),
        ),
    ],
)
def test_parse_feature_with_geometry(data: dict[str, Any], expected: Geometry) -> None:
    # when
    feature = Feature(type=GeoJSONObjectType.FEATURE, geometry=data, properties=None)

    # then
    assert feature.type is GeoJSONObjectType.FEATURE
    assert feature.geometry == expected
    assert feature.properties is None
    assert feature.id is None


def test_parse_feature_without_geometry() -> None:
    # given
    data = {
        "type": "Feature",
        "properties": None,
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Feature(**data)


def test_parse_feature_without_properties() -> None:
    # given
    data = {
        "type": "Feature",
        "geometry": None,
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Feature(**data)


def test_parse_feature_with_mapping_properties() -> None:
    # given
    data = {
        "type": "Feature",
        "geometry": None,
        "properties": {"some_key": 123},
    }

    # when
    feature = Feature(**data)

    # then
    assert feature.type is GeoJSONObjectType.FEATURE
    assert feature.geometry is None
    assert feature.properties == {"some_key": 123}
    assert feature.id is None


def test_parse_feature_with_invalid_properties() -> None:
    # given
    data = {
        "type": "Feature",
        "geometry": None,
        "properties": 123,
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Feature(**data)


@pytest.mark.parametrize("value", [1, "some-id", None])
def test_parse_feature_with_id(value: str | int | None) -> None:
    # given
    data = {
        "type": "Feature",
        "geometry": None,
        "properties": None,
        "id": value,
    }

    # when
    feature = Feature(**data)

    # then
    assert feature.type is GeoJSONObjectType.FEATURE
    assert feature.geometry is None
    assert feature.properties is None
    assert feature.id == value


def test_parse_feature_with_invalid_id() -> None:
    # given
    data = {
        "type": "Feature",
        "geometry": None,
        "properties": None,
        "id": [1, 2, 3],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Feature(**data)