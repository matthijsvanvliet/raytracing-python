from Include.Canvas import *
from  Include.Matrix import *

@dataclass
class Projectile:
    position: Tuple
    velocity: Tuple

@dataclass
class Environment:
    gravity: Tuple
    wind: Tuple

def tick(env: Environment, proj: Projectile):
    position = proj.position + proj.velocity
    velocity = proj.velocity + env.gravity + env.wind
    return Projectile(position, velocity)

p = Projectile(point(0, 100, 0), vector(1, 1.8, 0).normalize() * 5)
e = Environment(vector(0, -0.1, 0), vector(-0.01, 0, 0))

canvas = Canvas(900, 550)

while (tick(e, p).position.y > 0 and tick(e, p).position.x < canvas.width):
    p = tick(e, p)
    canvas.write_pixel(p.position.x, canvas.height - p.position.y - 3, Color(1, 0, 0))
ppm = canvas.to_ppm()
f = open("canvas.ppm", "w")
f.write(ppm)
f.close()