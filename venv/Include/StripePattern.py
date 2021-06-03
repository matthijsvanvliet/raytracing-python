from Include.Tuple import Tuple
from Include.Pattern import Pattern
import math

class StripePattern(Pattern):
    def pattern_at(self, point: Tuple):
        return self.a if math.floor(point.x) % 2 == 0 else self.b