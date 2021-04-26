import cadquery as cq
import os
import itertools
import math
inch = 25.4

if True:
    pt405 = cq.importers.importStep('../chase_dr/step/PT405.stp')
    pt405 = (pt405.rotate((0,0,0), (0,0,1), 120).translate((-80, 0, 0)))
    # show_object(pt405)
    
    dr = cq.importers.importStep('./outputs/dr.step')
    dr = dr.rotate((0,0,0), (0,0,1), -90).translate((35,0,-334-6))
    # show_object(dr)
    ovc = cq.importers.importStep('../chase_dr/step/2N_ISO_320_OF.stp')
    ovc = ovc.rotate((0,0,0), (0,1,0), 90)
    bbox = ovc.objects[0].BoundingBox()
    ovc = ovc.translate((-bbox.center.x, -bbox.center.y, -bbox.zmax-3.75*inch))
    # show_object(ovc, options = {
    #     "color" : (100, 0, 0),
    #     "alpha" :  0.95
    #     })

a = (cq.Assembly()
     .add(dr, name='dr')
     .add(pt405, name='pt405')
     .add(ovc, name='ovc')
     )
# a.solve()
show_object(a,name='a')
