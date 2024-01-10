from collections.abc import Sequence
from typing import Annotated, Literal

import pydantic

from geodantic.base import _GeoJSONObject
from geodantic.types import (
    GeoJSONObjectType,
    LineStringCoordinates,
    PolygonCoordinates,
    Position,
)


class Point(_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.POINT]
    coordinates: Position


class MultiPoint(_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.MULTI_POINT]
    coordinates: Sequence[Position]


class LineString(_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.LINE_STRING]
    coordinates: LineStringCoordinates


class MultiLineString(_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.MULTI_LINE_STRING]
    coordinates: Sequence[LineStringCoordinates]


class Polygon(_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.POLYGON]
    coordinates: PolygonCoordinates


class MultiPolygon(_GeoJSONObject, frozen=True):
    type: Literal[GeoJSONObjectType.MULTI_POLYGON]
    coordinates: Sequence[PolygonCoordinates]


class GeometryCollection[GeometryT: "Geometry"](_GeoJSONObject, frozen=True):
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
