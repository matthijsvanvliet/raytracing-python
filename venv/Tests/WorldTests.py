import unittest
from Include.World import *
from Include.Plane import Plane
from Include.Pattern import TestPattern

class TestWorld(unittest.TestCase):
    def test_World_creatingAWorld(self):
        self.w = World()

        self.assertEqual(len(self.w.objects), 0)
        self.assertEqual(self.w.light_source, None)

    def test_World_theDefaultWorld(self):
        self.light = PointLight(point(-10, 10, -10), Color(1, 1, 1))
        self.s1 = Sphere()
        self.s1.material.color = Color(0.8, 1.0, 0.6)
        self.s1.material.diffuse = 0.7
        self.s1.material.specular = 0.2
        self.s2 = Sphere()
        self.s2.transform = Matrix4.identity_matrix().scale(0.5, 0.5, 0.5)
        self.w = World.default()

        self.assertEqual(self.w.light_source, self.light)
        self.assertEqual(self.w.objects[0], self.s1)
        self.assertEqual(self.w.objects[1], self.s2)

    def test_World_intersectAWorldWithARay(self):
        self.w = World.default()
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.xs = self.w.intersect(self.r)

        self.assertEqual(len(self.xs), 4)
        self.assertEqual(self.xs[0].t, 4)
        self.assertEqual(self.xs[1].t, 4.5)
        self.assertEqual(self.xs[2].t, 5.5)
        self.assertEqual(self.xs[3].t, 6)

    def test_World_shadingAnIntersection(self):
        self.w = World.default()
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.shape = self.w.objects[0]
        self.i = Intersection(4, self.shape)

        self.comps = self.i.prepare_computations(self.r)
        self.c = self.w.shade_hit(self.comps)

        self.assertEqual(self.c, Color(0.38066, 0.47583, 0.2855))

    def test_World_shadingAnIntersectionFromTheInside(self):
        self.w = World.default()
        self.w.light_source = PointLight(point(0, 0.25, 0), Color(1, 1, 1))
        self.r = Ray(point(0, 0, 0), vector(0, 0, 1))
        self.shape = self.w.objects[1]
        self.i = Intersection(0.5, self.shape)

        self.comps = self.i.prepare_computations(self.r)
        self.c = self.w.shade_hit(self.comps)

        self.assertEqual(self.c, Color(0.90498, 0.90498, 0.90498))

    def test_World_theColorWhenARayMisses(self):
        self.w = World.default()
        self.r = Ray(point(0, 0, -5), vector(0, 1, 0))

        self.c = self.w.color_at(self.r)
        self.assertEqual(self.c, Color(0, 0, 0))

    def test_World_theColorWhenTheRayHits(self):
        self.w = World.default()
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))

        self.c = self.w.color_at(self.r)
        self.assertEqual(self.c, Color(0.38066, 0.47583, 0.2855))

    def test_World_theColorWithAnIntersectionBehindTheRay(self):
        self.w = World.default()
        self.outer = self.w.objects[0]
        self.outer.material.ambient = 1
        self.inner = self.w.objects[1]
        self.inner.material.ambient = 1
        self.r = Ray(point(0, 0, 0.75), vector(0, 0, -1))

        self.c = self.w.color_at(self.r)
        self.assertEqual(self.c, self.inner.material.color)

    def test_World_thereIsNoShadowWhenNothingIsCollinearWithPointAndLight(self):
        self.w = World.default()
        self.p = point(0, 10, 0)

        self.assertEqual(self.w.is_shadowed(self.p), False)

    def test_World_theShadowWhenAnObjectIsBetweenThePointAndTheLight(self):
        self.w = World.default()
        self.p = point(10, -10, 10)

        self.assertEqual(self.w.is_shadowed(self.p), True)

    def test_World_thereIsNoShadowWhenAnObjectisBehindTheLight(self):
        self.w = World.default()
        self.p = point(-20, 20, -20)

        self.assertEqual(self.w.is_shadowed(self.p), False)

    def test_World_thereIsNoShadowWhenAnObjectIsBehindThePoint(self):
        self.w = World.default()
        self.p = point(-2, 2, -2)

        self.assertEqual(self.w.is_shadowed(self.p), False)

    def test_World_shade_hitIsGivenAnIntersectionInShadow(self):
        self.w = World()
        self.w.light_source = PointLight(point(0, 0, -10), Color(1, 1, 1))
        self.s1 = Sphere()
        self.w.objects.append(self.s1)
        self.s2 = Sphere()
        self.s2.transform = self.s2.transform.translate(0, 0, 10)
        self.w.objects.append(self.s2)
        self.r = Ray(point(0, 0, 5), vector(0, 0, 1))
        self.i = Intersection(4, self.s2)

        self.comps = self.i.prepare_computations(self.r)
        self.c = self.w.shade_hit(self.comps)
        self.assertEqual(self.c, Color(0.1, 0.1, 0.1))

    def test_World_theHitShouldOffsetThePoint(self):
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.shape = Sphere()
        self.shape.transform = self.shape.transform.translate(0, 0, 1)
        self.i = Intersection(5, self.shape)

        self.comps = self.i.prepare_computations(self.r)

        self.assertLess(self.comps.over_point.z, -EPSILON/2)
        self.assertGreater(self.comps.point.z, self.comps.over_point.z)

    def test_World_theReflectedColorForANonreflectiveMaterial(self):
        self.w = World.default()
        self.r = Ray(point(0, 0, 0), vector(0, 0, 1))
        self.shape = self.w.objects[1]
        self.shape.material.ambient = 1
        self.i = Intersection(1, self.shape)

        self.comps = self.i.prepare_computations(self.r)
        self.color = self.w.reflected_color(self.comps)

        self.assertEqual(self.color, Color(0, 0, 0))

    def test_World_theReflectedColorForAReflectiveMaterial(self):
        self.w = World.default()
        self.shape = Plane()
        self.shape.material.reflective = 0.5
        self.shape.transform = self.shape.transform.translate(0, -1, 0)
        self.w.objects.append(self.shape)
        self.r = Ray(point(0, 0, -3), vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        self.i = Intersection(math.sqrt(2), self.shape)

        self.comps = self.i.prepare_computations(self.r)
        self.color = self.w.reflected_color(self.comps)

        self.assertEqual(self.color, Color(0.19033, 0.23791, 0.14274))

    def test_World_theShadeHitFunctionWithAReflectiveMaterial(self):
        self.w = World.default()
        self.shape = Plane()
        self.shape.material.reflective = 0.5
        self.shape.transform = self.shape.transform.translate(0, -1, 0)
        self.w.objects.append(self.shape)
        self.r = Ray(point(0, 0, -3), vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        self.i = Intersection(math.sqrt(2), self.shape)

        self.comps = self.i.prepare_computations(self.r)
        self.color = self.w.shade_hit(self.comps)

        self.assertEqual(self.color, Color(0.87676, 0.92434, 0.82917))

    def test_World_theColorAtFunctionWithMutuallyReflectiveSurfaces(self):
        self.w = World()
        self.w.light_source = PointLight(point(0, 0, 0), Color(1, 1, 1))
        self.lower = Plane()
        self.lower.material.reflective = 1
        self.lower.transform = self.lower.transform.translate(0, -1, 0)
        self.w.objects.append(self.lower)
        self.upper = Plane()
        self.upper.material.reflective = 1
        self.upper.transform = self.upper.transform.translate(0, 1, 0)
        self.w.objects.append(self.upper)
        self.r = Ray(point(0, 0, 0), vector(0, 1, 0))

        with self.assertRaises(RecursionError):
            self.w.color_at(self.r)

    def test_World_theReflectedColorAtTheMaximumRecursiveLength(self):
        self.w = World.default()
        self.shape = Plane()
        self.shape.material.reflective = 0.5
        self.shape.transform = self.shape.transform.translate(0, -1, 0)
        self.w.objects.append(self.shape)
        self.r = Ray(point(0, 0, -3), vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
        self.i = Intersection(math.sqrt(2), self.shape)

        self.comps = self.i.prepare_computations(self.r)
        self.color = self.w.reflected_color(self.comps, 0)

        self.assertEqual(self.color, Color(0, 0, 0))

    def test_World_theRefractedColorWithAnOpaqueSurface(self):
        self.w = World.default()
        self.shape = self.w.objects[0]
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.xs = Intersection.intersections(Intersection(4, self.shape), Intersection(6, self.shape))

        self.comps = self.xs[0].prepare_computations(self.r, self.xs)
        self.c = self.w.refracted_color(self.comps, 5)

        self.assertEqual(self.c, Color(0, 0, 0))

    def test_World_theRefractedColorAtTheMaximumRecursiveDepth(self):
        self.w = World.default()
        self.shape = self.w.objects[0]
        self.shape.material.transparency = 1.0
        self.shape.material.refractive_index = 1.5
        self.r = Ray(point(0, 0, -5), vector(0, 0, 1))
        self.xs = Intersection.intersections(Intersection(4, self.shape), Intersection(6, self.shape))

        self.comps = self.xs[0].prepare_computations(self.r, self.xs)
        self.c = self.w.refracted_color(self.comps, 0)

        self.assertEqual(self.c, Color(0, 0, 0))

    def test_World_theRefractedColorUnderTotalInternalReflection(self):
        self.w = World.default()
        self.shape = self.w.objects[0]
        self.shape.material.transparency = 1.0
        self.shape.material.refractive_index = 1.5
        self.r = Ray(point(0, 0, math.sqrt(2)/2), vector(0, 1, 0))
        self.xs = Intersection.intersections(Intersection(-math.sqrt(2)/2, self.shape), Intersection(math.sqrt(2)/2, self.shape))

        self.comps = self.xs[1].prepare_computations(self.r, self.xs)
        self.c = self.w.refracted_color(self.comps, 5)

        self.assertEqual(self.c, Color(0, 0, 0))

    def test_World_theRefractedColorWithARefractedRay(self):
        self.w = World.default()
        self.A = self.w.objects[0]
        self.A.material.ambient = 1.0
        self.A.material.pattern = TestPattern()
        self.B = self.w.objects[1]
        self.B.material.transparency = 1.0
        self.B.material.refractive_index = 1.5
        self.r = Ray(point(0, 0, 0.1), vector(0, 1, 0))
        self.xs = Intersection.intersections(Intersection(-0.9899, self.A), Intersection(-0.4899, self.B), Intersection(0.4899, self.B), Intersection(0.9899, self.A))

        self.comps = self.xs[2].prepare_computations(self.r, self.xs)
        self.c = self.w.refracted_color(self.comps, 5)

        self.assertEqual(self.c, Color(0, 0.99887, 0.04722))

    def test_World_shadehitWithATransparentMaterial(self):
        self.w = World.default()
        self.floor = Plane()
        self.floor.transform = self.floor.transform.translate(0, -1, 0)
        self.floor.material.transparency = 0.5
        self.floor.material.refractive_index = 1.5
        self.w.objects.append(self.floor)
        self.ball = Sphere()
        self.ball.material.color = Color(1, 0, 0)
        self.ball.material.ambient = 0.5
        self.ball.transform = self.ball.transform.translate(0, -3.5, -0.5)
        self.w.objects.append(self.ball)
        self.r = Ray(point(0, 0, -3), vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        self.xs = Intersection.intersections(Intersection(math.sqrt(2), self.floor))

        self.comps = self.xs[0].prepare_computations(self.r, self.xs)
        self.color = self.w.shade_hit(self.comps, 5)

        self.assertEqual(self.color, Color(0.93642, 0.68642, 0.68642))

if __name__ == '__main__':
    unittest.main()
