import sys, os
sys.path.append(os.path.abspath('../src'))

import bext, math, time, random

BLOCK = chr(9608)

width, height = bext.size()
DEFAULT_SCALEX = (width - 4) // 8
DEFAULT_SCALEY = (height - 4) // 4 # Text cells are twice as tall as they are wide, so set scaley accordingly.
DEFAULT_TRANSLATEX = (width - 4) // 2
DEFAULT_TRANSLATEY = (height - 4) // 2

def line(x1, y1, x2, y2):
    """
    Returns a generator that produces all of the points in a line between `x1`, `y1` and `x2`, `y2`.

    (Uses the Bresenham line algorithm.)

    >>> list(line(0, 0, 10, 3))
    [(0, 0), (1, 0), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2), (7, 2), (8, 2), (9, 3), (10, 3)]
    """
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # TODO - Do we want this line?

    isSteep = abs(y2-y1) > abs(x2-x1)
    if isSteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    isReversed = x1 > x2

    if isReversed:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y2
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x2, x1 - 1, -1):
            if isSteep:
                yield (y, x)
            else:
                yield (x, y)
            error -= deltay
            if error <= 0:
                y -= ystep
                error += deltax
    else:
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if isSteep:
                yield (y, x)
            else:
                yield (x, y)
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax


def rotateXYZ(x, y, z, ax, ay, az):
    # NOTE: Rotates around the origin (0, 0, 0)

    # Rotate along x
    rotatedX = x
    rotatedY = (y * math.cos(ax)) - (z * math.sin(ax))
    rotatedZ = (y * math.sin(ax)) + (z * math.cos(ax))
    x, y, z = rotatedX, rotatedY, rotatedZ

    # Rotate along y
    rotatedX = (z * math.sin(ay)) + (x * math.cos(ay))
    rotatedY = y
    rotatedZ = (z * math.cos(ay)) - (x * math.sin(ay))
    x, y, z = rotatedX, rotatedY, rotatedZ

    # Rotate along z
    rotatedX = (x * math.cos(az)) - (y * math.sin(az))
    rotatedY = (x * math.sin(az)) + (y * math.cos(az))
    rotatedZ = z

    return (rotatedX, rotatedY, rotatedZ)


def screenCoord(point1, point2, scalex=None, scaley=None, translatex=None, translatey=None):
    if scalex is None:
        scalex = DEFAULT_SCALEX
    if scaley is None:
        scaley = DEFAULT_SCALEY
    if translatex is None:
        translatex = DEFAULT_TRANSLATEX
    if translatey is None:
        translatey = DEFAULT_TRANSLATEY


    return (int(point1[0] * scalex + translatex),
            int(point1[1] * scaley + translatey),
            int(point2[0] * scalex + translatex),
            int(point2[1] * scaley + translatey))


width, height = bext.size()

bext.fg('random')

'''
Cube points:
   0+-----+1
   /     /|
  /     / |  -y
2+-----+3 |   |
 | 4+  |  +5  +-- +x
 |     | /   /
 |     |/   +z
6+-----+7
'''

points = [[-1, -1, -1],
          [ 1, -1, -1],
          [-1, -1,  1],
          [ 1, -1,  1],
          [-1,  1, -1],
          [ 1,  1, -1],
          [-1,  1,  1],
          [ 1,  1,  1]]
rotatedPoints = [None] * 10
rx = ry = rz = 0
step = 0

bext.clear()
try:
    while True:
        # Change color
        if step % 15 == 0:
            bext.fg('random')
        step += 1

        # Rotate cube
        rx += 0.05 + random.randint(1, 30) / 100
        ry += 0.1  + random.randint(1, 30) / 100
        rz += 0.15 + random.randint(1, 30) / 100
        for i in range(len(points)):
            rotatedPoints[i] = rotateXYZ(*points[i], rx, ry, rz)

        # Get cube line points
        screenPoints = []
        screenPoints.extend(line(*screenCoord(rotatedPoints[0], rotatedPoints[1])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[1], rotatedPoints[3])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[3], rotatedPoints[2])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[2], rotatedPoints[0])))

        screenPoints.extend(line(*screenCoord(rotatedPoints[0], rotatedPoints[4])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[1], rotatedPoints[5])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[2], rotatedPoints[6])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[3], rotatedPoints[7])))

        screenPoints.extend(line(*screenCoord(rotatedPoints[4], rotatedPoints[5])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[5], rotatedPoints[7])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[7], rotatedPoints[6])))
        screenPoints.extend(line(*screenCoord(rotatedPoints[6], rotatedPoints[4])))

        screenPoints = tuple(frozenset(screenPoints)) # Get rid of duplicate points.

        # Draw cube
        for x, y in screenPoints:
            # Writing to the terminal will by far be the slowest part of this program.
            bext.goto(x, y)
            print(BLOCK, end='')

        time.sleep(0.1)

        # Erase cube
        for x, y in screenPoints:
            bext.goto(x, y)
            print(' ', end='')

except KeyboardInterrupt:
    pass
