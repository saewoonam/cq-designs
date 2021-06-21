const { SVG, G, Circle, Rect, Line, registerWindow, Polygon, Text } = require('@svgdotjs/svg.js')
const inch = 25.4;
const {tap_list} = require('./screws.js')

bulkheads = {
    // name: [pcd, counterbore diameter, bore diamter, number_of_screws]
    'nw50':[3.25 * inch, 2.06 * 25.4, 1.97 * 25.4, 8],
    'nw40':[2.44 * inch, 41.2, 1.53 * 25.4, 6],
    'nw25':[1.89 * inch, 26.2,0.98 * 25.4, 6],  // 1.89" and 26.2 from Ancorp catalog
    }

oring_list = {
  '2-019':[0.813*inch, 0.084*inch, 0.052*inch], //# 25mm window
  '2-044':[3.739*inch, 0.125*inch, 0.052*inch], //# from first He3 design
  '2-046':[4.223*inch, 0.086*inch, 0.052*inch], //# from ENG sumitomo design
  '2-154':[3.737*inch, 0.125*inch, 0.074*inch], //# pg98 Parker O-ring (for groove width, depth)
  '2-163':[5.987*inch, 0.125*inch, 0.074*inch], //# pg98 Parker O-ring 
  '2-254':[5.484*inch, 0.164*inch, 0.101*inch], //# pg98 Parker O-ring 
  '2-258':[5.984*inch, 0.164*inch, 0.101*inch], //# pg98 Parker O-ring 
}

function oring(name, s) {
    [inner, width, depth] = oring_list[name]
    let g = new G()
    let c;
    c = new Circle().radius(inner/2.0 + width).fill('none').stroke({color:'black', width:0.1})
    c.addTo(g)
    c = new Circle().radius(inner/2.0).fill('none').stroke({color:'black', width:0.1})
    c.addTo(g)
    return g
}

function bc(pcd, hole_diameter, N, offset=0, className='') {
    offset = offset * Math.PI / 180;
    g = new G()
    for (i=0; i<N; i++) {
        let c = new Circle().radius(hole_diameter/2).fill('none').stroke({color:'black',width:0.1})
        if (className.length>0) c.addClass(className)
        let theta = 2*i*Math.PI / N + offset;
        c.translate( pcd/2 * Math.cos(theta), pcd/2 * Math.sin(theta))
        c.addTo(g)
    }
    return g
}

exports.nw_bulkhead = (bh, offset=0) => {
    let [pcd, cbd, d, n] = bulkheads[bh];
    let g = bc(pcd, tap_list['10-32'], n, offset=offset, className='10-32')
    let cutout;
    cutout = new Circle().radius(cbd/2).fill('none').stroke({color:'black', width:0.1})
    cutout.addTo(g)
    cutout = new Circle().radius(d/2).fill('none').stroke({ color: 'black', width: 0.1 })
    cutout.addTo(g)
    return g
}

exports.polygon = (N, radius) => {
    let point_list = []
    for (i=0; i<N; i++) {
        theta = i * 2 * Math.PI / N;
        x = radius * Math.cos(theta)
        y = radius * Math.sin(theta)
        point_list.push([x,y])
    }
    let p = new Polygon().fill('none').stroke({color: 'black', width: 0.1})
    p.plot(point_list)
    return p
}

exports.build_legend = (canvas, legend_info) => {
    var idx = 0;
    var g = new G()
    var class_list = Object.keys(legend_info); //['npt', 'q-20', 'M5', 'M4', '4-40', '4-40b']
    for (const item of class_list) {
        var list = canvas.find('.'+item)
        if (list.length>0) {
            list.fill(Tol_bright[idx])
            console.log(idx, item, list.length, Tol_bright[idx])
            var text;
            // let x = WIDTH/4;
            // let y = WIDTH/4 +  18 * idx;
            let x = 0;
            let y = 18 * idx;
            hole = new Circle().radius(tap_list[legend_info[item][0]]/2).fill('none')
            hole.stroke({width:0.1, color:'black'})
            hole.fill(Tol_bright[idx])
            hole.translate(x,y)
            hole.addTo(g)
            text = new Text()
            text.font({
                family:   'Helvetica'
                , size:     10
                , anchor:   'left'
                , leading:  '1.5em'
            })
            text.attr({'alignment-baseline':"middle"})
            text.plain(''+list.length)
            text.translate(x+20,y)
            text.addTo(g)
            text = new Text()
            text.font({
                family:   'Helvetica'
                , size:     10
                , anchor:   'left'
                , leading:  '1.5em'
            })
            text.attr({'alignment-baseline':"middle"})
            text.plain(legend_info[item][1])
            text.translate(x+50,y)
            text.addTo(g)
            idx++;
        }
    }
    return g
}
// From Paul Tol: https://personal.sron.nl/~pault/
const Tol_bright = ['#EE6677', '#228833', '#4477AA', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']
exports.Tol_bright = Tol_bright
exports.Tol_muted = ['#88CCEE', '#44AA99', '#117733', '#332288', '#DDCC77', '#999933','#CC6677', '#882255', '#AA4499', '#DDDDDD']

exports.Tol_light = ['#BBCC33', '#AAAA00', '#77AADD', '#EE8866', '#EEDD88', '#FFAABB', '#99DDFF', '#44BB99', '#DDDDDD']

// #From Color Universal Design (CUD): https://jfly.uni-koeln.de/color/
exports.Okabe_Ito = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"]
// http://mkweb.bcgsc.ca/colorblind/
exports.mkweb = ["#000000", "#2272B2", "#3DB7E9", "#F748A5", "#359B73", "#D55E00", "#e69f00", "#f0e442"]

exports.bulkheads = bulkheads;
exports.bc = bc;
exports.oring = oring;
