import cadquery as cq
import math
from screws import tap

inch = 25.4;

def polygon(
    self, nSides: int, diameter: float, offset: float = 0, forConstruction: bool = False
) -> "Workplane":
    """
    Creates a polygon inscribed in a circle of the specified diameter for each point on
    the stack

    The first vertex is always oriented in the x direction.

    :param nSides: number of sides, must be > 3
    :param diameter: the size of the circle the polygon is inscribed into
    :return: a polygon wire
    """

    # pnt is a vector in local coordinates
    angle = 2.0 * math.pi / nSides
    pnts = []
    offset = offset * math.pi / 180.0;
    # print(offset)
    for i in range(nSides + 1):
        pnts.append(
            cq.Vector(
                (diameter / 2.0 * math.cos(angle * i + offset)),
                (diameter / 2.0 * math.sin(angle * i + offset)),
                0,
            )
        )
    p = cq.Wire.makePolygon(pnts, forConstruction)

    return self.eachpoint(lambda loc: p.moved(loc), True)
cq.Workplane.polygon_offset = polygon;

def collar():
    T = 3.75*inch
    wall = 0.5*inch;
    diameter = 395+30
    sides = 12
    center_hole_dia = 155.816 * 2;

    # s = cq.Workplane("XY").polygon_offset(sides,diameter, 180/sides).extrude(T)
    s = cq.Workplane("XY").transformed(rotate=(0,0,180/sides)).polygon(sides,diameter).extrude(T)
    #  ISO320 hole and bolt circle
    s = (s.faces(">Z")
         .workplane()
         .cboreHole(center_hole_dia, 159.004*2, 4.5, T-wall)
         .faces(">Z")
         .workplane()
         .transformed(rotate=(0,0,180/sides))
         .polygon(sides, 395, forConstruction=True)  # ISO320 clamps
         #.polygon_offset(sides, 395, 180/sides)  # ISO320 clamps
         .vertices()
         .hole(*tap('M10-1.5', 0.75*inch))
#         .faces(">Z")
#         .workplane()
         )
    # print('polygon', cq.Workplane.polygon)
    #  Tag all sides
    for i in range(s.faces("#Z").size()):
        (s.faces("#Z")
         .item(i)
         .workplane(centerOption="CenterOfMass")
         .tag(f'index{i}')
         )
    #  KF50 bulkhead    
    for i in range(s.faces("#Z").size()):
        s = (s.workplaneFromTagged(f"index{i}")
             .cboreHole(1.97*25.4, 2.06*25.4, .105*25.4, 20)
             .workplaneFromTagged(f"index{i}")
             .polygon(8,3.25*inch,forConstruction=True)
             # .polygon_offset(8,3.25*inch,offset=0,forConstruction=True)
             .vertices().hole(*tap('10-32', 3.0*inch/8.0))
             )

    return s

# print(__name__)
# show_object(s)
if (__name__=='temp'):
    # print('hello')
    c = collar()
    # print(c)
    show_object(c)
"""
s = (s.faces("#Z").first()
     .workplane(centerOption="CenterOfMass").hole(30, 20));
"""

