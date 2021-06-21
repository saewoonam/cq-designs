import cadquery as cq
import math
import orings
import screws
import nw_bulkhead

from screws import tap
from orings import oring
from nw_bulkhead import nw_bulkhead
import importlib
importlib.reload(orings)
importlib.reload(screws)

inch = 25.4;

def collar():
    T = 3.75*inch
    wall = 0.5*inch;
    diameter = 395+30
    sides = 12
    center_hole_dia = 155.816 * 2;

    s = cq.Workplane("XY").transformed(rotate=(0,0,180/sides)).polygon(sides,diameter).extrude(T)
    s.faces("<Z").workplane().tag(f'top')
    #  ISO320 hole and bolt circle
    s = (s.faces(">Z")
         .workplane()
         .tag(f'bottom')
         .cboreHole(center_hole_dia, 159.004*2, 4.5, T-wall)
         .faces(">Z")
         .workplane()
         .transformed(rotate=(0,0,180/sides))
         .polygon(sides, 395, forConstruction=True)  # ISO320 clamps
         .vertices()
         .hole(*tap('M12-1.75', 0.75*inch))
         )
    # inner top
    s = (s.faces(">Z[1]").workplane().tag("inner")
         .polygon(8, 4.8*inch, forConstruction=True)
         .vertices()
         .hole(*tap('4-40', 0.375*inch))
         )
    support_locations = [
        {'center':[0, 100], 'rot':0},
        {'center':[0, -100], 'rot':0},
        {'center':[0, 115], 'rot':45},
        {'center':[0, -115], 'rot':-45},
        {'center':[0, 125], 'rot':-90+22.5},
        {'center':[0, -125], 'rot':90-22.5},
        ]
    for location in support_locations:
        s = (s.workplaneFromTagged("inner")
             .transformed(rotate=(0,0,location['rot']))
             .center(*location['center'])
             .moveTo(-5.0/16.0*25.4, 0)
             .lineTo(5.0/16*25.4, 0)
             .vertices()
             .hole(*tap('4-40', 0.375*inch))
             )
    # top
    #  PT405
    s = (s.workplaneFromTagged("top")
         .moveTo(-80,0)
         .hole(5*inch, 0.5*inch)  # through hole
         .faces("<Z")
         .workplane()
         .moveTo(-80,0)
         .polygon(6,6.5*inch,forConstruction=True)  # mounting screws
         .vertices().hole(*tap('M6', 3.0*inch/8.0))
         .faces("<Z")
         .workplane()
         .moveTo(-80,0)
        )
    s = oring('2-254', s)
    # 1/4-20 mounting holes
    s = (s.workplaneFromTagged("top")
         .rect(10*inch, 10*inch, forConstruction=True)
         .vertices()
         .hole(*tap('1/4-20', 0.375*inch))
         )
    locations = []
    for x in [185, -185]:
        for y in [-2*inch, 0, 2*inch]:
            locations.append((x,y))
            locations.append((y,x))
    for y in [-40, 40]:
        for x in [85, 165]:
            locations.append((x,y))
    s = (s.workplaneFromTagged("top")
         .pushPoints(locations)
         .hole(*tap('1/4-20', 0.375*inch))
         )
    s = (s.workplaneFromTagged("top")
         .center(-75, 120))
    s = nw_bulkhead(s, 'nw25', 0.5*inch)
    s = (s.workplaneFromTagged("top")
         .center(-75,-120))
    s = nw_bulkhead(s, 'nw25', 0.5*inch)
    for angle in range(5):
        s = (s.workplaneFromTagged("top")
             .transformed(rotate=(0,0,angle*45))
             .center(0,-125))
        s = nw_bulkhead(s, 'nw40', 0.5*inch)
        
    #  Tag all sides
    for i in range(s.faces("#Z").size()):
        (s.faces("#Z")
         .item(i)
         .workplane(centerOption="CenterOfMass")
         .tag(f'index{i}')
         )
    #  KF50 bulkhead    
    for i in range(s.faces("#Z").size()):
        s = s.workplaneFromTagged(f"index{i}")
        s = nw_bulkhead(s, 'nw50', 20, offset=True)
        s = (s.workplaneFromTagged(f"index{i}")
             .rect(3.5*inch, 3*inch)
             .vertices()
             .hole(*tap('4-40', 0.375*inch))
             )

        """
        s = (s.workplaneFromTagged(f"index{i}")
             .cboreHole(1.97*25.4, 2.06*25.4, .105*25.4, 20)
             .workplaneFromTagged(f"index{i}")
             .transformed(rotate=(0,0,180/8))
             .polygon(8,3.25*inch,forConstruction=True)
             # .polygon_offset(8,3.25*inch,offset=0,forConstruction=True)
             .vertices().hole(*tap('10-32', 3.0*inch/8.0))
             .workplaneFromTagged(f"index{i}")
             .rect(3.5*inch, 3*inch)
             .vertices()
             .hole(*tap('4-40', 0.375*inch))
             )
        """
    inner = cq.Solid.makeCylinder(190, 3.75*inch-1.125*inch)
    inner = inner.translate(cq.Vector(0,0,0.5*inch))
    s = s.cut(inner)
    return s
def write_svg(part, name, direction):
    with open(f'./svg/{name}','w') as f:
        f.write(part.toSvg(opts={"projectionDir": direction,
                              "showHidden": False,
                              "height": 800,
                              "width": 800,}))
# print(__name__)
# show_object(s)
if (__name__=='temp'):
    # print('hello')
    c = collar()
    # print(c)
    show_object(c)
    c = c.rotate((0,0,0), (1,0,0), 180)
    cq.exporters.export(c, './outputs/collar.step')
    if True:
        write_svg(c, 'collar_x.svg', (1,0,0))
        write_svg(c, 'collar_pz.svg', (0,0, 1))
        write_svg(c, 'collar_nz.svg', (0,0, -1))