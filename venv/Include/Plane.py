from Include.Tuple import *
from Include.Shape import Shape
from Include.Ray import Ray
from Include.Intersection import Intersection

import numpy as np

class Plane(Shape):
    def local_intersect(self, ray: Ray):
        if (abs(ray.direction.y) < EPSILON):
            return np.array([], dtype=object)
        return np.array([Intersection(-ray.origin.y/ray.direction.y, self)], dtype=object)

    def local_normal_at(self, local_point: Tuple):
        return vector(0, 1, 0)