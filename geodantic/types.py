from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated

import annotated_types as at

type Longitude = Annotated[float, at.Ge(-180), at.Le(180)]
type Latitude = Annotated[float, at.Ge(-90), at.Le(90)]

type Position2D = tuple[Longitude, Latitude]
type Position3D = tuple[Longitude, Latitude, float]
type Position = Position2D | Position3D


def _validate_bbox(bbox: tuple[float, ...]) -> bool:
    middle = len(bbox) // 2
    return bbox[0] <= bbox[middle] and bbox[1] <= bbox[middle + 1]


type BoundingBox2D = Annotated[
    tuple[Longitude, Latitude, Longitude, Latitude],
    at.Predicate(_validate_bbox),
]

type BoundingBox3D = Annotated[
    tuple[Longitude, Latitude, float, Longitude, Latitude, float],
    at.Predicate(_validate_bbox),
]

type BoundingBox = BoundingBox2D | BoundingBox3D


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
