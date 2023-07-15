from raytracer.matrix import Matrix
from raytracer.tuple import Tuple
import numpy as np


def test_equity():
    a = Matrix(np.array([2, 5]))
    b = Matrix(np.array([2, 5]))

    assert a == b


def test_matrix_mul():
    a = Matrix(np.array([1, 2, 3, 4,
                         5, 6, 7, 8,
                         9, 8, 7, 6,
                         5, 4, 3, 2]).reshape([4, 4]))

    b = Matrix(np.array([-2, 1, 2, 3,
                         3, 2, 1, -1,
                         4, 3, 6, 5,
                         1, 2, 7, 8]).reshape([4, 4]))
    c = Matrix(np.array([20, 22, 50, 48,
                         44, 54, 114, 108,
                         40, 58, 110, 102,
                         16, 26, 46, 42]).reshape([4, 4]))
    assert a * b == c


def test_matrix_tuple_mul():
    a = Matrix(np.array([1, 2, 3, 4,
               2, 4, 4, 2,
                         8, 6, 4, 1,
                         0, 0, 0, 1]).reshape([4, 4]))
    b = Tuple(1, 2, 3, 1)
    r = Tuple(18, 24, 33, 1)

    assert a * b == r


def test_matrix_inverse():
    a = Matrix(np.array([-5, 2, 6, -8,
                         1, -5, 1, 8,
                         7, 7, -6, -7,
                         1, -3, 7, 4]).reshape([4, 4]))
    result = Matrix(np.array([0.21805, 0.45113, 0.24060, -0.04511,
                              -0.80827, -1.45677, -0.44361, 0.52068,
                              -0.07895, -0.22368, -0.05263, 0.19737,
                              -0.52256, -0.81391, -0.30075, 0.30639]).reshape([4, 4]))
    assert a.inverse() == result
