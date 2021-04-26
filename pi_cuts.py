import cadquery as cq
import math

inch=25.4
OD=45
base = cq.Workplane().circle(OD/2).extrude(4)

r = OD
cos = math.cos
sin = math.sin
theta= -20/180*math.pi
dtheta = 40/180*math.pi

bore = 30;
base = base.faces(">Z").circle(bore/2).cutBlind(-5)
base = (base.faces(">Z")
     .polygon(6, 37.1, forConstruction=True)
     .vertices()
     .rotate((0,0,0),(0,0,1), 30)
     .hole(0.13*inch, 9)
     )
for i in range(6):
    
    offset = i* (60.0/180*math.pi)
    base = (base.faces(">Z").workplane()
        .lineTo(r*cos(offset + theta), r*sin(offset + theta))
        .lineTo(r*cos(offset+theta+dtheta), r*sin(offset+theta+dtheta))
        .close()
        .cutBlind(-4)
        )




show_object(base)