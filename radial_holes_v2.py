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

holes = radial_holes_tap(10, 3, '2-56', 6, 0)

s = cq.Workplane().add(holes)
# s = s.add()
# s = cq.Workplane(s)
s = s.translate((0,0,10))
# print('faces', s.faces('|Z'))
print(s.objects)
p = cq.Workplane("XY").circle(5).circle(4.9).extrude(10)
# for item in radial_holes_tap(10, 3, '2-56', 6, 0):
#     p = p.cut(item)
# p = p.faces(">Z").workplane().circle(3).extrude(2)
p = p.cut(s)
show_object(p)


def hole(
    self, diameter: float, depth: float = None, clean: bool = True
) -> "Workplane":
    """
    Makes a hole for each item on the stack.

    :param diameter: the diameter of the hole
    :type diameter: float > 0
    :param depth: the depth of the hole
    :type depth: float > 0 or None to drill thru the entire part.
    :param boolean clean: call :py:meth:`clean` afterwards to have a clean shape

    The surface of the hole is at the current workplane.

    One hole is created for each item on the stack.  A very common use case is to use a
    construction rectangle to define the centers of a set of holes, like so::

            s = Workplane(Plane.XY()).box(2,4,0.5).faces(">Z").workplane()\
                .rect(1.5,3.5,forConstruction=True)\
                .vertices().hole(0.125, 0.25,82,depth=None)

    This sample creates a plate with a set of holes at the corners.

    **Plugin Note**: this is one example of the power of plugins. CounterSunk holes are quite
    time consuming to create, but are quite easily defined by users.

    see :py:meth:`cboreHole` and :py:meth:`cskHole` to make counterbores or countersinks
    """
    if depth is None:
        depth = self.largestDimension()

    def build_shape(loc):
        print('loc',loc.wrapped.DumpJson())

        boreDir = cq.Vector(0, 0, -1)
        # first make the hole
        h = cq.Solid.makeCylinder(
            diameter / 2.0, depth, cq.Vector(), boreDir
        )  # local coordinates!
        return h
    
    boreDir = cq.Vector(0, 0, -1)
    # first make the hole
    h = cq.Solid.makeCylinder(
        diameter / 2.0, depth, cq.Vector(), boreDir
    )  # local coordinates!
    return self.each(lambda loc: print(loc.Center()))    
    # return self.cutEach(lambda loc: build_shape(loc).moved(loc), True, clean)    
    # return self.cutEach(build_shape, True, clean)

cq.Workplane.myext = hole

result = cq.Workplane("XY").box(10,10,3).faces(">Z").workplane().rect(5,5, forConstruction=True).vertices().myext(1)

show_object(result)
# show_object(s)