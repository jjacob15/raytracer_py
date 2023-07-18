from __future__ import annotations

import math
import typing as t
from dataclasses import dataclass, field

from raytracer.color import black,white, Color
from raytracer.tuple import Tuple
from raytracer.transforms import Matrix

if t.TYPE_CHECKING:
    from raytracer.shapes import Shape


@dataclass(frozen=True, slots=True)
class Pattern:
    """
    Base class for creating pattern objects; this is not intended to be instantiated.
    """

    a: Color = field(default_factory=white)
    b: Color = field(default_factory=black)
    transform: Matrix = field(default_factory=Matrix.identity)

    def at_point(self, pt: Tuple) -> Tuple:
        raise NotImplementedError

    def at_object(self, obj: Shape, world_pt: Tuple) -> Tuple:
        object_pt = obj.world_to_object(world_pt)
        pattern_pt = self.transform.inverse() * object_pt

        return self.at_point(pattern_pt)


@dataclass(frozen=True, slots=True)
class Stripe(Pattern):
    def at_point(self, pt: Tuple) -> Tuple:
        if math.floor(pt.x) % 2 == 0:
            return self.a
        else:
            return self.b
