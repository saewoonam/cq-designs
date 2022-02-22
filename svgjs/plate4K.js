// returns a window with a document and an svg root node
const { createSVGWindow } = require('svgdom')
const window = createSVGWindow() //Create  virtual Window and document
const document = window.document // shorten window.document ot document
const { SVG, G, Circle, Rect, Line, registerWindow, Polygon, Text, move } = require('@svgdotjs/svg.js') //load functions from svg.js
const fs = require('fs') //include library to read/write files
const { tap_list } = require('./screws.js') //picks out particular tap_list form screws.js
const {collar_parameters} = require('./collar_parameters.js')
const { bc, nw_bulkhead, bulkheads, polygon, oring, mkweb, Tol_bright, build_legend} = require('./utils.js');

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
let xaxis = new Line(); //Draws Axis through center
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
locations = [ [85, 80], [85, -80] ]
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

//Add  2-56 Radial Holes to Legend
hole = new Circle().radius(tap_list['2-56'] / 2).addClass('2-56').fill('none')
locations = [[WIDTH / 4, HEIGHT / 4 + 108], [WIDTH / 4, HEIGHT / 4 + 108], [WIDTH / 4, HEIGHT / 4 + 108], [WIDTH / 4, HEIGHT / 4 + 108],
            [WIDTH / 4, HEIGHT / 4 + 108], [WIDTH / 4, HEIGHT / 4 + 108], [WIDTH / 4, HEIGHT / 4 + 108], [WIDTH / 4, HEIGHT / 4 + 108]]
for (let loc of locations) {
    h = hole.clone()
    h.translate(loc[0], loc[1])
    h.addTo(canvas)
}

text = new Text()
text.plain('2-56 Blind Tap - 7.4mm Depth')
text.font({
    family: 'Helvetica'
    , size: 10
})
text.addTo(canvas)
text.translate(190, 3)
text.rotate(0, 0)

var star = SVG().polygon('50,0 60,20 55,20 55,50 45,50 45,20 40,20')
locations = [ {'pos': [-110, -25], 'rot': [90] },
    { 'pos': [-50, 130], 'rot': 0 }, { 'pos': [-50, -210], 'rot': 180 }
]

locations = [
    { 'center': [110, -25], 'rot': -90},
    { 'center': [-210, -25], 'rot': 90 },
    { 'center': [-50, 137], 'rot': 0 },
    { 'center': [-50, -187], 'rot': 180 },
    { 'center': [70, -137], 'rot': -135 },
    { 'center': [-167, -137], 'rot': 135 },
    { 'center': [-157, 97], 'rot': 45 },
    { 'center': [57, 97], 'rot': -45 },
]

star.fill('#BBBBBB')
for (let loc of locations) {
    h = star.clone()
    h.translate(...loc['center'])
    h.rotate(loc['rot'])
    h.addTo(canvas)
    }



legend_info = {
    'npt': ['1/4-npt', 'Tap thru 1/4 NPT, start tap from the other side'],
    'q-20': ['1/4-20', 'Tap thru 1/4-20'],
    'M5': ['M5', 'Tap thru M5'],
    'M4': ['M4', 'M4 Clearance Hole'],
    '4-40': ['4-40', 'Tap thru 4-40'],
    '4-40b': ['4-40', 'Blind Tap 4-40'],
    '2-56': ['2-56', 'Radial Holes 2-56 Blind Tap - 7.4mm Depth']
}
var legend = build_legend(canvas, legend_info)
legend.translate(200, 100)
legend.addTo(canvas)    
  

fs.writeFile('./plate4K.svg', canvas.svg(), (err) => {
    if (err) throw err;
    console.log('The file has been saved!');
})
