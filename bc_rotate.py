import cadquery as cq

result = cq.Workplane("XY").box(90, 90, 90)
"""
pcd = 68;
bc = (cq.Workplane("XY")
      .polygon(6, pcd, forConstruction=True)
      .vertices()
      .circle(2)
      .extrude(5)
      .translate((0,0,-5))
      .rotate((0,0,0), (0,0,1), 15)
     )
"""
def side(f):
    diameter = 6
    depth = 10
    boreDir = -f.normalAt()
    center = f.Center()
    # first make the hole
    hole = cq.Solid.makeCylinder(
        diameter / 2.0, depth, center, boreDir
    )  # local coordianates!
    return hole

result = (result.faces("#Z")
          .each(side, True)
          )

result.end().cut(result)
show_object(result)