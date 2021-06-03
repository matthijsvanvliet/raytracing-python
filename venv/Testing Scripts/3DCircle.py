from Include.Canvas import *
from Include.Shape import *
from Include.Sphere import Sphere
from Include.Light import PointLight
from Include.Intersection import Intersection
import time

canvas_pixels = 500
canvas = Canvas(canvas_pixels, canvas_pixels)
wall_z = 10
half = wall_z / 2
color = Color(1, 0, 0)
pixel_size = wall_z / canvas_pixels

s = Sphere()
s.transform = Matrix4.identity_matrix()
s.material.color = Color(1, 0.2, 1)
ray_origin = point(0, 0, -5)

light_position = point(-10, 10, -10)
light_color = Color(1, 1, 1)
light = PointLight(light_position, light_color)

for x in range(canvas_pixels - 1):
    world_x = -half + pixel_size * x
    for y in range(canvas_pixels - 1):
        world_y = half - pixel_size * y
        position = point(world_x, world_y, wall_z)
        r = Ray(ray_origin, (position - ray_origin).normalize())
        xs = s.intersect(r)

        hit = Intersection.hit(xs)

        if (hit != None):
            canvas_point = r.position(hit.t)
            normal = hit.object.normal_at(canvas_point)
            eye = -r.direction

            color = hit.object.material.lighting(light, canvas_point, eye, normal)

            canvas.write_pixel(x, y, color)
        else:
            canvas.write_pixel(x, y, Color(0, 0, 0))

ppm = canvas.to_ppm()
f = open("circle2.ppm", "w")
f.write(ppm)
f.close()
