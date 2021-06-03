from Include.MatrixNP import *

@dataclass
class Ray:
    origin: Tuple
    direction: Tuple

    def position(self, t):
        return self.origin + self.direction * t

    def transform(self, matrix: Matrix4):
        return Ray(matrix * self.origin, matrix * self.direction)