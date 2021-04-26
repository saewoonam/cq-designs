import cadquery as cq

import a
import b
# from a import c
import importlib
import collar
importlib.reload(collar)

result = a.box(cq)
result2 = b.box()
show_object(result)
show_object(result2)

show_object(collar.collar().rotate((0,0,0), (1,0,0), 180))
