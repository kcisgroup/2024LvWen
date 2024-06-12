let stimColorName = ["green", "yellow", "blue", "purple", "red"]
let stimColorName6 = ["green", "yellow", "blue", "purple", "red","cyan"]
let stimColorName3= ["green",  "blue", "red"]
const stimArray = ["rect", "triangle", "circle", "star", "hexagram"]
const stimArray6 = ["rect", "triangle", "circle", "star", "hexagram", "diamond"]
const stimArray3 = ["rect", "triangle", "circle"]
let stimColor = {
    "green": "#00bf00", "yellow": "#bfbf00", "blue": "#0000bf", "purple": "#bf00bf",
    "red": "#bf0000","cyan":"#00bfbf",
    "darkgreen": "#008000", "darkyellow": "#808000", "darkblue": "#000080", "darkpurple": "#800080",
    "darkred": "#800000","darkcyan":"#008080",
    "lightgreen": "#00ff00", "lightyellow": "#ffff00", "lightblue": "#0000ff", "lightpurple": "#ff00ff",
    "lightred": "#ff0000","lightcyan":"#00ffff",
}
let width = 1100
let height = 1000
const stim_dist = [[width / 2 - 300, height / 2], [width / 2, height / 2 - 300],
    [width / 2 + 300, height / 2], [width / 2, height / 2 + 300]]
let dist_loc6 = [
    [width / 2 - 300, height / 2], [width / 2 - 150, height / 2 - 150 * Math.sqrt(3)],
    [width / 2 + 150, height / 2 - 150 * Math.sqrt(3)], [width / 2 + 300, height / 2],
    [width / 2 + 150, height / 2 + 150 * Math.sqrt(3)], [width / 2 - 150, height / 2 + 150 * Math.sqrt(3)]
]
const dist_loc2 = [[width / 2 - 300, height / 2], [width / 2 + 300, height / 2]]
//从数组中随机获取指定大小的数组
function getArrayItems(colorarr, num) {
    var temp_array = new Array();
    for (var index in colorarr) {
        temp_array.push(colorarr[index]);
    }
    //取出的数值项,保存在此数组
    var return_array = new Array();
    for (var i = 0; i < num; i++) {
        if (temp_array.length > 0) {
            //在数组中产生一个随机索引
            var arrIndex = Math.floor(Math.random() * temp_array.length);
            //将随机索引的对应的数组元素值复制出来
            return_array[i] = temp_array[arrIndex];
            //删除此索引的数组元素
            temp_array.splice(arrIndex, 1);
        } else {
            break;
        }
    }
    return return_array;
}

function generatearray(type, stimarr, size ,shapeORcolor) {
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
            if (size===4){
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
            let stimcopy = stimarr.slice()
            stimcopy.splice(j, 1)
            let stim = getArrayItems(stimcopy, size - 1)
            stim.splice(i, 0, stimarr[j])
            if (shapeORcolor === 0) {
                if (type === "hole") {
                    if (stim[i] === "circle") stim[i] = "ring_1"
                    else stim[i] = stim[i] + "_1"
                }
                if (type === "hole-no-hole") {
                    if (stim[distractor_num] === "circle") stim[distractor_num] = "ring_1"
                    else stim[distractor_num] = stim[distractor_num] + "_1"
                }
                let array
                if (size===2) array = ["black", "black"]
                else if (size===6) array = ["black", "black", "black", "black","black", "black"]
                else array = ["black", "black","black", "black"]
                variables.push({
                    stim:stim,
                    color:array
                })
            } else {
                let array
                if (size===2) array = ["circle", "circle"]
                else if (size===6) array = ["circle", "circle", "circle", "circle","circle", "circle"]
                else array = ["circle", "circle","circle", "circle"]
                if (type === "hole") {
                    array[i] = "ring_1"
                }
                if (type === "no-hole")
                if (type === "hole-no-hole") {
                    array[distractor_num] = "ring_1"
                }
                variables.push({
                    stim:array,
                    color:stim
                })
            }
        }
    }
    return variables
}



var stage_stimuli = new Konva.Stage({
    container: 'container',
    width: width,
    height: height,
})

var layer_stimuli = new Konva.Layer()
stage_stimuli.add(layer_stimuli)

let array4=generatearray("hole",stimColorName,4,1)
let array2=generatearray("hole",stimColorName3,2,1)
let array6=generatearray("hole",stimColorName6,6,1)
console.log(array4,array2,array6)


document.getElementById('save').addEventListener('click', function A(){
    for (let i = 0; i < array2.length; i++) {
        let count=i
        let stimarray = array2[i]["stim"]
        let stimcolor = array2[i]["color"]
        for (let j = 0; j < stimarray.length; j++) {
            let stim
            if (stimarray[j].includes("_"))
                stim = Stimuli(stimarray[j].split("_")[0], 1, dist_loc2[j][0], dist_loc2[j][1], stimColor[stimcolor[j]])
            else stim = Stimuli(stimarray[j], 0, dist_loc2[j][0], dist_loc2[j][1], stimColor[stimcolor[j]])
            layer_stimuli.add(stim)
        }
        stage_stimuli.add(layer_stimuli)
        // 定义一个异步函数用于生成图片并下载
        async function generateAndDownloadImages() {
            // 使用 Konva.Stage.toDataURL 方法生成图片
            var dataURL = await new Promise(function (resolve) {
                stage_stimuli.toDataURL({
                    fill: "#c8c8c8",
                    callback: function (dataURL) {
                        resolve(dataURL);
                    }
                });
            });
            // 创建一个下载链接
            var downloadLink = document.createElement('a');
            downloadLink.href = dataURL;
            downloadLink.download = 'image_' + count + '.png'; // 设置下载的文件名
            // 触发下载链接
            downloadLink.click();
            console.log('所有图片下载完成！' + count);
        }
        // 调用异步函数生成并下载图片
        generateAndDownloadImages().catch(function(error) {
            console.error('图片下载出错：', error);
        });
        layer_stimuli.removeChildren()
    }
}, false);
