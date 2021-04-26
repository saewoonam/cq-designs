import cadquery
center_hole_dia = 22;
s = cadquery.Workplane("XY").box(80.0, 60.0, 10)
s = (s.faces(">Z").workplane().hole(center_hole_dia))

cadquery.show_object(s)
