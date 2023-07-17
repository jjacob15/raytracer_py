from __future__ import annotations
from dataclasses import dataclass
from raytracer import NUMERIC_T
from raytracer.tuple import Tuple, TupleType
from raytracer.matrix import Matrix


@dataclass(slots=True)
class Ray:
    origin: Tuple
    direction: Tuple

    def __post_init__(self) -> None:
        if self.origin.w != TupleType.POINT:
            raise ValueError("Ray origin must be a point")

        if self.direction.w != TupleType.VECTOR:
            raise ValueError("Ray direction must be a vector")

    def position(self, t: NUMERIC_T) -> Tuple:
        # rays position after time "t"
        return self.origin + (self.direction * t)

    def transform(self, matrix: Matrix) -> Ray:
        "new ray after applying the transformation on both origin and direction"
        new_origin = self.origin * matrix
        new_direction = self.direction * matrix
        return Ray(new_origin, new_direction)
