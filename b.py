import cadquery as cq

def box():
    return cq.Workplane("XY").box(20,20,20)
