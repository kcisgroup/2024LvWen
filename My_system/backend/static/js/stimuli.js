// var width = window.innerWidth
// var height = window.innerHeight
//
// var stage_stimuli = new Konva.Stage({
//     container: 'container',
//     width: width,
//     height: height,
// });
//
// var layer_stimuli = new Konva.Layer()
// stage_stimuli.add(layer_stimuli)
//
// // 屏幕长 59.77 厘米,屏幕宽 33.62 厘米,屏幕面积 2009.4674 平方厘米  2560*1440
// // 观察距离70cm 屏幕宽像素*图片宽/屏幕宽=图片像素
// let distToscreen=70
// let widthcm = Math.tan(1.53 * Math.PI / 180/2) * distToscreen * 2
// let widthpx = 2560/59.77*widthcm
// console.log( widthcm,widthpx)

// //S
// function S_generate() {
//     var blob = new Konva.Line({
//         points: [460, 30, 420, 20, 400,28,380, 50, 420, 65, 450, 80, 430, 90, 385, 70,
//             380, 75, 420, 100, 460, 80, 435,60,420, 55, 395, 45, 415, 32, 455, 38],
//         fill: "black",
//         closed: true,
//         tension: 0.4,
//     });
//     return blob;
// }
//
// var blob = S_generate();
// layer_stimuli.add(blob);


//十字，与空心是拓扑变化
function Cross(x, y, color) {
    let crosses = 40;
    let group = new Konva.Group();
    let line1 = new Konva.Line({
        points: [x - crosses, y , x + crosses, y ],
        stroke: color,
        strokeWidth: 28,
    });
    let line2 = new Konva.Line({
        points: [x , y + crosses, x , y - crosses],
        stroke: color,
        strokeWidth: 28,
    });
    group.add(line1);
    group.add(line2);
    return group;
}

