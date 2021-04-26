import cadquery as cq

result = (cq.Workplane("XY").box(10,10,2)

          .faces(">Z")
          .workplane()
          .transformed(rotate=(0,0,20))
          .rect(3,3, forConstruction=True)
          .vertices()
          .circle(0.5)
          .extrude(2)
          .faces(">Z")  # objects in space b/c >Z is above box
          .workplane()
          .rect(5,5, forConstruction=True)
          .vertices()
          .circle(0.5)
          .extrude(2)
          )
