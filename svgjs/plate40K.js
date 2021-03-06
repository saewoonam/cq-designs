// returns a window with a document and an svg root node
const { createSVGWindow } = require('svgdom')
const window = createSVGWindow()
const document = window.document
const { SVG, G, Circle, Rect, Line, registerWindow, Polygon, Symbol } = require('@svgdotjs/svg.js')
const fs = require('fs')
const {tap_list} = require('./screws.js')
const {collar_parameters} = require('./collar_parameters.js')
const {bc, nw_bulkhead, bulkheads, polygon, oring, build_legend} = require('./utils.js');

// register window and document
registerWindow(window, document)
const WIDTH=500;
const HEIGHT = WIDTH;
const inch = 25.4;

const plate40K = {
    'diameter': 290,
    'tube_wall': 1/16.0 * inch,
    'dr_offset': [-35, 0],
    'cryomech_offset': [80, 0],
}
const plate4K = {
    'diameter': 260,
    'tube_wall': 1/16.0 * inch,
    'dr_offset': [-35, 0],
    'cryomech_offset': [80, 0],
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
c = new Circle().radius(plate40K['diameter']/2).stroke({width: 0.1, color:'black'}).fill('none')
c.addTo(canvas)

let tube_offset = plate40K['tube_wall'] + 1;
c = new Circle().radius(plate40K['diameter']/2-tube_offset).stroke({width: 0.1, color:'black'}).fill('none')
c.addTo(canvas)

c = new Circle().radius(3.5*inch/2).stroke({width: 0.1, color:'black'}).fill('none')
c.translate(...plate40K['cryomech_offset'])
c.addTo(canvas)
c = bc(4.38*inch, tap_list['M5'], 6, offset=0, className='M5')
c.rotate(-10,0,0)
c.translate(...plate40K['cryomech_offset'])
c.addTo(canvas)

// bottom looking

support_locations = [
    {'center':[0, 100], 'rot':0},
    {'center':[0, -100], 'rot':0},
    {'center':[0, -115], 'rot':45},
    {'center':[0, 115], 'rot':-45},
    {'center':[0, -125], 'rot':-90+22.5},
    {'center':[0, 125], 'rot':90-22.5},
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
for (let angle of [0, 30, 150, 180]) {
    cutout = feedthru.clone()
    cutout.translate(0, 123)
    g = new G()
    cutout.addTo(g)
    g.rotate(angle, 0,0)
    g.addTo(canvas)
}

g = new G();
for (let i=0; i<4; i++) {
    for (let j=0; j<5; j++ ) {
        hole = new Circle().radius(tap_list['4-40']/2)
        hole.stroke({width:0.1, color:'black'}).addClass('4-40b')
        hole.translate( -(i-1)*inch, (j-2)*inch  )
        hole.addTo(g)
    }
}
g.translate(...plate40K['dr_offset'])
g.addTo(canvas)

hole = new Circle().radius(tap_list['1/4-npt']/2).addClass('npt').fill('none')
hole.stroke({width:0.1, color:'black'})
locations = [ [-85, 80], [-85, -80] ]
for (let loc of locations) {
    h= hole.clone()
    h.translate(loc[0], loc[1])
    h.addTo(canvas)
}

hole = new Circle().radius(tap_list['1/4-20']/2).addClass('q-20').fill('none')
hole.stroke({width:0.1, color:'black'})
locations = [ [63, 95], [63, -95] ]
for (let loc of locations) {
    h= hole.clone()
    h.translate(loc[0], loc[1])
    h.addTo(canvas)
}


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

fs.writeFile('./plate40K.svg', canvas.svg(), (err) => {
  if (err) throw err;
  console.log('The file has been saved!');
})
