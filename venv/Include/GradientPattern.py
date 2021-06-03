from Include.Tuple import Tuple
from Include.Pattern import Pattern
import math

class GradientPattern(Pattern):
    def pattern_at(self, point: Tuple):
        distance =  self.b - self.a
        fraction = point.x - math.floor(point.x)
        return self.a + distance * fraction