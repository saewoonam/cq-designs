// returns a window with a document and an svg root node
const { createSVGWindow } = require('svgdom')
const window = createSVGWindow()
const document = window.document
const { SVG, G, Circle, Rect, Line, registerWindow, Polygon, Text } = require('@svgdotjs/svg.js')
const fs = require('fs')
const {tap_list} = require('./screws.js')
const {collar_parameters} = require('./collar_parameters.js')
const {bc, nw_bulkhead, bulkheads, polygon, oring, mkweb, Tol_bright, build_legend} = require('./utils.js');

// register window and document
registerWindow(window, document)
const WIDTH=500;
const HEIGHT = WIDTH;
const inch = 25.4;

const plate40K = {
    'diameter': 290,
    'tube_wall': 1/16.0 * inch,
    'cryomech_offset': [80, 0],
}
const plate4K = {
    'diameter': 260,
    'tube_wall': 1/16.0 * inch,
    'dr_offset': [35, 0],
    'cryomech_offset': [-80, 0],
}
// create canvas
const canvas = SVG(document.documentElement).size("1500", "750")
canvas.viewbox(-WIDTH/2, -HEIGHT/2, 2*WIDTH, HEIGHT)
axes = new G()
let xaxis = new Line();
xaxis.plot(-WIDTH/2,0,WIDTH/2,0).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
xaxis.addTo(axes)
let yaxis = new Line();
yaxis.plot(0, -HEIGHT/2,0,HEIGHT/2).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
yaxis.addTo(axes)
axes.addTo(canvas)

// bottom face

let c;
c = new Circle().radius(plate4K['diameter']/2).stroke({width: 0.1, color:'black'}).fill('none')

c.addTo(canvas)
let tube_offset = plate4K['tube_wall'] + 1;
c = new Circle().radius(plate4K['diameter']/2-tube_offset).stroke({width: 0.1, color:'black'}).fill('none')
c.addTo(canvas)

c = bc(3*inch, tap_list['M4'], 6, offset=0, className='M4')
c.translate(...plate4K['cryomech_offset'])
c.addTo(canvas)
// DR
c = new Circle().radius(86).stroke({width: 0.1, color:'black'}).fill('none')
c.translate(...plate4K['dr_offset'])
c.addTo(canvas)
c = new Circle().radius(75).stroke({width: 0.1, color:'black'}).fill('none')
c.translate(...plate4K['dr_offset'])
c.addTo(canvas)
c = bc(160, tap_list['M5'], 12, offset=0, className='M5')
c.translate(...plate4K['dr_offset'])
c.addTo(canvas)

// bottom looking

support_locations = [
    {'center':[0, -100], 'rot':0},
    {'center':[0, 100], 'rot':0},
    {'center':[0, 115], 'rot':45},
    {'center':[0, -115], 'rot':-45},
    {'center':[0, 125], 'rot':-90+22.5},
    {'center':[0, -125], 'rot':90-22.5},
]
support_holes = new G()
let hole
hole = new Circle().radius(tap_list['4-40']/2)
hole.stroke({width:0.1, color:'black'}).addClass('4-40')
hole.translate(-5/16*inch, 0)
hole.addTo(support_holes)
hole = new Circle().radius(tap_list['4-40']/2)
hole.stroke({width:0.1, color:'black'}).addClass('4-40')
hole.translate(+5/16*inch, 0)
hole.addTo(support_holes)
for (loc of support_locations) {
    holes = support_holes.clone()
    if (loc['rot']==0) holes.rotate(90,0,0)
    holes.translate(...loc['center'])
    g = new G()
    holes.addTo(g)
    g.rotate(loc['rot'], 0,0)
    g.addTo(canvas)
}

