import unittest
from Include.Camera import *

class TestTransformations(unittest.TestCase):
    def test_Transformations_theTransformationMatrixForTheDefaultOrientation(self):
        self._from = point(0, 0, 0)
        self.to = point(0, 0, -1)
        self.up = vector(0, 1, 0)

        self.t = Camera.view_transform(self._from, self.to, self.up)
        self.assertEqual(self.t, Matrix4.identity_matrix())

    def test_Transformations_aViewTransformationMatrixLookingInPositiveZDirection(self):
        self._from = point(0, 0, 0)
        self.to = point(0, 0, 1)
        self.up = vector(0, 1, 0)

        self.t = Camera.view_transform(self._from, self.to, self.up)
        self.assertEqual(self.t, Matrix4.identity_matrix().scale(-1, 1, -1))

    def test_Transformations_theViewTransformationMovesTheWorld(self):
        self._from = point(0, 0, 8)
        self.to = point(0, 0, 0)
        self.up = vector(0, 1, 0)

        self.t = Camera.view_transform(self._from, self.to, self.up)
        self.assertEqual(self.t, Matrix4.identity_matrix().translate(0, 0, -8))

    def test_Transformations_anArbitraryViewTransformation(self):
        self.list = [-0.50709, 0.50709, 0.67612, -2.36643, 0.76772, 0.60609, 0.12122, -2.82843, -0.35857, 0.59761, -0.71714, 0.0, 0.0, 0.0, 0.0, 1.0]
        self.M = Matrix4()
        self.index = 0
        for x in range(self.M.length):
            for y in range(self.M.length):
                self.M.m[x][y] = self.list[self.index]
                self.index += 1


        self._from = point(1, 3, 2)
        self.to = point(4, -2, 8)
        self.up = vector(1, 1, 0)

        self.t = Camera.view_transform(self._from, self.to, self.up)
        self.assertEqual(self.t, self.M)

class TestCamera(unittest.TestCase):
    def test_Camera_constructingACamera(self):
        self.hsize = 160
        self.vsize = 120
        self.field_of_view = math.pi/2

        self.c = Camera(self.hsize, self.vsize, self.field_of_view)
        self.assertEqual(self.c.hsize, 160)
        self.assertEqual(self.c.vsize, 120)
        self.assertEqual(self.c.field_of_view, math.pi/2)
        self.assertEqual(self.c.transform, Matrix4.identity_matrix())

    def test_Camera_thePixelSizeForAHorizontalCanvas(self):
        self.c = Camera(200, 125, math.pi/2)

        self.assertEqual(self.c.pixel_size, 0.01)

    def test_Camera_thePixelSizeForAVerticalCanvas(self):
        self.c = Camera(125, 200, math.pi / 2)

        self.assertAlmostEqual(self.c.pixel_size, 0.01)

    def test_Camera_constructingARayThroughTheCenterOfTheCanvas(self):
        self.c = Camera(201, 101, math.pi/2)
        self.r = self.c.ray_for_pixel(100, 50)

        self.assertEqual(self.r.origin, point(0, 0, 0))
        self.assertEqual(self.r.direction, vector(0, 0, -1))

    def test_Camera_constructingARayThroughACornerOfTheCanvas(self):
        self.c = Camera(201, 101, math.pi / 2)
        self.r = self.c.ray_for_pixel(0, 0)

        self.assertEqual(self.r.origin, point(0, 0, 0))
        self.assertEqual(self.r.direction, vector(0.66519, 0.33259, -0.66851))

    def test_Camera_constructingARayWhenTheCameraIsTranformed(self):
        self.c = Camera(201, 101, math.pi / 2)
        self.c.transform = self.c.transform.translate(0, -2, 5).rotate_y(math.pi/4) # self.c.transform.rotate_y(math.pi/4) * Matrix4.identity_matrix().translate(0, -2, 5)
        self.r = self.c.ray_for_pixel(100, 50)

        self.assertEqual(self.r.origin, point(0, 2, -5))
        self.assertEqual(self.r.direction, vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2))

    def test_Camera_renderingAWorldWithACamera(self):
        self.w = World.default()
        self.c = Camera(11, 11, math.pi/2)
        self._from = point(0, 0, -5)
        self.to = point(0, 0, 0)
        self.up = vector(0, 1, 0)
        self.c.transform = Camera.view_transform(self._from, self.to, self.up)

        self.image = self.c.render(self.w)
        self.assertEqual(self.image.get_pixel(5, 5), Color(0.38066, 0.47583, 0.2855))

if __name__ == '__main__':
    unittest.main()
