from __future__ import annotations
from raytracer.color import Color
from pathlib import Path
import textwrap

import numpy as np


class Canvas:
    _pixels: np.ndarray

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self._pixels = np.zeros(shape=(width, height, 3))

    def write_pixel(self, x: int, y: int, color: Color) -> None:
        if not isinstance(color, Color):
            raise ValueError
        self._pixels[x, y, :] = [*color]  # using the color objects iterator to unpack color to the r, g and b value

    def pixel_at(self, x: int, y: int) -> Color:
        return Color(*self._pixels[x, y, :])

    def to_file(self, out_filepath: Path) -> None:
        """
        Output the current canvas as a Portable Pixmap (PPM).
        """
        full_text = (
            f"{_build_ppm_header(self.width, self.height)}\n"
            f"{_pixels_to_ppm(self._pixels)}\n"
        )
        out_filepath.write_text(full_text)


def _build_ppm_header(width: int, height: int):
    header = f"P3\n{width} {height}\n255"
    return header


def _pixels_to_ppm(pixels: np.ndarray):
    max_line_len = 70
    max_value = 255
    scaled = pixels * max_value
    scaled[scaled > max_value] = max_value
    scaled[scaled < 0] = 0

    # with np.printoptions(linewidth=np.inf, threshold=np.inf):  # type: ignore[arg-type]
    tmp = np.array2string(scaled.astype(int))
    output = "\n".join(" ".join(row.strip("[] ").split()) for row in tmp.splitlines())
    output = ' '.join(output.split())
    return textwrap.fill(output, width=max_line_len)
