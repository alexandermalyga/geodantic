from abc import ABC
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


class Point(Geometry):
    type: Literal[GeoJSONObjectType.POINT]
    coordinates: Position


class MultiPoint(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_POINT]
    coordinates: Sequence[Position]


class LineString(Geometry):
    type: Literal[GeoJSONObjectType.LINE_STRING]
    coordinates: LineStringCoordinates


class MultiLineString(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_LINE_STRING]
    coordinates: Sequence[LineStringCoordinates]


class Polygon(Geometry):
    type: Literal[GeoJSONObjectType.POLYGON]
    coordinates: PolygonCoordinates


class MultiPolygon(Geometry):
    type: Literal[GeoJSONObjectType.MULTI_POLYGON]
    coordinates: Sequence[PolygonCoordinates]


class GeometryCollection[GeometryT: "AnyGeometry"](Geometry):
    type: Literal[GeoJSONObjectType.GEOMETRY_COLLECTION]
    geometries: Sequence[
        Annotated[
            GeometryT,
            pydantic.Field(discriminator="type"),
        ]
    ]


type AnyGeometry = (
    Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | GeometryCollection
)
