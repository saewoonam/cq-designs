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
    Thickness = 6.35
    diameter = 7*inch
    hole_count = 6
    s = (cq.Workplane("XY")
    .circle(diameter/2)
    .extrude(Thickness)
    .faces(">Z")
    .polygon(6, 6.5*inch, forConstruction=True)
    .vertices().hole(6.35)
    )
    return s
result = qt405Plate()

show_object(result)

cq.exporters.export(result, './outputs/PT405_Block_Off_Plate.step')