import unittest
from Include.Material import *
from Include.Light import *
from Include.StripePattern import *
from Include.Sphere import *

class TestMaterial(unittest.TestCase):
    def test_Material_theDefaultMaterial(self):
        self.m = Material()

        self.assertEqual(self.m.color, Color(1, 1, 1))
        self.assertEqual(self.m.ambient, 0.1)
        self.assertEqual(self.m.diffuse, 0.9)
        self.assertEqual(self.m.specular, 0.9)
        self.assertEqual(self.m.shininess, 200.0)

    def test_Material_reflectivityForTheDefaultMaterial(self):
        self.m = Material()

        self.assertEqual(self.m.reflective, 0.0)

    def test_Material_transparencyAndRefractiveIndexForTheDefaultMaterial(self):
        self.m = Material()

        self.assertEqual(self.m.transparency, 0.0)
        self.assertEqual(self.m.refractive_index, 1.0)



class TestMaterialLightSetup(unittest.TestCase):
    def setUp(self):
        self.m = Material()
        self.position = point(0, 0, 0)

class TestMaterialLight(TestMaterialLightSetup):
    def test_Material_lightingWithTheEyeBetweenTheLightAndTheSurface(self):
        self.eyev = vector(0, 0, -1)
        self.normalv = vector(0, 0, -1)
        self.light = PointLight(point(0, 0, -10), Color(1, 1, 1))

        self.result = self.m.lighting(Sphere(), self.light, self.position, self.eyev, self.normalv, False)
        self.assertEqual(self.result, Color(1.9, 1.9, 1.9))

    def test_Material_lightingWithTheEyeBetweenLightAndSurfaceWithEyeOffset45Degrees(self):
        self.eyev = vector(0, math.sqrt(2)/2, math.sqrt(2)/2)
        self.normalv = vector(0, 0, -1)
        self.light = PointLight(point(0, 0, -10), Color(1, 1, 1))

        self.result = self.m.lighting(Sphere(), self.light, self.position, self.eyev, self.normalv, False)
        self.assertEqual(self.result, Color(1, 1, 1))

    def test_Material_lightingWithEyeOppositeSurfaceWithLightOffset45Degrees(self):
        self.eyev = vector(0, 0, -1)
        self.normalv = vector(0, 0, -1)
        self.light = PointLight(point(0, 10, -10), Color(1, 1, 1))

        self.result = self.m.lighting(Sphere(), self.light, self.position, self.eyev, self.normalv, False)
        self.assertEqual(self.result, Color(0.7364, 0.7364, 0.7364))

    def test_Material_lightingWithEyeInThePathOfTheReflectionVector(self):
        self.eyev = vector(0, -math.sqrt(2)/2, -math.sqrt(2)/2)
        self.normalv = vector(0, 0, -1)
        self.light = PointLight(point(0, 10, -10), Color(1, 1, 1))

        self.result = self.m.lighting(Sphere(), self.light, self.position, self.eyev, self.normalv, False)
        self.assertEqual(self.result, Color(1.6364, 1.6364, 1.6364))

    def test_Material_lightingWithTheLightBehindTheSurface(self):
        self.eyev = vector(0, 0, -1)
        self.normalv = vector(0, 0, -1)
        self.light = PointLight(point(0, 0, 10), Color(1, 1, 1))

        self.result = self.m.lighting(Sphere(), self.light, self.position, self.eyev, self.normalv, False)
        self.assertEqual(self.result, Color(0.1, 0.1, 0.1))

    def test_Material_lightningWithTheSurfaceInShadow(self):
        self.eyev = vector(0, 0, -1)
        self.normalv = vector(0, 0, -1)
        self.light = PointLight(point(0, 0, -10), Color(1, 1, 1))
        self.in_shadow = True

        self.result = self.m.lighting(Sphere(), self.light, self.position, self.eyev, self.normalv, self.in_shadow)
        self.assertEqual(self.result, Color(0.1, 0.1, 0.1))

    def test_Material_lightingWithAPatternApplied(self):
        self.m.pattern = StripePattern(Color(1, 1, 1), Color(0, 0, 0))
        self.m.ambient = 1
        self.m.diffuse = 0
        self.m.specular = 0
        self.eyev = vector(0, 0, -1)
        self.normalv = vector(0, 0, -1)
        self.light = PointLight(point(0, 0, -10), Color(1, 1, 1))

        self.c1 = self.m.lighting(Sphere(), self.light, point(0.9, 0, 0), self.eyev, self.normalv, False)
        self.c2 = self.m.lighting(Sphere(), self.light, point(1.1, 0, 0), self.eyev, self.normalv, False)

        self.assertEqual(self.c1, Color(1, 1, 1))
        self.assertEqual(self.c2, Color(0, 0, 0))

if __name__ == '__main__':
    unittest.main()
