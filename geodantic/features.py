from collections.abc import Mapping, Sequence
from typing import Any, Literal

import pydantic

from geodantic.base import GeoJSONObject, GeoJSONObjectType
from geodantic.geometries import AnyGeometry


class Feature[
    GeometryT: AnyGeometry | None,
    PropertiesT: Mapping[str, Any] | pydantic.BaseModel | None,
](GeoJSONObject):
    type: Literal[GeoJSONObjectType.FEATURE]
    geometry: GeometryT
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
    GeometryT: AnyGeometry | None,
    PropertiesT: Mapping[str, Any] | pydantic.BaseModel | None,
](GeoJSONObject):
    type: Literal[GeoJSONObjectType.FEATURE_COLLECTION]
    features: Sequence[Feature[GeometryT, PropertiesT]]
