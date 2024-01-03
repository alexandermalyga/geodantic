import pydantic
import pytest

from geodantic import GeoJSONObjectType, MultiPoint


def test_parse_multi_point_with_zero_points() -> None:
    # given
    data = {
        "type": "MultiPoint",
        "coordinates": [],
    }

    # when
    multi_point = MultiPoint(**data)

    # then
    assert multi_point.type is GeoJSONObjectType.MULTI_POINT
    assert multi_point.coordinates == []


def test_parse_multi_point_with_one_point() -> None:
    # given
    data = {
        "type": "MultiPoint",
        "coordinates": [[100.1, 80.2]],
    }

    # when
    multi_point = MultiPoint(**data)

    # then
    assert multi_point.type is GeoJSONObjectType.MULTI_POINT
    assert multi_point.coordinates == [(100.1, 80.2)]


def test_parse_multi_point_with_multiple_points() -> None:
    # given
    data = {
        "type": "MultiPoint",
        "coordinates": [[1.1, 2.2], [3.1, 4.2], [5.1, 6.2]],
    }

    # when
    multi_point = MultiPoint(**data)

    # then
    assert multi_point.type is GeoJSONObjectType.MULTI_POINT
    assert multi_point.coordinates == [(1.1, 2.2), (3.1, 4.2), (5.1, 6.2)]


def test_parse_multi_point_with_three_coordinates() -> None:
    # given
    data = {
        "type": "MultiPoint",
        "coordinates": [[100.1, 80.2, 900]],
    }

    # when
    multi_point = MultiPoint(**data)

    # then
    assert multi_point.type is GeoJSONObjectType.MULTI_POINT
    assert multi_point.coordinates == [(100.1, 80.2, 900)]


def test_parse_multi_point_with_invalid_coordinates() -> None:
    # given
    data = {
        "type": "MultiPoint",
        "coordinates": [[180.1, 80.2]],
    }

    with pytest.raises(pydantic.ValidationError):
        # when
        MultiPoint(**data)
