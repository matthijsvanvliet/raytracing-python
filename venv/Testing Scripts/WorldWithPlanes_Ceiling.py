from Include.Camera import *
from Include.Sphere import Sphere
from Include.Plane import Plane
from Include.World import *
import time

floor = Plane()
floor.material.color = Color(1, 0.9, 0.9)
floor.material.specular = 0

ceiling = Plane()
ceiling.transform = ceiling.transform.translate(0, 3, 0)
ceiling.material.color = Color(0, 0.8, 0)
ceiling.material.specular = 0

wall = Plane()
wall.transform = wall.transform.rotate_x(math.pi/2).translate(0, 0, 5)

middle = Sphere()
middle.transform = middle.transform.translate(-0.5, 1, 0.5)
middle.material.color = Color(0.1, 1, 0.5)
middle.material.diffuse = 0.7
middle.material.specular = 0.3

right = Sphere()
right.transform = right.transform.scale(0.5, 0.5, 0.5).translate(1.5, 0.5, -0.5)
right.material.color = Color(0.5, 1, 0.1)
right.material.diffuse = 0.7
right.material.specular = 0.3

left = Sphere()
left.transform = left.transform.scale(0.33, 0.33, 0.33).translate(-1.5, 0.33, -0.75)
left.material.color = Color(1, 0.8, 0.1)
left.material.diffuse = 0.7
left.material.specular = 0.3

world = World([floor, wall, ceiling, right, middle, left], PointLight(point(-10, 2.5, -10), Color(1, 1, 1)))
camera = Camera(1000, 500, math.pi/3)
camera.transform = Camera.view_transform(point(0, 1.5, -10), point(0, 1, 0), vector(0, 1, 0))

canvas = camera.render(world)

ppm = canvas.to_ppm()
f = open("ceiling.ppm", "w")
f.write(ppm)
f.close()