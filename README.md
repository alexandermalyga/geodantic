# geodantic

[![pypi](https://img.shields.io/pypi/v/geodantic.svg)](https://pypi.python.org/pypi/geodantic)
[![versions](https://img.shields.io/pypi/pyversions/geodantic.svg)](https://github.com/alexandermalyga/geodantic)

Lightweight, type-safe and spec-conforming [GeoJSON](https://datatracker.ietf.org/doc/html/rfc7946) parsing and validation using Pydantic.

## Installation

```
pip install geodantic
```

## Examples

Parse and validate GeoJSON features with custom properties:

```python
import pydantic
from geodantic import Feature, Point

# Use your own properties Pydantic models
@pydantic.dataclasses.dataclass
class MyProperties:
    foo: str

data = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [1, 2]},
    "properties": {"foo": "abc"},
}

# Parse and validate data into spec-conforming objects
parsed = Feature[Point, MyProperties](**data)
"""
Feature[Point, MyProperties](
    type=<GeoJSONObjectType.FEATURE: 'Feature'>, 
    bbox=None, 
    geometry=Point(
        type=<GeoJSONObjectType.POINT: 'Point'>, 
        bbox=None, 
        coordinates=(1.0, 2.0)
    ), 
    properties=MyProperties(foo='abc'), 
    id=None
)
"""

# Dump back into JSON using standard Pydantic methods
parsed.model_dump_json(exclude_unset=True, indent=2)
"""
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      1.0,
      2.0
    ]
  },
  "properties": {
    "foo": "abc"
  }
}
"""
```

Parse objects of arbitrary types:

```python
from geodantic import GeometryCollection

data = {
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "Polygon",
            "coordinates": [[[1, 2], [3, 4], [5, 6], [1, 2]]],
            "bbox": [1, 2, 3, 4],
        },
        {
            "type": "GeometryCollection",
            "geometries": [{"type": "Point", "coordinates": [1, 2]}],
        },
    ],
}

# Parse any geometry type
parsed = GeometryCollection(**data)
"""
GeometryCollection(
    type=<GeoJSONObjectType.GEOMETRY_COLLECTION: 'GeometryCollection'>, 
    bbox=None, 
    geometries=[
        Polygon(
            type=<GeoJSONObjectType.POLYGON: 'Polygon'>, 
            bbox=(1.0, 2.0, 3.0, 4.0), 
            coordinates=[[(1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (1.0, 2.0)]]
        ), 
        GeometryCollection(
            type=<GeoJSONObjectType.GEOMETRY_COLLECTION: 'GeometryCollection'>, 
            bbox=None, 
            geometries=[
                Point(
                    type=<GeoJSONObjectType.POINT: 'Point'>, 
                    bbox=None, 
                    coordinates=(1.0, 2.0)
                )
            ]
        )
    ]
)
"""
```

## Contributing

Set up the project using [Poetry](https://python-poetry.org/):

```
poetry install
```

Format the code:

```
make lint
```

Run tests:

```
make test
```

Check for typing and format issues:

```
make check
```
