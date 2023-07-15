from __future__ import annotations
from dataclasses import dataclass
from raytracer.tuple import Tuple
import numpy as np


@dataclass
class Matrix:
    """
    Matrix is build using ndarrays
    """

    matrix: np.ndarray

    def __mul__(self, other: object) -> Matrix | Tuple:
        if isinstance(other, Tuple):
            dotprod = self.matrix.dot(other.as_array())
            return Tuple.from_array(dotprod)
        elif isinstance(other, Matrix):
            return Matrix(self.matrix.dot(other.matrix))

        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return np.allclose(self.matrix, other.matrix, rtol=1e-4)

    def inverse(self) -> Matrix:
        return Matrix(np.linalg.inv(self.matrix))

    def transpose(self) -> Matrix:
        return Matrix(self.matrix.T)

    @staticmethod
    def identity() -> Matrix:
        return Matrix(np.identity(4))
