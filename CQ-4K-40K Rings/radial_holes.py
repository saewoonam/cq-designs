import cadquery as cq
from screws import tap, thru
import math

def radial_holes_type(diameter, depth, size, n, offset, hole_type):
    holes = []
    if (hole_type=='thru'):
        [screw_diameter, length] = thru(size, 1)
    if (hole_type=='tap'):
        [screw_diameter, length] = tap(size, 1)
    for index in range(n):
        theta = 360.0 * index / n + offset
        x = diameter/2.0 * math.cos(theta/180.0*math.pi)
        y = diameter/2.0 * math.sin(theta/180.0*math.pi)
        p = cq.Vector(x, y, 0)
        d = cq.Vector(-x, -y, 0)
        # print(theta, p,d)
        hole = cq.Solid.makeCylinder(screw_diameter/2, depth, pnt=p, dir=d)
        holes.append(hole)
    return holes

def radial_holes_thru(diameter, depth, size, n, offset):
    return radial_holes_type(diameter, depth, size, n, offset, 'thru')

def radial_holes_tap(diameter, depth, size, n, offset):
    return radial_holes_type(diameter, depth, size, n, offset, 'tap')

if  (__name__=='temp'):
    holes = radial_holes_tap(10, 3, '2-56', 6, 0)

    s = cq.Workplane().add(holes)
    # s = s.add()
    # s = cq.Workplane(s)
    s = s.translate((0,0,10))
    # print('faces', s.faces('|Z'))
    print(s.objects)
    p = cq.Workplane("XY").circle(5).circle(4.9).extrude(0)
    # for item in radial_holes_tap(10, 3, '2-56', 6, 0):
    #     p = p.cut(item)
    # p = p.faces(">Z").workplane().circle(3).extrude(2)
    p = p.cut(s)
    show_object(p)

