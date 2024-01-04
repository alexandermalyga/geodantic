from typing import Annotated

import pydantic

from .base import (
    BoundingBox,
    BoundingBox2D,
    BoundingBox3D,
    GeoJSONObject,
    GeoJSONObjectType,
    Latitude,
    LinearRing,
    LineStringCoordinates,
    Longitude,
    PolygonCoordinates,
    Position,
    Position2D,
    Position3D,
)
from .features import Feature, FeatureCollection
from .geometries import (
    AnyGeometry,
    Geometry,
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

type AnyGeoJSONObject = Annotated[
    Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | GeometryCollection
    | Feature
    | FeatureCollection,
    pydantic.Field(discriminator="type"),
]

__all__ = [
    "AnyGeoJSONObject",
    "AnyGeometry",
    "BoundingBox",
    "BoundingBox2D",
    "BoundingBox3D",
    "Feature",
    "FeatureCollection",
    "GeoJSONObject",
    "GeoJSONObjectType",
    "Geometry",
    "GeometryCollection",
    "Latitude",
    "LinearRing",
    "LineString",
    "LineStringCoordinates",
    "Longitude",
    "MultiLineString",
    "MultiPoint",
    "MultiPolygon",
    "Point",
    "Polygon",
    "PolygonCoordinates",
    "Position",
    "Position2D",
    "Position3D",
]
