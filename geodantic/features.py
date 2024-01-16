from collections.abc import Mapping, Sequence
from typing import Annotated, Any, Literal

import pydantic

from geodantic.base import _GeoJSONObject
from geodantic.geometries import Geometry
from geodantic.types import GeoJSONObjectType


class Feature[
    GeometryT: Geometry | None,
    PropertiesT: Mapping[str, Any] | pydantic.BaseModel | None,
](_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.FEATURE]
    geometry: Annotated[GeometryT, pydantic.Field(discriminator="type")]
    properties: PropertiesT
    id: str | int | None = None

    @pydantic.field_validator("id")
    @classmethod
    def _id_is_not_none(cls, value: Any) -> Any:
        # This validator will only run if the id was provided
        if value is None:
            raise ValueError("id cannot be None if present")
        return value


class FeatureCollection[
    FeatureT: Feature[
        Geometry | None,
        Mapping[str, Any] | pydantic.BaseModel | None,
    ]
](_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.FEATURE_COLLECTION]
    features: Sequence[FeatureT]
