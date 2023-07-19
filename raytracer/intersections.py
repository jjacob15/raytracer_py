from __future__ import annotations

import math
import typing as t
from collections import UserList
from dataclasses import dataclass,field

from raytracer import NUMERIC_T, EPSILON
from raytracer.rays import Ray
from raytracer.tuple import Tuple, dot

if t.TYPE_CHECKING:
    from raytracer.shapes import Shape


@dataclass(frozen=True, slots=True)
class Intersection:
    t: NUMERIC_T
    obj: Shape
    u: NUMERIC_T = 0
    v: NUMERIC_T = 0


class Intersections(UserList):

    def __init__(self, data: t.Generator[Intersection]) -> None:
        self.data = list(data)
        self.sort()

    def sort(self):
        self.data.sort(key = lambda x: x.t)

    def hit(self) -> Intersection | None:
        """loweset non negative intersection"""
        for intersect in self.data:
            if intersect.t > 0:
                return intersect

        return None


@dataclass(slots=True)
class IntersectionComp:
    t: NUMERIC_T
    obj: Shape
    point: Tuple
    eye_v: Tuple
    normal: Tuple
    inside: bool
    reflect_v: Tuple
    n1: NUMERIC_T  # Material being exited
    n2: NUMERIC_T  # Material being entered
    over_point: Tuple = field(init=False)
    under_point: Tuple = field(init=False)

    def __post_init__(self) -> None:
        self.over_point = self.point + self.normal * EPSILON
        self.under_point = self.point - self.normal * EPSILON


def _calc_refractive_indices(inter: Intersection, all_inters: Intersections) -> tuple[NUMERIC_T, NUMERIC_T]:
    containers: list[Shape] = []
    for i in all_inters:
        if i == inter:
            if not containers:
                n1: NUMERIC_T = 1.0
            else:
                n1 = containers[-1].material.refractive_index

        if i.obj in containers:
            containers.remove(i.obj)
        else:
            containers.append(i.obj)
        
        if i == inter:
            if not containers:
                n2: NUMERIC_T = 1.0
            else:
                n2 = containers[-1].material.refractive_index

    return n1, n2


def prepare_computation(inter: Intersection, ray: Ray, all_inters: Intersections | None = None) -> IntersectionComp:
    """
    helps with computation of ray's intersections
    If all intersections is None, seed it with the incoming intersection.
    """

    if all_inters is None:
        all_inters = Intersections([inter])

    point = ray.position(inter.t)
    eye_v = -ray.direction

    normal = inter.obj.normal_at(point, inter)
    if dot(normal, eye_v) < 0:
        inside = True
        normal = -normal
    else:
        inside = False

    reflect_v = ray.direction.reflect(normal)
    n1, n2 = _calc_refractive_indices(inter, all_inters)

    return IntersectionComp(
        t=inter.t,
        obj=inter.obj,
        point=point,
        eye_v=eye_v,
        normal=normal,
        inside=inside,
        reflect_v=reflect_v,
        n1=n1,
        n2=n2
    )


def schlick(comps: IntersectionComp) -> float:
    """
    Schlick approximation to determine surface reflectance at the intersection point.
    """
    cos = dot(comps.eye_v, comps.normal)

    # Total internal reflection can only occur if n1 > n2
    if comps.n1 > comps.n2:
        n = comps.n1 / comps.n2
        sin2_t = n**2 * (1.0 - cos**2)

        if sin2_t > 1:
            return 1.0

        cos_t = math.sqrt(1.0 - sin2_t)
        cos = cos_t

    r0 = ((comps.n1 - comps.n2) / (comps.n1 + comps.n2)) ** 2
    return r0 + (1 - r0) * (1 - cos) ** 5
