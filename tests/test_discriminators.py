from typing import Any

import pydantic
import pytest

from geodantic import Feature, FeatureCollection, GeoJSONObject, Point, Polygon

type SomeGeometry = Point | FeatureCollection | Polygon


class SomeModel(pydantic.BaseModel):
    some_field: SomeGeometry = pydantic.Field(discriminator="type")


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {"type": "Point", "coordinates": [1, 2]},
            Point(type="Point", coordinates=[1, 2]),
        ),
        (
            {
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
                            "type": "Polygon",
                            "coordinates": [[[1, 2], [3, 4], [5, 6], [1, 2]]],
                        },
                        "properties": {"some_key": "some_value"},
                    },
                    {
                        "type": "Feature",
                        "geometry": None,
                        "properties": None,
                    },
                ],
            },
            FeatureCollection(
                type="FeatureCollection",
                features=[
                    Feature(
                        type="Feature",
                        geometry=Point(type="Point", coordinates=[1, 2]),
                        properties=None,
                    ),
                    Feature(
                        type="Feature",
                        geometry=Polygon(
                            type="Polygon",
                            coordinates=[[[1, 2], [3, 4], [5, 6], [1, 2]]],
                        ),
                        properties={"some_key": "some_value"},
                    ),
                    Feature(
                        type="Feature",
                        geometry=None,
                        properties=None,
                    ),
                ],
            ),
        ),
    ],
)
def test_discriminators(data: dict[str, Any], expected: GeoJSONObject) -> None:
    # when
    result = SomeModel(some_field=data)

    # then
    assert result.some_field == expected


def test_non_matching_discriminator() -> None:
    # given
    data = {"type": "MultiPoint", "coordinates": [[1, 2]]}

    with pytest.raises(pydantic.ValidationError) as e:
        # when
        SomeModel(some_field=data)
