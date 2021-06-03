from Include.Pattern import *
import math

class SolidPattern(Pattern):
    def __init__(self, color: Color):
        self.a = color

    def pattern_at(self, point: Tuple):
        return self.a