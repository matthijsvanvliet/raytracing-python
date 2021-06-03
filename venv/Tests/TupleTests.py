import unittest
import math

from Include.Tuple import *

#
# Tuple Unit tests
#
class TestTuplePointVector(unittest.TestCase):
    def test_Tuple_ifWArgumentIsOneTupleIsPoint(self):
        self.a = Tuple(4.3, -4.2, 3.1, 1.0)
        self.assertEqual(self.a.x, 4.3)
        self.assertEqual(self.a.y, -4.2)
        self.assertEqual(self.a.z, 3.1)
        self.assertEqual(self.a.w, 1.0)
        self.assertEqual(self.a.get_type(), TupleTypes.POINT)
        self.assertNotEqual(self.a.get_type(), TupleTypes.VECTOR)

    def test_Tuple_ifWArgumentIsZeroTupleIsVector(self):
        self.a = Tuple(4.3, -4.2, 3.1, 0.0)
        self.assertEqual(self.a.x, 4.3)
        self.assertEqual(self.a.y, -4.2)
        self.assertEqual(self.a.z, 3.1)
        self.assertEqual(self.a.w, 0.0)
        self.assertEqual(self.a.get_type(), TupleTypes.VECTOR)
        self.assertNotEqual(self.a.get_type(), TupleTypes.POINT)

class TestTupleArithmetic(unittest.TestCase):
    def test_Tuple_addTwoTuples(self):
        self.a1 = Tuple(3, -2, 5, 1)
        self.a2 = Tuple(-2, 3, 1, 0)
        self.result = self.a1 + self.a2
        self.assertEqual(self.result, Tuple(1, 1, 6, 1))

    def test_Tuple_subtractTwoPoints(self):
        self.p1 = point(3, 2, 1)
        self.p2 = point(5, 6, 7)
        self.result = self.p1 - self.p2
        self.assertEqual(self.result, vector(-2, -4, -6))

    def test_Tuple_subtractAVectorFromAPoint(self):
        self.p = point(3, 2, 1)
        self.v = vector(5, 6, 7)
        self.result = self.p - self.v
        self.assertEqual(self.result, point(-2, -4, -6))

    def test_Tuple_subtractTwoVectors(self):
        self.v1 = vector(3, 2, 1)
        self.v2 = vector(5, 6, 7)
        self.result = self.v1 - self.v2
        self.assertEqual(self.result, vector(-2, -4, -6))

    def test_Tuple_subtractVectorFromZeroVector(self):
        self.zero = vector(0, 0, 0)
        self.v = vector(1, -2, 3)
        self.result = self.zero - self.v
        self.assertEqual(self.result, vector(-1, 2, -3))

    def test_Tuple_negateATuple(self):
        self.a = Tuple(1, -2, 3, -4)
        self.result = -self.a
        self.assertEqual(self.result, Tuple(-1, 2, -3, 4))

    def test_Tuple_multiplyATupleByAScalar(self):
        self.a = Tuple(1, -2, 3, -4)
        self.result = self.a * 3.5
        self.assertEqual(self.result, Tuple(3.5, -7, 10.5, -14))

    def test_Tuple_multiplyATupleByAFraction(self):
        self.a = Tuple(1, -2, 3, -4)
        self.result = self.a * 0.5
        self.assertEqual(self.result, Tuple(0.5, -1, 1.5, -2))

    def test_Tuple_divideATupleByAScalar(self):
        self.a = Tuple(1, -2, 3, -4)
        self.result = self.a / 2
        self.assertEqual(self.result, Tuple(0.5, -1, 1.5, -2))

class TestTupleMagnitude(unittest.TestCase):
    def test_Tuple_computeTheMagnitudeWithVectorXComponentOne(self):
        self.v = vector(1, 0, 0)
        self.result = self.v.magnitude()
        self.assertEqual(self.result, 1)

    def test_Tuple_computeTheMagnitudeWithVectorYComponentOne(self):
        self.v = vector(0, 1, 0)
        self.result = self.v.magnitude()
        self.assertEqual(self.result, 1)

    def test_Tuple_computeTheMagnitudeWithVectorZComponentOne(self):
        self.v = vector(0, 0, 1)
        self.result = self.v.magnitude()
        self.assertEqual(self.result, 1)

    def test_Tuple_computeTheMagnitudeWithVectorOneTwoThree(self):
        self.v = vector(1, 2, 3)
        self.result = self.v.magnitude()
        self.assertEqual(self.result, math.sqrt(14))

    def test_Tuple_computeTheMagnitudeWithVectorMinusOneTwoThree(self):
        self.v = vector(-1, -2, -3)
        self.result = self.v.magnitude()
        self.assertEqual(self.result, math.sqrt(14))

