import cadquery as cq

s = (cq.Workplane("XY")
     .circle(5)
     .circle(5.1)
     .extrude(10)
    )

s1 = s.section(5).toSvg()

with open('s1.svg','w') as f:
    f.write(s1)

show_object(s)
# out = s.toSVG()
# print(out)
