//定义要用的随机颜色
let similar_Color = ["#315d31", "#86860d", "#5353c5", "#de8fde", "#c95422",
    "#ff001a", "#c30000", "#af0000", "#790000"]
let stimColorName = ["green", "yellow", "blue", "purple", "red"]
let stimColorName6 = ["green", "yellow", "blue", "purple", "red", "cyan"]
let stimColorName3 = ["green", "blue", "red"]
let stimColor = {
    "green": "#00bf00", "yellow": "#bfbf00", "blue": "#0000bf", "purple": "#bf00bf",
    "red": "#bf0000", "cyan": "#00bfbf",
    "darkgreen": "#008000", "darkyellow": "#808000", "darkblue": "#000080", "darkpurple": "#800080",
    "darkred": "#800000", "darkcyan": "#008080",
    "lightgreen": "#00ff00", "lightyellow": "#ffff00", "lightblue": "#0000ff", "lightpurple": "#ff00ff",
    "lightred": "#ff0000", "lightcyan": "#00ffff",
}
const stimArray = ["rect", "triangle", "circle", "star", "hexagram"]
const stimArray6 = ["rect", "triangle", "circle", "star", "hexagram", "diamond"]
const stimArray3 = ["rect", "triangle", "circle"]

let anss = ["4", "8", "6", "2"], anss3 = ["4", "6", "5"], anss7 = ["4", "7", "9", "6", "3", "1", "5"]
let dist_loc6 = [
    [width / 2 - 300, height / 2], [width / 2 - 150, height / 2 - 150 * Math.sqrt(3)],
    [width / 2 + 150, height / 2 - 150 * Math.sqrt(3)], [width / 2 + 300, height / 2],
    [width / 2 + 150, height / 2 + 150 * Math.sqrt(3)], [width / 2 - 150, height / 2 + 150 * Math.sqrt(3)]
]

//exam_preload中generateStimArray()仅仅生成的是60个
//memory_exam2.js中
//拓扑作为干扰
//无优化
function generateStimArray_1(shapeORcolor) {
    let timeline_variables = [], distractor_num
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 5; j++) {
            // for (let k = 0; k < 3; k++) {
            //     if (i === 0) distractor_num = k + 1
            //     else if (i === 1) {
            //         if (k < 1) distractor_num = 0
            //         else distractor_num = k + 1
            //     } else if (i === 2) {
            //         if (k < 2) distractor_num = k
            //         else distractor_num = k + 1
            //     } else distractor_num = k
            //     if (shapeORcolor === 0) {
            //         let shapeCopy = ["rect", "triangle", "circle", "star", "hexagram"]
            //         shapeCopy.splice(j, 1)
            //         for (let l = 0; l < shapeCopy.length; l++) {
            //             let v = ["", "", "", ""], n = 0
            //             distractor = shapeCopy[l]
            //             if (distractor === "circle") distractor = "ring_1"
            //             else distractor = distractor + "_1"
            //             let copy_array = shapeCopy.slice()
            //             copy_array.splice(l, 1)
            //             let stim = getArrayItems(copy_array, 2)
            //             v[i] = stimArray[j]
            //             v[distractor_num] = distractor
            //             for (let m = 0; m < v.length; m++) {
            //                 if (v[m] === "") {
            //                     v[m] = stim[n]
            //                     n++
            //                 }
            //             }
            //             timeline_variables.push({
            //                 size: '4',
            //                 v1: v,
            //                 target: stimArray[j],
            //                 ans: anss[i],
            //                 type: "hole-no-hole",
            //                 distractor: v[distractor_num],
            //                 distractor_dist: anss[distractor_num],
            //                 shapeORcolor: 0
            //             })
            //         }
            //     } else {
            //         let colorCopy = ["green", "yellow", "blue", "purple", "red"]
            //         colorCopy.splice(j, 1)
            //         for (let l = 0; l < colorCopy.length; l++) {
            //             let color = ["", "", "", ""], n = 0, array = ["circle", "circle", "circle", "circle"]
            //             distractor = colorCopy[l]
            //             let copy_array = colorCopy.slice()
            //             copy_array.splice(l, 1)
            //             let stim = getArrayItems(copy_array, 2)
            //             color[i] = stimColor[stimColorName[j]]
            //             color[distractor_num] = stimColor[distractor]
            //             for (let m = 0; m < color.length; m++) {
            //                 if (color[m] === "") {
            //                     color[m] = stimColor[stim[n]]
            //                     n++
            //                 }
            //             }
            //             array[distractor_num] = "ring_1"
            //             timeline_variables.push({
            //                 size: '4',
            //                 v1: array,
            //                 color: color,
            //                 target: i,
            //                 type: "hole-no-hole",
            //                 ans: anss[i],
            //                 distractor: distractor_num,
            //                 distractor_dist: anss[distractor_num],
            //                 shapeORcolor: 1
            //             })
            //         }
            //     }
            // }
            if (j % 2 === 0) {
                if (i === 0) distractor_num = 2
                else if (i === 1) distractor_num = 0
                else if (i === 2) distractor_num = 3
                else distractor_num = 1
            } else {
                if (i === 0) distractor_num = 1
                else if (i === 1) distractor_num = 3
                else if (i === 2) distractor_num = 0
                else distractor_num = 2
            }
            if (shapeORcolor === 0) {
                let stimCopy = ["rect", "triangle", "circle", "star", "hexagram"]
                stimCopy.splice(j, 1)
                let stim = getArrayItems(stimCopy, 3)
                stim.splice(i, 0, stimArray[j])
                if (stim[distractor_num] === "circle") stim[distractor_num] = "ring_1"
                else stim[distractor_num] = stim[distractor_num] + "_1"
                timeline_variables.push({
                    size: '4',
                    v1: stim,
                    target: stimArray[j],
                    ans: anss[i],
                    type: "hole-no-hole",
                    distractor: stim[distractor_num],
                    distractor_dist: anss[distractor_num],
                    shapeORcolor: 0
                })
            } else {
                let colorCopy = ["green", "yellow", "blue", "purple", "red"]
                colorCopy.splice(j, 1)
                let array = ["circle", "circle", "circle", "circle"], color
                color = getArrayItems(colorCopy, 3)
                color.splice(i, 0, stimColorName[j])
                array[distractor_num] = "ring_1"
                timeline_variables.push({
                    size: '4',
                    v1: array,
                    color: color,
                    target: i,
                    type: "hole-no-hole",
                    ans: anss[i],
                    distractor: distractor_num,
                    distractor_dist: anss[distractor_num],
                    shapeORcolor: 1
                })
            }
        }
    }
    return timeline_variables
}


//五分之一的概率目标项不存在
function f7(stimArrays, size) {
    //深复制+排序
    let stims = JSON.parse(JSON.stringify(stimArrays)), stimm = []
    stims.sort(compareNames)
    if (size === 4) {
        for (let i = 0; i < 5; i++) {
            let stim = getArrayItems(group(stims, 4)[i], 1)[0]
            stim["ans"] = '5'
            if (stim.color) stim["target"] = 4
            else {
                let diffs = diff(stim["v1"], stimArray)[0]
                if (stim["type"] === "hole") {
                    if (diffs === "circle") stim["target"] = "ring_1"
                    else stim["target"] = diffs + "_1"
                } else stim["target"] = diffs
            }
            stimm.push(stim)
        }
    } else if (size === 2) {
        for (let i = 0; i < 3; i++) {
            let stim = getArrayItems(group(stims, 2)[i], 1)[0]
            stim["ans"] = '5'
            if (stim.color) stim["target"] = 2
            else {
                let diffs = diff(stim["v1"], stimArray)[0]
                if (stim["type"] === "hole") {
                    if (diffs === "circle") stim["target"] = "ring_1"
                    else stim["target"] = diffs + "_1"
                } else stim["target"] = diffs
            }
            stimm.push(stim)
        }
    }
    return stimm
}

//20,20,20,20
let color_topo_T = generateStimArray("hole", 1)
let shape_topo_T = generateStimArray("hole", 0)
let color_topo_D = generateStimArray_1(1)
let shape_topo_D = generateStimArray_1(0)


color_topo_T.push.apply(color_topo_T, f7(color_topo_T, 4))
shape_topo_T.push.apply(shape_topo_T, f7(shape_topo_T, 4))
color_topo_D.push.apply(color_topo_D, f7(color_topo_D, 4))
shape_topo_D.push.apply(shape_topo_D, f7(shape_topo_D, 4))


//size=6
function generatestim(type, stimarr, ansarr, size, shapeORcolor) {
    let variables = [], distractor_num
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < stimarr.length; j++) {
            if (size === 6) {
                if (j % 3 === 0) {
                    if (i === 0) distractor_num = 2
                    else if (i === 1) distractor_num = 4
                    else if (i === 2) distractor_num = 3
                    else if (i === 3) distractor_num = 5
                    else if (i === 4) distractor_num = 1
                    else distractor_num = 0
                } else if (j % 3 === 1) {
                    if (i === 0) distractor_num = 1
                    else if (i === 1) distractor_num = 3
                    else if (i === 2) distractor_num = 5
                    else if (i === 3) distractor_num = 4
                    else if (i === 4) distractor_num = 0
                    else distractor_num = 2
                } else {
                    if (i === 0) distractor_num = 3
                    else if (i === 1) distractor_num = 2
                    else if (i === 2) distractor_num = 4
                    else if (i === 3) distractor_num = 0
                    else if (i === 4) distractor_num = 5
                    else distractor_num = 1
                }
            }
            if (size === 2) {
                if (i === 0) distractor_num = 1
                else distractor_num = 0
            }
            let stimcopy = stimarr.slice()
            stimcopy.splice(j, 1)
            let stim = getArrayItems(stimcopy, size - 1)
            stim.splice(i, 0, stimarr[j])
            if (shapeORcolor === 0) {
                if (type === "hole") {
                    if (stim[i] === "circle") stim[i] = "ring_1"
                    else stim[i] = stim[i] + "_1"
                    variables.push({
                        size: size,
                        v1: stim,
                        target: stim[i],
                        ans: ansarr[i],
                        type: type,
                        shapeORcolor: 0
                    })
                }
                if (type === "no-hole")
                    variables.push({
                        size: size,
                        v1: stim,
                        target: stim[i],
                        ans: ansarr[i],
                        type: type,
                        shapeORcolor: 0
                    })
                if (type === "hole-no-hole") {
                    if (stim[distractor_num] === "circle") stim[distractor_num] = "ring_1"
                    else stim[distractor_num] = stim[distractor_num] + "_1"
                    variables.push({
                        size: size,
                        v1: stim,
                        target: stim[i],
                        distractor: stim[distractor_num],
                        ans: ansarr[i],
                        distractor_dist: anss[distractor_num],
                        type: type,
                        shapeORcolor: 0
                    })
                }
            } else {
                let array
                if (size === 2) array = ["circle", "circle"]
                else array = ["circle", "circle", "circle", "circle", "circle", "circle"]
                if (type === "hole") {
                    array[i] = "ring_1"
                    variables.push({
                        size: size,
                        v1: array,
                        color: stim,
                        target: i,
                        ans: ansarr[i],
                        type: type,
                        shapeORcolor: 1
                    })
                }
                if (type === "no-hole")
                    variables.push({
                        size: size,
                        v1: array,
                        color: stim,
                        target: i,
                        ans: ansarr[i],
                        type: type,
                        shapeORcolor: 1
                    })
                if (type === "hole-no-hole") {
                    array[distractor_num] = "ring_1"
                    variables.push({
                        size: size,
                        v1: array,
                        color: stim,
                        target: i,
                        distractor: distractor_num,
                        ans: ansarr[i],
                        distractor_dist: anss[distractor_num],
                        type: type,
                        shapeORcolor: 1
                    })
                }
            }

        }
    }
    return variables
}

'#f66f69',
    '#1597a5','#0e606b','#fff4f2','#feb3ae'
//动态实验
let ansarr = {2:["4", "6", "5"], 4: ["4", "8", "6", "2"], 5: ["7", "9", "6", "2", "4"], 6: ["4", "7", "9", "6", "3", "1"]}

