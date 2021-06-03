from Include.Canvas import *
from  Include.Matrix import *

canvas = Canvas(100, 100)
origin = point(0, 0, 0)

for x in range(12):
    position = IDENTITY_MATRIX.translate(0, 30, 0).rotate_z(x * math.pi / 6) * origin
    canvas.write_pixel(position.x - canvas.width/2, position.y - canvas.height/2, Color(1, 0, 0))

ppm = canvas.to_ppm()
f = open("clock.ppm", "w")
f.write(ppm)
f.close()
