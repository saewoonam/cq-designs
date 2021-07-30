import cadquery as cq
from screws import tap
import radial_holes
import Dimensions
from write_svg import write_svg
inch = 25.4
dimensions = Dimensions.Dimensions()

def band_tube4K():
    diameter = dimensions.plate4Kdiameter
    thickness = dimensions.plate4K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= 10   #fridge_height - (334+1/8*inch)
    p = (cq.Workplane("XY")
         .circle(diameter/2+1).circle(diameter/2-dimensions.tube_wall+1)
         .extrude(length))
    # radial holes for the  tube
    holes = radial_holes.radial_holes_thru(diameter+2, 10, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0,0,(thickness-tube_depth)/2 )
        )
    p = p.cut(holes_wp)
    return p
def band_Lip4K():
    diameter = dimensions.plate4Kdiameter
    thickness = dimensions.plate4K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= 10 # fridge_height - (146+1/8*inch)
    # length /= 2;
    #add top lip
    c = (cq.Workplane("XY")
        .circle(diameter/2+1).circle(diameter/2-dimensions.tube_wall+1-10)
        .extrude(3).translate((0,0,-3)))
        
    return c

if (__name__=='temp'):

    a = band_Lip4K()
    b = band_tube4K()
    c = a.union(b)
    #Holepunch Cutout
    Rotations = []
    for i in [0, 45, 90, 135]:
        Rotations.append((0,0,i))
        d = (cq.Workplane("XY")
             .rect(30,262).extrude(3).translate((0,0,-3)).rotateAboutCenter((0,0,1),i)
             )
        c=c.cut(d)
    cq.exporters.export(c, './outputs/4K_Ring.step')
    show_object(c) 

    if False:
        write_svg(p, 'plate4K_x.svg', (1,0,0))
        write_svg(p, 'plate4K_pz.svg', (0,0, 1))
        write_svg(p, 'plate4K_nz.svg', (0,0, -1))