from __future__ import annotations

import math
from dataclasses import dataclass

from raytracer.color import BLACK, WHITE, Color
from raytracer.intersections import IntersectionComp, Intersections, prepare_computation, schlick
from raytracer.lights import PointLight, lighting
from raytracer.materials import Material
from raytracer.tuple import Tuple, dot, point
from raytracer.rays import Ray
from raytracer.shapes import Shape, Sphere
from raytracer.transforms import scaling

DEFAULT_LIGHT = PointLight(point(-10, 10, -10), WHITE)

REF_LIMIT = 5


@dataclass(slots=True)
class World:
    light: PointLight
    objects: list[Shape]

    def intersect_world(self, ray: Ray) -> Intersections:
        """
        Calculate the `Ray`'s intersections with all objects in the current world.
        """
        all_intersections = Intersections([])
        for obj in self.objects:
            all_intersections.extend(obj.intersect(ray))

        all_intersections.sort()
        return all_intersections

    def _shade_hit(self, comps: IntersectionComp, remaining: int = REF_LIMIT) -> Color:
        """
        Calculate the color at the provided pre-computed intersection point in the world.

        """
        shadowed = self.is_shadowed(comps.over_point)
        surface = lighting(
            material=comps.obj.material,
            obj=comps.obj,
            light=self.light,
            surf_pos=comps.point,
            eye_v=comps.eye_v,
            normal=comps.normal,
            in_shadow=shadowed,
        )
        reflected = self.reflected_color(comps, remaining=remaining)
        refracted = self.refracted_color(comps, remaining=remaining)

        # Check if the surface material is both transparent and reflective, if it is then we'll use
        # the Schlick approximation to combine them.
        if comps.obj.material.reflective > 0 and comps.obj.material.transparency > 0:
            reflectance = schlick(comps)
            return surface + (reflected * reflectance) + (refracted * (1 - reflectance))
        else:
            return surface + reflected + refracted

    def color_at(self, r: Ray, remaining: int = REF_LIMIT) -> Color:
        """
        Calculate the color at the `Ray`'s first intersection point in the world.
        """
        hit = self.intersect_world(r).hit
        if not hit:
            return BLACK

        comps = prepare_computation(hit, r)
        return self._shade_hit(comps, remaining=remaining)

    def is_shadowed(self, pt: Tuple) -> bool:
        """Determine if the query point is shadowed by a world object."""
        pt_v = self.light.position - pt
        pt_dist = pt_v.magnitude()
        pt_dir = pt_v.normalize()
        r = Ray(pt, pt_dir)

        intersections = self.intersect_world(r)
        h = intersections.hit
        if h and h.t < pt_dist:  # Make sure hit isn't past the light source
            return True
        else:
            return False

    def reflected_color(self, comps: IntersectionComp, remaining: int = REF_LIMIT) -> Color:
        """
        Determine the reflected color for the provided precomputed intersection.
        """
        if comps.obj.material.reflective == 0:
            return BLACK
        if remaining <= 0:
            return BLACK

        reflect_ray = Ray(comps.over_point, comps.reflect_v)
        col = self.color_at(reflect_ray, remaining=remaining - 1)
        return col * comps.obj.material.reflective

    def refracted_color(self, comps: IntersectionComp, remaining: int = REF_LIMIT) -> Color:
        """
        Determine the reflected color for the provided precomputed intersection.
        """
        if comps.obj.material.transparency == 0:
            return BLACK
        if remaining <= 0:
            return BLACK

        n_ratio = comps.n1 / comps.n2
        cos_i = dot(comps.eye_v, comps.normal)
        sin2_t = n_ratio**2 * (1 - cos_i**2)

        if sin2_t > 1:
            return BLACK

        cos_t = math.sqrt(1.0 - sin2_t)
        direction = comps.normal * (n_ratio * cos_i - cos_t) - comps.eye_v * n_ratio
        refract_ray = Ray(comps.under_point, direction)

        color = self.color_at(refract_ray, remaining - 1) * comps.obj.material.transparency
        return color

    @staticmethod
    def default_world() -> World:  # pragma: no cover
        """Create a basic world containing two concentric spheres of varying material properties."""
        s1 = Sphere(material=Material(color=Color(0.8, 1.0, 0.6), diffuse=0.7, specular=0.2))
        s2 = Sphere(transform=scaling(0.5, 0.5, 0.5))

        return World(light=DEFAULT_LIGHT, objects=[s1, s2])