//双孔
//1方，2圆
function DoubleHoles(style, x, y, color,rotion) {
    let Outer, circle1, circle2,size
    let group = new Konva.Group()
    if (style === "rect") {//方形
        Outer = new Konva.Rect({
            x: x - 40,
            y: y - 40,
            width: 80,
            height: 80,
            fill: color,
        });
        circle1 = new Konva.Circle({
            x: x - 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
        circle2 = new Konva.Circle({
            x: x + 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
    }
    if (style === "ring") { //圆形
        Outer = new Konva.Circle({
            x: x,
            y: y,
            radius: 40,
            fill: color,
        });
        circle1 = new Konva.Circle({
            x: x - 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
        circle2 = new Konva.Circle({
            x: x + 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
    }
    if (style === "triangle") {
        Outer = new Konva.RegularPolygon({
            x: x ,
            y: y +12,
            sides: 3,
            radius: 90/Math.sqrt(3),
            fill: color,
        });
        circle1 = new Konva.Circle({
            x: x,
            y: y+12,
            radius: 19.5,
            fill: "#c8c8c8",
        });
        circle2 = new Konva.Ring({
            x: x,
            y: y+12,
            innerRadius: 14,
            outerRadius: 8,
            fill: color,
        });
    }
    if (style === "star") {
        Outer = new Konva.Star({
            x: x,
            y: y,
            numPoints: 5,
            innerRadius: 20,
            outerRadius: 40 / Math.cos( Math.PI/5),
            fill: color,
        });
        circle1 = new Konva.Circle({
            x: x,
            y: y,
            radius: 16,
            fill: "#c8c8c8",
        });
        circle2 = new Konva.Ring({
            x: x,
            y: y,
            innerRadius: 12,
            outerRadius: 7,
            fill: color,
        });
    }
    if (style === "diamond") {
        Outer = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 4,
            radius: 50,
            fill: color,
        });
        circle1 = new Konva.Circle({
            x: x - 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
        circle2 = new Konva.Circle({
            x: x + 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
    }
    if (style === "hexagram") {
        Outer = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 6,
            Radius: 80/Math.sqrt(3),
            fill: color,
        });
       Outer.rotate(30)
        circle1 = new Konva.Circle({
            x: x - 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
        circle2 = new Konva.Circle({
            x: x + 20,
            y: y,
            radius: 13,
            fill: "#c8c8c8",
        });
    }
    group.add(Outer);
    group.add(circle1);
    group.add(circle2);
    return group;
}

// var DoubleRing = DoubleHoles("triangle", 50, 60,"black")
// var DoubleRing1 = DoubleHoles("diamond", 150, 60,"black")
// layer_stimuli.add(DoubleRing)
//
// layer_stimuli.add(DoubleRing1)
// var DoubleRing2 = DoubleHoles("rect", 250, 60,"black")
// layer_stimuli.add(DoubleRing2)
// var DoubleRing3 = DoubleHoles("ring", 350, 60,"black")
// layer_stimuli.add(DoubleRing3)
// var DoubleRing4 = DoubleHoles("hexagram", 450, 60,"black")
// layer_stimuli.add(DoubleRing4)
// var DoubleRing5 = DoubleHoles("pentagon", 550, 60,"black")
// layer_stimuli.add(DoubleRing5)
// console.log(DoubleRing5.getSize())
//单孔
function SingleHole(style, x, y, color, rotation) {
    let hollow = new Konva.Group();
    if (style === "diamond") {
        hollow = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 4,
            radius: 38,
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 18,
        });
    }
    if (style==="trapezoid"){
        hollow = new Konva.Shape({
			x: x,
			y: y,
			sceneFunc: function(context) {
				context.beginPath();
				context.moveTo(-40, -26);
				context.lineTo(40, -26);
				context.lineTo(22, 26);
				context.lineTo(-22, 26);
				context.closePath();
				context.fillStrokeShape(this);
			},
			fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 18,
		});
    }
    if (style === "triangle") {
        hollow = new Konva.RegularPolygon({
            x: x,
            y: y + 12,
            sides: 3,
            radius: 90/Math.sqrt(3)-13,
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 15,
        });
    }
    if (style === "ring") {
        hollow = new Konva.Ring({
            x: x,
            y: y,
            innerRadius: 24,
            outerRadius: 40,
            fill: color,
        });
    }
    if (style === "rect") {
        hollow = new Konva.Rect({
            x: x - 30,
            y: y - 30,
            width: 64,
            height: 64,
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 16,
        });
    }
    if (style === "pentagon") {
        hollow = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 5,
            Radius: 43/Math.sin(72 / 180 * Math.PI)-9,
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 15,
        });
    }
    if (style === "hexagram") {
        hollow = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 6,
            Radius: 32*2/Math.sqrt(3),
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 16,
        });
        hollow.rotate(30)
    }
    if (style === "star") {
        hollow = new Konva.Star({
            x: x,
            y: y,
            numPoints: 5,
            innerRadius: 15,
            outerRadius: 80/Math.sqrt(3)-10,
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 11,
        });
    }

    if (color === "shadow") {
        hollow = Drawshadow(x, y, style, rotation)
        if (style === "rect") {
            var rect1 = new Konva.Rect({
                x: x - 20,
                y: y - 20,
                width: 40,
                height: 40,
                fill: "#c8c8c8",
                stroke: "black",
                strokeWidth: 3,
            });
            hollow.add(rect1)
        }
        if (style === "circle") {
            var circle1 = new Konva.Circle({
                x: x,
                y: y,
                Radius: 20,
                fill: "#c8c8c8",
            });
            hollow.add(circle1)
        }
    }
    return hollow;
}

// var hexagon_hollow = SingleHole("hexagram", 240, 60,"red")
//
// console.log(hexagon_hollow.getSize())
// var ring = SingleHole("ring", 150, 60,"red")
//
// console.log(ring.getSize())
// var rect_hollow = SingleHole("star", 900, 60,"red")
// layer_stimuli.add(rect_hollow)
// console.log(rect_hollow.getSize())
// var rect_hollow = SingleHole("triangle", 800, 60,"black")
// layer_stimuli.add(rect_hollow)
// console.log(rect_hollow.getSize())
// var rect_hollow = SingleHole("rect", 700, 60,"black")
// layer_stimuli.add(rect_hollow)
// console.log(rect_hollow.getSize())



//无孔
function NoHole(style, x, y, color, rotation) {
    let solid,size
    if(rotation===0) size=1
    else if(rotation===1) size=0.8
    else size=1.2
    if (style === "triangle") {
        solid = new Konva.RegularPolygon({
            x: x ,
            y: y +12,
            sides: 3,
            radius: 90*size/Math.sqrt(3),
            fill: color,
        });
    }
    if (style === "rect") {
        solid = new Konva.Rect({
            x: x - 40,
            y: y - 40,
            width: 80*size,
            height: 80*size,
            fill: color,
        });
    }
    if (style === "circle") {
        solid = new Konva.Circle({
            x: x,
            y: y,
            radius: 40*size,
            fill: color,
        });
    }
    if (style === "diamond") {
        solid = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 4,
            radius: 50*size,
            fill: color,
        });
    }
    if (style==="trapezoid"){
        solid = new Konva.Shape({
			x: x,
			y: y,
			sceneFunc: function(context) {
				context.beginPath();
				context.moveTo(-48, -35);
				context.lineTo(48, -35);
				context.lineTo(30, 35);
				context.lineTo(-30, 35);
				context.closePath();
				context.fillStrokeShape(this);
			},
			fill: color,
		});
    }
    if (style === "pentagon") {
        solid = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 5,
            Radius: 43/Math.sin(72 / 180 * Math.PI),
            fill: color,
        });
    }
     if (style === "hexagram") {
        solid = new Konva.RegularPolygon({
            x: x,
            y: y,
            sides: 6,
            Radius: 80*size/Math.sqrt(3),
            fill: color,
        });
       solid.rotate(30)
    }
     if (style === "star") {
        solid = new Konva.Star({
            x: x,
            y: y,
            numPoints: 5,
            innerRadius: 20*size,
            outerRadius: 40*size / Math.cos( Math.PI/5),
            fill: color,
        });
    }

    if (style === "cross") {
        return Cross(x, y,color);
    }
    if (color === "shadow") {
        solid = Drawshadow(x, y, style, rotation)
    }
    return solid;
}


