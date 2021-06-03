from Include.Tuple import Tuple
from Include.Pattern import Pattern
import math

class RingPattern(Pattern):
    def pattern_at(self, point: Tuple):
        return self.a if math.floor(math.sqrt(point.x * point.x + point.z * point.z)) % 2 == 0 else self.b