import numpy as np

inch = 25.4

thru_4_40 = 0.125 * inch
#tap_4_40 = 0.089 * inch
cbor_4_40 = 7/32. * inch
cbor_depth = 0.112 * inch

tap_list = {
  '0-80':0.0469*inch,
  '2-56':0.07*inch,
  '4-40':0.089*inch,
  '6-32':0.1065*inch,
  '8-32':0.1360*inch,
  '10-24':0.1495*inch,
  '10-32':0.159*inch,
  '1/4-20':0.201*inch,
  '1/4-npt':27.0/64.0*inch,
  'M2':1.60,
  'M2.5':2.05,
  'M3':2.5,
  'M4':3.3,
  'M5':4.2,
  'M6':5,
  'M8-1':7.0,
  'M8-1.25':6.8,
  'M10-1.5':8.5,
  'M10-1.25':8.8,
} 
tap_count={}
def reset_tap_count():
  global tap_count
  for tap in tap_list:
    tap_count[tap]=0
def print_tap_count(msg=''):
  global tap_count
  print('Tap list %s'%msg)
  for tap in tap_count:
    if tap_count[tap]>0:
      print('\t',tap,': %d'%tap_count[tap])
reset_tap_count()
thru_count={}
def reset_thru_count():
  global thru_count
  for tap in tap_list:
    thru_count[tap]=0
def print_thru_count(msg=''):
  global thru_count
  print("Thru list %s"%msg)
  for tap in thru_count:
    if thru_count[tap]>0:
      print('\t',tap,': %d'%thru_count[tap])
reset_thru_count()
# metric https://littlemachineshop.com/images/gallery/PDF/TapDrillSizes.pdf
close_list = {
  '0-80':0.0635*inch,
  '2-56':0.089*inch,
  '4-40':0.116*inch,
  '6-32':0.1440*inch,
  '8-32':0.1695*inch,
  '10-24':0.196*inch,
  '10-32':0.196*inch,
  '1/4-20':0.257*inch,
  'M2':2.4,
  'M2.5':2.9,
  'M3':3.15,
  'M4':4.2,
  'M5':5.25,
  'M8-1.25':8.4,
  'M8-1': 8.4
}
free_list = {
  '0-80':0.07*inch,
  '2-56':0.096*inch,
  '4-40':0.1285*inch,
  '6-32':0.1495*inch,
  '8-32':0.1770*inch,
  '10-24':0.201*inch,
  '10-32':0.201*inch,
  '1/4-20':0.266*inch,
  'M2':2.4,
  'M2.5':2.9,
  'M3':3.3,
  'M4':4.4,
  'M5':5.5,
  'M6':6.6,
  'M8-1.25':8.8,
  'M8-1':8.8
}
#  http://www.carbidedepot.com/formulas-cb-metric.htm
cb_list = {
  '0-80':[0.125*inch, 0.07*inch, 0.074*inch],
  '2-56':[3.0/16.0*inch, 0.086*inch, 0.102*inch],
  '4-40':[7.0/32.0*inch, 0.112*inch, 0.13 *inch],
  '6-32':[9./32.*inch, 0.138*inch, 0.158*inch],
  '10-32':[3.0/8.0*inch, 0.190*inch, 0.218*inch],
  '1/4-20':[7.0/16.0*inch, 0.250*inch, 0.278*inch],
  'M2':[4.4, 2, 2.6],
  'M2.5':[5.4, 2.5, 3.1],
  'M3':[6.5, 3.0, 3.6],
  'M4':[8.25, 4.0, 4.7],
  'M5':[9.75, 5.0, 5.7],
  'M6':[11.2, 6.0, 6.8],
  'M8':[14.50, 8.0, 9.2],
}



def tap(kw,length, *args, **kwargs):
  r = tap_list[kw]/2
  tap_count[kw] = tap_count[kw]+1
  return (tap_list[kw], length)

def thru(kw,length, *args, **kwargs):
  """ makeCylinder(radius,height,[pnt,dir,angle])
  """
  r = free_list[kw]/2
  # part = Part.makeCylinder(r,length,*args,**kwargs)
  thru_count[kw] = thru_count[kw]+1
  return (free_list[kw], length)

def thru_close(kw,length, *args, **kwargs):
  r = close_list[kw]/2
  # part = Part.makeCylinder(r,length,*args,**kwargs)
  thru_count[kw] = thru_count[kw]+1
  return (close_list[kw], length)

def cb(kw,length, *args, **kwargs):  # counter bore
  r = free_list[kw]/2
  # part = Part.makeCylinder(r,length,*args,**kwargs)
  cb_dimensions = cb_list[kw]
  # cb_part = Part.makeCylinder(cb_dimensions[0]/2.0, cb_dimensions[1], *args, **kwargs)
  # part = part.fuse(cb_part)
  thru_count[kw] = thru_count[kw]+1
  return (free_list[kw], cb_dimensions[0], cb_dimensions[1], length)
"""
def boltcircle(bcd, size,depth, n, offset=0, hole_type='thru'):
  if hole_type=='thru':
      makehole = thru
  elif hole_type =='cb':
      makehole = cb
  else:
      makehole = tap

  hole = makehole(size,depth, Vector(bcd/2.0,0,0), Vector(0,0,1))
  holes = hole.copy()
  for i in range(1,n):
    hole = makehole(size,depth, Vector(bcd/2.0,0,0), Vector(0,0,1))
    hole.rotate(origin, zaxis, 360.0/n*i)
    holes = holes.fuse(hole) 
  holes.rotate(origin, zaxis, offset)
  return holes

origin = Base.Vector(0,0,0)
xaxis = Base.Vector(1,0,0)
zaxis = Base.Vector(0,0,1)
"""

