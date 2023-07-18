from __future__ import annotations

import math
from dataclasses import dataclass, field

from raytracer.materials import Material
from raytracer.intersections import Intersections, Intersection
from raytracer.matrix import Matrix
from raytracer.rays import Ray
from raytracer.tuple import Tuple, TupleType, vector, point, dot


@dataclass(slots=True, eq=False)
class Shape:
    """child classes must define `_local_intersect` and `_local_normal_at` to calculate their
    respective local values"""
    transform: Matrix = field(default_factory=Matrix.identity)
    material: Material = Material()
    parent: Group | None = None

    def _local_intersect(self, local_ray: Ray) -> Intersections:  # pragma: no cover
        raise NotImplementedError

    def intersect(self, ray: Ray) -> Intersections:
        """
        Calculate the time position(s) where the provided Ray intersects the shape.
        """
        # Apply the inverse of the shape's transformation to the ray to account for the desired
        # shape transformation
        transformed_ray = ray.transform(self.transform.inverse())
        return self._local_intersect(transformed_ray)

    def _local_normal_at(self, local_point: Tuple, hit: Intersection) -> Tuple:  # pragma: no cover
        raise NotImplementedError

    def normal_at(self, query: Tuple, hit: Intersection) -> Tuple:
        """
        Calculate the normal vector from the shape at the provided surface point.
        """
        if query.w != TupleType.POINT:
            raise ValueError("Query location must be a point.")

        # Shift the  point from world space to the object space
        local_point = self.world_to_object(query)
        local_normal = self._local_normal_at(local_point, hit)

        # shift this back to the world space by transforming it with the inverse transpose of the sphere's
        # transformation matrix
        world_normal = self.normal_to_world(local_normal)

        return world_normal

    def world_to_object(self, pt: Tuple) -> Tuple:
        if self.parent is not None:
            pt = self.parent.world_to_object(pt)

        return self.transform.inverse() * pt

    def normal_to_world(self, norm: Tuple) -> Tuple:
        norm = self.transform.inverse().transpose() * norm
        new_norm = vector(*norm).normalize()

        if self.parent is not None:
            new_norm = self.parent.normal_to_world(new_norm)

        return new_norm



@dataclass(slots=True, eq=False)
class Group(Shape):
    """
    Shape group representation.

    Groups are abstract shapes with no surface of their own, taking their form instead from the
    shapes they contain. This allows us to organize them into trees, with groups containing both
    other groups and concrete primatives. Group transforms are applied implicitly to any shapes
    contained by the group, simplifying calculations on its members.
    """

    children: set[Shape] = field(default_factory=set)

    def _local_intersect(self, transformed_ray: Ray) -> Intersections:
        all_inters = Intersections([])
        for child in self.children:
            all_inters.extend(child.intersect(transformed_ray))

        all_inters.sort()
        return all_inters

    def _local_normal_at(self, local_point: Tuple, hit: Intersection) -> Tuple:
        raise NotImplementedError("Groups shold be delegating this call to children.")

    def add_child(self, other: Shape) -> None:
        """Add a `Shape` subclass to the group & set its `parent` attribute appropriately."""
        self.children.add(other)
        other.parent = self

@dataclass(slots=True, eq=False)
class Sphere(Shape):
    """
    Spheres are assumed to be unit spheres, i.e. centered at `(0, 0, 0)` with a radius of `1`.
    """

    def _local_intersect(self, transformed_ray: Ray) -> Intersections:

        sphere_to_ray = transformed_ray.origin - point(0, 0, 0)
        a = dot(transformed_ray.direction, transformed_ray.direction)
        b = 2 * dot(transformed_ray.direction, sphere_to_ray)
        c = dot(sphere_to_ray, sphere_to_ray) - 1
        discriminant = b**2 - (4 * a * c)

        if discriminant < 0:
            intersections = []
        else:
            intersections = [
                Intersection(((-b - math.sqrt(discriminant))) / (2 * a), self),
                Intersection(((-b + math.sqrt(discriminant))) / (2 * a), self),
            ]

        return Intersections(intersections)

    def _local_normal_at(self, local_point: Tuple, hit: Intersection) -> Tuple:
        return local_point - point(0, 0, 0)
