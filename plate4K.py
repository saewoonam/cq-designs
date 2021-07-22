import cadquery as cq
from screws import tap
import radial_holes
import Dimensions
from write_svg import write_svg
inch = 25.4
dimensions = Dimensions.Dimensions()

    
def plate4K():
    diameter = dimensions.plate4Kdiameter
    tube_offset = dimensions.tube_wall + 1
    tube_depth = 1/8*inch
    thickness = dimensions.plate4K['thickness']
    dr_offset = 35
    p = (cq.Workplane("XY")
         .circle(diameter/2).extrude(tube_depth))
    # make lip for tube
    p = (p.faces(">Z").workplane()
         .circle(diameter/2 - tube_offset)
         .extrude(thickness-tube_depth))
    # mark location of the dr_mounting point
    p = (p.faces(">Z").workplane().tag("bottom")
         .center(dr_offset,0).tag("dr_mount")
         )
    
    # make feedthroughs
    for angle in [0, 45, 135, 180]:
        p = (p.workplaneFromTagged("dr_mount")
             .transformed(rotate=(0,0,angle))
             .center(0, 100)
             .rect(40,15)
             .cutBlind(-thickness)
             .workplaneFromTagged("dr_mount")
             .transformed(rotate=(0,0,angle))
             .center(0, 100)
             .rect(46.3,0, forConstruction=True)
             .vertices()
             .hole(*tap('4-40', thickness))
             .edges("|Z")
             .fillet(0.047*inch)
             )
    # cut out mount for DR
    p = (p.workplaneFromTagged("dr_mount")
         .hole(86*2, 6)
         .workplaneFromTagged("dr_mount")
         .polygon(12, 160, forConstruction=True)
         .vertices()
         .hole(*tap('M5', thickness))
         .workplaneFromTagged("dr_mount")
         .hole(150)
         )
    # mounting holes for cryomech
    p = (p.workplaneFromTagged("bottom")
         .center(*dimensions.cryomech_offset)
         .polygon(6, 3*inch, forConstruction=True)
         .vertices()
         .hole(*tap('M4', thickness))
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
    points = []
    for i in range(9):
        points.append((0*inch, (i-4)*0.5*inch))
    for angle in [135, -135]:
        p = (p.workplaneFromTagged("dr_mount")
             .transformed(rotate=(0,0,angle))
             .center(120,0)
             .pushPoints(points)
             .hole(*tap('4-40', 8))
             )
    points =[]
    for i in range(7):
        points.append((0, (i-3)*0.5*inch))
        points.append(((i-3)*0.5*inch, 0))
    p = (p.workplaneFromTagged("bottom")
         .center(*dimensions.cryomech_offset)
         .pushPoints(points)
         .hole(*tap('4-40', 8))
         )

    support_locations = [
        {'center':[100,0], 'rot':90},  # rotate 90
        {'center':[-100, 0], 'rot':90},  #rot 90 to avoid feedthrough
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
        (0,0,(thickness+tube_depth)/2 )
        )
    p = p.cut(holes_wp)

    return p

def tube4K():
    diameter = dimensions.plate4Kdiameter
    thickness = dimensions.plate4K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= fridge_height - (334+1/8*inch)
    p = (cq.Workplane("XY")
         .circle(diameter/2).circle(diameter/2-dimensions.tube_wall)
         .extrude(length))
    # radial holes for the  tube
    holes = radial_holes.radial_holes_thru(diameter, 10, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0,0,(thickness-tube_depth)/2 )
        )
    p = p.cut(holes_wp)
    return p

def mold_tube4K():
    diameter = dimensions.plate4Kdiameter
    thickness = dimensions.plate4K['thickness']
    tube_depth = 1/8*inch
    fridge_height = 19.75*inch + 3.75*inch
    length= fridge_height - (334+1/8*inch)
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
    holes = radial_holes.radial_holes_thru(diameter, 10, '2-56', 8, 0)
    holes_wp = cq.Workplane().add(holes)
    holes_wp = holes_wp.translate(
        (0,0,(thickness-tube_depth)/2 )
        )
    p = p.cut(holes_wp)
    return p

if (__name__=='temp'):
    
    p = plate4K()
    show_object(p,options={"alpha":0.5, "color": (64, 164, 223)})
    """
    cq.exporters.export(p, './outputs/plate4K.step')
    t = tube4K()
    cq.exporters.export(t, './outputs/tube4K.step')
    t = t.translate((0,0,1/8*inch))
    show_object(t) 
    
    m = mold_tube4K()
    show_object(m)
    cq.exporters.export(m, './outputs/m4K.step')
    b = band_tube4K()
    cq.exporters.export(b, './outputs/b4K.step')
    show_object(b) 
    """
    if False:
        write_svg(p, 'plate4K_x.svg', (1,0,0))
        write_svg(p, 'plate4K_pz.svg', (0,0, 1))
        write_svg(p, 'plate4K_nz.svg', (0,0, -1))