from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass
from raytracer import NUMERIC_T, EPSILON
from enum import IntEnum


class TupleType(IntEnum):
    VECTOR = 0
    POINT = 1


@dataclass(frozen=True, slots=True)
class Tuple:
    """
    frozen -> makes it readonly class
    """
    x: NUMERIC_T
    y: NUMERIC_T
    z: NUMERIC_T
    w: TupleType

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tuple):
            return False
        return all(
            (self.w == other.w,
             math.isclose(self.x, other.x, abs_tol=EPSILON),
             math.isclose(self.x, other.x, abs_tol=EPSILON),
             math.isclose(self.z, other.z, abs_tol=EPSILON))
        )

    def __add__(self, other: Tuple) -> Tuple:
        return Tuple(x=self.x + other.x,
                     y=self.y + other.y,
                     z=self.z + other.z,
                     w=max(self.w, other.w))

    def __sub__(self, other: Tuple) -> Tuple:
        return Tuple(x=self.x - other.x,
                     y=self.y - other.y,
                     z=self.z - other.z,
                     w=abs(self.w - other.w))

    def __neg__(self) -> Tuple:
        return Tuple(
            x=-self.x,
            y=-self.y,
            z=-self.z,
            w=self.w,
        )

    def __mul__(self, other: object) -> Tuple:
        if not isinstance(other, (int | float)):
            return NotImplemented

        if isinstance(other, Tuple):
            return Tuple(x=self.x * other.x,
                         y=self.y * other.y,
                         z=self.z * other.z,
                         w=self.w)
        else:
            return Tuple(x=self.x * other,
                         y=self.y * other,
                         z=self.z * other,
                         w=self.w)

    def __rmul__(self, other: object) -> Tuple:
        return self * other

    def __truediv__(self, other: object) -> Tuple:
        if not isinstance(other, (int | float)):
            return NotImplemented

        if isinstance(other, Tuple):
            return Tuple(x=self.x / other.x,
                         y=self.y / other.y,
                         z=self.z / other.z,
                         w=self.w)
        else:
            return Tuple(x=self.x / other,
                         y=self.y / other,
                         z=self.z / other,
                         w=self.w)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Tuple:
        """Normalize into a unit Vector."""
        if self.w != TupleType.VECTOR:
            raise TypeError("Cannot normalize a non-Vector.")

        m = self.magnitude()
        return Tuple(
            x=self.x / m,
            y=self.y / m,
            z=self.z / m,
            w=self.w,
        )

    def reflect(self, normal: Tuple) -> Tuple:
        """Calculate the reflected vector."""
        if self.w != TupleType.VECTOR:
            raise ValueError("Cannot reflect a non-vector.")

        if normal.w != TupleType.VECTOR:
            raise ValueError("Normal must be a vector.")

        return self - (normal * 2 * dot(self, normal))
    

def point(x: NUMERIC_T, y: NUMERIC_T, z: NUMERIC_T) -> Tuple:
    return Tuple(x=x, y=y, z=z, w=TupleType.POINT)


def vector(x: NUMERIC_T, y: NUMERIC_T, z: NUMERIC_T) -> Tuple:
    return Tuple(x=x, y=y, z=z, w=TupleType.VECTOR)


def dot(left: Tuple, right: Tuple) -> NUMERIC_T:
    if not (left.w == TupleType.VECTOR and right.w == TupleType.VECTOR):
        raise ValueError(f"Both operands must be vectors. Received: {left.w} and {right.w}.")

    return (left.x * right.x) + (left.y * right.y) + (left.z * right.z)


def cross(left: Tuple, right: Tuple) -> Tuple:
    """
    Calculate the cross product of two Vectors.

    See: https://en.wikipedia.org/wiki/Cross_product
    """
    if not (left.w == TupleType.VECTOR and right.w == TupleType.VECTOR):
        raise ValueError(f"Both operands must be vectors. Received: {left.w} and {right.w}.")

    return Tuple(
        x=(left.y * right.z - left.z * right.y),
        y=(left.z * right.x - left.x * right.z),
        z=(left.x * right.y - left.y * right.x),
        w=TupleType.VECTOR,
    )


def is_point(inp: Tuple) -> bool:
    return inp.w == TupleType.POINT


def is_vector(inp: Tuple) -> bool:
    return inp.w == TupleType.VECTOR