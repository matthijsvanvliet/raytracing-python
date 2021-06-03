import unittest
from Include.Canvas import *

class TestCanvas(unittest.TestCase):
    def test_Canvas_createCanvas(self):
        self.c = Canvas(10, 20)
        self.assertEqual(self.c.width, 10)
        self.assertEqual(self.c.height, 20)
        for x in range(self.c.height):
            for y in range(self.c.width):
                self.assertEqual(self.c.pixel[x][y], Color(0, 0, 0))

    def test_Canvas_writePixelToCanvas(self):
        self.c = Canvas(10, 20)
        self.red = Color(1, 0, 0)
        self.c.write_pixel(2, 3, self.red)
        self.assertEqual(self.c.pixel[3][2], self.red)

    def test_Canvas_constructAPPMHeader(self):
        self.c = Canvas(5, 3)
        self.ppm = self.c.to_ppm()
        self.assertEqual(self.ppm[0:10], "P3\n5 3\n255")

    def test_Canvas_constructThePPMPixelData(self):
        self.c = Canvas(5, 3)
        self.c1 = Color(1.5, 0, 0)
        self.c2 = Color(0, 0.5, 0)
        self.c3 = Color(-0.5, 0, 1)

        self.c.write_pixel(0, 0, self.c1)
        self.c.write_pixel(2, 1, self.c2)
        self.c.write_pixel(4, 2, self.c3)

        self.ppm = self.c.to_ppm()
        self.assertEqual(self.ppm[11:-1], "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \n0 0 0 0 0 0 0 128 0 0 0 0 0 0 0 \n0 0 0 0 0 0 0 0 0 0 0 0 0 0 255 ")

    def test_Canvas_splittingLongLinesInPPMFile(self):
        self.c = Canvas(10, 2)
        for x in range(self.c.width):
            for y in range(self.c.height):
                self.c.write_pixel(x, y, Color(1, 0.8, 0.6))
        self.ppm = self.c.to_ppm()
        self.assertEqual(self.ppm[12:-1], "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204 \n153 255 204 153 255 204 153 255 204 153 255 204 153 \n255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204 \n153 255 204 153 255 204 153 255 204 153 255 204 153 ")

if __name__ == '__main__':
    unittest.main()
