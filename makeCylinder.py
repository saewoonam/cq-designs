import cadquery as cq

s = cq.Solid.makeCylinder(5,20, pnt=cq.Vector(10,10,0), dir=cq.Vector(9,9,0) )
s = cq.Workplane(s)
print(s.faces().item(2).normalAt())
show_object(s)