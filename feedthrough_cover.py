import cadquery as cq
import importlib
from screws import tap, thru
import radial_holes
import Dimensions
from write_svg import write_svg
import os
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))

inch = 25.4
dimensions = Dimensions.Dimensions()
import plate40K
def create_cover(solid=False):
    t = 3
    (W, H) = (42, 17)
    dx=5
    pts = [(-W/2, H/2), (W/2, H/2), (W/2, 3), (W/2+dx, 3), (W/2+dx, -3), (W/2, -3),
           (W/2 ,-H/2), (-W/2, -H/2),
           (-W/2, -3), (-W/2-dx, -3), (-W/2-dx, 3), (-W/2, 3)]
    
    cover = cq.Workplane("XY").polyline(pts).close().extrude(t)
    if(not solid):
        cover = cover.faces(">Z").workplane().rect(35,12).cutThruAll()
    cover = cover.edges("|Z").fillet(1)
    
    if(not solid):
        cover = cover.faces(">Z").workplane().rect(40,14).cutBlind(-0.5)
        cover = (cover.faces(">Z").workplane()
                 .rect(40,14, forConstruction=True).vertices()
                 .circle(0.5).cutBlind(-0.5)
                 )
    #print(cover.edges("|X").size())
    
    
    cover = (cover.faces(">Z").workplane()
             .pushPoints([(-46.3/2, 0), (46.3/2, 0)])
             .hole(*thru("4-40", 3))
             )
    return cover

cover = create_cover(True)
loom_cover = create_cover()
show_object(loom_cover)
test = False
if test:

    import loom_clamp.clamp
    importlib.reload(loom_clamp.clamp)
    
    c,b = loom_clamp.clamp.create_clamp()
    
    c = c.rotate((0,0,0), (1,0,0), 90)
    b = b.rotate((0,0,0), (1,0,0), 90)
    #show_object(b)
    #show_object(c)
    
    for i in range(-1, 2):
        temp = c.translate((0, 4*i-1, 5+3))
        show_object(temp)
        temp = b.translate((0, 4*i-1, 5+3))
        show_object(temp)
    for i in range(2,3):
        temp = b.translate((0, 4*i-1, 5+3))
        show_object(temp)
        
    p = plate40K.plate40K()
    p = p.translate( (0,123,-12.5) )
    show_object(p)