from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pydantic.dataclasses import dataclass

from geodantic.base import GeoJSONObject, GeoJSONObjectType
from geodantic.geometry import AnyGeometry


@dataclass(kw_only=True, slots=True)
class Feature[GeometryT: AnyGeometry | None](GeoJSONObject):
    type: Literal[GeoJSONObjectType.FEATURE]

    # TODO: How does this parse to the correct type without a discriminator field? Is performance
    # better with an explicit discriminator?
    geometry: GeometryT

    # TODO: Accept pydantic models
    properties: Mapping[str, Any] | None

    # TODO: Is null allowed here? Use sentinel value instead?
    id: str | int | None = None


@dataclass(kw_only=True, slots=True)
class FeatureCollection(GeoJSONObject):
    type: Literal[GeoJSONObjectType.FEATURE_COLLECTION]
    features: Sequence[Feature]
