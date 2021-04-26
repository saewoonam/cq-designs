import cadquery as cq
import collar_v2
import plate40K
import plate4K
import os
import importlib
import itertools
importlib.reload(collar_v2)

# pt405 = cq.importers.importStep('../chase_dr/step/PT405.stp')
# pt405 = (pt405.rotate((0,0,0), (0,0,1), 120).translate((-80, 0, 0)))
#show_object(pt405.rotate((0,0,0), (0,0,1), 120).translate((-80, 0, 0)))
# show_object(pt405)
dr = cq.importers.importStep('../chase_dr/step/CC_MINUS_NIST_DEF.STEP')
dr_center = dr.objects[0].CenterOfBoundBox()
dr = dr.translate(-dr_center)
show_object(dr)
# collar = collar_v2.collar().rotate((0,0,0), (1,0,0), 180)
# show_object(collar, options={'color':'silver'})
# cq.exporters.export(collar, "./outputs/collar.step")
                                 
# p40K = plate40K.plate40K()
# cq.exporters.export(p40K, "./outputs/plate40K.step")
# show_object(p40K)
# p4K = plate4K.plate4K()
# cq.exporters.export(p4K, "./outputs/plate4K.step")
# show_object(p4K)

collar = cq.importers.importStep('./outputs/collar.step')
p40K = cq.importers.importStep('./outputs/plate40K.step')
p4K = cq.importers.importStep('./outputs/plate4K.step')

p40K = p40K.rotate((0,0,0), (1,0,0), 180).translate((0,0,-146))
p4K = p4K.rotate((0,0,0), (1,0,0), 180).translate((0,0,-334))

show_object(pt405)
show_object(collar)
show_object(p40K)
show_object(p4K)
"""
cryostat = ( cq.Assembly()
            .add(pt405, name='pt405', color=cq.Color("red"))
            .add(collar, name='collar')
            .add(p40K, name='p40K')
            )

(cryostat.constrain('collar@faces@<Z', 'pt405@faces@>Z', "Axis")
     .constrain('collar@faces@<Z', 'pt405@faces@|Z', 'Plane')
     .constrain('collar@faces@<Z', 'pt405@faces@>Z', "Axis")
     .constrain('collar@faces@<Z', 'p40K@faces@<Z', "Axis")
     #.constrain('pt405@faces@<Z', 'p40K@faces@<Z', "Plane")
     # .constrain('p4K@faces>Z', 'pt405@faces@<Z', "Plane")
 )
cryostat.solve()
show_object(cryostat)
"""
"""
cq.exporters.export(collar, "./out.step")
"""
# cryostat.save("./out.step")
def exportStep(object_list, filename):
    vals = list(itertools.chain(*[o.vals() for obj in object_list for o in obj.all()]))
    compound = cq.Compound.makeCompound(vals)
    compound.exportStep(filename)
    return compound
    
# compound = exportStep([pt405, collar, p40K], './out.step')
# os.system('./viewerjs/3d-model-convert-to-gltf/convert.sh stp ./out.step ./viewerjs/out.glb')

# result = compound.faces(">X").workplane(-200).split()
# show_object(result)