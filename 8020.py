import cadquery as cq

strut = cq.importers.importStep('../output/2020 X 145.step')
box = cq.Workplane().box(100, 100, 100)

box2 = cq.Workplane().box(50,50, 100)

box = box.cut(box2)
strut2 = strut.translate((0,0,1000))
strut = strut.cut(strut2)
show_object(box)
show_object(strut2)