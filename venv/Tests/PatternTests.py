import unittest
from Include.StripePattern import *
from Include.Pattern import TestPattern
from Include.GradientPattern import GradientPattern
from Include.RingPattern import RingPattern
from Include.CheckerPattern import CheckerPattern
from Include.MatrixNP import *
from Include.Sphere import *

class TestPatternSetup(unittest.TestCase):
    def setUp(self):
        self.black = Color(0, 0, 0)
        self.white = Color(1, 1, 1)

class Test_Pattern(TestPatternSetup):
    def test_StripePattern_creatingAStripePattern(self):
        self.pattern = StripePattern(self.white, self.black)

        self.assertEqual(self.pattern.a, self.white)
        self.assertEqual(self.pattern.b, self.black)

    def test_StripePattern_aStripePatternIsConstantInY(self):
        self.pattern = StripePattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 1, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 2, 0)), self.white)

    def test_StripePattern_aStripePatternIsConstantInZ(self):
        self.pattern = StripePattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 0, 1)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 0, 2)), self.white)

    def test_StripePattern_aStripePatternAlternatesInX(self):
        self.pattern = StripePattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0.9, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(1, 0, 0)), self.black)
        self.assertEqual(self.pattern.pattern_at(point(-0.1, 0, 0)), self.black)
        self.assertEqual(self.pattern.pattern_at(point(-1, 0, 0)), self.black)
        self.assertEqual(self.pattern.pattern_at(point(-1.1, 0, 0)), self.white)

    def test_StripePattern_stripesWithAnObjectTransformation(self):
        self.object = Sphere()
        self.object.transform = self.object.transform.scale(2, 2, 2)
        self.pattern = StripePattern(self.white, self.black)

        self.c = self.pattern.pattern_at_object(self.object, point(1.5, 0, 0))

        self.assertEqual(self.c, self.white)

    def test_StripePattern_stripesWithAPatternTransformation(self):
        self.object = Sphere()
        self.pattern = StripePattern(self.white, self.black)
        self.pattern.transform = self.pattern.transform.scale(2, 2, 2)

        self.c = self.pattern.pattern_at_object(self.object, point(1.5, 0, 0))

        self.assertEqual(self.c, self.white)

    def test_StripePattern_stripesWithBothAnObjectAndAPatternTransformation(self):
        self.object = Sphere()
        self.object.transform = self.object.transform.scale(2, 2, 2)
        self.pattern = StripePattern(self.white, self.black)
        self.pattern.transform = self.pattern.transform.translate(0.5, 0, 0)

        self.c = self.pattern.pattern_at_object(self.object, point(2.5, 0, 0))

        self.assertEqual(self.c, self.white)

    def test_TestPattern_theDefaultPatternTransformation(self):
        self.pattern = TestPattern()

        self.assertEqual(self.pattern.transform, Matrix4.identity_matrix())

    def test_TestPattern_assigningATransformation(self):
        self.pattern = TestPattern()

        self.pattern.transform = self.pattern.transform.translate(1, 2, 3)

        self.assertEqual(self.pattern.transform, Matrix4.identity_matrix().translate(1, 2, 3))

    def test_TestPattern_aPatternWithAnObjectTransformation(self):
        self.shape = Sphere()
        self.shape.transform = self.shape.transform.scale(2, 2, 2)
        self.pattern = TestPattern()

        self.c = self.pattern.pattern_at_object(self.shape, point(2, 3, 4))

        self.assertEqual(self.c, Color(1, 1.5, 2))

    def test_TestPattern_aPatternWithAPatternTranformation(self):
        self.shape = Sphere()
        self.pattern = TestPattern()
        self.pattern.transform = self.pattern.transform.scale(2, 2, 2)

        self.c = self.pattern.pattern_at_object(self.shape, point(2, 3, 4))

        self.assertEqual(self.c, Color(1, 1.5, 2))

    def test_TestPattern_aPatternWothBothAnObjectAndAPatternTransformation(self):
        self.shape = Sphere()
        self.shape.transform = self.shape.transform.scale(2, 2, 2)
        self.pattern = TestPattern()
        self.pattern.transform = self.pattern.transform.translate(0.5, 1, 1.5)

        self.c = self.pattern.pattern_at_object(self.shape, point(2.5, 3, 3.5))

        self.assertEqual(self.c, Color(0.75, 0.5, 0.25))

    def test_GradientPattern_aGradientLinearlyInterpolatesBetweenColors(self):
        self.pattern = GradientPattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0.25, 0, 0)), Color(0.75, 0.75, 0.75))
        self.assertEqual(self.pattern.pattern_at(point(0.5, 0, 0)), Color(0.5, 0.5, 0.5))
        self.assertEqual(self.pattern.pattern_at(point(0.75, 0, 0)), Color(0.25, 0.25, 0.25))

    def test_RingPattern_aRingShouldExtendInBothXAndZ(self):
        self.pattern = RingPattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(1, 0, 0)), self.black)
        self.assertEqual(self.pattern.pattern_at(point(0, 0, 1)), self.black)
        self.assertEqual(self.pattern.pattern_at(point(0.708, 0, 0.708)), self.black)

    def test_CheckerPattern_checkersShouldRepeatInX(self):
        self.pattern = CheckerPattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0.99, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(1.01, 0, 0)), self.black)

    def test_CheckerPattern_checkersShouldRepeatInY(self):
        self.pattern = CheckerPattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 0.99, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 1.01, 0)), self.black)

    def test_CheckerPattern_checkersShouldRepeatInZ(self):
        self.pattern = CheckerPattern(self.white, self.black)

        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 0, 0.99)), self.white)
        self.assertEqual(self.pattern.pattern_at(point(0, 0, 1.01)), self.black)

if __name__ == '__main__':
    unittest.main()
