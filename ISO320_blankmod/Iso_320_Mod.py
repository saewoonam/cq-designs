import cadquery as cq
import os
import itertools
import math
import sys, os
current_path = os.path.realpath(os.path.dirname(__name__))
sys.path.append(os.path.join('..'))
from screws import tap, thru
from orings import oring
from nw_bulkhead import nw_bulkhead
import uuid

def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))
inch = 25.4
dist = -30
if True:
    s = cq.importers.importStep('./qf320-bk.stp')
    bbox = s.objects[0].BoundingBox()
    print(bbox)
    s.faces(">Z").workplane().tag(f'top')
    #s = s.workplaneFromTagged("top")
    
    s = (s.workplaneFromTagged("top")
         .moveTo(dist,0)
         .hole(5*inch)  # through hole
         .faces(">Z")
         .workplane()
         .moveTo(dist,0)
         .polygon(6,6.5*inch,forConstruction=True)  # mounting screws
         .vertices().hole(*tap('M6', 3.0*inch/8.0))
         .faces(">Z")
         .workplane()
         .moveTo(dist,0)
        )
    s = oring('2-254', s)

    
else:
    s = (cq.Workplane("XY").box(150, 150, 150)
         .faces(">Z")
         .workplane()
         )

    

# 1/4-20 mounting holes
s = (s.workplaneFromTagged("top")
     .rect(8*inch, 10*inch, forConstruction=True)
     .vertices()
     .hole(*tap('1/4-20', 0.375*inch))
     )

for angle in (-1, 1):
    s = s.workplaneFromTagged(f"top").transformed(rotate=(0,0,angle*90)).center(130,0)
    s = nw_bulkhead(s, 'nw40', 20, offset=True)#, offset=True)
    
s = s.workplaneFromTagged(f"top").center(120,0)
s = nw_bulkhead(s, 'nw50', 20, offset=True)

clamp = cq.importers.importStep('./qf40-150-bc.stp')
clamp= clamp.rotate((0,0,0), (0,1,0), 90).translate((0,130,20))

clamp50 = cq.importers.importStep('./qf50-200-bc.stp')
clamp50 = clamp50.rotate((0,0,0), (0,1,0), 90).translate((120,0,20))

pt405_cover = cq.Workplane("XY").circle(3.5*inch).extrude(6)
pt405_cover = ( pt405_cover.faces(">Z")
         .workplane()
         .polygon(6,6.5*inch,forConstruction=True)  # mounting screws
         .vertices().hole(*thru('M6', 3.0*inch/8.0))
         )
pt405_cover = pt405_cover.translate((dist, 0, bbox.zmax))

show_object(s)
show_object(pt405_cover)
show_object(clamp)
show_object(clamp50)
"""
cq.exporters.export(s, '. /Iso320BlankMod.step')
"""