//size=5,ISI=1000ms,anssarr
function DynamicStim(num, shapeORcolor, motion, topo) {
    let stimarr, timeline_variables = [], distractor_num, type, distractor_num1
    let array = ["circle", "circle", "circle", "circle", "circle", "circle"]
    for (let i = 0; i < num; i++) {
        for (let j = 0; j < 2; j++) {
            if (num === 2 && shapeORcolor === "shape") stimarr = getArrayItems(stimArray3, 2)
            if (num === 4 && shapeORcolor === "shape") stimarr = getArrayItems(stimArray6, 4)
            if (num === 5 && shapeORcolor === "shape") stimarr = getArrayItems(stimArray6, 5)
            if (num === 6 && shapeORcolor === "shape") stimarr = stimArray6
            if (num === 2 && shapeORcolor === "color") stimarr = getArrayItems(stimColorName3, 2)
            if (num === 4 && shapeORcolor === "color") stimarr = getArrayItems(stimColorName6, 4)
            if (num === 5 && shapeORcolor === "color") stimarr = getArrayItems(stimColorName6, 5)
            if (num === 6 && shapeORcolor === "color") stimarr = stimColorName6
            
            if (num === 2) {
                if (i === 0) distractor_num = 1
                else distractor_num = 0
            }
            if (num === 4) {
                if (j % 2 === 0) {
                    if (i === 0) distractor_num = 2
                    else if (i === 1) distractor_num = 0
                    else if (i === 2) distractor_num = 3
                    else distractor_num = 1
                } else {
                    if (i === 0) distractor_num = 1
                    else if (i === 1) distractor_num = 3
                    else if (i === 2) distractor_num = 0
                    else distractor_num = 2
                }
            }
            if (num === 5) {
                if (j % 2 === 0) {
                    if (i === 0) distractor_num = 1
                    else if (i === 1) distractor_num = 3
                    else if (i === 2) distractor_num = 0
                    else if (i === 3) distractor_num = 4
                    else distractor_num = 2
                } else {
                    if (i === 0) distractor_num = 2
                    else if (i === 1) distractor_num = 0
                    else if (i === 2) distractor_num = 4
                    else if (i === 3) distractor_num = 1
                    else distractor_num = 3
                }
            }
            if (num === 6) {
                if (j % 2 === 0) {
                    if (i === 0) distractor_num = 1
                    else if (i === 1) distractor_num = 3
                    else if (i === 2) distractor_num = 5
                    else if (i === 3) distractor_num = 0
                    else if (i === 4) distractor_num = 2
                    else distractor_num = 4
                } else {
                    if (i === 0) distractor_num = 2
                    else if (i === 1) distractor_num = 4
                    else if (i === 2) distractor_num = 1
                    else if (i === 3) distractor_num = 0
                    else if (i === 4) distractor_num = 5
                    else distractor_num = 3
                }
            }
            stimarr = shuffle(stimarr)
            if (motion === 1 && topo === 0) {
                if (j === 0) type = "zoom"
                else type = "trans"
                var randomValue = Math.floor(Math.random() * 2)
                if (shapeORcolor === "shape") {
                    if (stimarr[distractor_num] === "circle") stimarr[distractor_num] = randomValue === 0 ? "ring_1" : "ring_2"
                    else stimarr[distractor_num] = randomValue === 0 ? stimarr[distractor_num] + "_1" : stimarr[distractor_num] + "_2"
                    timeline_variables.push({
                        size: num,
                        v1: stimarr,
                        target: stimarr[i],
                        distractor: distractor_num,
                        ans: ansarr[num][i],
                        distractor_dist: ansarr[num][distractor_num],
                        type: shapeORcolor,
                        tchange: type,
                        shapeORcolor: 0,
                        motion: 1,
                        topo: 0
                    })

                } else if (shapeORcolor === "color") {
                    let arr = getArrayItems(array, num)
                    arr[distractor_num] = randomValue === 0 ? "ring_1" : "ring_2"
                    timeline_variables.push({
                        size: num,
                        v1: arr,
                        color: stimarr,
                        target: i,
                        distractor: distractor_num,
                        ans: ansarr[num][i],
                        distractor_dist: ansarr[num][distractor_num],
                        type: shapeORcolor,
                        tchange: type,
                        shapeORcolor: 1,
                        motion: 1,
                        topo: 0
                    })
                }
            }
            if (motion === 0 && topo === 1) {
                if (j === 0) type = "single"
                else type = "double"
                var randomValue = Math.floor(Math.random() * 2)
                if (shapeORcolor === "shape") {
                    if (stimarr[i] === "circle") {
                        if (type === "single") stimarr[i] = "ring_1"
                        else stimarr[i] = "ring_2"
                    } else {
                        if (type === "single") stimarr[i] = stimarr[i] + "_1"
                        else stimarr[i] = stimarr[i] + "_2"
                    }
                    timeline_variables.push({
                        size: num,
                        v1: stimarr,
                        target: stimarr[i],
                        distractor: distractor_num,
                        ans: ansarr[num][i],
                        distractor_dist: ansarr[num][distractor_num],
                        type: shapeORcolor,
                        tchange: type,
                        dchange: randomValue === 0 ? "zoom" : "trans",
                        shapeORcolor: 0,
                        motion: 0,
                        topo: 1
                    })
                }
                if (shapeORcolor === "color") {
                    let arr = getArrayItems(array, num)
                    if (type === "single") arr[i] = "ring_1"
                    else arr[i] = "ring_2"
                    timeline_variables.push({
                        size: num,
                        v1: arr,
                        color: stimarr,
                        target: i,
                        distractor: distractor_num,
                        ans: ansarr[num][i],
                        distractor_dist: ansarr[num][distractor_num],
                        type: shapeORcolor,
                        tchange: type,
                        dchange: randomValue === 0 ? "zoom" : "trans",
                        shapeORcolor: 1,
                        motion: 0,
                        topo: 1
                    })
                }
            }
            if (motion === 0 && topo === 0) {
                var randomValue1 = Math.floor(Math.random() * 2)
                var randomValue2 = Math.floor(Math.random() * 2)
                // console.log(randomValue1,randomValue2)
                var arrnum = Array.from({length: num}, (_, index) => index);
                arrnum.splice(i, 1)
                var disnum = getArrayItems(arrnum, 2)
                distractor_num = disnum[0] //motion
                distractor_num1 = disnum[1] //topo
                if (shapeORcolor === "shape") {
                    if (stimarr[distractor_num1] === "circle") stimarr[distractor_num1] = randomValue2 === 0 ? "ring_1" : "ring_2"
                    else stimarr[distractor_num1] = randomValue2 === 0 ? stimarr[distractor_num1] + "_1" : stimarr[distractor_num1] + "_2"
                    timeline_variables.push({
                        size: num,
                        v1: stimarr,
                        target: stimarr[i],
                        distractor1: distractor_num,
                        distractor2: distractor_num1,
                        ans: ansarr[num][i],
                        distractor_dist1: ansarr[num][distractor_num],
                        distractor_dist2: ansarr[num][distractor_num1],
                        type: shapeORcolor,
                        dchange1: randomValue1 === 0 ? "zoom" : "trans",
                        dchange2: randomValue2 === 0 ? "single" : "double",
                        shapeORcolor: 0,
                        motion: 0,
                        topo: 0
                    })
                } else if (shapeORcolor === "color") {
                    let arr = getArrayItems(array, num)
                    arr[distractor_num1] = randomValue2 === 0 ? "ring_1" : "ring_2"
                    timeline_variables.push({
                        size: num,
                        v1: arr,
                        color: stimarr,
                        target: i,
                        distractor1: distractor_num,
                        distractor2: distractor_num1,
                        ans: ansarr[num][i],
                        distractor_dist1: ansarr[num][distractor_num],
                        distractor_dist2: ansarr[num][distractor_num1],
                        type: shapeORcolor,
                        dchange1: randomValue1 === 0 ? "zoom" : "trans",
                        dchange2: randomValue2 === 0 ? "single" : "double",
                        shapeORcolor: 1,
                        motion: 0,
                        topo: 0
                    })
                }
            }
        }
    }
    return timeline_variables
}

function DynamicStim1(num, shapeORcolor, motion, topo, T) {
    let stimarr, timeline_variables = [], distractor_num, type, distractor_num1
    let array = ["circle", "circle", "circle", "circle", "circle", "circle"]
    for (let i = 0; i < num; i++) {
        for (let j = 0; j < 2; j++) {
            if (num === 4 && shapeORcolor === "shape") stimarr = getArrayItems(stimArray6, 4)
            if (num === 4 && shapeORcolor === "color") stimarr = getArrayItems(stimColorName6, 4)
            if (num === 4) {
                if (j % 2 === 0) {
                    if (i === 0) distractor_num = 2
                    else if (i === 1) distractor_num = 0
                    else if (i === 2) distractor_num = 3
                    else distractor_num = 1
                } else {
                    if (i === 0) distractor_num = 1
                    else if (i === 1) distractor_num = 3
                    else if (i === 2) distractor_num = 0
                    else distractor_num = 2
                }
            }
            stimarr = shuffle(stimarr)
            if (motion === 1 && topo === 0) {
                if (j === 0) type = "zoom"
                else type = "trans"
                var randomValue = Math.floor(Math.random() * 2)
                if (T === 1) {
                    if (shapeORcolor === "shape") {
                        timeline_variables.push({
                            size: num,
                            v1: stimarr,
                            target: stimarr[i],
                            ans: ansarr[num][i],
                            type: shapeORcolor,
                            tchange: type,
                            shapeORcolor: 0,
                            motion: 1,
                            topo: 0,
                            T:1
                        })

                    } else if (shapeORcolor === "color") {
                        let arr = getArrayItems(array, num)
                        timeline_variables.push({
                            size: num,
                            v1: arr,
                            color: stimarr,
                            target: i,
                            ans: ansarr[num][i],
                            type: shapeORcolor,
                            tchange: type,
                            shapeORcolor: 1,
                            motion: 1,
                            topo: 0,
                            T:1
                        })
                    }
                } else {
                    if (shapeORcolor === "shape") {
                        timeline_variables.push({
                            size: num,
                            v1: stimarr,
                            target: stimarr[i],
                            distractor: distractor_num,
                            ans: ansarr[num][i],
                            distractor_dist: ansarr[num][distractor_num],
                            type: shapeORcolor,
                            dchange: type,
                            shapeORcolor: 0,
                            motion: 1,
                            topo: 0,
                            T:0
                        })

                    } else if (shapeORcolor === "color") {
                        let arr = getArrayItems(array, num)
                        timeline_variables.push({
                            size: num,
                            v1: arr,
                            color: stimarr,
                            target: i,
                            distractor: distractor_num,
                            ans: ansarr[num][i],
                            type: shapeORcolor,
                            distractor_dist: ansarr[num][distractor_num],
                            dchange: type,
                            shapeORcolor: 1,
                            motion: 1,
                            topo: 0,
                            T:0
                        })
                    }
                }
            }
            if (motion === 0 && topo === 1) {
                if (j === 0) type = "single"
                else type = "double"
                var randomValue = Math.floor(Math.random() * 2)
                if (T === 1) {
                    if (shapeORcolor === "shape") {
                        if (stimarr[i] === "circle") {
                            if (type === "single") stimarr[i] = "ring_1"
                            else stimarr[i] = "ring_2"
                        } else {
                            if (type === "single") stimarr[i] = stimarr[i] + "_1"
                            else stimarr[i] = stimarr[i] + "_2"
                        }
                        timeline_variables.push({
                            size: num,
                            v1: stimarr,
                            target: stimarr[i],
                            ans: ansarr[num][i],
                            type: shapeORcolor,
                            tchange: type,
                            shapeORcolor: 0,
                            motion: 0,
                            topo: 1,
                            T:1
                        })
                    }
                    if (shapeORcolor === "color") {
                        let arr = getArrayItems(array, num)
                        if (type === "single") arr[i] = "ring_1"
                        else arr[i] = "ring_2"
                        timeline_variables.push({
                            size: num,
                            v1: arr,
                            color: stimarr,
                            target: i,
                            ans: ansarr[num][i],
                            type: shapeORcolor,
                            tchange: type,
                            shapeORcolor: 1,
                            motion: 0,
                            topo: 1,
                            T:1
                        })
                    }
                } else {
                    if (shapeORcolor === "shape") {
                        if (stimarr[distractor_num] === "circle") {
                            if (type === "single") stimarr[distractor_num] = "ring_1"
                            else stimarr[distractor_num] = "ring_2"
                        } else {
                            if (type === "single") stimarr[distractor_num] = stimarr[distractor_num] + "_1"
                            else stimarr[distractor_num] = stimarr[distractor_num] + "_2"
                        }
                        timeline_variables.push({
                            size: num,
                            v1: stimarr,
                            target: stimarr[i],
                            distractor: distractor_num,
                            ans: ansarr[num][i],
                            distractor_dist: ansarr[num][distractor_num],
                            type: shapeORcolor,
                            dchange: type,
                            shapeORcolor: 0,
                            motion: 0,
                            topo: 1,
                            T:0
                        })
                    }
                    if (shapeORcolor === "color") {
                        let arr = getArrayItems(array, num)
                        if (type === "single") arr[distractor_num] = "ring_1"
                        else arr[distractor_num] = "ring_2"
                        timeline_variables.push({
                            size: num,
                            v1: arr,
                            color: stimarr,
                            target: i,
                            distractor: distractor_num,
                            ans: ansarr[num][i],
                            distractor_dist: ansarr[num][distractor_num],
                            type: shapeORcolor,
                            dchange: type,
                            shapeORcolor: 1,
                            motion: 0,
                            topo: 1,
                            T:0
                        })
                    }
                }

            }
        }
    }
    return timeline_variables
}


