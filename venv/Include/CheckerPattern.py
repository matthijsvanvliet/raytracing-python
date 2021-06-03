from Include.Tuple import Tuple
from Include.Pattern import Pattern
import math

class CheckerPattern(Pattern):
    def pattern_at(self, point: Tuple):
        return self.a if math.floor(point.x) + math.floor(point.y) + math.floor(point.z) % 2 == 0 else self.b