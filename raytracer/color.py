from __future__ import annotations
from dataclasses import dataclass
from raytracer import NUMERIC_T, EPSILON
import math
import typing as t


@dataclass
class Color:
    r: NUMERIC_T
    g: NUMERIC_T
    b: NUMERIC_T

    def __iter__(self) -> t.Generator[int, None, None]:
        yield self.r
        yield self.g
        yield self.b

    def __add__(self, other: Color) -> Color:
        if not isinstance(other, Color):
            raise ValueError("Cannot add if its not a color")
        return Color(
            r=self.r + other.r,
            g=self.g + other.g,
            b=self.b + other.b)

    def __sub__(self, other: Color) -> Color:
        if not isinstance(other, Color):
            raise ValueError("Cannot add if its not a color")
        return Color(
            r=self.r - other.r,
            g=self.g - other.g,
            b=self.b - other.b)

    def __mul__(self, other: object) -> Color:
        if isinstance(other, Color):  # check if the instance is of type Color
            return Color(
                r=self.r * other.r,
                g=self.g * other.g,
                b=self.b * other.b)

        elif isinstance(other, float):
            return Color(
                r=self.r * other,
                g=self.g * other,
                b=self.b * other)

        else:
            return NotImplemented  # returning NotImplemented allows python to try other variations

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return False
        return all(
            (math.isclose(self.r, other.r, abs_tol=EPSILON),
             math.isclose(self.g, other.g, abs_tol=EPSILON),
             math.isclose(self.b, other.b, abs_tol=EPSILON)))


def black():
    return Color(0, 0, 0)
BLUE = Color(0.537, 0.831, 0.914)
PURPLE = Color(0.373, 0.404, 0.550)
RED = Color(0.941, 0.322, 0.388)
def white():
    return Color(1, 1, 1)