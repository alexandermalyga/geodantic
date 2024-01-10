from abc import ABC
from typing import Any

import pydantic

from geodantic.types import BoundingBox, GeoJSONObjectType


class _GeoJSONObject(pydantic.BaseModel, ABC, frozen=True):
    type: GeoJSONObjectType
    bbox: BoundingBox | None = None

    @pydantic.field_validator("bbox")
    @classmethod
    def _bbox_is_not_none(cls, bbox: Any) -> Any:
        # This validator will only run if the bbox was provided
        if bbox is None:
            raise ValueError("bbox cannot be None if present")
        return bbox
