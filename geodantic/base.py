from abc import ABC
from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated, Any

import annotated_types as at
import pydantic
from pydantic.dataclasses import dataclass

type Longitude = Annotated[float, at.Ge(-180), at.Le(180)]
type Latitude = Annotated[float, at.Ge(-90), at.Le(90)]

type Position2D = tuple[Longitude, Latitude]
type Position3D = tuple[Longitude, Latitude, float]
type Position = Position2D | Position3D

type BoundingBox2D = tuple[Longitude, Latitude, Longitude, Latitude]
type BoundingBox3D = tuple[Longitude, Latitude, float, Longitude, Latitude, float]


def _validate_bbox(bbox: BoundingBox2D | BoundingBox3D) -> bool:
    first_position = (bbox[0], bbox[1])
    second_position = (bbox[2], bbox[3]) if len(bbox) == 4 else (bbox[3], bbox[4])
    return all(a <= b for a, b in zip(first_position, second_position))


type BoundingBox = Annotated[
    BoundingBox2D | BoundingBox3D,
    at.Predicate(_validate_bbox),
]


def _validate_linear_ring(ring: Sequence[Position]) -> bool:
    return ring[0] == ring[-1]


type LinearRing = Annotated[
    Sequence[Position],
    at.MinLen(4),
    at.Predicate(_validate_linear_ring),
]

type LineStringCoordinates = Annotated[Sequence[Position], at.MinLen(2)]
type PolygonCoordinates = Sequence[LinearRing]


class GeoJSONObjectType(StrEnum):
    POINT = "Point"
    MULTI_POINT = "MultiPoint"
    LINE_STRING = "LineString"
    MULTI_LINE_STRING = "MultiLineString"
    POLYGON = "Polygon"
    MULTI_POLYGON = "MultiPolygon"
    GEOMETRY_COLLECTION = "GeometryCollection"
    FEATURE = "Feature"
    FEATURE_COLLECTION = "FeatureCollection"


@dataclass(kw_only=True, slots=True)
class GeoJSONObject(ABC):
    type: GeoJSONObjectType
    bbox: BoundingBox | None = None

    @pydantic.field_validator("bbox")
    @classmethod
    def _bbox_is_not_none(cls, bbox: Any) -> Any:
        # This validator will only run if the bbox was provided
        if bbox is None:
            raise ValueError("bbox cannot be None if present")
        return bbox
