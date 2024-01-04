from abc import ABC
from enum import StrEnum
from typing import Annotated, Any, Literal, Mapping

import annotated_types as at
from pydantic.dataclasses import dataclass

type Longitude = Annotated[float, at.Ge(-180), at.Le(180)]
type Latitude = Annotated[float, at.Ge(-90), at.Le(90)]
type Position = tuple[Longitude, Latitude] | tuple[Longitude, Latitude, float]
type LineStringCoordinates = Annotated[list[Position], at.MinLen(2)]
type BoundingBox2D = tuple[Longitude, Latitude, Longitude, Latitude]
type BoundingBox3D = tuple[Longitude, Latitude, float, Longitude, Latitude, float]
type BoundingBox = Annotated[
    BoundingBox2D | BoundingBox3D,
    at.Predicate(
        lambda b: (b[0], b[1]) <= ((b[2], b[3]) if len(b) == 4 else (b[3], b[4]))
    ),
]
type LinearRing = Annotated[
    list[Position],
    at.MinLen(4),
    at.Predicate(lambda r: r[0] == r[-1]),
]
type PolygonCoordinates = list[LinearRing]


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
    # TODO: https://datatracker.ietf.org/doc/html/rfc7946#section-6.1


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
    coordinates: list[Position]


@dataclass(kw_only=True, slots=True)
class LineString(Geometry):
    type: Literal[GeoJSONObjectType.LINE_STRING]
    coordinates: LineStringCoordinates


@dataclass(kw_only=True, slots=True)
class MultiLineString(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_LINE_STRING]
    coordinates: list[LineStringCoordinates]


@dataclass(kw_only=True, slots=True)
class Polygon(Geometry):
    type: Literal[GeoJSONObjectType.POLYGON]
    coordinates: PolygonCoordinates


@dataclass(kw_only=True, slots=True)
class MultiPolygon(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_POLYGON]
    coordinates: list[PolygonCoordinates]


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
    geometries: list[GeometryT | "GeometryCollection"]


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
    features: list[Feature]
