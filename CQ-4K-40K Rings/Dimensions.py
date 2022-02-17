inch = 25.4


class Dimensions:
    plate4K = {}
    plate4K['thickness'] = 0.5*inch
    plate4K['zoffset'] = -333.985
    # dr_offset = Vector(35, 0, 0)
    dr_offset = (35, 0)
    # dr_center = Vector(35, 0, plate4K['zoffset']-plate4K['thickness']+6)
    plate40Kdiameter = 290
    plate4Kdiameter = 260
    plate40K = {}
    plate40K['thickness'] = 0.5*inch
    plate40K['zoffset'] = -145.974
    plate40K['diameter'] = plate40Kdiameter
    # cryomech_offset = Vector(-80, 0, 0)
    cryomech_offset = (-80, 0)
    tube_wall = 1/16*inch

