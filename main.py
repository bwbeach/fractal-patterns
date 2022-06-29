#!/usr/bin/env python3

"""
Experiments in generating fractal shapes to an SVG file for use on a
quilting machine or Cricut.
"""

import abc
import itertools
import math

PRE = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="203.200mm" height="203.200mm" viewBox="0.000,0.000,100.000,100.000">"""

POST = "</svg>"


class Point:
    """
    A two-dimensional point.  Also used as a vector, for now.
    """
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

    def right(self, angle):
        return self.left(-angle)


class LineSegment:
    """
    A line segment from one point to another.
    """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class SidedSegment:
    """
    A line segment that owns the area to one side.
    """
    def __init__(self, p1, p2, side):
        assert side in ["left", "right"]
        self.p1 = p1
        self.p2 = p2
        self.side = side

    def up_half_across_and_down(self):
        """
        One step in a fractal.
        TODO: figure out how to describe this.
        """
        if self.side == "left":
            v_half = (self.p2 - self.p1) * 0.5
            v_up = v_half.left(math.pi / 2)
            p_a = self.p1 + v_up
            p_b = p_a + v_half
            p_c = self.p2 + v_up
            return [
                SidedSegment(self.p1, p_a, "right"),
                SidedSegment(p_a, p_b, "left"),
                SidedSegment(p_b, p_c, "left"),
                SidedSegment(p_c, self.p2, "right")
            ]
        else:
            v_half = (self.p2 - self.p1) * 0.5
            v_down = v_half.right(math.pi / 2)
            p_a = self.p1 + v_down
            p_b = p_a + v_half
            p_c = self.p2 + v_down
            return [
                SidedSegment(self.p1, p_a, "left"),
                SidedSegment(p_a, p_b, "right"),
                SidedSegment(p_b, p_c, "right"),
                SidedSegment(p_c, self.p2, "left")
            ]


def fractal(elem, f, depth):
    """
    Given a single element, returns the list of elements that replace it.
    :param elem:
    :param f:
    :param depth:
    :return:
    """
    if depth == 0:
        return [elem]
    else:
        sub_elems = f(elem)
        return list(itertools.chain(*(fractal(e, f, depth - 1) for e in sub_elems)))


def left_triangle(elem):
    """
    Each line segment owns a right equilateral triangle on its left side.
    """
    p1 = elem.p1
    p2 = elem.p2
    fwd = (p2 - p1) * 0.5
    left = fwd.left(math.pi / 2)
    mid = p1 + fwd
    up = mid + left
    return [
        LineSegment(p1, mid),
        LineSegment(mid, up),
        LineSegment(up, mid),
        LineSegment(mid, p2)
    ]


def make_pattern():
    # elems = fractal(LineSegment(Point(25, 50), Point(75, 50)), left_triangle, 1)
    init = SidedSegment(Point(25, 75), Point(75, 75), "left")
    elems = fractal(init, SidedSegment.up_half_across_and_down, 6)
    points = [elems[0].p1] + [e.p2 for e in elems]  # TODO: make render step
    point_strings = [
        "%6.3f,%6.3f" % (p.x, p.y)
        for p in points
    ]
    path = "M " + " L ".join(point_strings)
    path_element = '<path stroke="#000000" fill="none" stroke-width="0.25" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10.000" d="%s"/>' % path
    svg = PRE + path_element + POST
    file_name = "/Users/brianb/test.svg"
    with open(file_name, "w") as f:
        f.write(svg)
    print("wrote", file_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    make_pattern()