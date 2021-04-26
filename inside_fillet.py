result = cq.Workplane("front").circle(2.0).rect(0.5, 0.75).extrude(0.5)
result = result.edges("|Z").fillet(0.1)

import collar
show_object(collar.s)