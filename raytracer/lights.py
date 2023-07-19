from __future__ import annotations

from dataclasses import dataclass

from raytracer.color import BLUE
from raytracer.materials import Material
from raytracer.tuple import Tuple, TupleType, dot
from raytracer.color import Color, BLACK
from raytracer.shapes import Shape


@dataclass(frozen=True, slots=True)
class PointLight:
    position: Tuple
    intensity: Color


def lighting(
    material: Material,
    obj: Shape,
    light: PointLight,
    surf_pos: Tuple,
    eye_v: Tuple,
    normal: Tuple,
    in_shadow: bool = False,
) -> Color:
    """
    Calculate the shading from the given light source at the given point on an object.
    """
    if surf_pos.w != TupleType.POINT:
        raise ValueError("Surface position must be a point.")
    if eye_v.w != TupleType.VECTOR:
        raise ValueError("Eye vector must be a vector.")
    if normal.w != TupleType.VECTOR:
        raise ValueError("Normal vector must be a vector.")

    if material.pattern:
        surf_color = material.pattern.at_object(obj, surf_pos)
    else:
        surf_color = material.color

    effective_color = surf_color * light.intensity
    ambient = effective_color * material.ambient

    if in_shadow:
        return ambient

    light_vec = (light.position - surf_pos).normalize()
    light_dot_normal = dot(light_vec, normal)
    if light_dot_normal < 0:
        # A negative number means the light is on the other side of the surface, so the diffuse and
        # specular components go to 0
        diffuse = BLACK
        specular = BLACK
    else:
        diffuse = effective_color * material.diffuse * light_dot_normal

        # For the specular contribution, determine the angle between the reflection and eye vectors
        reflect_vec = -light_vec.reflect(normal)
        reflect_dot_eye = dot(reflect_vec, eye_v)
        if reflect_dot_eye <= 0:
            # Light is reflecting away from the eye
            specular = BLACK
        else:
            factor = reflect_dot_eye**material.shininess
            specular = light.intensity * material.specular * factor

    return ambient + diffuse + specular
