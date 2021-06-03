from Include.Tuple import *
import numpy as np
import functools as ft

class Matrix4:
    length = 4

    def __init__(self):
        self.m = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=float)

    @staticmethod
    def identity_matrix():
        M = Matrix4()
        M.m = np.identity(4, dtype=float)
        return M

    def transpose(self):
        M = Matrix4()
        M.m = self.m.transpose()
        return M

    def determinant(self):
        return round(np.linalg.det(self.m))

    def submatrix(self, row, column):
        M = Matrix3()
        M.m = np.delete(np.delete(self.m, row, 0), column, 1)
        return M

    def minor(self, row, column):
        return self.submatrix(row, column).determinant()

    def cofactor(self, row, column):
        return self.minor(row, column) if (row + column) % 2 == 0 else -self.minor(row, column)

    def invertible(self):
        return self.determinant() != 0

    @ft.lru_cache(None)
    def invert(self):
        M = Matrix4()
        M.m = np.linalg.inv(self.m)
        return M

    def translate(self, x, y, z):
        M = Matrix4.identity_matrix()
        M.m[0][3] = x
        M.m[1][3] = y
        M.m[2][3] = z
        return M * self

    def scale(self, x, y, z):
        M = Matrix4.identity_matrix()
        M.m[0][0] = x
        M.m[1][1] = y
        M.m[2][2] = z
        return M * self

    def rotate_x(self, radians):
        M = Matrix4.identity_matrix()
        M.m[1][1] = math.cos(radians)
        M.m[1][2] = -math.sin(radians)
        M.m[2][1] = math.sin(radians)
        M.m[2][2] = math.cos(radians)
        return M * self

    def rotate_y(self, radians):
        M = Matrix4.identity_matrix()
        M.m[0][0] = math.cos(radians)
        M.m[0][2] = math.sin(radians)
        M.m[2][0] = -math.sin(radians)
        M.m[2][2] = math.cos(radians)
        return M * self

    def rotate_z(self, radians):
        M = Matrix4.identity_matrix()
        M.m[0][0] = math.cos(radians)
        M.m[0][1] = -math.sin(radians)
        M.m[1][0] = math.sin(radians)
        M.m[1][1] = math.cos(radians)
        return M * self

    def rotate(self, yaw: float, pitch: float, roll: float):
        return Matrix4.identity_matrix().rotate_z(yaw).rotate_y(pitch).rotate_x(roll) * self

    def shear(self, xy, xz, yx, yz, zx, zy):
        M = Matrix4.identity_matrix()
        M.m[0][1] = xy
        M.m[0][2] = xz
        M.m[1][0] = yx
        M.m[1][2] = yz
        M.m[2][0] = zx
        M.m[2][1] = zy
        return M * self

    def __eq__(self, other):
        for x in range(self.length):
            for y in range(self.length):
                if (abs(self.m[x][y] - other.m[x][y]) > EPSILON):
                    return False
        return True

    def __mul__(self, other):
        if (type(other) is Matrix4):
            M = Matrix4()
            M.m = np.dot(self.m, other.m)
            return M
        elif (type(other) is Tuple):
            return Tuple(self.m[0][0] * other.x + self.m[0][1] * other.y + self.m[0][2] * other.z + self.m[0][3] * other.w,
                         self.m[1][0] * other.x + self.m[1][1] * other.y + self.m[1][2] * other.z + self.m[1][3] * other.w,
                         self.m[2][0] * other.x + self.m[2][1] * other.y + self.m[2][2] * other.z + self.m[2][3] * other.w,
                         self.m[3][0] * other.x + self.m[3][1] * other.y + self.m[3][2] * other.z + self.m[3][3] * other.w)

    def __hash__(self):
        return hash(bytes(self.m))

class Matrix3:
    length = 3

    def __init__(self):
        self.m = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def determinant(self):
        return round(np.linalg.det(self.m))

    def submatrix(self, row, column):
        M = Matrix2()
        M.m = np.delete(np.delete(self.m, row, 0), column, 1)
        return M

    def minor(self, row, column):
        return self.submatrix(row, column).determinant()

    def cofactor(self, row, column):
        return self.minor(row, column) if (row + column) % 2 == 0 else -self.minor(row, column)

    def __eq__(self, other):
        for x in range(self.length):
            for y in range(self.length):
                if (abs(self.m[x][y] - other.m[x][y]) > EPSILON):
                    return False
        return True

class Matrix2:
    length = 2

    def __init__(self):
        self.m = np.array([[0, 0], [0, 0]])

    def determinant(self):
        return round(np.linalg.det(self.m))

    def __eq__(self, other):
        for x in range(self.length):
            for y in range(self.length):
                if (abs(self.m[x][y] - other.m[x][y]) > EPSILON):
                    return False
        return True
