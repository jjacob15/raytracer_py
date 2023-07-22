from math import pi
from pathlib import Path

from raytracer.camera import Camera
from raytracer.color import WHITE,Color
from raytracer.lights import PointLight
from raytracer.materials import Material
from raytracer.tuple import point, vector
from raytracer.shapes import Sphere
from raytracer.transforms import rotate, scaling, translation, view_transform
from raytracer.world import World


def first_camera() -> None:
    # Create the floor & walls as extremely flattened spheres with a matte texture
    flatten_sphere = scaling(10, 0.01, 10)
    floor_material = Material(Color(1, 0.9, 0.9), specular=0)

    floor = Sphere(flatten_sphere, floor_material)
    left_wall = Sphere(
        translation(0, 0, 5) * rotate(x=pi / 2, y=-pi / 4) * flatten_sphere, floor_material
    )
    right_wall = Sphere(
        translation(0, 0, 5) * rotate(x=pi / 2, y=pi / 4) * flatten_sphere, floor_material
    )

    # Add some spheres to the scene
    middle = Sphere(
        translation(-0.5, 1, 0.5), Material(Color(0.1, 1, 0.5), diffuse=0.7, specular=0.3)
    )
    right = Sphere(
        translation(1.5, 0.5, -0.5) * scaling(0.5, 0.5, 0.5),
        Material(Color(0.5, 1, 0.1), diffuse=0.7, specular=0.3),
    )
    left = Sphere(
        translation(-1.5, 0.33, -0.75) * scaling(0.33, 0.33, 0.33),
        Material(Color(1, 0.8, 0.1), diffuse=0.7, specular=0.3),
    )

    # Now lighting & the camera
    world = World(
        PointLight(point(-10, 10, -10), WHITE),
        [floor, left_wall, right_wall, middle, right, left],
    )
    camera = Camera(
        300,
        150,
        pi / 3,
        transform=view_transform(point(0, 1.5, -5), point(0, 1, 0), vector(0, 1, 0)),
    )
    canvas = camera.render(world)

    canvas.to_file(Path("./raytracer_demo/output/chapter_7.ppm"))


if __name__ == "__main__":
    first_camera()
