import pytest

from raytracer.color import BLACK, WHITE, Color
from raytracer.patterns import Stripe
from raytracer.tuple import Tuple, point
from raytracer.shapes import Sphere
from raytracer.transforms import scaling, translation

STRIPED_TEST_CASES = (
    (point(0, 0, 0), WHITE),
    (point(0.9, 0, 0), WHITE),
    (point(1, 0, 0), BLACK),
    (point(1.1, 0, 0), BLACK),
    (point(-0.1, 0, 0), BLACK),
    (point(-1, 0, 0), BLACK),
    (point(-1.1, 0, 0), WHITE),
    # Constant along y
    (point(0, 1, 0), WHITE),
    (point(0, 2, 0), WHITE),
    # Constant along z
    (point(0, 0, 1), WHITE),
    (point(0, 0, 2), WHITE),
)


@pytest.mark.parametrize(("pt", "truth_color"), STRIPED_TEST_CASES)
def test_striped_colors(pt: Tuple, truth_color: Tuple) -> None:
    pattern = Stripe(WHITE, BLACK)
    assert pattern.at_point(pt) == truth_color


def test_striped_pattern_transform() -> None:
    obj = Sphere()
    pattern = Stripe(transform=scaling(2, 2, 2))

    c = pattern.at_object(obj, point(1.5, 0, 0))
    assert c == WHITE


def test_striped_object_transform() -> None:
    obj = Sphere(transform=scaling(2, 2, 2))
    pattern = Stripe()

    c = pattern.at_object(obj, point(1.5, 0, 0))
    assert c == WHITE


def test_striped_pattern_object_transform() -> None:
    obj = Sphere(transform=scaling(2, 2, 2))
    pattern = Stripe(transform=translation(0.5, 0, 0))

    c = pattern.at_object(obj, point(2.5, 0, 0))
    assert c == WHITE
