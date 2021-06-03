from Include.Pattern import *
import math

# Not implemented yet
class BlendedPattern(Pattern):
    def __init__(self, a: Pattern, b: Pattern):
        self.a = a
        self.b = b

    def pattern_at(self, point: Tuple):
        pass