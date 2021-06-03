import unittest
from Include.MatrixNP import *
from Include.Tuple import *

class TestMatrix(unittest.TestCase):
    def test_Matrix_constructAndInspectFourByFourMatrix(self):
        self.list = [ 1, 2, 3, 4, 5.5, 6.5, 7.5, 8.5, 9, 10, 11, 12, 13.5, 14.5, 15.5, 16.5 ]
        self.M = Matrix4()

        self.index = 0
        for x in range(self.M.length):
            for y in range(self.M.length):
                self.M.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.M.m[0][0], 1)
        self.assertEqual(self.M.m[0][3], 4)
        self.assertEqual(self.M.m[1][0], 5.5)
        self.assertEqual(self.M.m[1][2], 7.5)
        self.assertEqual(self.M.m[2][2], 11)
        self.assertEqual(self.M.m[3][0], 13.5)
        self.assertEqual(self.M.m[3][2], 15.5)

    def test_Matrix_representTwoByTwo(self):
        self.list = [-3, 5, 1, -2]
        self.M = Matrix2()

        self.index = 0
        for x in range(self.M.length):
            for y in range(self.M.length):
                self.M.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.M.m[0][0], -3)
        self.assertEqual(self.M.m[0][1], 5)
        self.assertEqual(self.M.m[1][0], 1)
        self.assertEqual(self.M.m[1][1], -2)

    def test_Matrix_representThreeByThree(self):
        self.list = [-3, 5, 0, 1, -2, -7, 0, 1, 1]
        self.M = Matrix3()

        self.index = 0
        for x in range(self.M.length):
            for y in range(self.M.length):
                self.M.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.M.m[0][0], -3)
        self.assertEqual(self.M.m[1][1], -2)
        self.assertEqual(self.M.m[2][2], 1)

    def test_Matrix_equalityWithIdenticalMatrices(self):
        self.list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2]
        self.A = Matrix4()
        self.B = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.B.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.A, self.B)

    def test_Matrix_equalityWithDifferentMatrices(self):
        self.list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2]
        self.list2 = [2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.A = Matrix4()
        self.B = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list1[self.index]
                self.B.m[x][y] = self.list2[self.index]
                self.index += 1

        self.assertNotEqual(self.A, self.B)

    def test_Matrix_multiplyingTwoMatrices(self):
        self.list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2]
        self.list2 = [-2, 1, 2, 3, 3, 2, 1, -1, 4, 3, 6, 5, 1, 2, 7, 8]
        self.resultList = [20, 22, 50, 48, 44, 54, 114, 108, 40, 58, 110, 102, 16, 26, 46, 42]

        self.A = Matrix4()
        self.B = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list1[self.index]
                self.B.m[x][y] = self.list2[self.index]
                self.index += 1
        self.index = 0
        self.result = self.A * self.B

        for x in range(self.result.length):
            for y in range(self.result.length):
                self.assertEqual(self.result.m[x][y], self.resultList[self.index])
                self.index += 1

    def test_Matrix_multiplyMatrixByTuple(self):
        self.list1 = [1, 2, 3, 4, 2, 4, 4, 2, 8, 6, 4, 1, 0, 0, 0, 1]
        self.A = Matrix4()
        self.T = Tuple(1, 2, 3, 1)

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list1[self.index]
                self.index += 1

        self.result = self.A * self.T
        self.assertEqual(self.result, Tuple(18, 24, 33, 1))

    def test_Matrix_multiplyingMatrixByIdentityMatrix(self):
        self.list = [0, 1, 2, 4, 1, 2, 4, 8, 2, 4, 8, 16, 4, 8, 16, 32]
        self.A = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.result = self.A * Matrix4.identity_matrix()
        self.assertEqual(self.result, self.A)

    def test_Matrix_multiplyingTupleByIdentityMatrix(self):
        a = Tuple(1, 2, 3, 4)
        self.result = Matrix4.identity_matrix() * a
        self.assertEqual(self.result, a)

    def test_Matrix_transposeAMatrix(self):
        self.list = [0, 9, 3, 0, 9, 8, 0, 8, 1, 8, 5, 3, 0, 0, 5, 8]
        self.resultList = [0, 9, 1, 0, 9, 8, 8, 0, 3, 0, 5, 5, 0, 8, 3, 8]
        self.A = Matrix4()
        self.B = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.B.m[x][y] = self.resultList[self.index]
                self.index += 1

        self.result = self.A.transpose()
        self.assertEqual(self.result, self.B)

    def test_Matrix_transposeIdentityMatrix(self):
        self.A = Matrix4.identity_matrix().transpose()
        self.assertEqual(self.A, Matrix4.identity_matrix())

    def test_Matrix_calculateTheDeterminantOfATwoByTwoMatrix(self):
        self.list = [1, 5, -3, 2]
        self.A = Matrix2()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.result = self.A.determinant()
        self.assertEqual(self.result, 17)

    def test_Matrix_createSubmatrixOfAThreeByThreeMatrix(self):
        self.list = [1, 5, 0, -3, 2, 7, 0, 6, -3]
        self.resultList = [-3, 2, 0, 6]
        self.A = Matrix3()
        self.B = Matrix2()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1
        self.index = 0
        for x in range(self.B.length):
            for y in range(self.B.length):
                self.B.m[x][y] = self.resultList[self.index]
                self.index += 1

        self.result = self.A.submatrix(0, 2)
        self.assertEqual(self.result, self.B)

    def test_Matrix_createSubmatrixOfAFourByFourMatrix(self):
        self.list = [-6, 1, 1, 6, -8, 5, 8, 6, -1, 0, 8, 2, -7, 1, -1, 1]
        self.resultList = [-6, 1, 6, -8, 8, 6, -7, -1, 1]

        self.A = Matrix4()
        self.B = Matrix3()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1
        self.index = 0
        for x in range(self.B.length):
            for y in range(self.B.length):
                self.B.m[x][y] = self.resultList[self.index]
                self.index += 1

        self.result = self.A.submatrix(2, 1)
        self.assertEqual(self.result, self.B)

    def test_Matrix_calculateAMinorOfAThreeByThreeMatrix(self):
        self.list = [3, 5, 0, 2, -1, -7, 6, -1, 5]
        self.A = Matrix3()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.B = self.A.submatrix(1, 0)

        self.assertEqual(self.B.determinant(), 25)
        self.assertEqual(self.A.minor(1, 0), 25)

    def test_Matrix_calculateCofactorOfThreeByThreeMatrix(self):
        self.list = [3, 5, 0, 2, -1, -7, 6, -1, 5]
        self.A = Matrix3()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.A.minor(0, 0), -12)
        self.assertEqual(self.A.cofactor(0, 0), -12)
        self.assertEqual(self.A.minor(1, 0), 25)
        self.assertEqual(self.A.cofactor(1, 0), -25)

    def test_Matrix_calculateTheDeterminantOfAThreeByThreeMatrix(self):
        self.list = [1, 2, 6, -5, 8, -4, 2, 6, 4]
        self.A = Matrix3()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.A.cofactor(0, 0), 56)
        self.assertEqual(self.A.cofactor(0, 1), 12)
        self.assertEqual(self.A.minor(0, 2), -46)
        self.assertEqual(self.A.determinant(), -196)

    def test_Matrix_calculateTheDeterminantOfAFourByFourMatrix(self):
        self.list = [-2, -8, 3, 5, -3, 1, 7, 3, 1, 2, -9, 6, -6, 7, 7, -9]
        self.A = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.A.cofactor(0, 0), 690)
        self.assertEqual(self.A.cofactor(0, 1), 447)
        self.assertEqual(self.A.cofactor(0, 2), 210)
        self.assertEqual(self.A.cofactor(0, 3), 51)
        self.assertEqual(self.A.determinant(), -4071)

    def test_Matrix_testInvertibleMatrixForInvertibility(self):
        self.list = [6, 4, 4, 4, 5, 5, 7, 6, 4, -9, 3, -7, 9, 1, 7, -6]
        self.A = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.A.determinant(), -2120)
        self.assertEqual(self.A.invertible(), True)

    def test_Matrix_testNonInvertibleMatrixForInvertibility(self):
        self.list = [-4, 2, -2, -3, 9, 6, 2, 6, 0, -5, 1, -5, 0, 0, 0, 0]
        self.A = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.index += 1

        self.assertEqual(self.A.determinant(), 0)
        self.assertEqual(self.A.invertible(), False)

    def test_Matrix_calculateInverseOfAMatrix(self):
        self.list = [-5, 2, 6, -8, 1, -5, 1, 8, 7, 7, -6, -7, 1, -3, 7, 4]
        self.resultList = [0.21805, 0.45113, 0.24060, -0.04511, -0.80827, -1.45677, -0.44361, 0.52068, -0.07895, -0.22368, -0.05263, 0.19737, -0.52256, -0.81391, -0.30075, 0.30639]
        self.A = Matrix4()
        self.result = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.result.m[x][y] = self.resultList[self.index]
                self.index += 1
        self.B = self.A.invert()

        self.assertEqual(self.A.determinant(), 532)
        self.assertEqual(self.A.cofactor(2, 3), -160)
        self.assertAlmostEqual(self.B.m[3][2], -160/532)
        self.assertEqual(self.A.cofactor(3, 2), 105)
        self.assertAlmostEqual(self.B.m[2][3], 105/532)

        for x in range(self.A.length):
            for y in range(self.A.length):
                self.assertAlmostEqual(self.B.m[x][y], self.result.m[x][y], 5)

    def test_Matrix_calculateTheInverseOfAnotherMatrix(self):
        self.list = [8, -5, 9, 2, 7, 5, 6, 1, -6, 0, 9, 6, -3, 0, -9, -4]
        self.resultList = [-0.15385, -0.15385, -0.28205, -0.53846, -0.07692, 0.12308, 0.02564, 0.03077, 0.35897, 0.35897, 0.43590, 0.92308, -0.69231, -0.69231, -0.76923, -1.92308]
        self.A = Matrix4()
        self.result = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.result.m[x][y] = self.resultList[self.index]
                self.index += 1
        self.B = self.A.invert()

        for x in range(self.A.length):
            for y in range(self.A.length):
                self.assertAlmostEqual(self.B.m[x][y], self.result.m[x][y], 5)

    def test_Matrix_calculateTheInverseOfAThirdMatrix(self):
        self.list = [9, 3, 0, 9, -5, -2, -6, -3, -4, 9, 6, 4, -7, 6, 6, 2]
        self.resultList = [-0.04074, -0.07778, 0.14444, -0.22222, -0.07778, 0.03333, 0.36667, -0.33333, -0.02901, -0.14630, -0.10926, 0.12963, 0.17778, 0.06667, -0.26667, 0.33333]
        self.A = Matrix4()
        self.result = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list[self.index]
                self.result.m[x][y] = self.resultList[self.index]
                self.index += 1
        self.B = self.A.invert()

        self.assertEqual(self.B, self.result)

    def test_Matrix_multiplyAProductByItsInverse(self):
        self.list1 = [3, -9, 7, 3, 3, -8, 2, -9, -4, 4, 4, 1, -6, 5, -1, 1]
        self.list2 = [8, 2, 2, 2, 3, -1, 7, 0, 7, 0, 5, 4, 6, -2, 0, 5]

        self.A = Matrix4()
        self.B = Matrix4()

        self.index = 0
        for x in range(self.A.length):
            for y in range(self.A.length):
                self.A.m[x][y] = self.list1[self.index]
                self.B.m[x][y] = self.list2[self.index]
                self.index += 1
        self.C = self.A * self.B

        self.result = self.C * self.B.invert()
        self.assertEqual(self.result, self.A)

