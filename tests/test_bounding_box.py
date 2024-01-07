import pydantic
import pytest

from geodantic import BoundingBox, GeoJSONObjectType, Point


def test_parse_object_without_bbox() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
    }

    # when
    point = Point(**data)

    # then
    assert point.type is GeoJSONObjectType.POINT
    assert point.coordinates == (100.1, 80.2)
    assert point.bbox is None


def test_parse_object_with_null_bbox() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
        "bbox": None,
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


def test_parse_object_with_empty_bbox() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
        "bbox": [],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


def test_parse_object_with_2d_bbox() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
        "bbox": [100.1, 80.2, 100.1, 80.2],
    }

    # when
    point = Point(**data)

    # then
    assert point.type is GeoJSONObjectType.POINT
    assert point.coordinates == (100.1, 80.2)
    assert point.bbox == (100.1, 80.2, 100.1, 80.2)


def test_parse_object_with_3d_bbox() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
        "bbox": [100.1, 80.2, 1000, 100.1, 80.2, 1000],
    }

    # when
    point = Point(**data)

    # then
    assert point.type is GeoJSONObjectType.POINT
    assert point.coordinates == (100.1, 80.2)
    assert point.bbox == (100.1, 80.2, 1000, 100.1, 80.2, 1000)


def test_parse_object_with_too_short_bbox() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
        "bbox": [1, 2, 3],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


def test_parse_object_with_too_long_bbox() -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
        "bbox": [1, 2, 3, 4, 5, 6, 7],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)


@pytest.mark.parametrize(
    "bbox",
    [
        [1, 2, 0, 4],
        [1, 2, 3, 1],
        [1, 2, 1000, 0, 4, 1000],
        [1, 2, 1000, 3, 1, 1000],
    ],
)
def test_parse_object_with_bbox_with_invalid_axes(bbox: BoundingBox) -> None:
    # given
    data = {
        "type": "Point",
        "coordinates": [100.1, 80.2],
        "bbox": bbox,
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        Point(**data)
