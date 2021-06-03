from Include.Canvas import *
from Include.Shape import *

canvas_pixels = 1000
canvas = Canvas(canvas_pixels, canvas_pixels)
wall_z = 10
half = wall_z / 2
color = Color(1, 0, 0)
pixel_size = wall_z / canvas_pixels

s = Sphere()
ray_origin = point(0, 0, -5)

for x in range(canvas_pixels - 1):
    world_x = -half + pixel_size * x
    for y in range(canvas_pixels - 1):
        world_y = half - pixel_size * y
        position = point(world_x, world_y, wall_z)
        r = Ray(ray_origin, (position - ray_origin).normalize())
        xs = s.intersect(r)

        if (Intersection.hit(xs) != None):
            canvas.write_pixel(x, y, color)
        else:
            canvas.write_pixel(x, y, Color(0, 0, 0))

ppm = canvas.to_ppm()
f = open("circle.ppm", "w")
f.write(ppm)
f.close()
