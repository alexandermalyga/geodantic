from collections.abc import Mapping, Sequence
from typing import Any, Literal

import pydantic
from pydantic.dataclasses import dataclass

from geodantic.base import GeoJSONObject, GeoJSONObjectType
from geodantic.geometries import AnyGeometry


@dataclass(frozen=True, kw_only=True, slots=True)
class Feature[GeometryT: AnyGeometry | None](GeoJSONObject):
    type: Literal[GeoJSONObjectType.FEATURE]
    geometry: GeometryT

    # TODO: Accept pydantic models https://github.com/pydantic/pydantic/issues/8489
    properties: Mapping[str, Any] | None
    id: str | int | None = None

    @pydantic.field_validator("id")
    @classmethod
    def _id_is_not_none(cls, value: Any) -> Any:
        # This validator will only run if the id was provided
        if value is None:
            raise ValueError("id cannot be None if present")
        return value


@dataclass(frozen=True, kw_only=True, slots=True)
class FeatureCollection(GeoJSONObject):
    type: Literal[GeoJSONObjectType.FEATURE_COLLECTION]
    features: Sequence[Feature]
