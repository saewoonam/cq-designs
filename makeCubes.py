def makeCubes(self,length):
    #self refers to the CQ or Workplane object

    #inner method that creates a cube
    def _singleCube(loc):
        #loc is a location in local coordinates
        #since we're using eachpoint with useLocalCoordinates=True
        print('loc',loc)
        return cq.Solid.makeBox(length,length,length).locate(loc)

    #use CQ utility method to iterate over the stack, call our
    #method, and convert to/from local coordinates.
    return self.eachpoint(_singleCube, True)

#link the plugin into CadQuery
cq.Workplane.makeCubes = makeCubes

#use the plugin
result = (cq.Workplane("XY").box(8.0,8., 8).faces("<Z")
          .workplane()
    .rect(4.0,4.0,forConstruction=True).vertices()
    .makeCubes(1.0).combineSolids())