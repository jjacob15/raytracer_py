from raytracer import NUMERIC_T
from raytracer.matrix import Matrix
import numpy as np
from math import sin, cos


def translation(x: NUMERIC_T, y: NUMERIC_T, z: NUMERIC_T) -> Matrix:
    """moves a point from one position to another in a 3D space"""
    identity = np.identity(4)
    identity[0:3, 3] = [x, y, z]
    return Matrix(matrix=identity)

def scaling(x: NUMERIC_T, y: NUMERIC_T, z: NUMERIC_T) -> Matrix:
    """scales a point up or down in a 3D space"""
    identity = np.identity(4)
    identity[0, 0] = x
    identity[1, 1] = y
    identity[2, 2] = z
    return Matrix(matrix=identity)

def rotate_x(a: NUMERIC_T) -> Matrix:
    """means rotating around the x axis by moving from the y axis towards the z axis"""
    identity = np.identity(4)
    identity[1, [1, 2]] = (cos(a), -sin(a))
    identity[2, [1, 2]] = (sin(a), cos(a))
    return Matrix(identity)


def rotate_y(a: NUMERIC_T) -> Matrix:

    identity = np.identity(4)
    identity[0, [0, 2]] = (cos(a), sin(a))
    identity[2, [0, 2]] = (-sin(a), cos(a))
    return Matrix(identity)


def rotate_z(a: NUMERIC_T) -> Matrix:

    identity = np.identity(4)
    identity[0, [0, 1]] = (cos(a), -sin(a))
    identity[1, [0, 1]] = (sin(a), cos(a))
    return Matrix(identity)


def rotate(x: float = 0, y: float = 0, z: float = 0) -> Matrix:
    # reverse the dot product
    return rotate_z(z) * rotate_y(y) * rotate_x(x)


def shearing(
    x_y: NUMERIC_T = 0,
    x_z: NUMERIC_T = 0,
    y_x: NUMERIC_T = 0,
    y_z: NUMERIC_T = 0,
    z_x: NUMERIC_T = 0,
    z_y: NUMERIC_T = 0,
) -> Matrix:
    matrix = np.array(
        [
            [1, x_y, x_z, 0],
            [y_x, 1, y_z, 0],
            [z_x, z_y, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    return Matrix(matrix)
