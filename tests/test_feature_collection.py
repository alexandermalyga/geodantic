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
            type="Feature",
            geometry=Point(type="Point", coordinates=[1, 2]),
            properties=None,
        ),
        Feature(
            type="Feature",
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
            type="Feature",
            geometry=None,
            properties=None,
        ),
    ]
