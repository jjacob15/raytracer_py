from raytracer.canvas import Canvas, _build_ppm_header
from raytracer.tuple import point
from raytracer.color import Color
import pytest
from pathlib import Path
from textwrap import dedent


def test_canvas_create() -> None:
    c = Canvas(10, 20)

    assert c.width == 10
    assert c.height == 20
    assert c._pixels.shape == (20, 10, 3)  # numpy indexing is row-first


def test_write_pixel() -> None:
    c = Canvas(10, 20)
    red = Color(1, 0, 0)

    c.write_pixel(2, 3, red)
    assert (c._pixels[3, 2, :] == [1, 0, 0]).all() == True


def test_get_pixel() -> None:
    c = Canvas(10, 20)
    red = Color(1, 0, 0)
    c.write_pixel(2, 3, red)  # numpy indexing is row-first

    assert c.pixel_at(2, 3) == red


def test_non_color_write_raises() -> None:
    c = Canvas(10, 20)
    with pytest.raises(ValueError):
        c.write_pixel(2, 3, point(1, 2, 3))


def test_build_ppm_header() -> None:
    assert _build_ppm_header(5, 3) == "P3\n5 3\n255"


def test_ppm_write(tmp_path: Path) -> None:
    c = Canvas(5, 3)
    c.write_pixel(0, 0, Color(1.5, 0, 0))
    c.write_pixel(2, 1, Color(0, 0.5, 0))
    c.write_pixel(4, 2, Color(-0.5, 0, 1))

    out_img = tmp_path / "my_img.ppm"
    c.to_file(out_img)

    # The trailing newline is intentional
    truth = dedent(
        """\
        P3
        5 3
        255
        255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 255
        """
    )
    assert out_img.read_text() == truth
