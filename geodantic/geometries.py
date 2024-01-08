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


class Point(GeoJSONObject):
    type: Literal[GeoJSONObjectType.POINT]
    coordinates: Position


class MultiPoint(GeoJSONObject):
    type: Literal[GeoJSONObjectType.MULTI_POINT]
    coordinates: Sequence[Position]


class LineString(GeoJSONObject):
    type: Literal[GeoJSONObjectType.LINE_STRING]
    coordinates: LineStringCoordinates


class MultiLineString(GeoJSONObject):
    type: Literal[GeoJSONObjectType.MULTI_LINE_STRING]
    coordinates: Sequence[LineStringCoordinates]


class Polygon(GeoJSONObject):
    type: Literal[GeoJSONObjectType.POLYGON]
    coordinates: PolygonCoordinates


class MultiPolygon(GeoJSONObject):
    type: Literal[GeoJSONObjectType.MULTI_POLYGON]
    coordinates: Sequence[PolygonCoordinates]


class GeometryCollection[GeometryT: "Geometry"](GeoJSONObject):
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
