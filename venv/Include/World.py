from Include.Light import *
from Include.Sphere import *
from Include.Intersection import *
from Include.MatrixNP import *

import numpy as np

class World:
    def __init__(self, world_objects = None, light_source: PointLight=None):
        self.objects = []
        if (type(world_objects) is list):
            for object in world_objects:
                if (isinstance(object, Shape)):
                    self.objects.append(object)
        elif (type(world_objects) is Shape):
            self.objects.append(world_objects)
        self.light_source = light_source

    @classmethod
    def default(cls):
        s1 = Sphere()
        s1.material.color = Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2
        s2 = Sphere()
        s2.transform = Matrix4.identity_matrix().scale(0.5, 0.5, 0.5)
        return cls([s1, s2], PointLight(point(-10, 10, -10), Color(1, 1, 1)))

    def intersect(self, ray: Ray):
        list = []
        for object in self.objects:
            for intersection in object.intersect(ray):
                list.append(intersection)
        return sorted(list, key=lambda x: x.t)

    def shade_hit(self, comps: Precomputations, remaining: int = 5):
        shadowed = self.is_shadowed(comps.over_point)

        surface = comps.object.material.lighting(comps.object, self.light_source, comps.over_point, comps.eyev, comps.normalv, shadowed)

        reflected = self.reflected_color(comps)
        refracted = self.refracted_color(comps)

        material = comps.object.material
        if (material.reflective > 0 and material.transparency > 0):
            reflectance = comps.schlick()
            return surface + reflected * reflectance + refracted * (1 - reflectance)
        else:
            return surface + reflected + refracted

    def color_at(self, ray: Ray, remaining: int = 5):
        intersections = self.intersect(ray)
        hit = Intersection.hit(intersections)

        if (hit == None):
            return Color(0, 0, 0)

        precomps = hit.prepare_computations(ray, intersections)
        return self.shade_hit(precomps, remaining)

    def is_shadowed(self, point: Tuple):
        v = self.light_source.position - point
        r = Ray(point, v.normalize())
        intersections = self.intersect(r)

        h = Intersection.hit(intersections)
        return True if (h != None and h.t < v.magnitude()) else False

    def reflected_color(self, comps: Precomputations, remaining: int = 5):
        if (comps.object.material.reflective == 0 or remaining < 1):
            return Color(0, 0, 0)

        reflect_ray = Ray(comps.over_point, comps.reflectv)
        color = self.color_at(reflect_ray, remaining - 1)

        return color * comps.object.material.reflective

    def refracted_color(self, comps, remaining: int = 3):
         if (remaining < 1 or comps.object.material.transparency == 0):
             return Color(0, 0, 0)

         n_ratio = comps.n1 / comps.n2
         cos_i = comps.eyev.dot(comps.normalv)
         sin2_t = pow(n_ratio, 2) * (1 - pow(cos_i, 2))

         if (sin2_t > 1):
             return Color(0, 0, 0)

         cos_t = math.sqrt(1.0 - sin2_t)
         direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio
         refract_ray = Ray(comps.under_point, direction)

         return self.color_at(refract_ray, remaining - 1) * comps.object.material.transparency
