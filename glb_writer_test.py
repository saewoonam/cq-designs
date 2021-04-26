import cadquery as cq
import OCP

w = 10
d = 10
h = 10

part1 = cq.Workplane().box(2*w,2*d,h)
part2 = cq.Workplane().box(w,d,2*h)
part3 = cq.Workplane().box(w,d,3*h)

assy = (
    cq.Assembly(part1, loc=cq.Location(cq.Vector(-w,0,h/2)))
    .add(part2, loc=cq.Location(cq.Vector(1.5*w,-.5*d,h/2)), color=cq.Color(0,0,1,0.5))
    .add(part3, loc=cq.Location(cq.Vector(-.5*w,-.5*d,2*h)), color=cq.Color("red"))
)
show_object(assy)

_, doc = cq.occ_impl.assembly.toCAF(assy)
name = OCP.TCollection.TCollection_AsciiString('assy.glb')
writer = OCP.RWGltf.RWGltf_CafWriter(name, True)
writer.SetTransformationFormat(OCP.RWGltf.RWGltf_WriterTrsfFormat.RWGltf_WriterTrsfFormat_Compact)
# copied from FreeCAD cpp code... the next commented line doesn't work yet.
# writer.ChangeCoordinateSystemConverter().SetInputCoordinateSystem(RWMesh_CoordinateSystemConverter)
header = OCP.TColStd.TColStd_IndexedDataMapOfStringString()
p = OCP.Message.Message_ProgressRange()
writer.Perform(doc, header, p)
