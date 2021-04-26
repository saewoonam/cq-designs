import cadquery as cq
from screws import tap
inch = 25.4;
import uuid

bulkheads = {
    # name: [pcd, counterbore diameter, bore diamter, number_of_screws]
    'nw50':[3.25 * inch, 2.06 * 25.4, 1.97 * 25.4, 8],
    'nw40':[2.44 * inch, 41.2, 1.53 * 25.4, 6],
    'nw25':[1.89 * inch, 26.2,0.98 * 25.4, 6],  # 1.89" and 26.2 from Ancorp catalog
    }

def nw_bulkhead(s, name, depth, offset=0):
    tagname = name+'_'+uuid.uuid4().hex
    [pcd, cbore, bore, n] = bulkheads[name]
    s = (s.tag(f'{tagname}')
         .cboreHole(bore, cbore, .105*25.4, depth)
         .workplaneFromTagged(f"{tagname}")
         .transformed(rotate=(0,0,180/n*offset))
         .polygon(n, pcd, forConstruction=True)
         # .polygon_offset(8,3.25*inch,offset=0,forConstruction=True)
         .vertices().hole(*tap('10-32', 3.0*inch/8.0))
        )
    return s

if (__name__=='temp'):
    name = 'nw50'
    s = (cq.Workplane("XY").box(150, 150, 150)
         .faces(">Z")
         .workplane()
         )
    s = nw_bulkhead(s, 'nw50', 20, offset=True)
