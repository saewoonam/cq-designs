// returns a window with a document and an svg root node
const { createSVGWindow } = require('svgdom')
const window = createSVGWindow() //Create  virtual Window and document
const document = window.document // shorten window.document ot document
const { SVG, G, Circle, Rect, Line, registerWindow, Polygon, Text } = require('@svgdotjs/svg.js') //load functions from svg.js
const fs = require('fs') //include library to read/write files
const { tap_list } = require('./screws.js') //picks out particular tap_list form screws.js
const { collar_parameters } = require('./collar_parameters.js')
const { bc, nw_bulkhead, bulkheads, polygon, oring, mkweb, Tol_bright, build_legend } = require('./utils.js');

// register window and document
registerWindow(window, document)
const WIDTH = 500;
const HEIGHT = WIDTH;
const inch = 25.4;

const PT405_BO = {
    'diameter': 7*inch,
    'tube_wall': 1 / 16.0 * inch,
    'cryomech_offset': [80, 0],
}

// create canvas
const canvas = SVG(document.documentElement).size("1500", "750")
canvas.viewbox(-WIDTH / 2, -HEIGHT / 2, 2 * WIDTH, HEIGHT)
axes = new G()
let xaxis = new Line(); //Draws Axis through center
xaxis.plot(-WIDTH / 2, 0, WIDTH / 2, 0).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
xaxis.addTo(axes)
let yaxis = new Line();
yaxis.plot(0, -HEIGHT / 2, 0, HEIGHT / 2).stroke({ color: 'grey', opacity: 0.6, width: 0.1 })
yaxis.addTo(axes)
axes.addTo(canvas)

//create circle
let hole
hole = new Circle().radius(PT405_BO['diameter'] / 2).stroke({ width: 0.1, color: 'black' }).fill('none')
hole.addTo(canvas)

//Create M6 Holes
let M6
M6 = bc(6.5 * inch, tap_list['M6'], 6, offset = 0, className = 'M6')
M6.addTo(canvas)

legend_info = {
    'M6': ['M6', 'M6 Clearance Hole'],
}
var legend = build_legend(canvas, legend_info)
legend.translate(WIDTH / 4, HEIGHT / 4)
legend.addTo(canvas)

fs.writeFile('./PT405_Block_Off.svg', canvas.svg(), (err) => {
    if (err) throw err;
    console.log('The file has been saved!');
})