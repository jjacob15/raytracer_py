from raytracer.transforms import translation, scaling, rotate_x, rotate_y, rotate_z, rotate,shearing
from raytracer.matrix import Matrix
from raytracer.tuple import point, vector,Tuple
import numpy as np
import math
import pytest

QUART = math.pi / 2
H_QUART = math.pi / 4
R2O2 = math.sqrt(2) / 2


def test_basic_traslation() -> None:
    t = translation(10, 5, 7)
    r = Matrix(np.array([
        [1, 0, 0, 10],
        [0, 1, 0, 5],
        [0, 0, 1, 7],
        [0, 0, 0, 1]
    ]))

    assert t == r


def test_transform_mul() -> None:
    p = point(-3, 4, 5)
    shift = translation(5, -3, 2)
    assert shift * p == point(2, 1, 7)


def test_transform_vector_mul() -> None:
    v = vector(-3, 4, 5)
    shift = translation(5, -3, 2)
    assert shift * v == v


def test_inv_transform_mul() -> None:
    p = point(-3, 4, 5)
    shift = translation(5, -3, 2).inverse()
    assert shift * p == point(-8, 7, 3)


def test_scaling_point() -> None:
    scale = point(-4, 6, 8)
    t = scaling(2, 3, 4)

    assert t * scale == point(-8, 18, 32)


def test_inv_scaling_point() -> None:
    p = vector(-4, 6, 8)
    scale = scaling(2, 3, 4).inverse()

    assert scale * p == vector(-2, 2, 2)


def test_reflection() -> None:
    p = point(2, 3, 4)
    scale = scaling(-1, 1, 1)

    assert scale * p == point(-2, 3, 4)


def test_vector_scaling_grow() -> None:
    v = vector(-4, 6, 8)
    truth_scaled = vector(-8, 18, 32)

    scaled = scaling(2, 3, 4)
    assert scaled * v == truth_scaled


def test_vector_scaling_shrink() -> None:
    v = vector(-4, 6, 8)
    truth_scaled = vector(-2, 2, 2)

    scaled = scaling(2, 3, 4).inverse()
    assert scaled * v == truth_scaled


def test_reflection() -> None:
    p = point(2, 3, 4)
    truth_reflected = point(-2, 3, 4)

    scaled = scaling(-1, 1, 1)
    assert scaled * p == truth_reflected


def test_rotate_x() -> None:
    p = point(0, 1, 0)
    truth_half_quarter = point(0, R2O2, R2O2)
    truth_full_quarter = point(0, 0, 1)

    half_quarter = rotate_x(H_QUART)
    assert half_quarter * p == truth_half_quarter

    full_quarter = rotate_x(QUART)
    assert full_quarter * p == truth_full_quarter


def test_rotate_y() -> None:
    p = point(0, 0, 1)
    truth_half_quarter = point(R2O2, 0, R2O2)
    truth_full_quarter = point(1, 0, 0)

    half_quarter = rotate_y(H_QUART)
    assert half_quarter * p == truth_half_quarter

    full_quarter = rotate_y(QUART)
    assert full_quarter * p == truth_full_quarter


def test_rotate_z() -> None:
    p = point(0, 1, 0)
    truth_half_quarter = point(-R2O2, R2O2, 0)
    truth_full_quarter = point(-1, 0, 0)

    half_quarter = rotate_z(H_QUART)
    assert half_quarter * p == truth_half_quarter

    full_quarter = rotate_z(QUART)
    assert full_quarter * p == truth_full_quarter


def test_rotate() -> None:
    p = point(0, 1, 0)
    truth_full_quarter = point(1, 0, 0)

    full_quarter = rotate(x=QUART, y=QUART)
    assert full_quarter * p == truth_full_quarter

SHEARING_TEST_CASES = (
      ((0, 0, 0, 0, 0, 0), point(2, 3, 4)),
    ((1, 0, 0, 0, 0, 0), point(5, 3, 4)),
    ((0, 1, 0, 0, 0, 0), point(6, 3, 4)),
    ((0, 0, 1, 0, 0, 0), point(2, 5, 4)),
    ((0, 0, 0, 1, 0, 0), point(2, 7, 4)),
    ((0, 0, 0, 0, 1, 0), point(2, 3, 6)),
    ((0, 0, 0, 0, 0, 1), point(2, 3, 7)),
)

@pytest.mark.parametrize(("shear_args","truth"),SHEARING_TEST_CASES)
def test_shearing(shear_args:tuple[int,int,int,int,int,int],truth: Tuple) -> None:
    p = point(2, 3, 4)

    shear = shearing(*shear_args)
    assert shear * p == truth