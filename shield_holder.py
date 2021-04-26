import cadquery as cq
import os
import itertools
import math
inch = 25.4
import radial_holes
from screws import tap, cb

def tube(OD, ID, H):
    p = cq.Workplane("XY").circle(OD/2).circle(ID/2).extrude(H)
    return p

def can(OD, ID, H):
    p = tube(OD, ID, H)
    lid = cq.Workplane("XY").circle(OD/2).extrude((OD-ID)/2)
    p = p.union(lid)
    p = p.rotate((0,0,0),(1,0,0),180).translate((0,0,H))
    # make through holes
    holes = radial_holes.radial_holes_thru(OD, 5, '2-56', 4, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate((0,0,3))    
    p = p.cut(holes_wp)
    return p
    
outer_shield = can(45, 43.56, 117).translate((0,0,4))
inner_shield = can(41.15, 39.6, 106.9).translate((0,0,6+4))

# show_object(outer_shield)
# show_object(inner_shield)
OD = 45
ID = 43.56
# p = cq.Workplane("XY").circle(OD/2).extrude(12)
# p = p.faces(">Z").circle(OD/2).circle(ID/2).cutBlind(-9)
p = cq.Workplane("XY").circle(ID/2).extrude(12)
base = cq.Workplane("XY").circle(OD/2).extrude(4)
holes = radial_holes.radial_holes_tap(ID, 5, '2-56', 4, 15)
holes_wp = cq.Workplane().add(holes)
holes_wp = holes_wp.translate((0,0,3))

p = p.cut(holes_wp)

OD = 45
ID = 39.6
p = p.faces(">Z").circle(OD/2).circle(ID/2).cutBlind(-6)
holes = radial_holes.radial_holes_tap(ID, 5, '2-56', 4, 15)
holes_wp = cq.Workplane().add(holes)
holes_wp = holes_wp.translate((0,0,9))
p = p.cut(holes_wp)

bore = 30
cb_diameter = 7.0/32.0*25.4
p = p.faces(">Z").circle(bore/2).cutBlind(-12)
p = (p.faces(">Z")
     .polygon(6, 37.1, forConstruction=True)
     .vertices()
     .rotate((0,0,0),(0,0,1), 30)
     .hole(cb_diameter, 9)
     .polygon(6, 37.1, forConstruction=True)
     .vertices()
     .rotate((0,0,0),(0,0,1), 30)
     .hole(0.13*inch, 9)
     )

base = base.faces(">Z").circle(bore/2).cutBlind(-4)
base = (base.faces(">Z")
     .polygon(6, 37.1, forConstruction=True)
     .vertices()
     .rotate((0,0,0),(0,0,1), 30)
     .hole(0.13*inch, 9)
     )
r = OD
cos = math.cos
sin = math.sin
theta= -20/180*math.pi
dtheta = 40/180*math.pi

for i in range(6):
    offset = i* (60.0/180*math.pi)
    base = (base.faces(">Z").workplane()
        .lineTo(r*cos(offset + theta), r*sin(offset + theta))
        .lineTo(r*cos(offset+theta+dtheta), r*sin(offset+theta+dtheta))
        .close()
        .cutBlind(-4)
        )
    
# show_object(base)
# show_object(p)
p = p.translate((0,0,4))
p = p.union(base)
standoff = cq.Workplane().circle(3/16/2*25.4).extrude(90)
standoff = standoff.faces(">Z").workplane().hole(*tap('2-56', 6))
standoff = standoff.faces("<Z").workplane().hole(*tap('2-56', 6))
standoff = standoff.translate((0,0,12+4))
standoff = standoff.translate((17, 0, 0))
standoff2 = standoff.rotate((0,0,0), (0,0,1), 120)
standoff3 = standoff2.rotate((0,0,0), (0,0,1), 120)
standoffs = standoff.union(standoff2)
standoffs = standoffs.union(standoff3)

DY = 21
plate = cq.Workplane().circle(39/2).rect(25,17).translate((-12.5, -8.5, 0)).extrude(6)
plate = plate.edges("|Z").fillet(1)
plate = plate.translate((0,0,90+12))
plate = plate.faces(">Z").polygon(3, 34, forConstruction=True).vertices().cboreHole(*cb('2-56',6))
plate = plate.faces(">Z").translate((0,DY /2,0)).hole(*tap('2-56',6))
plate = plate.faces(">Z").translate((0,-DY/2,0)).hole(*tap('2-56',6))
# show_object(p)
# show_object(standoffs)
# show_object(plate)
pcb = cq.importers.importStep('./mu_shield_thru.step')
bbox = pcb.objects[0].BoundingBox();
pcb = pcb.translate( (-(bbox.xmin+bbox.xmax)/2, -(bbox.ymin+bbox.ymax)/2, 1.6))# pcb = pcb.rotate((0,0,0), (0,0,1), 90)
pcb = pcb.translate((0,0,4+12+90))

# show_object(pcb)
p4 = cq.importers.importStep('./outputs/supercables/p4.stp')
p4 = p4.translate((0,0,-6))
show_object(p4)
all_parts = (cq.Assembly()
       .add(p)
       .add(standoffs)
#       .add(plate)
       .add(inner_shield, color=cq.Color(1, 0, 1, 0.2))
       .add(outer_shield, color=cq.Color(0, 1, 1, 0.1))
       .add(pcb, color=cq.Color(0, 1, 0))
       )
all_parts.save("shield.step")

show_object(all_parts)