// var hexagon_solid = NoHole("hexagram", 240, 60,"black")
// console.log(hexagon_solid.getSize())
//
// var rect_solid = NoHole("rect", 60, 60,"red")
// console.log(rect_solid.getHeight())
// layer_stimuli.add(rect_solid)
// layer_stimuli.add(hexagon_solid)
// layer_stimuli.add(hexagon_hollow)
// var circle = NoHole("circle", 150, 60,"black")
// layer_stimuli.add(circle)
// layer_stimuli.add(ring)

var line = NoHole("triangle", 40, 60,"red")
console.log(line.getSize())
// layer_stimuli.add(line)
var star = NoHole("pentagon", 1000, 60,"black")
console.log(star.getSize())
// layer_stimuli.add(star)


//6、9
function SixOrNine(style, x, y, color) {
    let line1, line2, rect;
    if (style === 1) { //6
        rect = new Konva.Rect({
            x: x - 24,
            y: y,
            width: 50,
            height: 44,
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 8,
        });
        line1 = new Konva.Line({
            points: [x - 24, y - 4, x - 24, y - 40],
            stroke: color,
            strokeWidth: 8,
        });
        line2 = new Konva.Line({
            points: [x - 28, y - 40, x + 30, y - 40],
            stroke: color,
            strokeWidth: 8,
        });
    }
    if (style === 2) { //9
        rect = new Konva.Rect({
            x: x - 24,
            y: y - 40,
            width: 50,
            height: 44,
            fill: "#c8c8c8",
            stroke: color,
            strokeWidth: 8,
        });
        line1 = new Konva.Line({
            points: [x + 26, y + 4, x + 26, y + 44],
            stroke: color,
            strokeWidth: 8,
        });
        line2 = new Konva.Line({
            points: [x + 30, y + 44, x - 26, y + 44],
            stroke: color,
            strokeWidth: 8,
        });
    }
    return [rect, line1, line2];
}

// var Six = SixOrNine(1, 60, 160);
// var Nine = SixOrNine(2, 130, 160);
// layer_stimuli.add(Six[0]);
// layer_stimuli.add(Six[1]);
// layer_stimuli.add(Six[2]);
// layer_stimuli.add(Nine[0]);
// layer_stimuli.add(Nine[1]);
// layer_stimuli.add(Nine[2]);