//memory_exam4_pro.js
//color中的hole-no-hole
let color_hole_no_hole = [
    {"标准序": 19, "运行序": 1, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "D", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 7, "运行序": 2, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "B", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 25, "运行序": 3, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "A", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 28, "运行序": 4, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "A", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 21, "运行序": 5, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "D", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 20, "运行序": 6, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "D", "TARGETC": "topo", "STIM-D": 2},
    {"标准序": 37, "运行序": 7, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "C", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 48, "运行序": 8, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "D", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 43, "运行序": 9, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "D", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 33, "运行序": 10, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "B", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 5, "运行序": 11, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "A", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 40, "运行序": 12, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "C", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 17, "运行序": 13, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "C", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 31, "运行序": 14, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "B", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 29, "运行序": 15, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "A", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 18, "运行序": 16, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "C", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 23, "运行序": 17, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "D", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 13, "运行序": 18, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "C", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 1, "运行序": 19, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "A", "TARGETC": "topo", "STIM-D": 1},
    {"标准序": 47, "运行序": 20, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "D", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 6, "运行序": 21, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "A", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 2, "运行序": 22, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "A", "TARGETC": "topo", "STIM-D": 2},
    {"标准序": 16, "运行序": 23, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "C", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 3, "运行序": 24, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "A", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 15, "运行序": 25, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "C", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 4, "运行序": 26, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "A", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 41, "运行序": 27, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "C", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 14, "运行序": 28, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "C", "TARGETC": "topo", "STIM-D": 2},
    {"标准序": 42, "运行序": 29, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "C", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 34, "运行序": 30, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "B", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 35, "运行序": 31, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "B", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 38, "运行序": 32, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "C", "TARGETC": "topo", "STIM-D": 2},
    {"标准序": 44, "运行序": 33, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "D", "TARGETC": "topo", "STIM-D": 2},
    {"标准序": 30, "运行序": 34, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "A", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 32, "运行序": 35, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "B", "TARGETC": "topo", "STIM-D": 2},
    {"标准序": 10, "运行序": 36, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "B", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 9, "运行序": 37, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "B", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 36, "运行序": 38, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "B", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 22, "运行序": 39, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "D", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 8, "运行序": 40, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "B", "TARGETC": "topo", "STIM-D": 2},
    {"标准序": 45, "运行序": 41, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "D", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 46, "运行序": 42, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "D", "TARGETC": "color", "STIM-D": 1},
    {"标准序": 27, "运行序": 43, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "A", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 11, "运行序": 44, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "B", "TARGETC": "color", "STIM-D": 2},
    {"标准序": 12, "运行序": 45, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "B", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 24, "运行序": 46, "点类型": 1, "区组": 1, "COLOR": "明", "STIM-T": "D", "TARGETC": "color", "STIM-D": 3},
    {"标准序": 39, "运行序": 47, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "C", "TARGETC": "topo", "STIM-D": 3},
    {"标准序": 26, "运行序": 48, "点类型": 1, "区组": 1, "COLOR": "暗", "STIM-T": "A", "TARGETC": "topo", "STIM-D": 2}
]

function f(color_hole_no_hole) {
    let variables = [], ans, distractor, target
    for (let i = 0; i < color_hole_no_hole.length; i++) {
        let v1 = ['circle', 'circle', 'circle', 'circle']
        let stim_color = getArrayItems(stimColorName, 4)
        if (color_hole_no_hole[i]["STIM-T"] === "A") {
            target = 0
            distractor = color_hole_no_hole[i]["STIM-D"]
        } else if (color_hole_no_hole[i]["STIM-T"] === "B") {
            target = 1
            if (color_hole_no_hole[i]["STIM-D"] === 1) distractor = 0
            else distractor = color_hole_no_hole[i]["STIM-D"]
        } else if (color_hole_no_hole[i]["STIM-T"] === "C") {
            target = 2
            if (color_hole_no_hole[i]["STIM-D"] === 3) distractor = 3
            else distractor = color_hole_no_hole[i]["STIM-D"] - 1
        } else {
            target = 3
            distractor = color_hole_no_hole[i]["STIM-D"] - 1
        }
        if (color_hole_no_hole[i]["TARGETC"] === "topo") {
            v1[target] = "ring_1"
            if (color_hole_no_hole[i]["COLOR"] === "明") stim_color[distractor] = "light" + stim_color[distractor]
            else stim_color[distractor] = "dark" + stim_color[distractor]
        } else {
            if (color_hole_no_hole[i]["COLOR"] === "明") stim_color[target] = "light" + stim_color[target]
            else stim_color[target] = "dark" + stim_color[target]
            v1[distractor] = "ring_1"
        }
        ans = anss[target]
        variables.push({
            size: '4',
            v1: v1,
            color: stim_color,
            shade: color_hole_no_hole[i]["COLOR"],
            target: target,
            type: "color",
            targettype: color_hole_no_hole[i]["TARGETC"],
            distractor: distractor,
            ans: ans
        })
    }
    return variables
}

//shape中的hole-no-hole
let shape_hole_no_hole = [
    {"标准序": 6, "运行序": 1, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 8, "运行序": 2, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 15, "运行序": 3, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 25, "运行序": 4, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "TARGET": "shape", "STIM-D": 1},
    {"标准序": 7, "运行序": 5, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "TARGET": "shape", "STIM-D": 1},
    {"标准序": 20, "运行序": 6, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 18, "运行序": 7, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 33, "运行序": 8, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 3, "运行序": 9, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 19, "运行序": 10, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "TARGET": "shape", "STIM-D": 1},
    {"标准序": 41, "运行序": 11, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 1, "运行序": 12, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "TARGET": "shape", "STIM-D": 1},
    {"标准序": 47, "运行序": 13, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 23, "运行序": 14, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 27, "运行序": 15, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 2, "运行序": 16, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 39, "运行序": 17, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 44, "运行序": 18, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 14, "运行序": 19, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 17, "运行序": 20, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 35, "运行序": 21, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 28, "运行序": 22, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 30, "运行序": 23, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 43, "运行序": 24, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "TARGET": "shape", "STIM-D": 1},
    {"标准序": 48, "运行序": 25, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 38, "运行序": 26, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 10, "运行序": 27, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 40, "运行序": 28, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 36, "运行序": 29, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 9, "运行序": 30, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 22, "运行序": 31, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 13, "运行序": 32, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "TARGET": "shape", "STIM-D": 1},
    {"标准序": 46, "运行序": 33, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 29, "运行序": 34, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 34, "运行序": 35, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 4, "运行序": 36, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 24, "运行序": 37, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 37, "运行序": 38, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "TARGET": "shape", "STIM-D": 1},
    {"标准序": 26, "运行序": 39, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 12, "运行序": 40, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 5, "运行序": 41, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 16, "运行序": 42, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "TARGET": "topo", "STIM-D": 1},
    {"标准序": 11, "运行序": 43, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "TARGET": "topo", "STIM-D": 2},
    {"标准序": 32, "运行序": 44, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "TARGET": "shape", "STIM-D": 2},
    {"标准序": 45, "运行序": 45, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 42, "运行序": 46, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "TARGET": "topo", "STIM-D": 3},
    {"标准序": 21, "运行序": 47, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "TARGET": "shape", "STIM-D": 3},
    {"标准序": 31, "运行序": 48, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "TARGET": "shape", "STIM-D": 1}
]
let shape = ['rect', 'diamond', 'trapezoid']

function f1(shape_hole_no_hole) {
    let variables = [], ans, distractor, target
    for (let i = 0; i < shape_hole_no_hole.length; i++) {
        let v1 = shuffle(shape)
        if (shape_hole_no_hole[i]["STIM-T"] === "A") {
            target = 0
            distractor = shape_hole_no_hole[i]["STIM-D"]
        } else if (shape_hole_no_hole[i]["STIM-T"] === "B") {
            target = 1
            if (shape_hole_no_hole[i]["STIM-D"] === 1) distractor = 0
            else distractor = shape_hole_no_hole[i]["STIM-D"]
        } else if (shape_hole_no_hole[i]["STIM-T"] === "C") {
            target = 2
            if (shape_hole_no_hole[i]["STIM-D"] === 3) distractor = 3
            else distractor = shape_hole_no_hole[i]["STIM-D"] - 1
        } else {
            target = 3
            distractor = shape_hole_no_hole[i]["STIM-D"] - 1
        }
        if (shape_hole_no_hole[i]["TARGET"] === "topo") {
            if (shape_hole_no_hole[i]["SHAPE"] === "circle") v1.splice(distractor, 0, "circle")
            else v1.splice(distractor, 0, "triangle")
            v1[target] = v1[target] + "_1"
        } else {
            if (shape_hole_no_hole[i]["SHAPE"] === "circle") v1.splice(target, 0, "circle")
            else v1.splice(target, 0, "triangle")
            v1[distractor] = v1[distractor] + "_1"
        }
        ans = anss[target]
        variables.push({
            size: '4',
            v1: v1,
            shape: shape_hole_no_hole[i]["SHAPE"],
            target: target,
            targettype: shape_hole_no_hole[i]["TARGET"],
            type: "shape",
            distractor: distractor,
            ans: ans
        })
    }
    return variables
}


// let color_hole_no_hole_variables = f(color_hole_no_hole)
// let shape_hole_no_hole_variables = f1(shape_hole_no_hole)
// console.log(color_hole_no_hole_variables, shape_hole_no_hole_variables)

let color_no_hole = [
    {"标准序": 33, "运行序": 1, "点类型": 1, "区组": 1, "shade": "暗", "color": "blue", "Dist-T": "A"},
    {"标准序": 3, "运行序": 2, "点类型": 1, "区组": 1, "shade": "明", "color": "red", "Dist-T": "C"},
    {"标准序": 17, "运行序": 3, "点类型": 1, "区组": 1, "shade": "明", "color": "purple", "Dist-T": "A"},
    {"标准序": 43, "运行序": 4, "点类型": 1, "区组": 1, "shade": "暗", "color": "purple", "Dist-T": "C"},
    {"标准序": 7, "运行序": 5, "点类型": 1, "区组": 1, "shade": "明", "color": "green", "Dist-T": "C"},
    {"标准序": 8, "运行序": 6, "点类型": 1, "区组": 1, "shade": "明", "color": "green", "Dist-T": "D"},
    {"标准序": 12, "运行序": 7, "点类型": 1, "区组": 1, "shade": "明", "color": "blue", "Dist-T": "D"},
    {"标准序": 36, "运行序": 8, "点类型": 1, "区组": 1, "shade": "暗", "color": "blue", "Dist-T": "D"},
    {"标准序": 41, "运行序": 9, "点类型": 1, "区组": 1, "shade": "暗", "color": "purple", "Dist-T": "A"},
    {"标准序": 38, "运行序": 10, "点类型": 1, "区组": 1, "shade": "暗", "color": "yellow", "Dist-T": "B"},
    {"标准序": 42, "运行序": 11, "点类型": 1, "区组": 1, "shade": "暗", "color": "purple", "Dist-T": "B"},
    {"标准序": 10, "运行序": 12, "点类型": 1, "区组": 1, "shade": "明", "color": "blue", "Dist-T": "B"},
    {"标准序": 2, "运行序": 13, "点类型": 1, "区组": 1, "shade": "明", "color": "red", "Dist-T": "B"},
    {"标准序": 14, "运行序": 14, "点类型": 1, "区组": 1, "shade": "明", "color": "yellow", "Dist-T": "B"},
    {"标准序": 16, "运行序": 15, "点类型": 1, "区组": 1, "shade": "明", "color": "yellow", "Dist-T": "D"},
    {"标准序": 40, "运行序": 16, "点类型": 1, "区组": 1, "shade": "暗", "color": "yellow", "Dist-T": "D"},
    {"标准序": 30, "运行序": 17, "点类型": 1, "区组": 1, "shade": "暗", "color": "green", "Dist-T": "B"},
    {"标准序": 46, "运行序": 18, "点类型": 1, "区组": 1, "shade": "暗", "color": "cyan", "Dist-T": "B"},
    {"标准序": 27, "运行序": 19, "点类型": 1, "区组": 1, "shade": "暗", "color": "red", "Dist-T": "C"},
    {"标准序": 35, "运行序": 20, "点类型": 1, "区组": 1, "shade": "暗", "color": "blue", "Dist-T": "C"},
    {"标准序": 22, "运行序": 21, "点类型": 1, "区组": 1, "shade": "明", "color": "cyan", "Dist-T": "B"},
    {"标准序": 44, "运行序": 22, "点类型": 1, "区组": 1, "shade": "暗", "color": "purple", "Dist-T": "D"},
    {"标准序": 34, "运行序": 23, "点类型": 1, "区组": 1, "shade": "暗", "color": "blue", "Dist-T": "B"},
    {"标准序": 1, "运行序": 24, "点类型": 1, "区组": 1, "shade": "明", "color": "red", "Dist-T": "A"},
    {"标准序": 25, "运行序": 25, "点类型": 1, "区组": 1, "shade": "暗", "color": "red", "Dist-T": "A"},
    {"标准序": 28, "运行序": 26, "点类型": 1, "区组": 1, "shade": "暗", "color": "red", "Dist-T": "D"},
    {"标准序": 48, "运行序": 27, "点类型": 1, "区组": 1, "shade": "暗", "color": "cyan", "Dist-T": "D"},
    {"标准序": 20, "运行序": 28, "点类型": 1, "区组": 1, "shade": "明", "color": "purple", "Dist-T": "D"},
    {"标准序": 6, "运行序": 29, "点类型": 1, "区组": 1, "shade": "明", "color": "green", "Dist-T": "B"},
    {"标准序": 9, "运行序": 30, "点类型": 1, "区组": 1, "shade": "明", "color": "blue", "Dist-T": "A"},
    {"标准序": 39, "运行序": 31, "点类型": 1, "区组": 1, "shade": "暗", "color": "yellow", "Dist-T": "C"},
    {"标准序": 19, "运行序": 32, "点类型": 1, "区组": 1, "shade": "明", "color": "purple", "Dist-T": "C"},
    {"标准序": 13, "运行序": 33, "点类型": 1, "区组": 1, "shade": "明", "color": "yellow", "Dist-T": "A"},
    {"标准序": 31, "运行序": 34, "点类型": 1, "区组": 1, "shade": "暗", "color": "green", "Dist-T": "C"},
    {"标准序": 15, "运行序": 35, "点类型": 1, "区组": 1, "shade": "明", "color": "yellow", "Dist-T": "C"},
    {"标准序": 21, "运行序": 36, "点类型": 1, "区组": 1, "shade": "明", "color": "cyan", "Dist-T": "A"},
    {"标准序": 29, "运行序": 37, "点类型": 1, "区组": 1, "shade": "暗", "color": "green", "Dist-T": "A"},
    {"标准序": 11, "运行序": 38, "点类型": 1, "区组": 1, "shade": "明", "color": "blue", "Dist-T": "C"},
    {"标准序": 47, "运行序": 39, "点类型": 1, "区组": 1, "shade": "暗", "color": "cyan", "Dist-T": "C"},
    {"标准序": 37, "运行序": 40, "点类型": 1, "区组": 1, "shade": "暗", "color": "yellow", "Dist-T": "A"},
    {"标准序": 18, "运行序": 41, "点类型": 1, "区组": 1, "shade": "明", "color": "purple", "Dist-T": "B"},
    {"标准序": 23, "运行序": 42, "点类型": 1, "区组": 1, "shade": "明", "color": "cyan", "Dist-T": "C"},
    {"标准序": 4, "运行序": 43, "点类型": 1, "区组": 1, "shade": "明", "color": "red", "Dist-T": "D"},
    {"标准序": 45, "运行序": 44, "点类型": 1, "区组": 1, "shade": "暗", "color": "cyan", "Dist-T": "A"},
    {"标准序": 32, "运行序": 45, "点类型": 1, "区组": 1, "shade": "暗", "color": "green", "Dist-T": "D"},
    {"标准序": 24, "运行序": 46, "点类型": 1, "区组": 1, "shade": "明", "color": "cyan", "Dist-T": "D"},
    {"标准序": 26, "运行序": 47, "点类型": 1, "区组": 1, "shade": "暗", "color": "red", "Dist-T": "B"},
    {"标准序": 5, "运行序": 48, "点类型": 1, "区组": 1, "shade": "明", "color": "green", "Dist-T": "A"}
]

