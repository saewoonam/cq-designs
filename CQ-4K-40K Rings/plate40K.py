import cadquery as cq
from screws import tap
import radial_holes
import Dimensions
from write_svg import write_svg
inch = 25.4
dimensions = Dimensions.Dimensions()


def band_tube40K():
    diameter = dimensions.plate40Kdiameter
    thickness = dimensions.plate40K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= 10 # fridge_height - (146+1/8*inch)
    # length /= 2;
    p = (cq.Workplane("XY")
         .circle(diameter/2+1).circle(diameter/2-dimensions.tube_wall+1)
         .extrude(length))
    # radial holes for the  tube
    holes = radial_holes.radial_holes_thru(diameter+2, 20, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0,0,(thickness-tube_depth)/2 )
        )
    p = p.cut(holes_wp)

    return p

def band_Lip40K():
    diameter = dimensions.plate40Kdiameter
    thickness = dimensions.plate40K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= 10 # fridge_height - (146+1/8*inch)
    # length /= 2;
    #add top lip
    c = (cq.Workplane("XY")
        .circle(diameter/2+1).circle(diameter/2-dimensions.tube_wall+1-10)
        .extrude(3).translate((0,0,10)))
    return c
if (__name__ == 'temp'):
    """
    p = plate40K()
    show_object(p)
    cq.exporters.export(p, './outputs/plate40K.step')
    t = tube40K()
    cq.exporters.export(t, './outputs/tube40K.step')
    t = t.translate((0,0,1/8*inch))
    show_object(t) 
    """
    a = band_Lip40K()
    b = band_tube40K()
    c = a.add(b)
    cq.exporters.export(c, './40K_Ring.step')
    show_object(c) 

    if False:
        write_svg(p, 'plate40K_x.svg', (1,0,0))
        write_svg(p, 'plate40K_pz.svg', (0,0, 1))
        write_svg(p, 'plate40K_nz.svg', (0,0, -1))