function Drawshadow(x, y, style, rotation) {
    let group = new Konva.Group();
    if (style === "rect") {
        var rect1 = new Konva.Rect({
            x: x - 40,
            y: y - 40,
            width: 80,
            height: 80,
            stroke: 'black',
            strokeWidth: 3
        });
        group.add(rect1)
        if (rotation === 0) {
            for (let i = 0; i < rect1.width() / 10; i++) {
                // let line1 = new Konva.Line({
                //     points: [rect1.x() + i * 20, rect1.y(), rect1.x() + rect1.width(), rect1.y() + rect1.width() - i * 20],
                //     stroke: 'black',
                //     strokeWidth: 3
                // });
                 let line1 = new Konva.Line({
                    points: [rect1.x(), rect1.y()+ i * 10, rect1.x() + rect1.width(), rect1.y()  + i * 10],
                    stroke: 'black',
                    strokeWidth: 2
                });
                group.add(line1)
            }
            // for (let i = 1; i < rect1.width() / 20; i++) {
            //     let line2 = new Konva.Line({
            //         points: [rect1.x(), rect1.y() + i * 20, rect1.x() + rect1.width() - i * 20, rect1.y() + rect1.height()],
            //         stroke: 'black',
            //         strokeWidth: 3
            //     });
            //     group.add(line2)
            // }
        } else if (rotation === 1) {
            for (let i = 0; i < rect1.width() / 10; i++) {
                // let line1 = new Konva.Line({
                //     points: [rect1.x() + (i + 1) * 20, rect1.y(), rect1.x(), rect1.y() + (i + 1) * 20],
                //     stroke: 'black',
                //     strokeWidth: 3
                // });
                let line1 = new Konva.Line({
                    points: [rect1.x() + i * 10, rect1.y(), rect1.x()+ i * 10, rect1.y() + rect1.height()],
                    stroke: 'black',
                    strokeWidth: 2
                });
                group.add(line1)
            }
            // for (let i = 1; i < rect1.width() / 20; i++) {
            //     let line2 = new Konva.Line({
            //         points: [rect1.x() + rect1.width() - i * 20, rect1.y() + rect1.height(), rect1.x() + rect1.width(), rect1.y() + rect1.height() - i * 20],
            //         stroke: 'black',
            //         strokeWidth: 3
            //     });
            //     group.add(line2)
            // }
        }
    }
    if (style === "circle") {
        var circle = new Konva.Circle({
            x: x,
            y: y,
            radius: 40,
            stroke: 'black',
            strokeWidth: 3,
        });
        group.add(circle)
        var j;
        if (rotation === 0) {
            for (let i = 0; i < circle.radius() / 20; i++) {
                j = Math.asin(20 * i / circle.radius())
                let line1 = new Konva.Line({
                    points: [(circle.x() + 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() - 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() + 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() - 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2)],
                    stroke: 'black',
                    strokeWidth: 3
                });
                group.add(line1)
            }
            for (let i = 1; i < circle.radius() / 20; i++) {
                j = Math.asin(20 * i / circle.radius())
                let line2 = new Konva.Line({
                    points: [(circle.x() - 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() + 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() - 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() + 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2)],
                    stroke: 'black',
                    strokeWidth: 3
                });
                group.add(line2)
            }
        } else if (rotation === 1) {
            for (let i = 0; i < circle.radius() / 20; i++) {
                j = Math.asin(20 * i / circle.radius())
                let line1 = new Konva.Line({
                    points: [(circle.x() - 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() - 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() - 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() - 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2)],
                    stroke: 'black',
                    strokeWidth: 3
                });
                group.add(line1)
            }
            for (let i = 1; i < circle.radius() / 20; i++) {
                j = Math.asin(20 * i / circle.radius())
                let line2 = new Konva.Line({
                    points: [(circle.x() + 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() + 20 * i / Math.sqrt(2)) - Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() + 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2),
                        (circle.x() + 20 * i / Math.sqrt(2)) + Math.cos(j) * circle.radius() / Math.sqrt(2)],
                    stroke: 'black',
                    strokeWidth: 3
                });
                group.add(line2)
            }
        }
    }
    return group;
}


function Stimuli(style, holes, x, y, color = "black", rotation = 0) {
    if (holes === 0) {
        return NoHole(style, x, y, color, rotation);
    }
    if (holes === 1) {
        return SingleHole(style, x, y, color, rotation);
    }
    if (holes === 2) {
        return DoubleHoles(style, x, y, color, rotation);
    }
}