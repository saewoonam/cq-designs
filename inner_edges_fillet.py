import cadquery as cq

s = (cq.Workplane().box(20,20,1)
     .faces(">Z").workplane().tag("top")
     .center(5,0)
     .rect(2,2).cutBlind(-1)
     .workplaneFromTagged("top")
     .center(-5,0)
     .rect(2,2).cutBlind(-1)
     .edges("|Z")
     .edges("not (<X or >X or <Y or >Y)")
#     .edges(cq.selectors.NearestToPointSelector((0,0)))
     .fillet(0.5)
     )