function f2(color_no_hole) {
    let variables = [], ans, target
    for (let i = 0; i < color_no_hole.length; i++) {
        let v1 = ['circle', 'circle', 'circle', 'circle']
        let stim_color = getArrayItems(stimColorName, 4)
        if (color_no_hole[i]["Dist-T"] === "A") target = 0
        else if (color_no_hole[i]["Dist-T"] === "B") target = 1
        else if (color_no_hole[i]["Dist-T"] === "C") target = 2
        else target = 3
        ans = anss[target]
        if (color_no_hole[i]["shade"] === "明") stim_color[target] = "light" + color_no_hole[i]["color"]
        else stim_color[target] = "dark" + color_no_hole[i]["color"]
        variables.push({
            size: '4',
            v1: v1,
            color: stim_color,
            shade: color_no_hole[i]["shade"],
            target: target,
            type: "color",
            ans: ans
        })
    }
    return variables
}

let shape_no_hole = [
    {"标准序": 5, "运行序": 1, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A"},
    {"标准序": 1, "运行序": 2, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A"},
    {"标准序": 7, "运行序": 3, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C"},
    {"标准序": 2, "运行序": 4, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B"},
    {"标准序": 3, "运行序": 5, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C"},
    {"标准序": 4, "运行序": 6, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D"},
    {"标准序": 8, "运行序": 7, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D"},
    {"标准序": 6, "运行序": 8, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B"}
]

function f3(shape_no_hole) {
    let variables = [], ans, target
    for (let i = 0; i < shape_no_hole.length; i++) {
        let v1 = shuffle(shape)
        if (shape_no_hole[i]["STIM-T"] === "A") {
            ans = "4"
            target = 0
        } else if (shape_no_hole[i]["STIM-T"] === "B") {
            ans = "8"
            target = 1
        } else if (shape_no_hole[i]["STIM-T"] === "C") {
            ans = "6"
            target = 2
        } else {
            ans = "2"
            target = 3
        }
        if (shape_no_hole[i]["SHAPE"] === "triangle") v1.splice(target, 0, "triangle")
        else v1.splice(target, 0, "circle")
        variables.push({
            size: '4',
            v1: v1,
            shape: shape_no_hole[i]["SHAPE"],
            target: target,
            type: "shape",
            ans: ans
        })
    }
    return variables
}

//memory_exam中
//一个48个
let hole_no_hole_TopoVSShape = [
    {"标准序": 21, "运行序": 1, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "STIM-D": 3},
    {"标准序": 35, "运行序": 2, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "D", "STIM-D": 2},
    {"标准序": 10, "运行序": 3, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "STIM-D": 1},
    {"标准序": 48, "运行序": 4, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "D", "STIM-D": 3},
    {"标准序": 45, "运行序": 5, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "C", "STIM-D": 3},
    {"标准序": 33, "运行序": 6, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "C", "STIM-D": 3},
    {"标准序": 44, "运行序": 7, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "C", "STIM-D": 2},
    {"标准序": 38, "运行序": 8, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "A", "STIM-D": 2},
    {"标准序": 2, "运行序": 9, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "STIM-D": 2},
    {"标准序": 23, "运行序": 10, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "STIM-D": 2},
    {"标准序": 6, "运行序": 11, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "STIM-D": 3},
    {"标准序": 18, "运行序": 12, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "STIM-D": 3},
    {"标准序": 47, "运行序": 13, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "D", "STIM-D": 2},
    {"标准序": 22, "运行序": 14, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "STIM-D": 1},
    {"标准序": 1, "运行序": 15, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "STIM-D": 1},
    {"标准序": 46, "运行序": 16, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "D", "STIM-D": 1},
    {"标准序": 4, "运行序": 17, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "STIM-D": 1},
    {"标准序": 34, "运行序": 18, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "D", "STIM-D": 1},
    {"标准序": 37, "运行序": 19, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "A", "STIM-D": 1},
    {"标准序": 27, "运行序": 20, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "A", "STIM-D": 3},
    {"标准序": 24, "运行序": 21, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "D", "STIM-D": 3},
    {"标准序": 13, "运行序": 22, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "STIM-D": 1},
    {"标准序": 29, "运行序": 23, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "B", "STIM-D": 2},
    {"标准序": 14, "运行序": 24, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "STIM-D": 2},
    {"标准序": 17, "运行序": 25, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "STIM-D": 2},
    {"标准序": 9, "运行序": 26, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "STIM-D": 3},
    {"标准序": 25, "运行序": 27, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "A", "STIM-D": 1},
    {"标准序": 20, "运行序": 28, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "STIM-D": 2},
    {"标准序": 42, "运行序": 29, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "B", "STIM-D": 3},
    {"标准序": 39, "运行序": 30, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "A", "STIM-D": 3},
    {"标准序": 8, "运行序": 31, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "STIM-D": 2},
    {"标准序": 31, "运行序": 32, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "C", "STIM-D": 1},
    {"标准序": 19, "运行序": 33, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "C", "STIM-D": 1},
    {"标准序": 30, "运行序": 34, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "B", "STIM-D": 3},
    {"标准序": 3, "运行序": 35, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "A", "STIM-D": 3},
    {"标准序": 12, "运行序": 36, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "STIM-D": 3},
    {"标准序": 28, "运行序": 37, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "B", "STIM-D": 1},
    {"标准序": 41, "运行序": 38, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "B", "STIM-D": 2},
    {"标准序": 40, "运行序": 39, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "B", "STIM-D": 1},
    {"标准序": 43, "运行序": 40, "点类型": 1, "区组": 1, "SHAPE": "diamond", "STIM-T": "C", "STIM-D": 1},
    {"标准序": 5, "运行序": 41, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "B", "STIM-D": 2},
    {"标准序": 7, "运行序": 42, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "C", "STIM-D": 1},
    {"标准序": 16, "运行序": 43, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "B", "STIM-D": 1},
    {"标准序": 36, "运行序": 44, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "D", "STIM-D": 3},
    {"标准序": 26, "运行序": 45, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "A", "STIM-D": 2},
    {"标准序": 32, "运行序": 46, "点类型": 1, "区组": 1, "SHAPE": "rect", "STIM-T": "C", "STIM-D": 2},
    {"标准序": 11, "运行序": 47, "点类型": 1, "区组": 1, "SHAPE": "circle", "STIM-T": "D", "STIM-D": 2},
    {"标准序": 15, "运行序": 48, "点类型": 1, "区组": 1, "SHAPE": "triangle", "STIM-T": "A", "STIM-D": 3}
]

function f4(hole_no_hole_TopoVSShape) {
    let anss = ["4", "8", "6", "2"]
    let variables = [], ans, target, distractor_num
    const stimArray = ["rect", "triangle", "circle", "diamond"]
    for (let i = 0; i < hole_no_hole_TopoVSShape.length; i++) {
        if (hole_no_hole_TopoVSShape[i]["STIM-T"] === "A") {
            ans = "4"
            target = 0
            distractor_num = hole_no_hole_TopoVSShape[i]["STIM-D"]
        } else if (hole_no_hole_TopoVSShape[i]["STIM-T"] === "B") {
            ans = "8"
            target = 1
            if (hole_no_hole_TopoVSShape[i]["STIM-D"] === 1) distractor_num = 0
            else distractor_num = hole_no_hole_TopoVSShape[i]["STIM-D"]
        } else if (hole_no_hole_TopoVSShape[i]["STIM-T"] === "C") {
            ans = "6"
            target = 2
            if (hole_no_hole_TopoVSShape[i]["STIM-D"] === 3) distractor_num = 3
            else distractor_num = hole_no_hole_TopoVSShape[i]["STIM-D"] - 1
        } else {
            ans = "2"
            target = 3
            distractor_num = hole_no_hole_TopoVSShape[i]["STIM-D"] - 1
        }
        let v1 = RandomArray(stimArray, target, "hole-no-hole", hole_no_hole_TopoVSShape[i]["SHAPE"])
        if (v1[distractor_num] === "circle") v1[distractor_num] = "ring_1"
        else v1[distractor_num] = v1[distractor_num] + "_1"
        variables.push({
            size: '4',
            v1: v1,
            target: hole_no_hole_TopoVSShape[i]["SHAPE"],
            type: "hole-no-hole",
            ans: ans,
            distractor: v1[distractor_num],
            distractor_dist: anss[distractor_num],
            shapeORcolor: 0
        })
    }
    return variables
}

let hole_no_hole_ColorVSShape = [
    {"标准序": 1, "运行序": 1, "点类型": 1, "区组": 1, "STIM-D": 1, "STIM-T": "A"},
    {"标准序": 4, "运行序": 2, "点类型": 1, "区组": 1, "STIM-D": 1, "STIM-T": "D"},
    {"标准序": 12, "运行序": 3, "点类型": 1, "区组": 1, "STIM-D": 3, "STIM-T": "D"},
    {"标准序": 5, "运行序": 4, "点类型": 1, "区组": 1, "STIM-D": 2, "STIM-T": "A"},
    {"标准序": 11, "运行序": 5, "点类型": 1, "区组": 1, "STIM-D": 3, "STIM-T": "C"},
    {"标准序": 7, "运行序": 6, "点类型": 1, "区组": 1, "STIM-D": 2, "STIM-T": "C"},
    {"标准序": 2, "运行序": 7, "点类型": 1, "区组": 1, "STIM-D": 1, "STIM-T": "B"},
    {"标准序": 8, "运行序": 8, "点类型": 1, "区组": 1, "STIM-D": 2, "STIM-T": "D"},
    {"标准序": 3, "运行序": 9, "点类型": 1, "区组": 1, "STIM-D": 1, "STIM-T": "C"},
    {"标准序": 10, "运行序": 10, "点类型": 1, "区组": 1, "STIM-D": 3, "STIM-T": "B"},
    {"标准序": 9, "运行序": 11, "点类型": 1, "区组": 1, "STIM-D": 3, "STIM-T": "A"},
    {"标准序": 6, "运行序": 12, "点类型": 1, "区组": 1, "STIM-D": 2, "STIM-T": "B"}
]

let hole_no_hole_ColorVSShape1 = [
    {"标准序": 72, "运行序": 1, "点类型": 1, "区组": 1, "dist-T": "D", "color": "cyan", "dist-D": 3},
    {"标准序": 49, "运行序": 2, "点类型": 1, "区组": 1, "dist-T": "C", "color": "purple", "dist-D": 1},
    {"标准序": 18, "运行序": 3, "点类型": 1, "区组": 1, "dist-T": "A", "color": "cyan", "dist-D": 3},
    {"标准序": 51, "运行序": 4, "点类型": 1, "区组": 1, "dist-T": "C", "color": "purple", "dist-D": 3},
    {"标准序": 22, "运行序": 5, "点类型": 1, "区组": 1, "dist-T": "B", "color": "green", "dist-D": 1},
    {"标准序": 28, "运行序": 6, "点类型": 1, "区组": 1, "dist-T": "B", "color": "yellow", "dist-D": 1},
    {"标准序": 67, "运行序": 7, "点类型": 1, "区组": 1, "dist-T": "D", "color": "purple", "dist-D": 1},
    {"标准序": 29, "运行序": 8, "点类型": 1, "区组": 1, "dist-T": "B", "color": "yellow", "dist-D": 2},
    {"标准序": 52, "运行序": 9, "点类型": 1, "区组": 1, "dist-T": "C", "color": "cyan", "dist-D": 1},
    {"标准序": 19, "运行序": 10, "点类型": 1, "区组": 1, "dist-T": "B", "color": "red", "dist-D": 1},
    {"标准序": 11, "运行序": 11, "点类型": 1, "区组": 1, "dist-T": "A", "color": "yellow", "dist-D": 2},
    {"标准序": 17, "运行序": 12, "点类型": 1, "区组": 1, "dist-T": "A", "color": "cyan", "dist-D": 2},
    {"标准序": 61, "运行序": 13, "点类型": 1, "区组": 1, "dist-T": "D", "color": "blue", "dist-D": 1},
    {"标准序": 38, "运行序": 14, "点类型": 1, "区组": 1, "dist-T": "C", "color": "red", "dist-D": 2},
    {"标准序": 27, "运行序": 15, "点类型": 1, "区组": 1, "dist-T": "B", "color": "blue", "dist-D": 3},
    {"标准序": 64, "运行序": 16, "点类型": 1, "区组": 1, "dist-T": "D", "color": "yellow", "dist-D": 1},
    {"标准序": 5, "运行序": 17, "点类型": 1, "区组": 1, "dist-T": "A", "color": "green", "dist-D": 2},
    {"标准序": 43, "运行序": 18, "点类型": 1, "区组": 1, "dist-T": "C", "color": "blue", "dist-D": 1},
    {"标准序": 10, "运行序": 19, "点类型": 1, "区组": 1, "dist-T": "A", "color": "yellow", "dist-D": 1},
    {"标准序": 57, "运行序": 20, "点类型": 1, "区组": 1, "dist-T": "D", "color": "red", "dist-D": 3},
    {"标准序": 7, "运行序": 21, "点类型": 1, "区组": 1, "dist-T": "A", "color": "blue", "dist-D": 1},
    {"标准序": 55, "运行序": 22, "点类型": 1, "区组": 1, "dist-T": "D", "color": "red", "dist-D": 1},
    {"标准序": 14, "运行序": 23, "点类型": 1, "区组": 1, "dist-T": "A", "color": "purple", "dist-D": 2},
    {"标准序": 48, "运行序": 24, "点类型": 1, "区组": 1, "dist-T": "C", "color": "yellow", "dist-D": 3},
    {"标准序": 30, "运行序": 25, "点类型": 1, "区组": 1, "dist-T": "B", "color": "yellow", "dist-D": 3},
    {"标准序": 54, "运行序": 26, "点类型": 1, "区组": 1, "dist-T": "C", "color": "cyan", "dist-D": 3},
    {"标准序": 20, "运行序": 27, "点类型": 1, "区组": 1, "dist-T": "B", "color": "red", "dist-D": 2},
    {"标准序": 32, "运行序": 28, "点类型": 1, "区组": 1, "dist-T": "B", "color": "purple", "dist-D": 2},
    {"标准序": 26, "运行序": 29, "点类型": 1, "区组": 1, "dist-T": "B", "color": "blue", "dist-D": 2},
    {"标准序": 36, "运行序": 30, "点类型": 1, "区组": 1, "dist-T": "B", "color": "cyan", "dist-D": 3},
    {"标准序": 35, "运行序": 31, "点类型": 1, "区组": 1, "dist-T": "B", "color": "cyan", "dist-D": 2},
    {"标准序": 37, "运行序": 32, "点类型": 1, "区组": 1, "dist-T": "C", "color": "red", "dist-D": 1},
    {"标准序": 50, "运行序": 33, "点类型": 1, "区组": 1, "dist-T": "C", "color": "purple", "dist-D": 2},
    {"标准序": 60, "运行序": 34, "点类型": 1, "区组": 1, "dist-T": "D", "color": "green", "dist-D": 3},
    {"标准序": 3, "运行序": 35, "点类型": 1, "区组": 1, "dist-T": "A", "color": "red", "dist-D": 3},
    {"标准序": 41, "运行序": 36, "点类型": 1, "区组": 1, "dist-T": "C", "color": "green", "dist-D": 2},
    {"标准序": 68, "运行序": 37, "点类型": 1, "区组": 1, "dist-T": "D", "color": "purple", "dist-D": 2},
    {"标准序": 12, "运行序": 38, "点类型": 1, "区组": 1, "dist-T": "A", "color": "yellow", "dist-D": 3},
    {"标准序": 31, "运行序": 39, "点类型": 1, "区组": 1, "dist-T": "B", "color": "purple", "dist-D": 1},
    {"标准序": 69, "运行序": 40, "点类型": 1, "区组": 1, "dist-T": "D", "color": "purple", "dist-D": 3},
    {"标准序": 44, "运行序": 41, "点类型": 1, "区组": 1, "dist-T": "C", "color": "blue", "dist-D": 2},
    {"标准序": 47, "运行序": 42, "点类型": 1, "区组": 1, "dist-T": "C", "color": "yellow", "dist-D": 2},
    {"标准序": 34, "运行序": 43, "点类型": 1, "区组": 1, "dist-T": "B", "color": "cyan", "dist-D": 1},
    {"标准序": 39, "运行序": 44, "点类型": 1, "区组": 1, "dist-T": "C", "color": "red", "dist-D": 3},
    {"标准序": 58, "运行序": 45, "点类型": 1, "区组": 1, "dist-T": "D", "color": "green", "dist-D": 1},
    {"标准序": 45, "运行序": 46, "点类型": 1, "区组": 1, "dist-T": "C", "color": "blue", "dist-D": 3},
    {"标准序": 9, "运行序": 47, "点类型": 1, "区组": 1, "dist-T": "A", "color": "blue", "dist-D": 3},
    {"标准序": 15, "运行序": 48, "点类型": 1, "区组": 1, "dist-T": "A", "color": "purple", "dist-D": 3},
    {"标准序": 63, "运行序": 49, "点类型": 1, "区组": 1, "dist-T": "D", "color": "blue", "dist-D": 3},
    {"标准序": 46, "运行序": 50, "点类型": 1, "区组": 1, "dist-T": "C", "color": "yellow", "dist-D": 1},
    {"标准序": 59, "运行序": 51, "点类型": 1, "区组": 1, "dist-T": "D", "color": "green", "dist-D": 2},
    {"标准序": 13, "运行序": 52, "点类型": 1, "区组": 1, "dist-T": "A", "color": "purple", "dist-D": 1},
    {"标准序": 1, "运行序": 53, "点类型": 1, "区组": 1, "dist-T": "A", "color": "red", "dist-D": 1},
    {"标准序": 70, "运行序": 54, "点类型": 1, "区组": 1, "dist-T": "D", "color": "cyan", "dist-D": 1},
    {"标准序": 71, "运行序": 55, "点类型": 1, "区组": 1, "dist-T": "D", "color": "cyan", "dist-D": 2},
    {"标准序": 4, "运行序": 56, "点类型": 1, "区组": 1, "dist-T": "A", "color": "green", "dist-D": 1},
    {"标准序": 6, "运行序": 57, "点类型": 1, "区组": 1, "dist-T": "A", "color": "green", "dist-D": 3},
    {"标准序": 16, "运行序": 58, "点类型": 1, "区组": 1, "dist-T": "A", "color": "cyan", "dist-D": 1},
    {"标准序": 62, "运行序": 59, "点类型": 1, "区组": 1, "dist-T": "D", "color": "blue", "dist-D": 2},
    {"标准序": 42, "运行序": 60, "点类型": 1, "区组": 1, "dist-T": "C", "color": "green", "dist-D": 3},
    {"标准序": 24, "运行序": 61, "点类型": 1, "区组": 1, "dist-T": "B", "color": "green", "dist-D": 3},
    {"标准序": 33, "运行序": 62, "点类型": 1, "区组": 1, "dist-T": "B", "color": "purple", "dist-D": 3},
    {"标准序": 65, "运行序": 63, "点类型": 1, "区组": 1, "dist-T": "D", "color": "yellow", "dist-D": 2},
    {"标准序": 2, "运行序": 64, "点类型": 1, "区组": 1, "dist-T": "A", "color": "red", "dist-D": 2},
    {"标准序": 25, "运行序": 65, "点类型": 1, "区组": 1, "dist-T": "B", "color": "blue", "dist-D": 1},
    {"标准序": 23, "运行序": 66, "点类型": 1, "区组": 1, "dist-T": "B", "color": "green", "dist-D": 2},
    {"标准序": 8, "运行序": 67, "点类型": 1, "区组": 1, "dist-T": "A", "color": "blue", "dist-D": 2},
    {"标准序": 56, "运行序": 68, "点类型": 1, "区组": 1, "dist-T": "D", "color": "red", "dist-D": 2},
    {"标准序": 21, "运行序": 69, "点类型": 1, "区组": 1, "dist-T": "B", "color": "red", "dist-D": 3},
    {"标准序": 53, "运行序": 70, "点类型": 1, "区组": 1, "dist-T": "C", "color": "cyan", "dist-D": 2},
    {"标准序": 66, "运行序": 71, "点类型": 1, "区组": 1, "dist-T": "D", "color": "yellow", "dist-D": 3},
    {"标准序": 40, "运行序": 72, "点类型": 1, "区组": 1, "dist-T": "C", "color": "green", "dist-D": 1}]

function f5(hole_no_hole_ColorVSShape) {
    let anss = ["4", "8", "6", "2"]
    let variables = [], ans, target, distractor_num
    for (let i = 0; i < hole_no_hole_ColorVSShape.length; i++) {
        let v1 = ['circle', 'circle', 'circle', 'circle']
        let stim_color = getArrayItems(stimColorName, 4)
        if (hole_no_hole_ColorVSShape[i]["STIM-T"] === "A") {
            ans = "4"
            target = 0
            distractor_num = hole_no_hole_ColorVSShape[i]["STIM-D"]
        } else if (hole_no_hole_ColorVSShape[i]["STIM-T"] === "B") {
            ans = "8"
            target = 1
            if (hole_no_hole_ColorVSShape[i]["STIM-D"] === 1) distractor_num = 0
            else distractor_num = hole_no_hole_ColorVSShape[i]["STIM-D"]
        } else if (hole_no_hole_ColorVSShape[i]["STIM-T"] === "C") {
            ans = "6"
            target = 2
            if (hole_no_hole_ColorVSShape[i]["STIM-D"] === 3) distractor_num = 3
            else distractor_num = hole_no_hole_ColorVSShape[i]["STIM-D"] - 1
        } else {
            ans = "2"
            target = 3
            distractor_num = hole_no_hole_ColorVSShape[i]["STIM-D"] - 1
        }
        v1[distractor_num] = "ring_1"
        variables.push({
            size: '4',
            v1: v1,
            color: stim_color,
            target: target,
            type: "hole-no-hole",
            ans: ans,
            distractor: distractor_num,
            distractor_dist: anss[distractor_num],
            shapeORcolor: 1
        })
    }
    return variables
}


let vari = [{"标准序": 98, "运行序": 1, "点类型": 1, "区组": 1, "color": "yellow", "明": 1, "暗": "1'", "T": "B"},
    {"标准序": 229, "运行序": 2, "点类型": 1, "区组": 1, "color": "blue", "明": 4, "暗": "1'", "T": "A"},
    {"标准序": 193, "运行序": 3, "点类型": 1, "区组": 1, "color": "blue", "明": 1, "暗": "1'", "T": "A"},
    {"标准序": 175, "运行序": 4, "点类型": 1, "区组": 1, "color": "cyan", "明": 3, "暗": "2'", "T": "C"},
    {"标准序": 90, "运行序": 5, "点类型": 1, "区组": 1, "color": "green", "明": 4, "暗": "2'", "T": "B"},
    {"标准序": 170, "运行序": 6, "点类型": 1, "区组": 1, "color": "cyan", "明": 3, "暗": "1'", "T": "B"},
    {"标准序": 33, "运行序": 7, "点类型": 1, "区组": 1, "color": "red", "明": 3, "暗": "3'", "T": "A"},
    {"标准序": 203, "运行序": 8, "点类型": 1, "区组": 1, "color": "blue", "明": 1, "暗": "3'", "T": "C"},
    {"标准序": 169, "运行序": 9, "点类型": 1, "区组": 1, "color": "cyan", "明": 3, "暗": "1'", "T": "A"},
    {"标准序": 174, "运行序": 10, "点类型": 1, "区组": 1, "color": "cyan", "明": 3, "暗": "2'", "T": "B"}, {
        "标准序": 213,
        "运行序": 11,
        "点类型": 1,
        "区组": 1,
        "color": "blue",
        "明": 2,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 70, "运行序": 12, "点类型": 1, "区组": 1, "color": "green", "明": 2, "暗": "3'", "T": "B"}, {
        "标准序": 272,
        "运行序": 13,
        "点类型": 1,
        "区组": 1,
        "color": "purple",
        "明": 3,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 74, "运行序": 14, "点类型": 1, "区组": 1, "color": "green", "明": 3, "暗": "1'", "T": "B"}, {
        "标准序": 278,
        "运行序": 15,
        "点类型": 1,
        "区组": 1,
        "color": "purple",
        "明": 4,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 69, "运行序": 16, "点类型": 1, "区组": 1, "color": "green", "明": 2, "暗": "3'", "T": "A"}, {
        "标准序": 242,
        "运行序": 17,
        "点类型": 1,
        "区组": 1,
        "color": "purple",
        "明": 1,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 277, "运行序": 18, "点类型": 1, "区组": 1, "color": "purple", "明": 4, "暗": "1'", "T": "A"}, {
        "标准序": 88,
        "运行序": 19,
        "点类型": 1,
        "区组": 1,
        "color": "green",
        "明": 4,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 55, "运行序": 20, "点类型": 1, "区组": 1, "color": "green", "明": 1, "暗": "2'", "T": "C"}, {
        "标准序": 187,
        "运行序": 21,
        "点类型": 1,
        "区组": 1,
        "color": "cyan",
        "明": 4,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 59, "运行序": 22, "点类型": 1, "区组": 1, "color": "green", "明": 1, "暗": "3'", "T": "C"}, {
        "标准序": 279,
        "运行序": 23,
        "点类型": 1,
        "区组": 1,
        "color": "purple",
        "明": 4,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 270, "运行序": 24, "点类型": 1, "区组": 1, "color": "purple", "明": 3, "暗": "2'", "T": "B"}, {
        "标准序": 248,
        "运行序": 25,
        "点类型": 1,
        "区组": 2,
        "color": "purple",
        "明": 1,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 48, "运行序": 26, "点类型": 1, "区组": 2, "color": "red", "明": 4, "暗": "3'", "T": "D"}, {
        "标准序": 235,
        "运行序": 27,
        "点类型": 1,
        "区组": 2,
        "color": "blue",
        "明": 4,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 192, "运行序": 28, "点类型": 1, "区组": 2, "color": "cyan", "明": 4, "暗": "3'", "T": "D"}, {
        "标准序": 268,
        "运行序": 29,
        "点类型": 1,
        "区组": 2,
        "color": "purple",
        "明": 3,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 179, "运行序": 30, "点类型": 1, "区组": 2, "color": "cyan", "明": 3, "暗": "3'", "T": "C"}, {
        "标准序": 224,
        "运行序": 31,
        "点类型": 1,
        "区组": 2,
        "color": "blue",
        "明": 3,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 75, "运行序": 32, "点类型": 1, "区组": 2, "color": "green", "明": 3, "暗": "1'", "T": "C"}, {
        "标准序": 243,
        "运行序": 33,
        "点类型": 1,
        "区组": 2,
        "color": "purple",
        "明": 1,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 274, "运行序": 34, "点类型": 1, "区组": 2, "color": "purple", "明": 3, "暗": "3'", "T": "B"}, {
        "标准序": 186,
        "运行序": 35,
        "点类型": 1,
        "区组": 2,
        "color": "cyan",
        "明": 4,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 118, "运行序": 36, "点类型": 1, "区组": 2, "color": "yellow", "明": 2, "暗": "3'", "T": "B"}, {
        "标准序": 4,
        "运行序": 37,
        "点类型": 1,
        "区组": 2,
        "color": "red",
        "明": 1,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 26, "运行序": 38, "点类型": 1, "区组": 2, "color": "red", "明": 3, "暗": "1'", "T": "B"}, {
        "标准序": 145,
        "运行序": 39,
        "点类型": 1,
        "区组": 2,
        "color": "cyan",
        "明": 1,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 266, "运行序": 40, "点类型": 1, "区组": 2, "color": "purple", "明": 3, "暗": "1'", "T": "B"}, {
        "标准序": 265,
        "运行序": 41,
        "点类型": 1,
        "区组": 2,
        "color": "purple",
        "明": 3,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 133, "运行序": 42, "点类型": 1, "区组": 2, "color": "yellow", "明": 4, "暗": "1'", "T": "A"}, {
        "标准序": 172,
        "运行序": 43,
        "点类型": 1,
        "区组": 2,
        "color": "cyan",
        "明": 3,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 31, "运行序": 44, "点类型": 1, "区组": 2, "color": "red", "明": 3, "暗": "2'", "T": "C"}, {
        "标准序": 81,
        "运行序": 45,
        "点类型": 1,
        "区组": 2,
        "color": "green",
        "明": 3,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 245, "运行序": 46, "点类型": 1, "区组": 2, "color": "purple", "明": 1, "暗": "2'", "T": "A"}, {
        "标准序": 246,
        "运行序": 47,
        "点类型": 1,
        "区组": 2,
        "color": "purple",
        "明": 1,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 12, "运行序": 48, "点类型": 1, "区组": 2, "color": "red", "明": 1, "暗": "3'", "T": "D"}, {
        "标准序": 204,
        "运行序": 49,
        "点类型": 1,
        "区组": 3,
        "color": "blue",
        "明": 1,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 30, "运行序": 50, "点类型": 1, "区组": 3, "color": "red", "明": 3, "暗": "2'", "T": "B"}, {
        "标准序": 219,
        "运行序": 51,
        "点类型": 1,
        "区组": 3,
        "color": "blue",
        "明": 3,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 267, "运行序": 52, "点类型": 1, "区组": 3, "color": "purple", "明": 3, "暗": "1'", "T": "C"}, {
        "标准序": 205,
        "运行序": 53,
        "点类型": 1,
        "区组": 3,
        "color": "blue",
        "明": 2,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 143, "运行序": 54, "点类型": 1, "区组": 3, "color": "yellow", "明": 4, "暗": "3'", "T": "C"}, {
        "标准序": 151,
        "运行序": 55,
        "点类型": 1,
        "区组": 3,
        "color": "cyan",
        "明": 1,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 191, "运行序": 56, "点类型": 1, "区组": 3, "color": "cyan", "明": 4, "暗": "3'", "T": "C"}, {
        "标准序": 25,
        "运行序": 57,
        "点类型": 1,
        "区组": 3,
        "color": "red",
        "明": 3,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 261, "运行序": 58, "点类型": 1, "区组": 3, "color": "purple", "明": 2, "暗": "3'", "T": "A"}, {
        "标准序": 283,
        "运行序": 59,
        "点类型": 1,
        "区组": 3,
        "color": "purple",
        "明": 4,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 185, "运行序": 60, "点类型": 1, "区组": 3, "color": "cyan", "明": 4, "暗": "2'", "T": "A"}, {
        "标准序": 162,
        "运行序": 61,
        "点类型": 1,
        "区组": 3,
        "color": "cyan",
        "明": 2,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 225, "运行序": 62, "点类型": 1, "区组": 3, "color": "blue", "明": 3, "暗": "3'", "T": "A"}, {
        "标准序": 73,
        "运行序": 63,
        "点类型": 1,
        "区组": 3,
        "color": "green",
        "明": 3,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 282, "运行序": 64, "点类型": 1, "区组": 3, "color": "purple", "明": 4, "暗": "2'", "T": "B"}, {
        "标准序": 284,
        "运行序": 65,
        "点类型": 1,
        "区组": 3,
        "color": "purple",
        "明": 4,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 221, "运行序": 66, "点类型": 1, "区组": 3, "color": "blue", "明": 3, "暗": "2'", "T": "A"}, {
        "标准序": 202,
        "运行序": 67,
        "点类型": 1,
        "区组": 3,
        "color": "blue",
        "明": 1,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 125, "运行序": 68, "点类型": 1, "区组": 3, "color": "yellow", "明": 3, "暗": "2'", "T": "A"}, {
        "标准序": 176,
        "运行序": 69,
        "点类型": 1,
        "区组": 3,
        "color": "cyan",
        "明": 3,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 34, "运行序": 70, "点类型": 1, "区组": 3, "color": "red", "明": 3, "暗": "3'", "T": "B"}, {
        "标准序": 5,
        "运行序": 71,
        "点类型": 1,
        "区组": 3,
        "color": "red",
        "明": 1,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 194, "运行序": 72, "点类型": 1, "区组": 3, "color": "blue", "明": 1, "暗": "1'", "T": "B"}, {
        "标准序": 263,
        "运行序": 73,
        "点类型": 1,
        "区组": 4,
        "color": "purple",
        "明": 2,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 36, "运行序": 74, "点类型": 1, "区组": 4, "color": "red", "明": 3, "暗": "3'", "T": "D"}, {
        "标准序": 184,
        "运行序": 75,
        "点类型": 1,
        "区组": 4,
        "color": "cyan",
        "明": 4,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 153, "运行序": 76, "点类型": 1, "区组": 4, "color": "cyan", "明": 1, "暗": "3'", "T": "A"}, {
        "标准序": 3,
        "运行序": 77,
        "点类型": 1,
        "区组": 4,
        "color": "red",
        "明": 1,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 199, "运行序": 78, "点类型": 1, "区组": 4, "color": "blue", "明": 1, "暗": "2'", "T": "C"}, {
        "标准序": 13,
        "运行序": 79,
        "点类型": 1,
        "区组": 4,
        "color": "red",
        "明": 2,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 47, "运行序": 80, "点类型": 1, "区组": 4, "color": "red", "明": 4, "暗": "3'", "T": "C"}, {
        "标准序": 220,
        "运行序": 81,
        "点类型": 1,
        "区组": 4,
        "color": "blue",
        "明": 3,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 39, "运行序": 82, "点类型": 1, "区组": 4, "color": "red", "明": 4, "暗": "1'", "T": "C"}, {
        "标准序": 106,
        "运行序": 83,
        "点类型": 1,
        "区组": 4,
        "color": "yellow",
        "明": 1,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 178, "运行序": 84, "点类型": 1, "区组": 4, "color": "cyan", "明": 3, "暗": "3'", "T": "B"}, {
        "标准序": 253,
        "运行序": 85,
        "点类型": 1,
        "区组": 4,
        "color": "purple",
        "明": 2,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 11, "运行序": 86, "点类型": 1, "区组": 4, "color": "red", "明": 1, "暗": "3'", "T": "C"}, {
        "标准序": 228,
        "运行序": 87,
        "点类型": 1,
        "区组": 4,
        "color": "blue",
        "明": 3,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 142, "运行序": 88, "点类型": 1, "区组": 4, "color": "yellow", "明": 4, "暗": "3'", "T": "B"}, {
        "标准序": 285,
        "运行序": 89,
        "点类型": 1,
        "区组": 4,
        "color": "purple",
        "明": 4,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 127, "运行序": 90, "点类型": 1, "区组": 4, "color": "yellow", "明": 3, "暗": "2'", "T": "C"}, {
        "标准序": 198,
        "运行序": 91,
        "点类型": 1,
        "区组": 4,
        "color": "blue",
        "明": 1,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 260, "运行序": 92, "点类型": 1, "区组": 4, "color": "purple", "明": 2, "暗": "2'", "T": "D"}, {
        "标准序": 91,
        "运行序": 93,
        "点类型": 1,
        "区组": 4,
        "color": "green",
        "明": 4,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 22, "运行序": 94, "点类型": 1, "区组": 4, "color": "red", "明": 2, "暗": "3'", "T": "B"}, {
        "标准序": 35,
        "运行序": 95,
        "点类型": 1,
        "区组": 4,
        "color": "red",
        "明": 3,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 258, "运行序": 96, "点类型": 1, "区组": 4, "color": "purple", "明": 2, "暗": "2'", "T": "B"}, {
        "标准序": 159,
        "运行序": 97,
        "点类型": 1,
        "区组": 5,
        "color": "cyan",
        "明": 2,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 128, "运行序": 98, "点类型": 1, "区组": 5, "color": "yellow", "明": 3, "暗": "2'", "T": "D"}, {
        "标准序": 226,
        "运行序": 99,
        "点类型": 1,
        "区组": 5,
        "color": "blue",
        "明": 3,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 83, "运行序": 100, "点类型": 1, "区组": 5, "color": "green", "明": 3, "暗": "3'", "T": "C"}, {
        "标准序": 166,
        "运行序": 101,
        "点类型": 1,
        "区组": 5,
        "color": "cyan",
        "明": 2,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 122, "运行序": 102, "点类型": 1, "区组": 5, "color": "yellow", "明": 3, "暗": "1'", "T": "B"}, {
        "标准序": 241,
        "运行序": 103,
        "点类型": 1,
        "区组": 5,
        "color": "purple",
        "明": 1,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 180, "运行序": 104, "点类型": 1, "区组": 5, "color": "cyan", "明": 3, "暗": "3'", "T": "D"}, {
        "标准序": 61,
        "运行序": 105,
        "点类型": 1,
        "区组": 5,
        "color": "green",
        "明": 2,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 76, "运行序": 106, "点类型": 1, "区组": 5, "color": "green", "明": 3, "暗": "1'", "T": "D"}, {
        "标准序": 167,
        "运行序": 107,
        "点类型": 1,
        "区组": 5,
        "color": "cyan",
        "明": 2,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 149, "运行序": 108, "点类型": 1, "区组": 5, "color": "cyan", "明": 1, "暗": "2'", "T": "A"}, {
        "标准序": 116,
        "运行序": 109,
        "点类型": 1,
        "区组": 5,
        "color": "yellow",
        "明": 2,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 239, "运行序": 110, "点类型": 1, "区组": 5, "color": "blue", "明": 4, "暗": "3'", "T": "C"}, {
        "标准序": 230,
        "运行序": 111,
        "点类型": 1,
        "区组": 5,
        "color": "blue",
        "明": 4,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 100, "运行序": 112, "点类型": 1, "区组": 5, "color": "yellow", "明": 1, "暗": "1'", "T": "D"}, {
        "标准序": 264,
        "运行序": 113,
        "点类型": 1,
        "区组": 5,
        "color": "purple",
        "明": 2,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 102, "运行序": 114, "点类型": 1, "区组": 5, "color": "yellow", "明": 1, "暗": "2'", "T": "B"}, {
        "标准序": 273,
        "运行序": 115,
        "点类型": 1,
        "区组": 5,
        "color": "purple",
        "明": 3,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 80, "运行序": 116, "点类型": 1, "区组": 5, "color": "green", "明": 3, "暗": "2'", "T": "D"}, {
        "标准序": 132,
        "运行序": 117,
        "点类型": 1,
        "区组": 5,
        "color": "yellow",
        "明": 3,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 93, "运行序": 118, "点类型": 1, "区组": 5, "color": "green", "明": 4, "暗": "3'", "T": "A"}, {
        "标准序": 37,
        "运行序": 119,
        "点类型": 1,
        "区组": 5,
        "color": "red",
        "明": 4,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 249, "运行序": 120, "点类型": 1, "区组": 5, "color": "purple", "明": 1, "暗": "3'", "T": "A"}, {
        "标准序": 71,
        "运行序": 121,
        "点类型": 1,
        "区组": 6,
        "color": "green",
        "明": 2,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 168, "运行序": 122, "点类型": 1, "区组": 6, "color": "cyan", "明": 2, "暗": "3'", "T": "D"}, {
        "标准序": 124,
        "运行序": 123,
        "点类型": 1,
        "区组": 6,
        "color": "yellow",
        "明": 3,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 237, "运行序": 124, "点类型": 1, "区组": 6, "color": "blue", "明": 4, "暗": "3'", "T": "A"}, {
        "标准序": 227,
        "运行序": 125,
        "点类型": 1,
        "区组": 6,
        "color": "blue",
        "明": 3,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 281, "运行序": 126, "点类型": 1, "区组": 6, "color": "purple", "明": 4, "暗": "2'", "T": "A"}, {
        "标准序": 217,
        "运行序": 127,
        "点类型": 1,
        "区组": 6,
        "color": "blue",
        "明": 3,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 188, "运行序": 128, "点类型": 1, "区组": 6, "color": "cyan", "明": 4, "暗": "2'", "T": "D"}, {
        "标准序": 165,
        "运行序": 129,
        "点类型": 1,
        "区组": 6,
        "color": "cyan",
        "明": 2,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 115, "运行序": 130, "点类型": 1, "区组": 6, "color": "yellow", "明": 2, "暗": "2'", "T": "C"}, {
        "标准序": 17,
        "运行序": 131,
        "点类型": 1,
        "区组": 6,
        "color": "red",
        "明": 2,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 79, "运行序": 132, "点类型": 1, "区组": 6, "color": "green", "明": 3, "暗": "2'", "T": "C"}, {
        "标准序": 110,
        "运行序": 133,
        "点类型": 1,
        "区组": 6,
        "color": "yellow",
        "明": 2,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 14, "运行序": 134, "点类型": 1, "区组": 6, "color": "red", "明": 2, "暗": "1'", "T": "B"}, {
        "标准序": 56,
        "运行序": 135,
        "点类型": 1,
        "区组": 6,
        "color": "green",
        "明": 1,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 155, "运行序": 136, "点类型": 1, "区组": 6, "color": "cyan", "明": 1, "暗": "3'", "T": "C"}, {
        "标准序": 54,
        "运行序": 137,
        "点类型": 1,
        "区组": 6,
        "color": "green",
        "明": 1,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 123, "运行序": 138, "点类型": 1, "区组": 6, "color": "yellow", "明": 3, "暗": "1'", "T": "C"}, {
        "标准序": 129,
        "运行序": 139,
        "点类型": 1,
        "区组": 6,
        "color": "yellow",
        "明": 3,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 223, "运行序": 140, "点类型": 1, "区组": 6, "color": "blue", "明": 3, "暗": "2'", "T": "C"}, {
        "标准序": 197,
        "运行序": 141,
        "点类型": 1,
        "区组": 6,
        "color": "blue",
        "明": 1,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 15, "运行序": 142, "点类型": 1, "区组": 6, "color": "red", "明": 2, "暗": "1'", "T": "C"}, {
        "标准序": 97,
        "运行序": 143,
        "点类型": 1,
        "区组": 6,
        "color": "yellow",
        "明": 1,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 236, "运行序": 144, "点类型": 1, "区组": 6, "color": "blue", "明": 4, "暗": "2'", "T": "D"}, {
        "标准序": 41,
        "运行序": 145,
        "点类型": 1,
        "区组": 7,
        "color": "red",
        "明": 4,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 152, "运行序": 146, "点类型": 1, "区组": 7, "color": "cyan", "明": 1, "暗": "2'", "T": "D"}, {
        "标准序": 10,
        "运行序": 147,
        "点类型": 1,
        "区组": 7,
        "color": "red",
        "明": 1,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 183, "运行序": 148, "点类型": 1, "区组": 7, "color": "cyan", "明": 4, "暗": "1'", "T": "C"}, {
        "标准序": 46,
        "运行序": 149,
        "点类型": 1,
        "区组": 7,
        "color": "red",
        "明": 4,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 29, "运行序": 150, "点类型": 1, "区组": 7, "color": "red", "明": 3, "暗": "2'", "T": "A"}, {
        "标准序": 173,
        "运行序": 151,
        "点类型": 1,
        "区组": 7,
        "color": "cyan",
        "明": 3,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 275, "运行序": 152, "点类型": 1, "区组": 7, "color": "purple", "明": 3, "暗": "3'", "T": "C"}, {
        "标准序": 119,
        "运行序": 153,
        "点类型": 1,
        "区组": 7,
        "color": "yellow",
        "明": 2,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 23, "运行序": 154, "点类型": 1, "区组": 7, "color": "red", "明": 2, "暗": "3'", "T": "C"}, {
        "标准序": 215,
        "运行序": 155,
        "点类型": 1,
        "区组": 7,
        "color": "blue",
        "明": 2,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 58, "运行序": 156, "点类型": 1, "区组": 7, "color": "green", "明": 1, "暗": "3'", "T": "B"}, {
        "标准序": 117,
        "运行序": 157,
        "点类型": 1,
        "区组": 7,
        "color": "yellow",
        "明": 2,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 286, "运行序": 158, "点类型": 1, "区组": 7, "color": "purple", "明": 4, "暗": "3'", "T": "B"}, {
        "标准序": 95,
        "运行序": 159,
        "点类型": 1,
        "区组": 7,
        "color": "green",
        "明": 4,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 114, "运行序": 160, "点类型": 1, "区组": 7, "color": "yellow", "明": 2, "暗": "2'", "T": "B"}, {
        "标准序": 101,
        "运行序": 161,
        "点类型": 1,
        "区组": 7,
        "color": "yellow",
        "明": 1,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 50, "运行序": 162, "点类型": 1, "区组": 7, "color": "green", "明": 1, "暗": "1'", "T": "B"}, {
        "标准序": 251,
        "运行序": 163,
        "点类型": 1,
        "区组": 7,
        "color": "purple",
        "明": 1,
        "暗": "3'",
        "T": "C"
    }, {"标准序": 161, "运行序": 164, "点类型": 1, "区组": 7, "color": "cyan", "明": 2, "暗": "2'", "T": "A"}, {
        "标准序": 150,
        "运行序": 165,
        "点类型": 1,
        "区组": 7,
        "color": "cyan",
        "明": 1,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 82, "运行序": 166, "点类型": 1, "区组": 7, "color": "green", "明": 3, "暗": "3'", "T": "B"}, {
        "标准序": 160,
        "运行序": 167,
        "点类型": 1,
        "区组": 7,
        "color": "cyan",
        "明": 2,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 222, "运行序": 168, "点类型": 1, "区组": 7, "color": "blue", "明": 3, "暗": "2'", "T": "B"}, {
        "标准序": 259,
        "运行序": 169,
        "点类型": 1,
        "区组": 8,
        "color": "purple",
        "明": 2,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 16, "运行序": 170, "点类型": 1, "区组": 8, "color": "red", "明": 2, "暗": "1'", "T": "D"}, {
        "标准序": 210,
        "运行序": 171,
        "点类型": 1,
        "区组": 8,
        "color": "blue",
        "明": 2,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 18, "运行序": 172, "点类型": 1, "区组": 8, "color": "red", "明": 2, "暗": "2'", "T": "B"}, {
        "标准序": 256,
        "运行序": 173,
        "点类型": 1,
        "区组": 8,
        "color": "purple",
        "明": 2,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 200, "运行序": 174, "点类型": 1, "区组": 8, "color": "blue", "明": 1, "暗": "2'", "T": "D"}, {
        "标准序": 77,
        "运行序": 175,
        "点类型": 1,
        "区组": 8,
        "color": "green",
        "明": 3,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 65, "运行序": 176, "点类型": 1, "区组": 8, "color": "green", "明": 2, "暗": "2'", "T": "A"}, {
        "标准序": 135,
        "运行序": 177,
        "点类型": 1,
        "区组": 8,
        "color": "yellow",
        "明": 4,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 211, "运行序": 178, "点类型": 1, "区组": 8, "color": "blue", "明": 2, "暗": "2'", "T": "C"}, {
        "标准序": 207,
        "运行序": 179,
        "点类型": 1,
        "区组": 8,
        "color": "blue",
        "明": 2,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 62, "运行序": 180, "点类型": 1, "区组": 8, "color": "green", "明": 2, "暗": "1'", "T": "B"}, {
        "标准序": 86,
        "运行序": 181,
        "点类型": 1,
        "区组": 8,
        "color": "green",
        "明": 4,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 32, "运行序": 182, "点类型": 1, "区组": 8, "color": "red", "明": 3, "暗": "2'", "T": "D"}, {
        "标准序": 158,
        "运行序": 183,
        "点类型": 1,
        "区组": 8,
        "color": "cyan",
        "明": 2,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 103, "运行序": 184, "点类型": 1, "区组": 8, "color": "yellow", "明": 1, "暗": "2'", "T": "C"}, {
        "标准序": 147,
        "运行序": 185,
        "点类型": 1,
        "区组": 8,
        "color": "cyan",
        "明": 1,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 269, "运行序": 186, "点类型": 1, "区组": 8, "color": "purple", "明": 3, "暗": "2'", "T": "A"}, {
        "标准序": 254,
        "运行序": 187,
        "点类型": 1,
        "区组": 8,
        "color": "purple",
        "明": 2,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 131, "运行序": 188, "点类型": 1, "区组": 8, "color": "yellow", "明": 3, "暗": "3'", "T": "C"}, {
        "标准序": 271,
        "运行序": 189,
        "点类型": 1,
        "区组": 8,
        "color": "purple",
        "明": 3,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 111, "运行序": 190, "点类型": 1, "区组": 8, "color": "yellow", "明": 2, "暗": "1'", "T": "C"}, {
        "标准序": 201,
        "运行序": 191,
        "点类型": 1,
        "区组": 8,
        "color": "blue",
        "明": 1,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 94, "运行序": 192, "点类型": 1, "区组": 8, "color": "green", "明": 4, "暗": "3'", "T": "B"}, {
        "标准序": 89,
        "运行序": 193,
        "点类型": 1,
        "区组": 9,
        "color": "green",
        "明": 4,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 276, "运行序": 194, "点类型": 1, "区组": 9, "color": "purple", "明": 3, "暗": "3'", "T": "D"}, {
        "标准序": 164,
        "运行序": 195,
        "点类型": 1,
        "区组": 9,
        "color": "cyan",
        "明": 2,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 234, "运行序": 196, "点类型": 1, "区组": 9, "color": "blue", "明": 4, "暗": "2'", "T": "B"}, {
        "标准序": 231,
        "运行序": 197,
        "点类型": 1,
        "区组": 9,
        "color": "blue",
        "明": 4,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 104, "运行序": 198, "点类型": 1, "区组": 9, "color": "yellow", "明": 1, "暗": "2'", "T": "D"}, {
        "标准序": 9,
        "运行序": 199,
        "点类型": 1,
        "区组": 9,
        "color": "red",
        "明": 1,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 240, "运行序": 200, "点类型": 1, "区组": 9, "color": "blue", "明": 4, "暗": "3'", "T": "D"}, {
        "标准序": 64,
        "运行序": 201,
        "点类型": 1,
        "区组": 9,
        "color": "green",
        "明": 2,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 190, "运行序": 202, "点类型": 1, "区组": 9, "color": "cyan", "明": 4, "暗": "3'", "T": "B"}, {
        "标准序": 280,
        "运行序": 203,
        "点类型": 1,
        "区组": 9,
        "color": "purple",
        "明": 4,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 7, "运行序": 204, "点类型": 1, "区组": 9, "color": "red", "明": 1, "暗": "2'", "T": "C"}, {
        "标准序": 196,
        "运行序": 205,
        "点类型": 1,
        "区组": 9,
        "color": "blue",
        "明": 1,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 137, "运行序": 206, "点类型": 1, "区组": 9, "color": "yellow", "明": 4, "暗": "2'", "T": "A"}, {
        "标准序": 195,
        "运行序": 207,
        "点类型": 1,
        "区组": 9,
        "color": "blue",
        "明": 1,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 105, "运行序": 208, "点类型": 1, "区组": 9, "color": "yellow", "明": 1, "暗": "3'", "T": "A"}, {
        "标准序": 144,
        "运行序": 209,
        "点类型": 1,
        "区组": 9,
        "color": "yellow",
        "明": 4,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 1, "运行序": 210, "点类型": 1, "区组": 9, "color": "red", "明": 1, "暗": "1'", "T": "A"}, {
        "标准序": 209,
        "运行序": 211,
        "点类型": 1,
        "区组": 9,
        "color": "blue",
        "明": 2,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 78, "运行序": 212, "点类型": 1, "区组": 9, "color": "green", "明": 3, "暗": "2'", "T": "B"}, {
        "标准序": 154,
        "运行序": 213,
        "点类型": 1,
        "区组": 9,
        "color": "cyan",
        "明": 1,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 85, "运行序": 214, "点类型": 1, "区组": 9, "color": "green", "明": 4, "暗": "1'", "T": "A"}, {
        "标准序": 84,
        "运行序": 215,
        "点类型": 1,
        "区组": 9,
        "color": "green",
        "明": 3,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 8, "运行序": 216, "点类型": 1, "区组": 9, "color": "red", "明": 1, "暗": "2'", "T": "D"}, {
        "标准序": 139,
        "运行序": 217,
        "点类型": 1,
        "区组": 10,
        "color": "yellow",
        "明": 4,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 148, "运行序": 218, "点类型": 1, "区组": 10, "color": "cyan", "明": 1, "暗": "1'", "T": "D"}, {
        "标准序": 262,
        "运行序": 219,
        "点类型": 1,
        "区组": 10,
        "color": "purple",
        "明": 2,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 255, "运行序": 220, "点类型": 1, "区组": 10, "color": "purple", "明": 2, "暗": "1'", "T": "C"}, {
        "标准序": 140,
        "运行序": 221,
        "点类型": 1,
        "区组": 10,
        "color": "yellow",
        "明": 4,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 171, "运行序": 222, "点类型": 1, "区组": 10, "color": "cyan", "明": 3, "暗": "1'", "T": "C"}, {
        "标准序": 216,
        "运行序": 223,
        "点类型": 1,
        "区组": 10,
        "color": "blue",
        "明": 2,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 63, "运行序": 224, "点类型": 1, "区组": 10, "color": "green", "明": 2, "暗": "1'", "T": "C"}, {
        "标准序": 214,
        "运行序": 225,
        "点类型": 1,
        "区组": 10,
        "color": "blue",
        "明": 2,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 43, "运行序": 226, "点类型": 1, "区组": 10, "color": "red", "明": 4, "暗": "2'", "T": "C"}, {
        "标准序": 44,
        "运行序": 227,
        "点类型": 1,
        "区组": 10,
        "color": "red",
        "明": 4,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 87, "运行序": 228, "点类型": 1, "区组": 10, "color": "green", "明": 4, "暗": "1'", "T": "C"}, {
        "标准序": 247,
        "运行序": 229,
        "点类型": 1,
        "区组": 10,
        "color": "purple",
        "明": 1,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 49, "运行序": 230, "点类型": 1, "区组": 10, "color": "green", "明": 1, "暗": "1'", "T": "A"}, {
        "标准序": 250,
        "运行序": 231,
        "点类型": 1,
        "区组": 10,
        "color": "purple",
        "明": 1,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 126, "运行序": 232, "点类型": 1, "区组": 10, "color": "yellow", "明": 3, "暗": "2'", "T": "B"}, {
        "标准序": 72,
        "运行序": 233,
        "点类型": 1,
        "区组": 10,
        "color": "green",
        "明": 2,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 146, "运行序": 234, "点类型": 1, "区组": 10, "color": "cyan", "明": 1, "暗": "1'", "T": "B"}, {
        "标准序": 233,
        "运行序": 235,
        "点类型": 1,
        "区组": 10,
        "color": "blue",
        "明": 4,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 107, "运行序": 236, "点类型": 1, "区组": 10, "color": "yellow", "明": 1, "暗": "3'", "T": "C"}, {
        "标准序": 40,
        "运行序": 237,
        "点类型": 1,
        "区组": 10,
        "color": "red",
        "明": 4,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 252, "运行序": 238, "点类型": 1, "区组": 10, "color": "purple", "明": 1, "暗": "3'", "T": "D"}, {
        "标准序": 66,
        "运行序": 239,
        "点类型": 1,
        "区组": 10,
        "color": "green",
        "明": 2,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 28, "运行序": 240, "点类型": 1, "区组": 10, "color": "red", "明": 3, "暗": "1'", "T": "D"}, {
        "标准序": 96,
        "运行序": 241,
        "点类型": 1,
        "区组": 11,
        "color": "green",
        "明": 4,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 20, "运行序": 242, "点类型": 1, "区组": 11, "color": "red", "明": 2, "暗": "2'", "T": "D"}, {
        "标准序": 120,
        "运行序": 243,
        "点类型": 1,
        "区组": 11,
        "color": "yellow",
        "明": 2,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 113, "运行序": 244, "点类型": 1, "区组": 11, "color": "yellow", "明": 2, "暗": "2'", "T": "A"}, {
        "标准序": 45,
        "运行序": 245,
        "点类型": 1,
        "区组": 11,
        "color": "red",
        "明": 4,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 212, "运行序": 246, "点类型": 1, "区组": 11, "color": "blue", "明": 2, "暗": "2'", "T": "D"}, {
        "标准序": 57,
        "运行序": 247,
        "点类型": 1,
        "区组": 11,
        "color": "green",
        "明": 1,
        "暗": "3'",
        "T": "A"
    }, {"标准序": 218, "运行序": 248, "点类型": 1, "区组": 11, "color": "blue", "明": 3, "暗": "1'", "T": "B"}, {
        "标准序": 121,
        "运行序": 249,
        "点类型": 1,
        "区组": 11,
        "color": "yellow",
        "明": 3,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 182, "运行序": 250, "点类型": 1, "区组": 11, "color": "cyan", "明": 4, "暗": "1'", "T": "B"}, {
        "标准序": 2,
        "运行序": 251,
        "点类型": 1,
        "区组": 11,
        "color": "red",
        "明": 1,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 287, "运行序": 252, "点类型": 1, "区组": 11, "color": "purple", "明": 4, "暗": "3'", "T": "C"}, {
        "标准序": 53,
        "运行序": 253,
        "点类型": 1,
        "区组": 11,
        "color": "green",
        "明": 1,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 244, "运行序": 254, "点类型": 1, "区组": 11, "color": "purple", "明": 1, "暗": "1'", "T": "D"}, {
        "标准序": 51,
        "运行序": 255,
        "点类型": 1,
        "区组": 11,
        "color": "green",
        "明": 1,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 67, "运行序": 256, "点类型": 1, "区组": 11, "color": "green", "明": 2, "暗": "2'", "T": "C"}, {
        "标准序": 19,
        "运行序": 257,
        "点类型": 1,
        "区组": 11,
        "color": "red",
        "明": 2,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 208, "运行序": 258, "点类型": 1, "区组": 11, "color": "blue", "明": 2, "暗": "1'", "T": "D"}, {
        "标准序": 206,
        "运行序": 259,
        "点类型": 1,
        "区组": 11,
        "color": "blue",
        "明": 2,
        "暗": "1'",
        "T": "B"
    }, {"标准序": 157, "运行序": 260, "点类型": 1, "区组": 11, "color": "cyan", "明": 2, "暗": "1'", "T": "A"}, {
        "标准序": 27,
        "运行序": 261,
        "点类型": 1,
        "区组": 11,
        "color": "red",
        "明": 3,
        "暗": "1'",
        "T": "C"
    }, {"标准序": 181, "运行序": 262, "点类型": 1, "区组": 11, "color": "cyan", "明": 4, "暗": "1'", "T": "A"}, {
        "标准序": 52,
        "运行序": 263,
        "点类型": 1,
        "区组": 11,
        "color": "green",
        "明": 1,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 42, "运行序": 264, "点类型": 1, "区组": 11, "color": "red", "明": 4, "暗": "2'", "T": "B"}, {
        "标准序": 68,
        "运行序": 265,
        "点类型": 1,
        "区组": 12,
        "color": "green",
        "明": 2,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 24, "运行序": 266, "点类型": 1, "区组": 12, "color": "red", "明": 2, "暗": "3'", "T": "D"}, {
        "标准序": 138,
        "运行序": 267,
        "点类型": 1,
        "区组": 12,
        "color": "yellow",
        "明": 4,
        "暗": "2'",
        "T": "B"
    }, {"标准序": 232, "运行序": 268, "点类型": 1, "区组": 12, "color": "blue", "明": 4, "暗": "1'", "T": "D"}, {
        "标准序": 156,
        "运行序": 269,
        "点类型": 1,
        "区组": 12,
        "color": "cyan",
        "明": 1,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 108, "运行序": 270, "点类型": 1, "区组": 12, "color": "yellow", "明": 1, "暗": "3'", "T": "D"}, {
        "标准序": 163,
        "运行序": 271,
        "点类型": 1,
        "区组": 12,
        "color": "cyan",
        "明": 2,
        "暗": "2'",
        "T": "C"
    }, {"标准序": 6, "运行序": 272, "点类型": 1, "区组": 12, "color": "red", "明": 1, "暗": "2'", "T": "B"}, {
        "标准序": 92,
        "运行序": 273,
        "点类型": 1,
        "区组": 12,
        "color": "green",
        "明": 4,
        "暗": "2'",
        "T": "D"
    }, {"标准序": 38, "运行序": 274, "点类型": 1, "区组": 12, "color": "red", "明": 4, "暗": "1'", "T": "B"}, {
        "标准序": 112,
        "运行序": 275,
        "点类型": 1,
        "区组": 12,
        "color": "yellow",
        "明": 2,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 288, "运行序": 276, "点类型": 1, "区组": 12, "color": "purple", "明": 4, "暗": "3'", "T": "D"}, {
        "标准序": 136,
        "运行序": 277,
        "点类型": 1,
        "区组": 12,
        "color": "yellow",
        "明": 4,
        "暗": "1'",
        "T": "D"
    }, {"标准序": 141, "运行序": 278, "点类型": 1, "区组": 12, "color": "yellow", "明": 4, "暗": "3'", "T": "A"}, {
        "标准序": 130,
        "运行序": 279,
        "点类型": 1,
        "区组": 12,
        "color": "yellow",
        "明": 3,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 189, "运行序": 280, "点类型": 1, "区组": 12, "color": "cyan", "明": 4, "暗": "3'", "T": "A"}, {
        "标准序": 238,
        "运行序": 281,
        "点类型": 1,
        "区组": 12,
        "color": "blue",
        "明": 4,
        "暗": "3'",
        "T": "B"
    }, {"标准序": 134, "运行序": 282, "点类型": 1, "区组": 12, "color": "yellow", "明": 4, "暗": "1'", "T": "B"}, {
        "标准序": 109,
        "运行序": 283,
        "点类型": 1,
        "区组": 12,
        "color": "yellow",
        "明": 2,
        "暗": "1'",
        "T": "A"
    }, {"标准序": 21, "运行序": 284, "点类型": 1, "区组": 12, "color": "red", "明": 2, "暗": "3'", "T": "A"}, {
        "标准序": 257,
        "运行序": 285,
        "点类型": 1,
        "区组": 12,
        "color": "purple",
        "明": 2,
        "暗": "2'",
        "T": "A"
    }, {"标准序": 99, "运行序": 286, "点类型": 1, "区组": 12, "color": "yellow", "明": 1, "暗": "1'", "T": "C"}, {
        "标准序": 60,
        "运行序": 287,
        "点类型": 1,
        "区组": 12,
        "color": "green",
        "明": 1,
        "暗": "3'",
        "T": "D"
    }, {"标准序": 177, "运行序": 288, "点类型": 1, "区组": 12, "color": "cyan", "明": 3, "暗": "3'", "T": "A"}]

function f6(vari) {
    let color, target, ans, lightloc, darkloc, variables = []
    let anss = ["4", "8", "6", "2"]
    for (let i = 0; i < vari.length; i++) {
        color = vari[i]["color"]
        let colorArray = [color, color, color, color]
        lightloc = vari[i]["明"] - 1
        if (lightloc === 0) darkloc = vari[i]["暗"][0]
        else if (lightloc === 1) {
            if (vari[i]["暗"][0] === 1) darkloc = 0
            else darkloc = vari[i]["暗"][0]
        } else if (lightloc === 2) {
            if (vari[i]["暗"][0] === 3) darkloc = 3
            else darkloc = vari[i]["暗"][0] - 1
        } else darkloc = vari[i]["暗"][0] - 1
        colorArray[lightloc] = "light" + color
        colorArray[darkloc] = "dark" + color
        if (vari[i]["T"][0] === "A") target = 0
        else if (vari[i]["T"][0] === "B") target = 1
        else if (vari[i]["T"][0] === "C") target = 2
        else target = 3
        ans = anss[target]
        if (lightloc === target) target = "light" + color
        else if (darkloc === target) target = "dark" + color
        else {
            target = colorArray[target]
        }
        variables.push({
            size: '4',
            v1: ["circle", "circle", "circle", "circle"],
            color: colorArray,
            target: target,
            type: "hole-no-hole",
            ans: ans,
            block: vari[i]["区组"],
            shapeORcolor: 1
        })
    }
    return variables
}