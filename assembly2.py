import cadquery as cq
import os
import itertools
import math
inch = 25.4

if True:
    pt405 = cq.importers.importStep('chase_dr/step/PT405.stp')
    pt405 = (pt405.rotate((0,0,0), (0,0,1), 120).translate((-80, 0, 0)))
    show_object(pt405)
    # dr = cq.importers.importStep('../chase_dr/step/CC_MINUS_NIST_DEF_v2.STEP')
    # dr_center = dr.objects[0].CenterOfBoundBox()
    # dr = dr.translate(-dr_center)
    # dr = dr.translate((0, 0, dr_center.z-65.6685))
    # cq.exporters.export(dr, './outputs/dr.step')
    
    dr = cq.importers.importStep('./outputs/dr.step')
    dr = dr.rotate((0,0,0), (0,0,1), -90).translate((35,0,-334-6))
    show_object(dr)
    ovc = cq.importers.importStep('./chase_dr/step/2N_ISO_320_OF.stp')
    ovc = ovc.rotate((0,0,0), (0,1,0), 90)
    bbox = ovc.objects[0].BoundingBox()
    ovc = ovc.translate((-bbox.center.x, -bbox.center.y, -bbox.zmax-3.75*inch))
    # .translate((0,0,-3.75*inch))
    show_object(ovc, options = {
        "color" : (100, 0, 0),
        "alpha" :  0.95
        })

bc25 = cq.importers.importStep('./chase_dr/step/qf25-100-bc.stp')
bc25 = bc25.rotate((0,0,0), (0,1,0), -90).translate((-75, -120,0))
show_object(bc25)
bc40 = cq.importers.importStep('./chase_dr/step/qf40-150-bc.stp')
bc40 = bc40.rotate((0,0,0), (1,0,0), 90).rotate((0,0,0), (0,0,1), 30).translate((0, -125,0))
show_object(bc40)
bc40 = bc40.rotate((0,0,0), (0,0,1), 45)
show_object(bc40)
bc50 = cq.importers.importStep('./chase_dr/step/qf50-200-bc.stp')
bc50 = bc50.rotate((0,0,0), (1,0,0), 90).translate((0, -220,-3.75*inch/2))
show_object(bc50)

support_clamp = cq.importers.importStep('./outputs/support_clamp.step')
collar = cq.importers.importStep('./outputs/collar.step')
p40K = cq.importers.importStep('./outputs/plate40K.step')
t40K = cq.importers.importStep('./outputs/tube40K.step')
p4K = cq.importers.importStep('./outputs/plate4K.step')
t4K = cq.importers.importStep('./outputs/tube4K.step')

p40K = p40K.rotate((0,0,0), (1,0,0), 180).translate((0,0,-146))
t40K = t40K.rotate((0,0,0), (1,0,0), 180).translate((0, 0, -146-1/8*inch))
p4K = p4K.rotate((0,0,0), (1,0,0), 180).translate((0,0,-334))
t4K = t4K.rotate((0,0,0), (1,0,0), 180).translate((0, 0, -334-1/8*inch))

rail = cq.Workplane().box(12*inch, 1*inch, 1*inch).translate((0, -185,0.5*inch))
show_object(rail)
rail = cq.Workplane().box(1*inch, 12*inch, 1*inch).translate((-185,0,0.5*inch))
show_object(rail)

support_locations = [
    {'center':[0, 100], 'rot':0},  # rotate 90
    {'center':[0, -100], 'rot':0},  #rot 90 to avoid feedthrough
    {'center':[0, 115], 'rot':45},
    {'center':[0, -115], 'rot':-45},
    {'center':[0, 125], 'rot':-90+22.5},
    {'center':[0, -125], 'rot':90-22.5},
    ]
def build_clamps(down= False, z_offset= -334):
    clamps = []
    # down = False
    for loc in support_locations:
        if down:
            temp = support_clamp.rotate((0,0,0), (1,0,0), 180)
        else:
            temp = support_clamp.rotate((0,0,0), (1,0,0), 0)
    
        if loc['center'][1]<0:
            temp = temp.rotate((0,0,0), (0,0,1), -90)
        elif loc['center'][1]>0:
            temp = temp.rotate((0,0,0), (0,0,1), 90)
        if (z_offset==-334) and (loc['center'][1]==100 or loc['center'][1] ==-100):
            temp = temp.rotate((0,0,0), (0,0,1), 90)
    
        temp = temp.translate((0,0,0))
        
        #center = (*rot_2d(loc['center'], loc['rot']),0)
        #temp = temp.translate(center)
        temp = temp.translate((*loc['center'], 0))
        temp = temp.rotate((0,0,0), (0,0,1), loc['rot'])
        clamps.append(temp)
    layer = clamps[0]
    for c in clamps[1:]:
        layer = layer.union(c)
    layer = layer.translate((0,0,z_offset))
    return layer
layer = build_clamps(False, -334)
show_object(layer)
layer = build_clamps(False, -146)
show_object(layer)
layer = build_clamps(True, -146-12)
show_object(layer)
layer = build_clamps(True, -0.5*inch)
show_object(layer)
    # show_object(temp)

show_object(collar)
show_object(p40K)
show_object(t40K, options={'color':0x008000, 'alpha':0.8})
show_object(p4K)
show_object(t4K, options={'color':0x000080, 'alpha':0.8})

def exportStep(object_list, filename):
    vals = list(itertools.chain(*[o.vals() for obj in object_list for o in obj.all()]))
    compound = cq.Compound.makeCompound(vals)
    compound.exportStep(filename)
    return compound
   
compound = exportStep([pt405, collar, p40K], './out.step')
# os.system('./viewerjs/3d-model-convert-to-gltf/convert.sh stp ./out.step ./viewerjs/out.glb')

# result = compound.faces(">X").workplane(-200).split()
# show_object(result)