import unittest
from Include.Shape import *
from Include.Matrix import *

class TestRay(unittest.TestCase):
    def test_Ray_createAndQueryingARay(self):
        self.origin = point(1, 2, 3)
        self.direction = vector(4, 5, 6)
        self.r = Ray(self.origin, self.direction)

        self.assertEqual(self.r.origin, self.origin)
        self.assertEqual(self.r.direction, self.direction)

    def test_Ray_computingAPointFromADistance(self):
        self.r = Ray(point(2, 3, 4), vector(1, 0, 0))

        self.assertEqual(self.r.position(0), point(2, 3, 4))
        self.assertEqual(self.r.position(1), point(3, 3, 4))
        self.assertEqual(self.r.position(-1), point(1, 3, 4))
        self.assertEqual(self.r.position(2.5), point(4.5, 3, 4))

    def test_Ray_translatingARay(self):
        self.r = Ray(point(1, 2, 3), vector(0, 1, 0))
        self.m = Matrix4.identity_matrix().translate(3, 4, 5)
        self.r2 = self.r.transform(self.m)

        self.assertEqual(self.r2.origin, point(4, 6, 8))
        self.assertEqual(self.r2.direction, vector(0, 1, 0))

    def test_Ray_scalingARay(self):
        self.r = Ray(point(1, 2, 3), vector(0, 1, 0))
        self.m = Matrix4.identity_matrix().scale(2, 3, 4)
        self.r2 = self.r.transform(self.m)

        self.assertEqual(self.r2.origin, point(2, 6, 12))
        self.assertEqual(self.r2.direction, vector(0, 3, 0))





if __name__ == '__main__':
    unittest.main()
