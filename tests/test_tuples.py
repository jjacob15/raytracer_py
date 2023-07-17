from raytracer.tuple import Tuple, TupleType, point, vector, dot, cross
import math
import pytest


def test_is_point():
    t = Tuple(4.3, -4.2, 3.1, TupleType.POINT)
    assert t.x == 4.3
    assert t.y == -4.2
    assert t.z == 3.1
    assert t.w == TupleType.POINT


def test_is_vector():
    t = Tuple(4.3, -4.2, 3.1, TupleType.VECTOR)
    assert t.x == 4.3
    assert t.y == -4.2
    assert t.z == 3.1
    assert t.w == TupleType.VECTOR


def test_point_equality():
    t = Tuple(4.3, -4.2, 3.1, TupleType.POINT)
    p = point(4.3, -4.2, 3.1)
    assert t == p


def test_vector_equality():
    t = Tuple(4.3, -4.2, 3.1, TupleType.VECTOR)
    p = vector(4.3, -4.2, 3.1)
    assert t == p


def test_point_vector_addition():
    p = point(3, -2, 5)
    v = vector(-2, 3, 1)
    assert p + v == point(1, 1, 6)


def test_point_addition():
    p = point(3, -2, 5)
    v = point(-2, 3, 1)
    assert p + v == point(1, 1, 6)


def test_point_vector_sub():
    p = point(3, 2, 1)
    v = vector(5, 6, 7)
    assert p - v == point(-2, -4, -6)


def test_negation():
    p = point(1, -2, 3)
    p2 = point(-1, 2, -3)
    assert -p == p2


def test_point_scalar_mul():
    p = point(1, -2, 3)
    expected = point(3.5, -7, 10.5)
    r = p * 3.5
    assert r == expected


def test_point_scalar_div():
    p = point(1, -2, 3)
    expected = point(.5, -1, 1.5)
    r = p / 2
    assert r == expected


def test_magnitude_one():
    v = vector(0, 1, 0)
    assert v.magnitude() == 1


def test_magnitude_two():
    v = vector(0, 0, 1)
    assert v.magnitude() == 1


def test_magnitude_three():
    v = vector(1, 2, 3)
    assert v.magnitude() == math.sqrt(14)


def test_normalize_one():
    v = vector(4, 0, 0)
    assert v.normalize() == vector(1, 0, 0)


def test_normalize_two():
    v = vector(1, 2, 3)
    assert v.normalize() == vector(0.26726, 0.53452, 0.80178)


def test_dot_product():
    v1 = vector(1, 2, 3)
    v2 = vector(2, 3, 4)
    assert dot(v1, v2) == 20


def test_cross_product():
    v1 = vector(1, 2, 3)
    v2 = vector(2, 3, 4)
    assert cross(v1, v2) == vector(-1, 2, -1)
    assert cross(v2, v1) == vector(1, -2, 1)


def test_reflect_vector_45():
    v1 = vector(1, -1, 0)
    v2 = vector(0, 1, 0)
    assert vector(1, 1, 0) == v1.reflect(v2)


def test_invalid_tuple():
    with pytest.raises(ValueError):
        _ = Tuple(0, 0, 0, 8)
