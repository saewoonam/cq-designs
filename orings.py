import cadquery as cq

inch = 25.4
# Inner Diameter, groove width, groove depth

oring_list = {
  '2-019':[0.813*inch, 0.084*inch, 0.052*inch], # 25mm window
  '2-044':[3.739*inch, 0.125*inch, 0.052*inch], # from first He3 design
  '2-046':[4.223*inch, 0.086*inch, 0.052*inch], # from ENG sumitomo design
  '2-154':[3.737*inch, 0.125*inch, 0.074*inch], # pg98 Parker O-ring (for groove width, depth)
  '2-163':[5.987*inch, 0.125*inch, 0.074*inch], # pg98 Parker O-ring 
  '2-254':[5.484*inch, 0.164*inch, 0.101*inch], # pg98 Parker O-ring 
  '2-258':[5.984*inch, 0.164*inch, 0.101*inch], # pg98 Parker O-ring 
}

def oring_orig(name):
  d = oring_list[name]
  inner=d[0]
  width=d[1]
  depth=d[2]
  return (cq.Workplane("XY")
          .circle(inner/2.0+width).circle(inner/2.0)
          .extrude(-depth)
          )
  # p = Part.makeCylinder(inner/2.0+width, depth)
  # hole = Part.makeCylinder(inner/2.0,depth)
  # p = p.cut(hole)
  # return p 


def oring(name, s):
    [inner, width, depth] = oring_list[name]
    return (s.circle(inner/2.0+width).circle(inner/2.0)
            .cutBlind(-depth)
            )
if (__name__=='temp'):
    box = cq.Workplane("XY").box(50,50,10)
    box = (box.faces(">Z")
           .workplane()
           )
    box = oring('2-019', box)
    show_object(box)
