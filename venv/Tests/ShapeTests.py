import unittest
from Include.Shape import *
from Include.Sphere import Sphere
from Include.Plane import Plane
from Include.Intersection import Intersection

class Test_Shape(unittest.TestCase):
    def test_Sphere_aRayIntersectsASphereAtTwoPoints(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.s = Sphere()
        self.xs = self.s.intersect(self.r)

        self.assertEqual(len(self.xs), 2)
        self.assertEqual(self.xs[0].t, 4.0)
        self.assertEqual(self.xs[1].t, 6.0)

    def test_Sphere_aRayIntersectsASphereAtATangent(self):
        self.r = Ray(point(0, 1, -5), vector(0, 0, 1))
        self.s = Sphere()
        self.xs = self.s.intersect(self.r)

        self.assertEqual(len(self.xs), 2)
        self.assertEqual(self.xs[0].t, 5.0)
        self.assertEqual(self.xs[1].t, 5.0)

    def test_Sphere_aRayMissesASphere(self):
        self.r = Ray(point(0, 2, -5), vector(0, 0, 1))
        self.s = Sphere()
        self.xs = self.s.intersect(self.r)

        self.assertEqual(len(self.xs), 0)

    def test_Sphere_aRayOriginatesInsideASphere(self):
        self.r = Ray(point(0, 0, 0), vector(0, 0, 1))
        self.s = Sphere()
        self.xs = self.s.intersect(self.r)

        self.assertEqual(len(self.xs), 2)
        self.assertEqual(self.xs[0].t, -1.0)
        self.assertEqual(self.xs[1].t, 1.0)

    def test_Sphere_aSphereIsBehindARay(self):
        self.r = Ray(point(0, 0, 5), vector(0, 0, 1))
        self.s = Sphere()
        self.xs = self.s.intersect(self.r)

        self.assertEqual(len(self.xs), 2)
        self.assertEqual(self.xs[0].t, -6.0)
        self.assertEqual(self.xs[1].t, -4.0)

    def test_Sphere_aSpheresDefaultTranformation(self):
        self.s = Sphere()

        self.assertEqual(self.s.transform, Matrix4.identity_matrix())

    def test_Sphere_changingASpheresTransformation(self):
        self.s = Sphere()
        self.t = Matrix4.identity_matrix().translate(2, 3, 4)
        self.s.transform = self.t

        self.assertEqual(self.s.transform, self.t)

    def test_Sphere_intersectingAScaledSphereWithARay(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.s = Sphere()

        self.s.transform = Matrix4.identity_matrix().scale(2, 2, 2)
        self.xs = self.s.intersect(self.r)

        self.assertEqual(len(self.xs), 2)
        self.assertEqual(self.xs[0].t, 3)
        self.assertEqual(self.xs[1].t, 7)

    def test_Sphere_intersectingATranslatedSphereWithARay(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.s = Sphere()

        self.s.transform = Matrix4.identity_matrix().translate(5, 0, 0)
        self.xs = self.s.intersect(self.r)

        self.assertEqual(len(self.xs), 0)

    def test_Sphere_theNormalOnASphereAtAPointOnTheXAxis(self):
        self.s = Sphere()
        self.n = self.s.normal_at(point(1, 0, 0))

        self.assertEqual(self.n, vector(1, 0, 0))

    def test_Sphere_theNormalOnASphereAtAPointOnTheYAxis(self):
        self.s = Sphere()
        self.n = self.s.normal_at(point(0, 1, 0))

        self.assertEqual(self.n, vector(0, 1, 0))

    def test_Sphere_theNormalOnASphereAtAPointOnTheZAxis(self):
        self.s = Sphere()
        self.n = self.s.normal_at(point(0, 0, 1))

        self.assertEqual(self.n, vector(0, 0, 1))

    def test_Sphere_theNormalOnASphereAtANonaxialPoint(self):
        self.s = Sphere()
        self.n = self.s.normal_at(point(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))

        self.assertEqual(self.n, vector(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))

    def test_Sphere_theNormalIsANormalizedVector(self):
        self.s = Sphere()
        self.n = self.s.normal_at(point(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))

        self.assertEqual(self.n, self.n.normalize())

    def test_Sphere_computingTheNormalOnATranslatedSphere(self):
        self.s = Sphere()
        self.s.transform = Matrix4.identity_matrix().translate(0, 1, 0)

        self.n = self.s.normal_at(point(0, 1.70711, -0.70711))
        self.assertEqual(self.n, vector(0, 0.70711, -0.70711))

    def test_Sphere_computingTheNormalOnATransformedSphere(self):
        self.s = Sphere()
        self.m = Matrix4.identity_matrix().scale(1, 0.5, 1) * Matrix4.identity_matrix().rotate_z(math.pi / 5)
        self.s.transform = self.m

        self.n = self.s.normal_at(point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
        self.assertEqual(self.n, vector(0, 0.97014, -0.24254))

    def test_TestShape_TheDefaultTransformation(self):
        self.s = TestShape()

        self.assertEqual(self.s.transform, Matrix4.identity_matrix())

    def test_TestShape_assigningATranformation(self):
        self.s = TestShape()

        self.s.transform = self.s.transform.translate(2, 3, 4)

        self.assertEqual(self.s.transform, Matrix4.identity_matrix().translate(2, 3, 4))

    def test_TestShape_theDefaultMaterial(self):
        self.s = TestShape()

        self.m = self.s.material

        self.assertEqual(self.m, Material())

    def test_TestShape_assigningAMaterial(self):
        self.s = TestShape()
        self.m = Material()
        self.m.ambient = 1

        self.s.material = self.m

        self.assertEqual(self.s.material, self.m)

    def test_TestShape_intersectingAScaledShapeWithARay(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.s = TestShape()

        self.s.transform = self.s.transform.scale(2, 2, 2)
        self.xs = self.s.intersect(self.r)

        self.assertEqual(self.s.saved_ray.origin, point(0, 0, -2.5))
        self.assertEqual(self.s.saved_ray.direction, vector(0, 0, 0.5))

    def test_TestShape_intersectingATranslatedShapeWithARay(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.s = TestShape()

        self.s.transform = self.s.transform.translate(5, 0, 0)
        self.xs = self.s.intersect(self.r)

        self.assertEqual(self.s.saved_ray.origin, point(-5, 0, -5))
        self.assertEqual(self.s.saved_ray.direction, vector(0, 0, 1))

    def test_TestShape_computingTheNormalOnATranslatedShape(self):
        self.s = TestShape()

        self.s.transform = self.s.transform.translate(0, 1, 0)
        self.n = self.s.normal_at(point(0, 1.70711, -0.70711))

        self.assertEqual(self.n, vector(0, 0.70711, -0.70711))

    def test_TestShape_computingTheNormalOnATransformedShape(self):
        self.s = TestShape()

        self.s.transform = self.s.transform.rotate_z(math.pi/5).scale(1, 0.5, 1)
        self.n = self.s.normal_at(point(0, math.sqrt(2)/2, -math.sqrt(2)/2))

        self.assertEqual(self.n, vector(0, 0.97014, -0.24254))

    def test_Sphere_parentObjectIsShape(self):
        self.s = Sphere()

        self.assertIsInstance(self.s, Shape)

    def test_Plane_theNormalOfAPlaneIsConstantEverywhere(self):
        self.p = Plane()

        self.n1 = self.p.local_normal_at(point(0, 0, 0))
        self.n2 = self.p.local_normal_at(point(10, 0, -10))
        self.n3 = self.p.local_normal_at(point(-5, 0, 150))

        self.assertEqual(self.n1, vector(0, 1, 0))
        self.assertEqual(self.n2, vector(0, 1, 0))
        self.assertEqual(self.n3, vector(0, 1, 0))

    def test_Plane_intersectWithARayParallelToThePlane(self):
        self.p = Plane()
        self.r = Ray(point(0, 10, 0), vector(0, 0, 1))

        self.xs = self.p.local_intersect(self.r)

        self.assertEqual(len(self.xs), 0)

    def test_Plane_intersectWithACoplanarRay(self):
        self.p = Plane()
        self.r = Ray(point(0, 0, 0), vector(0, 0, 1))

        self.xs = self.p.local_intersect(self.r)

        self.assertEqual(len(self.xs), 0)

    def test_Plane_aRayIntersectingAPlaneFromAbove(self):
        self.p = Plane()
        self.r = Ray(point(0, 1, 0), vector(0, -1, 0))

        self.xs = self.p.local_intersect(self.r)

        self.assertEqual(len(self.xs), 1)
        self.assertEqual(self.xs[0].t, 1)
        self.assertEqual(self.xs[0].object, self.p)

    def test_Plane_aRayIntersectingAPlaneFromBelow(self):
        self.p = Plane()
        self.r = Ray(point(0, -1, 0), vector(0, 1, 0))

        self.xs = self.p.local_intersect(self.r)

        self.assertEqual(len(self.xs), 1)
        self.assertEqual(self.xs[0].t, 1)
        self.assertEqual(self.xs[0].object, self.p)

    def test_Sphere_aHelperForProducingASphereWithAGlassyMaterial(self):
        self.s = Sphere.Glass()

        self.assertEqual(self.s.transform, Matrix4.identity_matrix())
        self.assertEqual(self.s.material.transparency, 1.0)
        self.assertEqual(self.s.material.refractive_index, 1.5)

if __name__ == '__main__':
    unittest.main()