let feedthru = new G()
hole = new Circle().radius(tap_list['4-40']/2)
hole.stroke({width:0.1, color:'black'}).addClass('4-40')
hole.translate(-46.3/2, 0)
hole.addTo(feedthru)
hole = new Circle().radius(tap_list['4-40']/2)
hole.stroke({width:0.1, color:'black'}).addClass('4-40')
hole.translate(46.3/2, 0)
hole.addTo(feedthru)
let box = new Rect({width: 40, height:15}).translate(-20, -7.5).fill('none')
box.stroke({width:0.1, color:'black'})
box.addTo(feedthru)
var locations = []
for (let angle of [0, 45, 135, 180]) {
    cutout = feedthru.clone()
    cutout.translate(0, 100)
    g = new G()
    cutout.addTo(g)
    g.rotate(angle, 0,0)
    g.translate(...plate4K['dr_offset'])
    g.addTo(canvas)
}
// 4-40 blindtaps
g = new G();
let h = new Circle().radius(tap_list['4-40']/2)
h.stroke({width:0.1, color:'black'}).addClass('4-40b')
hole = h.clone()
hole.translate(120, 0)
hole.addTo(g)
for (i=0; i<4; i++) {
    hole = h.clone()
    hole.translate(120, (i+1)*0.5*inch)
    hole.addTo(g)
    hole = h.clone()
    hole.translate(120, -(i+1)*0.5*inch)
    hole.addTo(g)
}
gg = g.clone()
gg.rotate(135,0,0)
gg.translate(...plate4K['dr_offset'])
gg.addTo(canvas)
gg = g.clone()
gg.rotate(-135,0,0)
gg.translate(...plate4K['dr_offset'])
gg.addTo(canvas)
g = new G();
for (i=0; i<3; i++) {
    hole = h.clone()
    hole.translate(0, (i+1)*0.5*inch)
    hole.addTo(g)
    hole = h.clone()
    hole.translate(0, -(i+1)*0.5*inch)
    hole.addTo(g)
}
g.translate(...plate4K['cryomech_offset'])
g.addTo(canvas)
g = new G();
for (i=0; i<2; i++) {
    hole = h.clone()
    hole.translate((i+1)*0.5*inch, 0)
    hole.addTo(g)
    hole = h.clone()
    hole.translate( -(i+1)*0.5*inch, 0)
    hole.addTo(g)
}
g.translate(...plate4K['cryomech_offset'])
g.addTo(canvas)
hole = h.clone()
hole.translate(...plate4K['cryomech_offset'])
hole.addTo(canvas)
// fiber / vacuum ports
hole = new Circle().radius(tap_list['1/4-npt']/2).addClass('npt').fill('none')
hole.stroke({width:0.1, color:'black'})
locations = [ [80, 85], [80, -85] ]
for (let loc of locations) {
    h= hole.clone()
    h.translate(loc[0], loc[1])
    h.addTo(canvas)
}

hole = new Circle().radius(tap_list['1/4-20']/2).addClass('q-20').fill('none')
hole.stroke({width:0.1, color:'black'})
locations = [ [-63, 95], [-63, -95] ]
for (let loc of locations) {
    h= hole.clone()
    h.translate(loc[0], loc[1])
    h.addTo(canvas)
}
// color holes
/*
var list = canvas.find('.M10')
list.fill('#f06')
list = canvas.find('.4-40')
list.fill('blue')
list = canvas.find('.10-32')
list.fill('orange')
list = canvas.find('.M6')
list.fill('red')
list = canvas.find('.q-20')
list.fill('#FF00FF')
list = canvas.find('.npt')
list.fill('salmon')
list = canvas.find('.M4')
list.fill('pink')
*/
legend_info = {'npt': ['1/4-npt','tap thru 1/4 NPT, start tap from the other side'],
    'q-20': ['1/4-20', 'tap thru 1/4-20'],
    'M5': ['M5', 'tap thru M5'],
    'M4': ['M4', 'tap thru M4'],
    '4-40': ['4-40', 'tap thru 4-40'],
    '4-40b': ['4-40', 'blindtap 4-40'],
}
var legend = build_legend(canvas, legend_info)
legend.translate(WIDTH/4, HEIGHT/4)
legend.addTo(canvas)
fs.writeFile('./index.svg', canvas.svg(), (err) => {
  if (err) throw err;
  console.log('The file has been saved!');
})
