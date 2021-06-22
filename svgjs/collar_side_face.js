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
const canvas = SVG(document.documentElement).size("750", "750")
canvas.viewbox(-WIDTH/2, -HEIGHT/2, WIDTH, HEIGHT)
axes = new G()
let xaxis = new Line();
xaxis.plot(-WIDTH/2,0,WIDTH/2,0).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
xaxis.addTo(axes)
let yaxis = new Line();
yaxis.plot(0, -HEIGHT/2,0,HEIGHT/2).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
yaxis.addTo(axes)
axes.addTo(canvas)

// bottom face

let face;
let w=collar_parameters['diameter']/2 * Math.sin(360/12/2*Math.PI / 180) * 2;
let T = 3.75*inch; 
face = new Rect().size(w, T).translate(-w/2, -T/2).fill('none')
face.stroke({width:0.1, color:'black'})
face.addTo(canvas)

let b = nw_bulkhead('nw50', offset=22.5)
b.addTo(canvas)

let holes = new G()
for (let x of [-1, 1]) {
    for (let y of [-1, 1]) {
        hole = new Circle().radius(tap_list['4-40']/2)
        hole.stroke({width:0.1, color:'black'}).addClass('4-40')
        hole.translate(x*0.5*3.5*inch, y*0.5*3*inch)
        // console.log(x, x*0.5*3.5*inch);
        hole.addTo(holes)
    }
}
holes.addTo(canvas)

var list = canvas.find('.M12')
list.fill('#f06')
list = canvas.find('.4-40')
list.fill('blue')
list = canvas.find('.10-32')
list.fill('orange')

legend_info = {'npt': ['1/4-npt','tap thru 1/4 NPT, start tap from the other side'],
    'q-20': ['1/4-20', 'tap thru 1/4-20'],
    'M5': ['M5', 'tap thru M5'],
    'M4': ['M4', 'tap thru M4'],
    '4-40': ['4-40', 'blindtap 4-40'],
    '10-32': ['10-32', 'blindtap 10-32'],
}
var legend = build_legend(canvas, legend_info)
legend.translate(-50, 70)
legend.addTo(canvas)

function makeLabel(content,x=0, y=0) {
    text = new Text()
    text.font({
        family:   'Helvetica'
        , size:     14
        , anchor:   'Left'
        , leading:  '1.5em'
    })
    text.attr({'alignment-baseline':"middle"})
    text.plain(content);
    text.translate(x,y);
    return text
}

let text;
text = makeLabel('Each side face of the collar (12x)');
text.translate(-100,-70)
text.addTo(canvas)
text = makeLabel('Total of 48 blindtap 4-40, 96 blindtap 10-32')
text.translate(-125,110)
text.addTo(canvas)

fs.writeFile('./collar_face.svg', canvas.svg(), (err) => {
  if (err) throw err;
  console.log('The file has been saved!');
})
