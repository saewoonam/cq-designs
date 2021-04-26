import cadquery as cq

dxf = cq.importers.importDXF('./1010.dxf')
scaled = cq.Workplane(dxf.objects[0].scale(25.4))
# dxf = dxf.wires().toPending()
# show_object(dxf)
# dxf = dxf.wires().toPending().extrude(10)

def series10(length):
    # return dxf.wires().toPending().extrude(length)
    return scaled.wires().toPending().extrude(length)

if (__name__=='temp'):
    # pass
    part = series10(1)
    show_object(part)