class TestMatrixTransformations(unittest.TestCase):
    def test_Matrix_multiplyByATranslationMatrix(self):
        self.transform = Matrix4.identity_matrix().translate(5, -3, 2)
        self.p = point(-3, 4, 5)

        self.result = self.transform * self.p
        self.assertEqual(self.result, point(2, 1, 7))

    def test_Matrix_multiplyByTheInverseOfATranslationMatrix(self):
        self.transform = Matrix4.identity_matrix().translate(5, -3, 2)
        self.inv = self.transform.invert()
        self.p = point(-3, 4, 5)

        self.result = self.inv * self.p
        self.assertEqual(self.result, point(-8, 7, 3))

    def test_Matrix_translationDoesNotAffectVectors(self):
        self.transform = Matrix4.identity_matrix().translate(5, -3, 2)
        self.v = vector(-3, 4, 5)

        self.result = self.transform * self.v
        self.assertEqual(self.result, self.v)

    def test_Matrix_scalingMatrixAppliedToAPoint(self):
        self.transform = Matrix4.identity_matrix().scale(2, 3, 4)
        self.p = point(-4, 6, 8)

        self.result = self.transform * self.p
        self.assertEqual(self.result, point(-8, 18, 32))

    def test_Matrix_scalingMatrixAppliedToAVector(self):
        self.transform = Matrix4.identity_matrix().scale(2, 3, 4)
        self.v = vector(-4, 6, 8)

        self.result = self.transform * self.v
        self.assertEqual(self.result, vector(-8, 18, 32))

    def test_Matrix_multiplyByTheInverseOfAScalingMatrix(self):
        self.transform = Matrix4.identity_matrix().scale(2, 3, 4)
        self.inv = self.transform.invert()
        self.v = vector(-4, 6, 8)

        self.result = self.inv * self.v
        self.assertEqual(self.result, vector(-2, 2, 2))

    def test_Matrix_reflectionIsScalingByANegativeValue(self):
        self.transform = Matrix4.identity_matrix().scale(-1, 1, 1)
        self.p = point(2, 3, 4)

        self.result = self.transform * self.p
        self.assertEqual(self.result, point(-2, 3, 4))

    def test_Matrix_rotatingAPointAroundTheXAxis(self):
        self.p = point(0, 1, 0)
        self.half_quarter = Matrix4.identity_matrix().rotate_x(math.pi / 4)
        self.full_quarter = Matrix4.identity_matrix().rotate_x(math.pi / 2)

        self.assertEqual(self.half_quarter * self.p, point(0, math.sqrt(2)/2, math.sqrt(2)/2))
        self.assertEqual(self.full_quarter * self.p, point(0, 0, 1))

    def test_Matrix_theInverseOfAnXRotationRotatesInTheOppositeDirection(self):
        self.p = point(0, 1, 0)
        self.half_quarter = Matrix4.identity_matrix().rotate_x(math.pi / 4)

        self.inv = self.half_quarter.invert()
        self.assertEqual(self.inv * self.p, point(0, math.sqrt(2)/2, -math.sqrt(2)/2))

    def test_Matrix_rotatingAPointAroundTheYAxis(self):
        self.p = point(0, 0, 1)
        self.half_quarter = Matrix4.identity_matrix().rotate_y(math.pi / 4)
        self.full_quarter = Matrix4.identity_matrix().rotate_y(math.pi / 2)

        self.assertEqual(self.half_quarter * self.p, point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2))
        self.assertEqual(self.full_quarter * self.p, point(1, 0, 0))

    def test_Matrix_rotatingAPointAroundTheZAxis(self):
        self.p = point(0, 1, 0)
        self.half_quarter = Matrix4.identity_matrix().rotate_z(math.pi / 4)
        self.full_quarter = Matrix4.identity_matrix().rotate_z(math.pi / 2)

        self.assertEqual(self.half_quarter * self.p, point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0))
        self.assertEqual(self.full_quarter * self.p, point(-1, 0, 0))

    def test_Matrix_shearingTransformationMovesXInProportionToY(self):
        self.transform = Matrix4.identity_matrix().shear(1, 0, 0, 0, 0, 0)
        self.p = point(2, 3, 4)
        self.assertEqual(self.transform * self.p, point(5, 3, 4))

    def test_Matrix_shearingTransformationMovesXInProportionToZ(self):
        self.transform = Matrix4.identity_matrix().shear(0, 1, 0, 0, 0, 0)
        self.p = point(2, 3, 4)
        self.assertEqual(self.transform * self.p, point(6, 3, 4))

    def test_Matrix_shearingTransformationMovesYInProportionToX(self):
        self.transform = Matrix4.identity_matrix().shear(0, 0, 1, 0, 0, 0)
        self.p = point(2, 3, 4)
        self.assertEqual(self.transform * self.p, point(2, 5, 4))

    def test_Matrix_shearingTransformationMovesYInProportionToZ(self):
        self.transform = Matrix4.identity_matrix().shear(0, 0, 0, 1, 0, 0)
        self.p = point(2, 3, 4)
        self.assertEqual(self.transform * self.p, point(2, 7, 4))

    def test_Matrix_shearingTransformationMovesZInProportionToX(self):
        self.transform = Matrix4.identity_matrix().shear(0, 0, 0, 0, 1, 0)
        self.p = point(2, 3, 4)
        self.assertEqual(self.transform * self.p, point(2, 3, 6))

    def test_Matrix_shearingTransformationMovesZInProportionToY(self):
        self.transform = Matrix4.identity_matrix().shear(0, 0, 0, 0, 0, 1)
        self.p = point(2, 3, 4)
        self.assertEqual(self.transform * self.p, point(2, 3, 7))

    def test_Matrix_individualTransformationsAreSuppliedInSequence(self):
        self.p = point(1, 0, 1)
        self.A = Matrix4.identity_matrix().rotate_x(math.pi / 2)
        self.B = Matrix4.identity_matrix().scale(5, 5, 5)
        self.C = Matrix4.identity_matrix().translate(10, 5, 7)

        self.p2 = self.A * self.p
        self.assertEqual(self.p2, point(1, -1, 0))

        self.p3 = self.B * self.p2
        self.assertEqual(self.p3, point(5, -5, 0))

        self.p4 = self.C * self.p3
        self.assertEqual(self.p4, point(15, 0, 7))

    def test_Matrix_chainedTransformationsMustBeAppliedInReverseOrder(self):
        self.p = point(1, 0, 1)
        self.A = Matrix4.identity_matrix().rotate_x(math.pi / 2)
        self.B = Matrix4.identity_matrix().scale(5, 5, 5)
        self.C = Matrix4.identity_matrix().translate(10, 5, 7)

        self.T = self.C * self.B * self.A
        self.assertEqual(self.T * self.p, point(15, 0, 7))

    def test_Matrix_chainedTransformationsInOneLine(self):
        self.transform = Matrix4.identity_matrix().rotate_x(math.pi / 2).scale(5, 5, 5).translate(10, 5, 7)
        self.p = point(1, 0, 1)

        self.assertEqual(self.transform * self.p, point(15, 0, 7))


if __name__ == '__main__':
    unittest.main()
