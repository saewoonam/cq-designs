import cadquery as cq

T = 50
wall = 6
diameter = 200
sides = 8
center_hole_dia = 160;

s = cq.Workplane("XY").box(10, 10,10)
def makeCubes(self,length):
    #self refers to the CQ or Workplane object

    #inner method that creates a cube
    def _singleCube(loc):
        #loc is a location in local coordinates
        #since we're using eachpoint with useLocalCoordinates=True
        return cq.Solid.makeBox(length,length,length).locate(loc)

    #use CQ utility method to iterate over the stack, call our
    #method, and convert to/from local coordinates.
    return self.eachpoint(_singleCube,True)
#link the plugin into CadQuery
cq.Workplane.makeCubes = makeCubes


def add_bumps(s):
    return (s.faces('<Z').workplane()
     .rect(4.0,4.0,forConstruction=True)
     .vertices().makeCubes(1).combineSolids()
     )
s = add_bumps(s)
"""
def side2(f):
    diameter = 6
    depth = 10
    boreDir = -f.normalAt()
    center = f.Center()
    print('center', center)
    # center = cq.Vector(10,0,0)
    # first make the hole
    hole = cq.Solid.makeCylinder(
        diameter / 2.0, depth, center, boreDir
    )  # local coordianates!
    return hole

def side(f):
    cut = cq.Solid.makeCylinder(15,20, f.Center(),-f.normalAt())
    return cut

s = (s.faces('#Z')
     .each(side2, True)
#     .each(lambda f: cq.Solid.makeCylinder(15,20, f.Center(),-f.normalAt()))
     )
s = s.end().cut(s)
"""
show_object(s)
# show_object(s.end().cut(s))