import cadquery as cq
import os
import itertools
import math
import sys, os
current_path = os.path.realpath(os.path.dirname(__name__))
sys.path.append(os.path.join(current_path, '..'))
from screws import tap, thru
from orings import oring
from nw_bulkhead import nw_bulkhead

import uuid
def create_clamp():
    t = 2
    clamp = cq.Workplane("XY").rect(40, 10).extrude(t)
    
    groove = cq.Workplane("XY").rect(6.5,10).extrude(0.65)
    dx = 10
    for i in range(-1, 2):
        g = groove.translate((i*dx, 0, 0))
        
        clamp = clamp.cut(g)
    clamp = clamp.rotate((0,0,0),(1,0,0), 180)
    clamp = clamp.edges("|X and <Z").fillet(0.5)
    clamp = clamp.edges(" (>Y or <Y)").edges("not (>Z or <Z)").edges("|X").fillet(0.5)
    
    spacer = cq.Workplane("XY").rect(40, 10).extrude(t)
    spacer = spacer.edges("|X").fillet(0.5)
    # blank = blank.faces(">Z").hole(3)
    dx = 16.5
    for i in [-1, 1]:
        clamp = clamp.faces(">Z").workplane().moveTo(i*dx, 0).hole(*thru("4-40", t))
        spacer = spacer.faces(">Z").workplane().moveTo(i*dx, 0).hole(*thru("4-40", t))
    return clamp, spacer

if (__name__=='temp'):
    clamp, spacer = create_clamp()
    show_object(spacer)
    show_object(clamp)
    write_step = True
    if write_step:
        cq.exporters.export(clamp, "outputs/clamp.step")
        cq.exporters.export(spacer, "outputs/spacer.step")