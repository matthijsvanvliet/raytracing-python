from Include.Tuple import *
from Include.Shape import Shape
from Include.Ray import Ray
from Include.Intersection import Intersection

import numpy as np

class Sphere(Shape):
    def local_intersect(self, ray: Ray):
        sphere_to_ray = ray.origin - point(0, 0, 0)

        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1

        discriminant = b * b - 4 * a * c

        if (discriminant < 0):
            return np.array([], dtype=object)
        else:
            return np.array([Intersection((-b - math.sqrt(discriminant)) / (2 * a), self), Intersection((-b + math.sqrt(discriminant)) / (2 * a), self)], dtype=object)

    def local_normal_at(self, local_point: Tuple):
        return local_point - point(0, 0, 0)

    @staticmethod
    def Glass():
        S = Sphere()
        S.material.transparency = 1.0
        S.material.refractive_index = 1.5
        return S
