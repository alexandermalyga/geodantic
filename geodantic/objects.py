from abc import ABC
from collections.abc import Mapping, Sequence
from enum import StrEnum
from typing import Annotated, Any, Literal

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


@dataclass(kw_only=True, slots=True)
class Geometry(GeoJSONObject, ABC):
    type: Literal[
        GeoJSONObjectType.POINT,
        GeoJSONObjectType.MULTI_POINT,
        GeoJSONObjectType.LINE_STRING,
        GeoJSONObjectType.MULTI_LINE_STRING,
        GeoJSONObjectType.POLYGON,
        GeoJSONObjectType.MULTI_POLYGON,
        GeoJSONObjectType.GEOMETRY_COLLECTION,
    ]


@dataclass(kw_only=True, slots=True)
class Point(Geometry):
    type: Literal[GeoJSONObjectType.POINT]
    coordinates: Position


@dataclass(kw_only=True, slots=True)
class MultiPoint(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_POINT]
    coordinates: Sequence[Position]


@dataclass(kw_only=True, slots=True)
class LineString(Geometry):
    type: Literal[GeoJSONObjectType.LINE_STRING]
    coordinates: LineStringCoordinates


@dataclass(kw_only=True, slots=True)
class MultiLineString(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_LINE_STRING]
    coordinates: Sequence[LineStringCoordinates]


@dataclass(kw_only=True, slots=True)
class Polygon(Geometry):
    type: Literal[GeoJSONObjectType.POLYGON]
    coordinates: PolygonCoordinates


@dataclass(kw_only=True, slots=True)
class MultiPolygon(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_POLYGON]
    coordinates: Sequence[PolygonCoordinates]


@dataclass(kw_only=True, slots=True)
class GeometryCollection[
    GeometryT: Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
](Geometry):
    type: Literal[GeoJSONObjectType.GEOMETRY_COLLECTION]

    # TODO: Is there any way of defining a recursive generic class?
    geometries: Sequence[GeometryT | "GeometryCollection"]


@dataclass(kw_only=True, slots=True)
class Feature[
    GeometryT: Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | GeometryCollection
    | None
](GeoJSONObject):
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
