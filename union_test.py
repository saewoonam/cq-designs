import cadquery as cq

def union_test(D, H, offset):
    p = (cq.Workplane("XY")
         .circle(D/2+1e-12).extrude(H)  # some kind of rounding problem at times
         )

    clamp = (cq.Workplane("XY")
             .box(D/2+offset, D, H)
             .translate((-(D/2+offset)/2, 0, H/2))
             )
    
    p = p.union(clamp)
    return p

# p_works = union_test(9, 12, 6)

inch = 25.4
D = 3/8*inch
H = 1/2*inch
offset = 1/4*inch

p_fails = union_test(D, H, offset)

def extrude_outline():
    D = 10
    left = -5
    H = 10
    p = ( cq.Workplane("XY")
         .moveTo(left,0).vLineTo(D/2).hLineTo(0)
         .radiusArc((0,-D/2), D/2)
         .hLineTo(left)
         .vLineTo(0)
         .close()
         .extrude(H)
         )