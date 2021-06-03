from Include.Tuple import *
import numpy as np

class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixel = [[Color(0,0,0) for x in range(width)] for y in range(height)]

    def get_pixel(self, x, y):
        return self.pixel[y][x]

    def write_pixel(self, x, y, color: Color):
        self.pixel[round(y)][round(x)] = color

    def to_ppm(self):
        maxColVal = 255
        string = f'P3\n{self.width} {self.height}\n{maxColVal}\n'
        index = len(string) + 1
        nextLine = False

        for x in range(self.height):
            for y in range(self.width):
                list = np.array([clamp(self.pixel[x][y].red, 0, maxColVal), clamp(self.pixel[x][y].green, 0, maxColVal), clamp(self.pixel[x][y].blue, 0, maxColVal)])

                for color in list:
                    if ((len(string) + len(f'{color} ')) - index <= 70):
                        string += f'{color} '
                    else:
                        string += f'\n'
                        index = len(string)
                        string += f'{color} '

                if (y == self.width - 1):
                    string += '\n'
                    index = len(string)

        return string

def clamp(n, smallest, largest):
    value = round(n * largest)

    if (value > largest):
        return largest
    elif (value < smallest):
        return smallest
    else:
        return value
