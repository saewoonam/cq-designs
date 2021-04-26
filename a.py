import cadquery as cq

def box():
    return cq.Workplane("XY").box(10,20,30)

c = cq.Workplane("XY").box(30,20,10)
