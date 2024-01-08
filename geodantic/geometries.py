from collections.abc import Sequence
from typing import Annotated, Literal

import pydantic

from geodantic.base import (
    GeoJSONObject,
    GeoJSONObjectType,
    LineStringCoordinates,
    PolygonCoordinates,
    Position,
)


class Point(GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.POINT]
    coordinates: Position


class MultiPoint(GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.MULTI_POINT]
    coordinates: Sequence[Position]


class LineString(GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.LINE_STRING]
    coordinates: LineStringCoordinates


class MultiLineString(GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.MULTI_LINE_STRING]
    coordinates: Sequence[LineStringCoordinates]


class Polygon(GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.POLYGON]
    coordinates: PolygonCoordinates


class MultiPolygon(GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.MULTI_POLYGON]
    coordinates: Sequence[PolygonCoordinates]


class GeometryCollection[GeometryT: "Geometry"](GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.GEOMETRY_COLLECTION]
    geometries: Sequence[
        Annotated[
            GeometryT,
            pydantic.Field(discriminator="type"),
        ]
    ]


type Geometry = (
    Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | GeometryCollection
)
