from Include.Ray import *
from Include.Material import Material

class Shape:
    def __init__(self):
        self.transform = Matrix4.identity_matrix()
        self.material = Material()

    def intersect(self, ray: Ray):
        local_ray = ray.transform(self.transform.invert())
        return self.local_intersect(local_ray)

    def local_intersect(self, ray: Ray):
        raise NotImplementedError("Please implement this method")

    def normal_at(self, world_point: Tuple):
        local_point = self.transform.invert() * world_point
        local_normal = self.local_normal_at(local_point)
        world_normal = self.transform.invert().transpose() * local_normal
        world_normal.w = 0
        return world_normal.normalize()

    def local_normal_at(self, local_point: Tuple):
        raise NotImplementedError("Please implement this method")

    def __eq__(self, other):
        return self.transform == other.transform and self.material == other.material

class TestShape(Shape):
    saved_ray: Ray

    def local_intersect(self, ray: Ray):
        self.saved_ray = ray

    def local_normal_at(self, local_point: Tuple):
        local_point.w = 0
        return local_point
