import cadquery as cq
from screws import tap, thru
import radial_holes
import Dimensions
from write_svg import write_svg
import os
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))

inch = 25.4
dimensions = Dimensions.Dimensions()


def plate40K():
    diameter = dimensions.plate40Kdiameter
    tube_offset = dimensions.tube_wall + 1
    tube_depth = 1/8*inch
    thickness = dimensions.plate40K['thickness']
    dr_offset = 35
    p = (cq.Workplane("XY")
         .circle(diameter/2).extrude(tube_depth))
    # make lip for tube
    p = (p.faces(">Z").workplane()
         .circle(diameter/2 - tube_offset)
         .extrude(thickness-tube_depth))
    # mark location of the dr_mounting point
    p = (p.faces(">Z").workplane().tag("bottom")
         .center(dr_offset, 0).tag("dr_mount")
         )

    # make feedthroughs
    for angle in [0, 30, 150, 180]:
        p = (p.workplaneFromTagged("bottom")
             .transformed(rotate=(0,0,angle))
             .center(0,-123)
             .rect(40,15)
             .cutBlind(-thickness)
             .workplaneFromTagged("bottom")
             .transformed(rotate=(0,0,angle))
             .center(0,-123)
             .rect(46.3,0, forConstruction=True)
             .vertices()
             .hole(*tap('4-40', thickness))
             .edges("|Z")
             .fillet(0.047*inch)
             )
    # mounting holes for cryomech
    p = (p.workplaneFromTagged("bottom")
         .center(*dimensions.cryomech_offset)
         .transformed(rotate=(0,0,-10))
         .polygon(6, 4.38*inch, forConstruction=True)
         .vertices()
         .hole(*thru('M5', thickness))
         .workplaneFromTagged("bottom")
         .center(*dimensions.cryomech_offset)
         .hole(3.5*inch)
         )
    
    # fiber / pumpout
    p = (p.workplaneFromTagged("bottom")
         .pushPoints([ (85, 80), (85,-80)])
         .hole(*tap('1/4-npt', thickness))
         )
    p = (p.workplaneFromTagged("bottom")
         .pushPoints([ (-63, 95), (-63,-95)])
         .hole(*tap('1/4-20', thickness))
         )
    # 4-40 holes for mounting stuff
    points =[]
    for i in range(4):
        for j in range(5):
            points.append(((i-1)*inch, (j-2)*inch))

    p = (p.workplaneFromTagged("bottom")
         .center(*dimensions.dr_offset)
         .pushPoints(points)
         .hole(*tap('4-40', 8))
         )

    support_locations = [
        {'center':[0,100], 'rot':0},  # rotate 90
        {'center':[0, -100], 'rot':0},  #rot 90 to avoid feedthrough
        {'center':[0, 115], 'rot':45},
        {'center':[0, -115], 'rot':-45},
        {'center':[0, 125], 'rot':-90+22.5},
        {'center':[0, -125], 'rot':90-22.5},
        ]
    for location in support_locations:
        p = (p.workplaneFromTagged("bottom")
             .transformed(rotate=(0,0,location['rot']))
             .center(*location['center'])
             .moveTo(-5.0/16.0*25.4, 0)
             .lineTo(5.0/16*25.4, 0)
             .vertices()
             .hole(*tap('4-40', thickness))
             )
    # radial holes for the  tube
    holes = radial_holes.radial_holes_tap(diameter, 10, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0, 0, (thickness+tube_depth)/2)
        )
    p = p.cut(holes_wp)

    return p


def tube40K():
    diameter = dimensions.plate40Kdiameter
    thickness = dimensions.plate40K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length = fridge_height - (146+1/8*inch)
    p = (cq.Workplane("XY")
         .circle(diameter/2).circle(diameter/2-dimensions.tube_wall)
         .extrude(length))
    # radial holes for the  tube
    holes = radial_holes.radial_holes_thru(diameter, 10, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0, 0, (thickness-tube_depth)/2)
        )
    p = p.cut(holes_wp)
    return p

def mold_tube40K():
    diameter = dimensions.plate40Kdiameter
    thickness = dimensions.plate40K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= fridge_height - (146+1/8*inch)
    length /= 2;
    p = (cq.Workplane("XY")
         .circle(diameter/2-dimensions.tube_wall).circle(diameter/2-3*dimensions.tube_wall)
         .extrude(length))
    # radial holes for the  tube
    holes = radial_holes.radial_holes_thru(diameter, 10, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0,0,(thickness-tube_depth)/2 )
        )
    p = p.cut(holes_wp)
    return p
def band_tube40K():
    diameter = dimensions.plate40Kdiameter
    thickness = dimensions.plate40K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= thickness-tube_depth
    offset = 0.5;
    # fridge_height - (146+1/8*inch)
    # length /= 2;
    p = (cq.Workplane("XY")
         .circle(diameter/2+1).circle(diameter/2-dimensions.tube_wall+offset)
         .extrude(length))
    # radial holes for the  tube
    holes = radial_holes.radial_holes_thru(diameter, 10, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0,0,(thickness-tube_depth)/2 )
        )
    p = p.cut(holes_wp)
    return p

if (__name__ == 'temp'):
    
    p = plate40K()
    show_object(p)
    """
    cq.exporters.export(p, './outputs/plate40K.step')
    
    t = tube40K()
    cq.exporters.export(t, './outputs/tube40K.step')
    t = t.translate((0,0,1/8*inch))
    show_object(t) 
    
    m = mold_tube40K()
    cq.exporters.export(m, fixpath('./outputs/m40K.step'))
    show_object(m) 
    b = band_tube40K()
    cq.exporters.export(b, fixpath('./outputs/b40K.step'))
    show_object(b) 
"""
    if False:
        write_svg(p, 'plate40K_x.svg', (1,0,0))
        write_svg(p, 'plate40K_pz.svg', (0,0, 1))
        write_svg(p, 'plate40K_nz.svg', (0,0, -1))