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

def qt405Plate():
    Thickness = 10
    diameter = 7*inch
    hole_count = 6
    s = (cq.Workplane("XY")
    .circle(diameter/2)
    .extrude(Thickness)
    .faces(">Z")
    .polygon(6, 6.5*inch, forConstruction=True)
    .vertices().hole(*tap('M6', Thickness))
    )
    return s
result = qt405Plate()
show_object(result)