import cadquery as cq

result = (cq.Workplane("XY").box(10,10,5).faces(">Z").workplane()
          .moveTo(-3,0).lineTo(3,0).vertices().circle(1).extrude(2)
          )