class TestTupleNormalize(unittest.TestCase):
    def test_Tuple_normalizeVectorWithXAsFour(self):
        self.v = vector(4, 0, 0)
        self.result = self.v.normalize()
        self.assertEqual(self.result, vector(1, 0, 0))

    def test_Tuple_normalizeVectorMinusOneTwoThree(self):
        self.v = vector(1, 2, 3)
        self.magnitude = math.sqrt(14)
        self.result = self.v.normalize()
        self.assertEqual(self.result, vector(1/self.magnitude, 2/self.magnitude, 3/self.magnitude))

    def test_Tuple_computeMagnitudeOfNormalizedVector(self):
        self.v = vector(1, 2, 3)
        self.norm = self.v.normalize()
        self.result = self.norm.magnitude()
        self.assertEqual(self.result, 1)

class TestTupleDotProduct(unittest.TestCase):
    def test_Tuple_theDotProductOfTwoTuples(self):
        self.a = vector(1, 2, 3)
        self.b = vector(2, 3, 4)
        self.result = self.a.dot(self.b)
        self.assertEqual(self.result, 20)

class TestTupleCrossProduct(unittest.TestCase):
    def test_Tuple_theCrossProductOfTwoVectors(self):
        self.a = vector(1, 2, 3)
        self.b = vector(2, 3, 4)
        self.result1 = self.a.cross(self.b)
        self.result2 = self.b.cross(self.a)
        self.assertEqual(self.result1, vector(-1, 2, -1))
        self.assertEqual(self.result2, vector(1, -2, 1))

#
# Color Struct Unit test
#
class TestTupleColor(unittest.TestCase):
    def test_Color_createsAColor(self):
        self.c = Color(-0.5, 0.4, 1.7)
        self.assertEqual(self.c.red, -0.5)
        self.assertEqual(self.c.green, 0.4)
        self.assertEqual(self.c.blue, 1.7)

    def test_Color_AddColors(self):
        self.c1 = Color(0.9, 0.6, 0.75)
        self.c2 = Color(0.7, 0.1, 0.25)
        self.result = self.c1 + self.c2
        self.assertEqual(self.result, Color(1.6, 0.7, 1.0))

    def test_Color_SubtractColors(self):
        self.c1 = Color(0.9, 0.6, 0.75)
        self.c2 = Color(0.6, 0.1, 0.25)
        self.result = self.c1 - self.c2
        self.assertEqual(self.result, Color(0.3, 0.5, 0.5))

    def test_Color_MultiplyColorWithScalar(self):
        self.c = Color(0.2, 0.3, 0.4)
        self.result = self.c * 2
        self.assertEqual(self.result, Color(0.4, 0.6, 0.8))

    def test_Color_MultiplyingColors(self):
        self.c1 = Color(1, 0.2, 0.4)
        self.c2 = Color(0.9, 1, 0.1)
        self.result = self.c1 * self.c2
        self.assertEqual(self.result, Color(0.9, 0.2, 0.04))

    def test_Tuple_reflectingAVectorApproachingAt45Degrees(self):
        self.v = vector(1, -1, 0)
        self.n = vector(0, 1, 0)

        self.r = self.v.reflect(self.n)
        self.assertEqual(self.r, vector(1, 1, 0))

    def test_Tuple_reflectingAVectorOffASlantedSurface(self):
        self.v = vector(0, -1, 0)
        self.n = vector(math.sqrt(2)/2, math.sqrt(2)/2, 0)

        self.r = self.v.reflect(self.n)
        self.assertEqual(self.r, vector(1, 0, 0))



#
# Point function Unit tests
#
class TestTuplePoint(unittest.TestCase):
    def test_point_functionCreatesATupleAsAPoint(self):
        self.point = point(4, -4, 3)
        self.assertEqual(self.point, Tuple(4, -4, 3, 1))

#
# Vector function Unit tests
#
class TestTupleVector(unittest.TestCase):
    def test_vector_functionCreatesATupleAsAVector(self):
        self.vector = vector(4, -4, 3)
        self.assertEqual(self.vector, Tuple(4, -4, 3, 0))

if __name__ == '__main__':
    unittest.main()


