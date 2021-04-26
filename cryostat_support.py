import cadquery as cq
import series10

inch = 25.4
c = cq.importers.importStep('./outputs/collar.step')
show_object(c, options={'color':0})
rail = series10.series10(12*inch).translate((0,0,-6*inch))
rail = rail.rotate((0,0,0), (1,0,0), 90).translate((0,0,0.5*inch))
rail1 = rail.translate((185,0,0))
rail2 = rail.translate((-185,0,0))
show_object(rail1, options={'color':0x808080, 'alpha':0.95})
show_object(rail2, options={'color':0x808080, 'alpha':0.95})
