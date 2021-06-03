from Include.Shape import Shape
from Include.Ray import Ray
from Include.Tuple import *

import numpy as np

class Precomputations:
    t: float
    object: Shape
    point: Tuple
    eyev: Tuple
    normalv: Tuple
    reflectv: Tuple
    inside: bool
    over_point: Tuple
    under_point: Tuple
    n1: float
    n2: float

    def schlick(self):
        cos = self.eyev.dot(self.normalv)

        if (self.n1 > self.n2):
            n = self.n1 / self.n2
            sin2_t = n ** 2 * (1.0 - cos ** 2)
            if (sin2_t > 1.0):
                return 1.0

            cos_t = math.sqrt(1.0 - sin2_t)
            cos = cos_t

        r0 = ((self.n1 - self.n2) / (self.n1 + self.n2)) ** 2
        return r0 + (1 - r0) * (1 - cos) ** 5

    def __eq__(self, other):
        return self.t == other.t and self.object == other.object and self.point == other.point and self.eyev == other.eyev \
               and self.normalv == other.eyev and self.reflectv == other.reflectv and self.inside == other.inside and self.over_point == other.over_point

class Intersection:
    def __init__(self, t: float, object: Shape):
        self.t = t
        self.object = object

    @staticmethod
    def intersections(*args):
        list = []
        for arg in args:
            list.append(arg)
        return list

    @staticmethod
    def hit(intersections: np.ndarray):
        hit_intersection = Intersection(float('inf'), Shape())

        for intersection in intersections:
            if (intersection.t > 0 and intersection.t < hit_intersection.t):
                hit_intersection = intersection
        return hit_intersection if type(hit_intersection.object) != Shape else None

    def prepare_computations(self, ray: Ray, intersections: list = []):
        comps = Precomputations()

        comps.t = self.t
        comps.object = self.object

        comps.point = ray.position(comps.t)
        comps.eyev = -ray.direction
        comps.normalv = comps.object.normal_at(comps.point)

        if (comps.normalv.dot(comps.eyev) < 0):
            comps.inside = True
            comps.normalv = -comps.normalv
        else:
            comps.inside = False

        comps.over_point = comps.point + comps.normalv * EPSILON
        comps.under_point = comps.point - comps.normalv * EPSILON

        comps.reflectv = ray.direction.reflect(comps.normalv)

        containers = []

        for intersection in intersections:
            if (intersection == self):
                comps.n1 = 1.0 if len(containers) == 0 else containers[-1].material.refractive_index

            containers.remove(intersection.object) if (intersection.object in containers) else containers.append(intersection.object)

            if (intersection == self):
                comps.n2 = 1.0 if (len(containers) == 0) else containers[-1].material.refractive_index

        return comps
