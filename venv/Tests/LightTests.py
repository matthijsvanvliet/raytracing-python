import unittest
from Include.Light import *

class TestPointLight(unittest.TestCase):
    def test_PointLight_aPointLightHasAPositionAndIntensity(self):
        self.intensity = Color(1, 1, 1)
        self.position = point(0, 0, 0)

        self.light = PointLight(self.position, self.intensity)
        self.assertEqual(self.light.position, self.position)
        self.assertEqual(self.light.intensity, self.intensity)


if __name__ == '__main__':
    unittest.main()
