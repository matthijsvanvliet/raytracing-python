import unittest
from Include.Shape import *
from Include.Sphere import Sphere
from Include.Intersection import Intersection
from Include.Plane import Plane
from Include.World import World

class TestIntersection(unittest.TestCase):
    def test_Intersection_anIntersectionEncapsulatesTAndObject(self):
        self.s = Sphere()
        self.i = Intersection(3.5, self.s)

        self.assertEqual(self.i.t, 3.5)
        self.assertEqual(self.i.object, self.s)

    def test_Intersection_aggregatingIntersections(self):
        self.s = Sphere()
        self.i1 = Intersection(1, self.s)
        self.i2 = Intersection(2, self.s)

        self.xs = Intersection.intersections(self.i1, self.i2)
        self.assertEqual(len(self.xs), 2)
        self.assertEqual(self.xs[0].t, 1)
        self.assertEqual(self.xs[1].t, 2)

    def test_Intersection_intersectSetsTheObjectOnTheIntersection(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.s = Sphere()

        self.xs = self.s.intersect(self.r)
        self.assertEqual(self.xs[0].object, self.s)
        self.assertEqual(self.xs[1].object, self.s)

    def test_Intersection_theHitWhenAllIntersectionsHaveAPositiveT(self):
        self.s = Sphere()
        self.i1 = Intersection(1, self.s)
        self.i2 = Intersection(2, self.s)
        self.xs = Intersection.intersections(self.i1, self.i2)

        self.i = Intersection.hit(self.xs)
        self.assertEqual(self.i, self.i1)

    def test_Intersection_theHitWhenSomeIntersectionsHaveNegativeT(self):
        self.s = Sphere()
        self.i1 = Intersection(-1, self.s)
        self.i2 = Intersection(1, self.s)
        self.xs = Intersection.intersections(self.i2, self.i1)

        self.i = Intersection.hit(self.xs)
        self.assertEqual(self.i, self.i2)

    def test_Intersection_theHitWhenAllIntersectionsHaveNegativeT(self):
        self.s = Sphere()
        self.i1 = Intersection(-2, self.s)
        self.i2 = Intersection(-1, self.s)
        self.xs = Intersection.intersections(self.i2, self.i1)

        self.i = Intersection.hit(self.xs)
        self.assertEqual(self.i, None)

    def test_Intersection_theHitIsAlwaysTheLowestNonnegativeIntersection(self):
        self.s = Sphere()
        self.i1 = Intersection(5, self.s)
        self.i2 = Intersection(7, self.s)
        self.i3 = Intersection(-3, self.s)
        self.i4 = Intersection(2, self.s)
        self.xs = Intersection.intersections(self.i1, self.i2, self.i3, self.i4)

        self.i = Intersection.hit(self.xs)
        self.assertEqual(self.i, self.i4)

    def test_Intersection_precomputeTheStateOfAnIntersection(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.shape = Sphere()
        self.i = Intersection(4, self.shape)

        self.comps = self.i.prepare_computations(self.r)

        self.assertEqual(self.comps.t, self.i.t)
        self.assertEqual(self.comps.object, self.i.object)
        self.assertEqual(self.comps.point, point(0, 0, -1))
        self.assertEqual(self.comps.eyev, vector(0, 0, -1))
        self.assertEqual(self.comps.normalv, vector(0, 0, -1))

    def test_Intersection_theHitWhenAnIntersectionOccursOnTheOutside(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.shape = Sphere()
        self.i = Intersection(4, self.shape)

        self.comps = self.i.prepare_computations(self.r)

        self.assertEqual(self.comps.inside, False)

    def test_Intersection_theHitWhenAnIntersectionOccursOnTheInside(self):
        self.r = Ray(point(0, 0, 0), vector(0, 0, 1))
        self.shape = Sphere()
        self.i = Intersection(1, self.shape)

        self.comps = self.i.prepare_computations(self.r)

        self.assertEqual(self.comps.point, point(0, 0, 1))
        self.assertEqual(self.comps.eyev, vector(0, 0, -1))
        self.assertEqual(self.comps.inside, True)
        self.assertEqual(self.comps.normalv, vector(0, 0, -1))

    def test_Intersection_precomputingTheReflectionVector(self):
        self.shape = Plane()
        self.r = Ray(point(0, 1, -1), vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        self.i = Intersection(math.sqrt(2), self.shape)

        self.comps = self.i.prepare_computations(self.r)

        self.assertEqual(self.comps.reflectv, vector(0, math.sqrt(2)/2, math.sqrt(2)/2))

    def test_Intersection_findingN1AndN2AtVariousIntersections(self):
        self.n1 = [1.0, 1.5, 2.0, 2.5, 2.5, 1.5]
        self.n2 = [1.5, 2.0, 2.5, 2.5, 1.5, 1.0]

        for index in range(len(self.n1)):
            self.A = Sphere.Glass()
            self.A.transform = self.A.transform.scale(2, 2, 2)
            self.A.material.refractive_index = 1.5
            self.B = Sphere.Glass()
            self.B.transform = self.B.transform.translate(0, 0, -0.25)
            self.B.material.refractive_index = 2.0
            self.C = Sphere.Glass()
            self.C.transform = self.C.transform.translate(0, 0, 0.25)
            self.C.material.refractive_index = 2.5
            self.r = Ray(point(0, 0, -4), vector(0, 0, 1))
            self.xs = Intersection.intersections(Intersection(2, self.A), Intersection(2.75, self.B), Intersection(3.25, self.C), Intersection(4.75, self.B), Intersection(5.25, self.C),
                                                 Intersection(6, self.A))

            self.comps = self.xs[index].prepare_computations(self.r, self.xs)

            self.assertEqual(self.comps.n1, self.n1[index])
            self.assertEqual(self.comps.n2, self.n2[index])

    def test_Intersection_theUnderPointIsOffsetBelowTheSurface(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.shape = Sphere.Glass()
        self.shape.transform = self.shape.transform.translate(0, 0, 1)
        self.i = Intersection(5, self.shape)
        self.xs = Intersection.intersections(self.i)

        self.comps = self.i.prepare_computations(self.r, self.xs)

        self.assertGreater(self.comps.under_point.z, EPSILON/2)
        self.assertLess(self.comps.point.z, self.comps.under_point.z)

    def test_Precomputations_theSchlickApproximationUnderTotalInternalReflection(self):
        self.shape = Sphere.Glass()
        self.r = Ray(point(0, 0, math.sqrt(2)/2), vector(0, 1, 0))
        self.xs = Intersection.intersections(Intersection(-math.sqrt(2)/2, self.shape), Intersection(math.sqrt(2)/2, self.shape))

        self.comps = self.xs[1].prepare_computations(self.r, self.xs)
        self.reflectance = self.comps.schlick()

        self.assertEqual(self.reflectance, 1.0)

    def test_Precomputations_theSchlickApproximationWithAPerpendicularViewingAngle(self):
        self.shape = Sphere.Glass()
        self.r = Ray(point(0, 0, 0), vector(0, 1, 0))
        self.xs = Intersection.intersections(Intersection(-1, self.shape), Intersection(1, self.shape))

        self.comps = self.xs[1].prepare_computations(self.r, self.xs)
        self.reflectance = self.comps.schlick()

        self.assertAlmostEqual(self.reflectance, 0.04)

    def test_Precomputations_theSchlickApproximationWithSmallAngleAndN2GreaterThanN1(self):
        self.shape = Sphere.Glass()
        self.r = Ray(point(0, 0.99, -2), vector(0, 0, 1))
        self.xs = Intersection.intersections(Intersection(1.8589, self.shape))

        self.comps = self.xs[0].prepare_computations(self.r, self.xs)
        self.reflectance = self.comps.schlick()

        self.assertAlmostEqual(self.reflectance, 0.48873, 5)

    def test_Intersection_shadeHitWithAReflectiveTransparentMaterial(self):
        self.w = World.default()
        self.r = Ray(point(0, 0, -3), vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        self.floor = Plane()
        self.floor.transform = self.floor.transform.translate(0, -1, 0)
        self.floor.material.reflective = 0.5
        self.floor.material.transparency = 0.5
        self.floor.material.refractive_index = 1.5
        self.w.objects.append(self.floor)
        self.ball = Sphere()
        self.ball.material.color = Color(1, 0, 0)
        self.ball.material.ambient = 0.5
        self.ball.transform = self.ball.transform.translate(0, -3.5, -0.5)
        self.w.objects.append(self.ball)
        self.xs = Intersection.intersections(Intersection(math.sqrt(2), self.floor))

        self.comps = self.xs[0].prepare_computations(self.r, self.xs)
        self.color = self.w.shade_hit(self.comps, 5)

        self.assertEqual(self.color, Color(0.93391, 0.69643, 0.69243))

if __name__ == '__main__':
    unittest.main()
