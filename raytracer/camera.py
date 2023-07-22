import math
from dataclasses import dataclass, field
from itertools import product

from raytracer import NUMERIC_T
from raytracer.canvas import Canvas
from raytracer.tuple import point
from raytracer.rays import Ray
from raytracer.transforms import Matrix
from raytracer.world import World


@dataclass(slots=True)
class Camera: 
    h_size: int
    v_size: int
    fov: NUMERIC_T  # radians
    transform: Matrix = field(default_factory=Matrix.identity)

    pixel_size: NUMERIC_T = field(init=False)
    _half_width: NUMERIC_T = field(init=False)
    _half_height: NUMERIC_T = field(init=False)

    def __post_init__(self) -> None:
        """
        Determine pixel scaling from the provided camera parameters.
        """
        half_view = math.tan(self.fov / 2)
        aspect_ratio = self.h_size / self.v_size
        if aspect_ratio >= 1:
            self._half_width = half_view
            self._half_height = half_view / aspect_ratio
        else:
            self._half_width = half_view * aspect_ratio
            self._half_height = half_view

        self.pixel_size = (self._half_width * 2) / self.h_size

    def ray_for_pixel(self, x: int, y: int) -> Ray:
        """Compute a ray from the camera to the center of the pixel at the given XY coordinates."""
        x_offset = (x + 0.5) * self.pixel_size
        y_offset = (y + 0.5) * self.pixel_size

        world_x = self._half_width - x_offset
        world_y = self._half_height - y_offset

        inv_trans = self.transform.inverse()
        pixel = inv_trans * point(world_x, world_y, -1)
        origin = inv_trans * point(0, 0, 0)
        direction = (pixel - origin).normalize()

        return Ray(origin, direction)

    def render(self, world: World) -> Canvas:
        """Render the camera's current fiew of the world."""
        img = Canvas(self.h_size, self.v_size)
        for y,x in product(range(self.v_size - 1), range(self.h_size - 1)):
            r = self.ray_for_pixel(x, y)
            c = world.color_at(r)
            img.write_pixel(x, y, c)

        return img
