import cadquery as cq
from screws import tap, cb, thru
inch = 25.4

p = (cq.Workplane("XY")
     .circle(3/8*inch/2).extrude(0.5*inch)
     )
clamp = (cq.Workplane("XY")
         .box(3/8*inch/2+1/4*inch, 3/8*inch, 0.5*inch)
         .translate((-7/32*inch, 0, 0.25*inch))
         .faces(">Y")
         .workplane(centerOption="CenterOfBoundBox")
         .center(3/32*inch, 0.125*inch)
         .hole(*tap('2-56', 3/8*inch))
         .faces("<Y")
         .workplane(centerOption="CenterOfBoundBox")
         .center(-3/32*inch, 0.125*inch)
         .cboreHole(*cb('2-56', 3/16*inch))
         )

slot = (cq.Workplane("XY")
         .box(3/8*inch/2+1/4*inch, 2, 0.5*inch)
         .translate((-7/32*inch, 0, 0.25*inch))
)
clamp = clamp.cut(slot)
p = p.cut(slot)

p = p.union(clamp)
p = p.faces(">Z").workplane().hole(0.256*inch)

box = (cq.Workplane("XY").box(0.25*inch+3/16*inch, 3/8*inch, 0.25*inch)
       .translate((-7/32*inch, 0, 0.125*inch))
       )
p = p.cut(box)

base = (cq.Workplane("XY").box(3/8*inch, 7/8*inch, 3)
        .translate((0,0,1.5))
        .faces(">Z")
        .workplane()
        .rect(0, 5/8*inch, forConstruction=True)
        .vertices()
        .hole(*thru('4-40', 3))
        )
p = p.union(base)
cq.exporters.export(p, './outputs/support_clamp.step')
show_object(p)
"""

"""