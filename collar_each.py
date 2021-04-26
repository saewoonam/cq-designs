import cadquery as cq

T = 50
wall = 6
diameter = 200
sides = 8
center_hole_dia = 160;

s = cq.Workplane("XY").polygon(sides,diameter).extrude(T)

def side(f):
    cut = cq.Solid.makeCylinder(1,20, f.Center(),-f.normalAt())
    #box = cq.Solid.makeCylinder(1, 20, f.Center(), -f.normalAt())
    #cut  = cut.fuse(box)
    return cut

s = (s.faces(">Z")
     .workplane()
     .hole(center_hole_dia, T-wall)
     .faces('#Z')
     .each(side)
#     .each(lambda f: cq.Solid.makeCylinder(15,20, f.Center(),-f.normalAt()))
     )
cuts = s
s = s.end()
s = s.cut(cuts)
show_object(s)
show_object(cuts)

# show_object(s.end().cut(s))