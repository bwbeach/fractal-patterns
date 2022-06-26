#!/usr/bin/env python3

import itertools
import math

PRE = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="203.200mm" height="203.200mm" viewBox="0.000,0.000,100.000,100.000">"""

POST = "</svg>"


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def left(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Point(c * self.x + s * self.y, -s * self.x + c * self.y)


def fractal(p1, p2, f, depth):
    if depth == 0:
        return [p1, p2]
    else:
        points = f(p1, p2)
        sequences = [
            fractal(a, b, f, depth - 1)
            for a, b in itertools.pairwise(points)
        ]
        result = [p1]
        for s in sequences:
            result = result + s[1:]
        return result


def no_op(p1, p2):
    return [p1, p2]


def half(p1, p2):
    mid = (p1 + p2) * 0.5
    return [p1, mid, p2]


def zigzag(p1, p2):
    v = p2 - p1
    left = (v * (math.sqrt(2) / 3)).left(math.pi / 4)
    return [p1, p1 + left, p2 - left, p2]


def left_square(p1, p2):
    v = p2 - p1
    q = v * 0.25
    left = q.left(math.pi / 2)
    return [p1, p1 + q, p1 + q + left, p1 + q*3 + left * -1, p1 + q*3, p2]


def left_triangle(p1, p2):
    """
    Each line segment owns a right equilateral triange on its left side.
    """
    fwd = (p2 - p1) * 0.5
    left = fwd.left(math.pi / 2)
    mid = p1 + fwd
    up = mid + left
    return [p1, mid, up, mid, p2]


def make_pattern():
    points = fractal(Point(25, 50), Point(75, 50), left_triangle, 1)
    point_strings = [
        "%6.3f,%6.3f" % (p.x, p.y)
        for p in points
    ]
    path = "M " + " L ".join(point_strings)
    path_element = '<path stroke="#000000" fill="none" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10.000" d="%s"/>' % path
    svg = PRE + path_element + POST
    file_name = "/Users/brianb/test.svg"
    with open(file_name, "w") as f:
        f.write(svg)
    print("wrote", file_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    make_pattern()