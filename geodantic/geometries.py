from abc import ABC
from collections.abc import Sequence
from typing import Annotated, Literal

import pydantic
from pydantic.dataclasses import dataclass

from geodantic.base import (
    GeoJSONObject,
    GeoJSONObjectType,
    LineStringCoordinates,
    PolygonCoordinates,
    Position,
)


@dataclass(frozen=True, kw_only=True, slots=True)
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


@dataclass(frozen=True, kw_only=True, slots=True)
class Point(Geometry):
    type: Literal[GeoJSONObjectType.POINT]
    coordinates: Position


@dataclass(frozen=True, kw_only=True, slots=True)
class MultiPoint(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_POINT]
    coordinates: Sequence[Position]


@dataclass(frozen=True, kw_only=True, slots=True)
class LineString(Geometry):
    type: Literal[GeoJSONObjectType.LINE_STRING]
    coordinates: LineStringCoordinates


@dataclass(frozen=True, kw_only=True, slots=True)
class MultiLineString(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_LINE_STRING]
    coordinates: Sequence[LineStringCoordinates]


@dataclass(frozen=True, kw_only=True, slots=True)
class Polygon(Geometry):
    type: Literal[GeoJSONObjectType.POLYGON]
    coordinates: PolygonCoordinates


@dataclass(frozen=True, kw_only=True, slots=True)
class MultiPolygon(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_POLYGON]
    coordinates: Sequence[PolygonCoordinates]


@dataclass(frozen=True, kw_only=True, slots=True)
class GeometryCollection[
    GeometryT: Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
](Geometry):
    type: Literal[GeoJSONObjectType.GEOMETRY_COLLECTION]
    geometries: Sequence[
        Annotated[
            GeometryT | "GeometryCollection",
            pydantic.Field(discriminator="type"),
        ]
    ]


type AnyGeometry = Annotated[
    Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | GeometryCollection,
    pydantic.Field(discriminator="type"),
]
