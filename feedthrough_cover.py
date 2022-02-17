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
def create_cover(solid=False, pocket=True):
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
    
    if(pocket and not solid):
        (l,w, d) = 40.1, 14.1, 0.5
        cover = cover.faces(">Z").workplane().rect(l,w).cutBlind(-d)
        cover = (cover.faces(">Z").workplane()
                 .rect(l,w, forConstruction=True).vertices()
                 .circle(0.5).cutBlind(-d)
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
write_step = True
if write_step:
    cq.exporters.export(loom_cover, "outputs/loom_cover.step")
    cq.exporters.export(cover, "outputs/feedthru_cover.step")
test = True
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