from Include.Camera import *
from Include.Shape import *
from Include.World import *
import time

floor = Sphere()
floor.transform = floor.transform.scale(10, 0.01, 10)
floor.material.color = Color(1, 0.9, 0.9)
floor.material.specular = 0

left_wall = Sphere()
left_wall.transform = left_wall.transform.scale(10, 0.01, 10).rotate_x(math.pi/2).rotate_y(-math.pi/4).translate(0, 0, 5)

right_wall = Sphere()
right_wall.transform = right_wall.transform.scale(10, 0.01, 10).rotate_x(math.pi/2).rotate_y(math.pi/4).translate(0, 0, 5)

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

world = World([floor, left_wall, right_wall, right, middle, left], PointLight(point(-10, 10, -10), Color(1, 1, 1)))
camera = Camera(1000, 500, math.pi/3)
camera.transform = Camera.view_transform(point(0, 1.5, -5), point(0, 1, 0), vector(0, 1, 0))

canvas = camera.render(world)

ppm = canvas.to_ppm()
f = open("shadow.ppm", "w")
f.write(ppm)
f.close()