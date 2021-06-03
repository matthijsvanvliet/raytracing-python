from Include.Tuple import *

class Matrix4:
    length = 4

    def __init__(self):
        self.m = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    @staticmethod
    def identity_matrix():
        M = Matrix4()
        M.m[0][0] = 1.0
        M.m[1][1] = 1.0
        M.m[2][2] = 1.0
        M.m[3][3] = 1.0
        return M

    def transpose(self):
        M = Matrix4()
        for row in range(M.length):
            for col in range(M.length):
                M.m[row][col] = self.m[col][row]
        return M

    def determinant(self):
        det = 0
        for x in range(self.length):
            det += self.m[0][x] * self.cofactor(0, x)
        return det

    def submatrix(self, row, column):
        M = Matrix3()
        i = 0

        for r in range(self.length):
            j = 0
            if (r == row):
                continue

            for c in range(self.length):
                if (c == column):
                    continue

                M.m[i][j] = self.m[r][c]
                j += 1
            i += 1
        return M

    def minor(self, row, column):
        return self.submatrix(row, column).determinant()

    def cofactor(self, row, column):
        return self.minor(row, column) if (row + column) % 2 == 0 else -self.minor(row, column)

    def invertible(self):
        return self.determinant() != 0

    def invert(self):
        if (not self.invertible()):
            return

        M = Matrix4()
        for row in range(self.length):
            for col in range(self.length):
                c = self.cofactor(row, col)
                M.m[col][row] = c / self.determinant()
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
            for row in range(M.length):
                for col in range(M.length):
                    for index in range(M.length):
                        M.m[row][col] += (self.m[row][index] * other.m[index][col])
            return M
        elif (type(other) is Tuple):
            return Tuple(self.m[0][0] * other.x + self.m[0][1] * other.y + self.m[0][2] * other.z + self.m[0][3] * other.w,
                         self.m[1][0] * other.x + self.m[1][1] * other.y + self.m[1][2] * other.z + self.m[1][3] * other.w,
                         self.m[2][0] * other.x + self.m[2][1] * other.y + self.m[2][2] * other.z + self.m[2][3] * other.w,
                         self.m[3][0] * other.x + self.m[3][1] * other.y + self.m[3][2] * other.z + self.m[3][3] * other.w)

class Matrix3:
    length = 3

    def __init__(self):
        self.m = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def determinant(self):
        det = 0
        for x in range(self.length):
            det += self.m[0][x] * self.cofactor(0, x)
        return det

    def submatrix(self, row, column):
        M = Matrix2()
        i = 0

        for r in range(self.length):
            j = 0
            if (r == row):
                continue

            for c in range(self.length):
                if (c == column):
                    continue

                M.m[i][j] = self.m[r][c]
                j += 1
            i += 1
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
        self.m = [[0, 0], [0, 0]]

    def determinant(self):
        return self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0]

    def __eq__(self, other):
        for x in range(self.length):
            for y in range(self.length):
                if (abs(self.m[x][y] - other.m[x][y]) > EPSILON):
                    return False
        return True

#
# Matrix class with variable width and hight (not optimal)
#
class Matrix:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.m = [[0.0 for x in range(width)] for y in range(height)]

    @staticmethod
    def identity_matrix(length: int):
        M = Matrix(length, length)
        for x in range(length):
            M.m[x][x] = 1
        return M

    def transpose(self):
        M = Matrix(4, 4)
        for row in range(M.width):
            for col in range(M.height):
                M.m[row][col] = self.m[col][row]
        return M

    def determinant(self):
        if (self.width == 2):
            return self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0]
        else:
            det = 0
            for x in range(self.width):
                det += self.m[0][x] * self.cofactor(0, x)
            return det

    def submatrix(self, row, column):
        M = Matrix(self.width-1, self.height-1)
        list = []
        index = 0
        for x in range(self.width):
            if (x != row):
                for y in range(self.height):
                    if (y != column):
                        list.append(self.m[x][y])

        for x in range(M.width):
            for y in range(M.height):
                M.m[x][y] = list[index]
                index += 1
        return M

    def minor(self, row, column):
        return self.submatrix(row, column).determinant()

    def cofactor(self, row, column):
        return self.minor(row, column) if (row + column) % 2 == 0 else -self.minor(row, column)

    def invertible(self):
        return self.determinant() != 0

    def inverse(self):
        if (not self.invertible()):
            return

        M2 = Matrix(self.width, self.height)
        for row in range(self.width):
            for col in range(self.height):
                c = self.cofactor(row, col)
                M2.m[col][row] = c / self.determinant()
        return M2

    def translate(self, x, y, z):
        M = Matrix.identity_matrix()
        M.m[0][3] = x
        M.m[1][3] = y
        M.m[2][3] = z
        return M * self

    def scale(self, x, y, z):
        M = Matrix.identity_matrix()
        M.m[0][0] = x
        M.m[1][1] = y
        M.m[2][2] = z
        return M * self

    def rotate_x(self, radians):
        M = Matrix.identity_matrix()
        M.m[1][1] = math.cos(radians)
        M.m[1][2] = -math.sin(radians)
        M.m[2][1] = math.sin(radians)
        M.m[2][2] = math.cos(radians)
        return M * self

    def rotate_y(self, radians):
        M = Matrix.identity_matrix()
        M.m[0][0] = math.cos(radians)
        M.m[0][2] = math.sin(radians)
        M.m[2][0] = -math.sin(radians)
        M.m[2][2] = math.cos(radians)
        return M * self

    def rotate_z(self, radians):
        M = Matrix.identity_matrix()
        M.m[0][0] = math.cos(radians)
        M.m[0][1] = -math.sin(radians)
        M.m[1][0] = math.sin(radians)
        M.m[1][1] = math.cos(radians)
        return M * self

    def shear(self, xy, xz, yx, yz, zx, zy):
        M = Matrix.identity_matrix()
        M.m[0][1] = xy
        M.m[0][2] = xz
        M.m[1][0] = yx
        M.m[1][2] = yz
        M.m[2][0] = zx
        M.m[2][1] = zy
        return M * self

    def __eq__(self, other):
        for x in range(self.width):
            for y in range(self.height):
                if (abs(self.m[x][y] - other.m[x][y]) > EPSILON):
                    return False
        return True

    def __mul__(self, other):
        if (type(other) is Matrix):
            M = Matrix(self.width, self.height)
            for row in range(M.width):
                for col in range(M.height):
                    for index in range(M.width):
                        M.m[row][col] += (self.m[row][index] * other.m[index][col])
            return M
        elif (type(other) is Tuple):
            return Tuple(self.m[0][0] * other.x + self.m[0][1] * other.y + self.m[0][2] * other.z + self.m[0][3] * other.w,
                         self.m[1][0] * other.x + self.m[1][1] * other.y + self.m[1][2] * other.z + self.m[1][3] * other.w,
                         self.m[2][0] * other.x + self.m[2][1] * other.y + self.m[2][2] * other.z + self.m[2][3] * other.w,
                         self.m[3][0] * other.x + self.m[3][1] * other.y + self.m[3][2] * other.z + self.m[3][3] * other.w)