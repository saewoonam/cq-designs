shape= cq.importers.importStep('./734130050.stp')
bbox = shape.objects[0].BoundingBox()
shape = shape.translate((-bbox.xmax, -bbox.ymin, 0))
shape = shape.rotate((0,0,0), (0,1,0), 90)
bbox = shape.objects[0].BoundingBox()
shape = shape.translate((-(bbox.xmax+bbox.xmin)/2, 
                         -(bbox.ymin+bbox.ymax)/2,
                         0))
shape = shape.translate((0,0,-1.8))
show_object(shape)
cq.exporters.export(shape,'ssmcx_thru.step')