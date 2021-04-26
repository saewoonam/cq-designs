import cadquery as cq

s = cq.Solid.makeCylinder(5,28, pnt=cq.Vector(10,10,0), dir=cq.Vector(-1,-1,0) )
s = cq.Workplane(s)

print('each', s.faces().each(lambda f: print(f.normalAt())))
s = s.faces().item(2).workplane().circle(2).extrude(10)
show_object(s)

with open('out.svg','w') as f:
    f.write(s.toSvg(opts={"projectionDir": (-20, -20, 0),
                          "showHidden": False,}))