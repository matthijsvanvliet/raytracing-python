from Include.Ray import *
from Include.World import *
from Include.Canvas import *

class Camera:
    def __init__(self, hsize: int, vsize: int, field_of_view: float):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transform = Matrix4.identity_matrix()

        self.half_view = math.tan(self.field_of_view/2)
        self.aspect = self.hsize/self.vsize

        if (self.aspect >= 1):
            self.half_width = self.half_view
            self.half_height = self.half_view / self.aspect
        else:
            self.half_width = self.half_view * self.aspect
            self.half_height = self.half_view

        self.pixel_size = round((self.half_width * 2) / self.hsize, 17)

    def ray_for_pixel(self, px, py):
        xoffset = (px + 0.5) * self.pixel_size
        yoffset = (py + 0.5) * self.pixel_size

        world_x = self.half_width - xoffset
        world_y = self.half_height - yoffset

        pixel = self.transform.invert() * point(world_x, world_y, -1)
        origin = self.transform.invert() * point(0, 0, 0)
        direction = (pixel - origin).normalize()

        return Ray(origin, direction)

    def render(self, world: World):
        image = Canvas(self.hsize, self.vsize)

        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                image.write_pixel(x, y, color)
        return image

    @staticmethod
    def view_transform(_from: Tuple, to: Tuple, up: Tuple):
        forward = (to - _from).normalize()
        left = forward.cross(up.normalize())
        true_up = left.cross(forward)
        orientation = Matrix4.identity_matrix()
        orientation.m[0][0] = left.x
        orientation.m[0][1] = left.y
        orientation.m[0][2] = left.z
        orientation.m[1][0] = true_up.x
        orientation.m[1][1] = true_up.y
        orientation.m[1][2] = true_up.z
        orientation.m[2][0] = -forward.x
        orientation.m[2][1] = -forward.y
        orientation.m[2][2] = -forward.z
        return orientation * Matrix4.identity_matrix().translate(-_from.x, -_from.y, -_from.z)