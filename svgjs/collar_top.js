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

// create canvas
const canvas = SVG(document.documentElement).size("750", "750")
canvas.viewbox(-WIDTH/2, -HEIGHT/2, 1.1*WIDTH, HEIGHT)
axes = new G()
let xaxis = new Line();
xaxis.plot(-WIDTH/2,0,WIDTH/2,0).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
xaxis.addTo(axes)
let yaxis = new Line();
yaxis.plot(0, -HEIGHT/2,0,HEIGHT/2).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
yaxis.addTo(axes)
// axes.addTo(canvas)

// bottom face

p = polygon(12, collar_parameters['diameter']/2)
p.rotate(180/12)
p.addTo(canvas)
bc1 = bc(collar_parameters['diameter']-30, tap_list['M12-1.75'], 12, offset=0, className='M12')
bc1.rotate(180/12)
// bc1.addTo(canvas)

let c;
// ISO320
/*
c = new Circle().radius(155.816).stroke({width: 0.1, color:'black'}).fill('none')
c.addTo(canvas)
c = new Circle().radius(159.004).stroke({width: 0.1, color:'black'}).fill('none')
c.addTo(canvas)
*/
c = new Circle().radius(5*inch/2).stroke({width: 0.1, color:'black'}).fill('none')
c.translate(-80, 0)
c.addTo(canvas)
// bottom looking
/*
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
//support_holes.addTo(canvas)
for (let loc of support_locations) {
    holes = support_holes.clone()
    holes.translate(...loc['center'])
    g = new G()
    holes.addTo(g)
    g.rotate(loc['rot'], 0,0)
    g.addTo(canvas)
}
*/
for (let i=0; i<5; i++) {
    let c, g;
    c = nw_bulkhead('nw40')
    g = new G()
    c.fill('none').stroke({color:'black', width: 0.1})
    c.translate(0,-125)
    c.addTo(g)
    g.rotate(i*45, 0, 0)
    g.addTo(canvas)
}
c = nw_bulkhead('nw25')
c.translate(-75, 120)
c.addTo(canvas)
c = nw_bulkhead('nw25')
c.translate(-75, -120)
c.addTo(canvas)

c = bc(6.5*inch, tap_list['M6'], 6, offset=0, className='M6')
c.translate(-80, 0)
c.addTo(canvas)

c = oring('2-254')
c.translate(-80, 0)
c.addTo(canvas)

hole = new Circle().radius(tap_list['1/4-20']/2).addClass('q-20').fill('none')
hole.stroke({width:0.1, color:'black'})

h = hole.clone()
h.translate(5*inch, 5*inch)
h.addTo(canvas)
h = hole.clone()
h.translate(-5*inch, 5*inch)
h.addTo(canvas)
h = hole.clone()
h.translate(-5*inch, -5*inch)
h.addTo(canvas)
h = hole.clone()
h.translate(5*inch, -5*inch)
h.addTo(canvas)
var locations = []
for (let x of [185, -185]) {
    for (let y of [-2*inch, 0, 2*inch]) {
        locations.push([x,y])
        locations.push([y,x])
    }
}
for (let y of [-40, 40]) {
    for (let x of [85, 165]) {
        locations.push([x,y])
    }
}
for (let loc of locations) {
    h= hole.clone()
    h.translate(loc[0], loc[1])
    h.addTo(canvas)
}

var list = canvas.find('.M12')
list.fill('#f06')
list = canvas.find('.4-40')
list.fill('blue')
list = canvas.find('.10-32')
list.fill('orange')
list = canvas.find('.M6')
list.fill('red')
list = canvas.find('.q-20')
console.log('list',list)
list.fill('#FF00FF')
console.log(canvas.svg())

legend_info = {'M12': ['M12-1.75','blindtap M12-1.75'],
    '4-40': ['4-40', 'blindtap 4-40'],
    '10-32': ['10-32', 'blindtap 10-32'],
    'M6': ['M5', 'blindtap M6'],
    'q-20': ['1/4-20', 'blindtap 1/4-20'],
}
var legend = build_legend(canvas, legend_info)
legend.translate(WIDTH/3.5, HEIGHT/3)
legend.addTo(canvas)


fs.writeFile('./index.html', canvas.svg(), (err) => {
  if (err) throw err;
  console.log('The file has been saved!');
})
