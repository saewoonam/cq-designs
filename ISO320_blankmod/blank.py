import cadquery as cq
import os
import itertools
import math
import sys, os
current_path = os.path.realpath(os.path.dirname(__name__))
sys.path.append(os.path.join(current_path, '..', 'designs'))
from screws import tap, thru
from orings import oring
from nw_bulkhead import nw_bulkhead
import uuid

def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))
inch = 25.4

if True:
    s = cq.importers.importStep('./qf320-bk.stp')
    bbox = s.objects[0].BoundingBox()
    print(bbox)
    s.faces(">Z").workplane().tag(f'top')
    #s = s.workplaneFromTagged("top")
    
    s = (s.workplaneFromTagged("top")
         #.moveTo(-80,0)
         .hole(5*inch)  # through hole
         .faces(">Z")
         .workplane()
         #.moveTo(-80,0)
         .polygon(6,6.5*inch,forConstruction=True)  # mounting screws
         .vertices().hole(*tap('M6', 3.0*inch/8.0))
         .faces(">Z")
         .workplane()
         #.moveTo(-80,0)
        )
    s = oring('2-254', s)

    
else:
    s = (cq.Workplane("XY").box(150, 150, 150)
         .faces(">Z")
         .workplane()
         )

    
"""
# 1/4-20 mounting holes
s = (s.workplaneFromTagged("top")
     .rect(10*inch, 10*inch, forConstruction=True)
     .vertices()
     .hole(*tap('1/4-20', 0.375*inch))
     )
"""
for angle in range(-1, 2):
    s = s.workplaneFromTagged(f"top").transformed(rotate=(0,0,angle*45)).center(130,0)
    s = nw_bulkhead(s, 'nw40', 20, offset=True) #, offset=True)

clamp = cq.importers.importStep('./qf40-150-bc.stp')
clamp= clamp.rotate((0,0,0), (0,1,0), 90).translate((130,0,20))

pt405_cover = cq.Workplane("XY").circle(3.5*inch).extrude(6)
pt405_cover = ( pt405_cover.faces(">Z")
         .workplane()
         .polygon(6,6.5*inch,forConstruction=True)  # mounting screws
         .vertices().hole(*thru('M6', 3.0*inch/8.0))
         )
pt405_cover = pt405_cover.translate((0, 0, bbox.zmax))
show_object(s)
show_object(pt405_cover)
show_object(clamp)