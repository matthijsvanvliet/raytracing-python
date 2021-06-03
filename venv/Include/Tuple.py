from dataclasses import dataclass
from enum import Enum
import math
import sys

EPSILON = 0.00001

def isEqual(a, b):
    return True if abs(a - b) < EPSILON else False

# Tuple types enum
class TupleTypes(Enum):
    VECTOR = 0
    POINT = 1

# Tuple struct
# Implement tuple as numpy array of 4 elements with properties for x, y, z and w
class Tuple:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def magnitude(self):
        return math.sqrt(pow(self.x, 2) +
                         pow(self.y, 2) +
                         pow(self.z, 2) +
                         pow(self.w, 2))

    def normalize(self):
        magnitude = self.magnitude()
        return Tuple(self.x / magnitude,
                     self.y / magnitude,
                     self.z / magnitude,
                     self.w / magnitude)

    def dot(self, other):
        return (self.x * other.x +
                self.y * other.y +
                self.z * other.z +
                self.w * other.w)

    def cross(self, other):
        return vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def reflect(self, normal):
        return self - normal * 2 * self.dot(normal)

    def get_type(self):
        if (self.w == 0):
            return TupleTypes.VECTOR
        elif (self.w == 1):
            return TupleTypes.POINT

    def __eq__(self, other):
        return True if isEqual(self.x, other.x) and isEqual(self.y, other.y) and isEqual(self.z, other.z) and isEqual(self.w, other.w) else False

    def __add__(self, other):
        return Tuple((self.x + other.x), (self.y + other.y), (self.z + other.z), (self.w + other.w))

    def __sub__(self, other):
        return Tuple((self.x - other.x), (self.y - other.y), (self.z - other.z), (self.w - other.w))

    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, other):
        return Tuple((self.x * other), (self.y * other), (self.z * other), (self.w * other))

    def __truediv__(self, other):
        return Tuple((self.x / other), (self.y / other), (self.z / other), (self.w / other))

    def __abs__(self):
        return Tuple(abs(self.x), abs(self.y), abs(self.z), abs(self.w))

    def __str__(self):
        return f'{self.x, self.y, self.z, self.w}'

class Color:
    def __init__(self, red: float, green: float, blue: float):
        self.red = red
        self.green = green
        self.blue = blue

    def hadamard_product(self, other):
        return Color((self.red * other.red), (self.green * other.green), (self.blue * other.blue))

    def __eq__(self, other):
        return True if isEqual(self.red, other.red) and isEqual(self.green, other.green) and isEqual(self.blue, other.blue) else False

    def __add__(self, other):
        return Color((self.red + other.red), (self.green + other.green), (self.blue + other.blue))

    def __sub__(self, other):
        return Color((self.red - other.red), (self.green - other.green), (self.blue - other.blue))

    def __neg__(self):
        return Color(-self.red, -self.green, -self.blue)

    def __mul__(self, other):
        return self.hadamard_product(other) if type(other) is Color else Color((self.red * other), (self.green * other), (self.blue * other))

    def __truediv__(self, other: float):
        return Color((self.red / other), (self.green / other), (self.blue / other))

    def __abs__(self):
        return Color(abs(self.red), abs(self.green), abs(self.blue))

    def __str__(self):
        return f'{self.red, self.green, self.blue}'

# Functions to instantiate Tuples as different types
def point(x, y, z):
    return Tuple(x, y, z, TupleTypes.POINT.value)

def vector(x, y, z):
    return Tuple(x, y, z, TupleTypes.VECTOR.value)


