from Include.MatrixNP import *
from Include.Shape import Shape

class Pattern:
    def __init__(self, color_a: Color, color_b: Color):
        self.a = color_a
        self.b = color_b
        self.transform = Matrix4.identity_matrix()

    def pattern_at(self, point: Tuple):
        raise NotImplementedError("Please implement this method")

    def pattern_at_object(self, object: Shape, world_point: Tuple):
        object_point = object.transform.invert() * world_point
        pattern_point = self.transform.invert() * object_point

        return self.pattern_at(pattern_point)

class TestPattern(Pattern):
    def __init__(self):
        self.transform = Matrix4.identity_matrix()

    def pattern_at(self, point: Tuple):
        return Color(point.x, point.y, point.z)