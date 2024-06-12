/*
*定义一些变量
*/
let width = 1100;
let height = 850;
// 定义konva所需要的container容器
const containers = document.createElement("div");
containers.id = "container";
//定义刺激组，方便设置眼动目标
let stimuli = [], dist_loc, target, examtype, setsize, color = [], shapeORcolor, randomValue, randomValue1;
let mchange, tchange, motion, topo
//定义位置
const dist_loc2_1 = [[width / 2 - 150, height / 2], [width / 2 + 150, height / 2]];
const dist_loc2_2 = [[width / 2 - 450, height / 2], [width / 2 + 450, height / 2]];
const dist_loc2 = [[width / 2 - 300, height / 2], [width / 2 + 300, height / 2]];
const dist_loc3 = [[width / 2 - 250, height / 2], [width / 2, height / 2], [width / 2 + 250, height / 2]];
const dist_loc4 = [[width / 2 - 200, height / 2 - 200], [width / 2 + 200, height / 2 - 200],
    [width / 2 - 200, height / 2 + 200], [width / 2 + 200, height / 2 + 200]];
//刺激宽高
let stimWandH = {
    'ring_1': [80, 80],
    'circle': [80, 80],
    'ring_2': [80, 80],
    'rect': [80, 80],
    'rect_1': [80, 80],
    'rect_2': [80, 80],
    'diamond': [100, 100],
    'diamond_1': [100, 100],
    'diamond_2': [100, 100],
    'triangle': [124, 124],
    'triangle_1': [124, 124],
    'triangle_2': [124, 124],
    'trapezoid': [96, 70],
    'trapezoid_1': [96, 70],
    'star': [100, 100],
    'star_1': [100, 100],
    'star_2': [100, 100],
    'hexagram': [160 / Math.sqrt(3), 80],
    'hexagram_1': [160 / Math.sqrt(3), 80],
    'hexagram_2': [160 / Math.sqrt(3), 80],
    'pentagon': [90, 90],
    'pentagon_1': [90, 90],
    'pentagon_2': [90, 90],
};

//相应的正确答案，方便后期计算准确率
let ans = [], answer, shade
let ISI = [500, 1000, 1500]
let choices = {
    2: ['4', '5', '6'],
    4: ['4', '8', '5', '6', '2'],
    5: ["7", "9", "6", "2", "4", "5"],
    6: ['4', '7', '9', '6', '3', '1', '5']
}

/*
* 实验前的准备工作：
* 包括全屏设置、眼动校准、图片预加载；
*/
const enter_fullscreen = {
    type: jsPsychFullscreen,
    fullscreen_mode: true,
    css_classes: ['mouse'],
}

const exit_fullscreen = {
    type: jsPsychFullscreen,
    fullscreen_mode: false,
    css_classes: ['mouse'],
    delay_after: 0
}

const images = ['../img/ring_1.png', '../img/circle.png'];

const preload = {
    type: jsPsychPreload,
    images: images,
}

const trail_blank = {
    type: jsPsychHtmlKeyboardResponse,
    choices: "NO_KEYS",
    stimulus: " ",
    trial_duration: 600,
    post_trial_gap: 2400
}

const init_camera = {
    type: jsPsychWebgazerInitCamera,
    css_classes: ['mouse'],
};

const calibration_instructions = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `
        <p>现在，眼动追踪器将经过校准，将你眼睛的图像从网络摄像头转换到你屏幕上的某个位置。</p>
        <p>为此，需要单击一系列点。</p>
        <p>保持头不动，点击每一个出现的点。当点击它的时候，看着这个点。</p>
      `,
    choices: ['开始'],
    css_classes: ['mouse'],
    post_trial_gap: 1000
};
//校准
const calibration = {
    type: jsPsychWebgazerCalibrate,
    calibration_points: [[50, 50], [25, 25], [25, 50], [25, 75],
        [50, 25], [50, 75], [75, 25], [75, 50], [75, 75]],
    repetitions_per_point: 1,
    randomize_calibration_order: true,
    css_classes: ['mouse'],
};

const validation_instructions = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `
        <p>展示眼球追踪的准确性</p>
        <p>保持头不动，当每个点出现时，移动眼睛聚焦在它上面。</p>
        <p>不需要点击点。移动眼睛看这些点。</p>
      `,
    choices: ['开始'],
    css_classes: ['mouse'],
    post_trial_gap: 1000
};

const validation = {
    type: jsPsychWebgazerValidate,
    validation_points: [
        [25, 25], [75, 25], [50, 50], [25, 75], [75, 75]
    ],
    roi_radius: 200,
    time_to_saccade: 1000,
    show_validation_data: true,
    validation_duration: 2000,
    data: {
        task: 'validate'
    }
}

const recalibrate_instructions = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `
          <p>校准的精度较低。</p>
          <p>请重新校准.</p>
          <p>在下一个屏幕上，注视圆点并单击它们。<p>
        `,
    choices: ['继续'],
    css_classes: ['mouse'],
}

const recalibrate = {
    timeline: [recalibrate_instructions, calibration, validation_instructions, validation],
    conditional_function: function () {
        var validation_data = data.get().filter({task: 'validate'}).values()[0];
        return validation_data.percent_in_roi.some(function (x) {
            var minimum_percent_acceptable = 50;
            return x < minimum_percent_acceptable;
        });
    },
    data: {
        phase: 'recalibration'
    }
}

const recalibrate_define = {
    timeline: [recalibrate],
    loop_function: function () {
        var validation_data = data.getLastTrialData().filter({task: 'validate'}).values()[0];
        return validation_data.percent_in_roi.some(function (x) {
            var minimum_percent_acceptable = 50;
            return x < minimum_percent_acceptable;
        });
    },
    data: {
        phase: 'recalibration_define'
    }
}

//眼动校准时间线
const calibration_timeline = {
    timeline: [calibration_instructions, calibration,
        validation_instructions, validation, recalibrate_define]
}
/*
*实验中共用的一些函数
*/

//实验中心点+
function fixtion() {
    let group = new Konva.Group();
    let line1 = new Konva.Line({
        points: [width / 2 + 1, height / 2 - 8 + 1, width / 2 + 1, height / 2 + 8 + 1],
        stroke: 'black',
        strokeWidth: 2,
    });
    let line2 = new Konva.Line({
        points: [width / 2 - 8 + 1, height / 2 + 1, width / 2 + 8 + 1, height / 2 + 1],
        stroke: 'black',
        strokeWidth: 2,
    });
    group.add(line1);
    group.add(line2);
    return group;
}

//实验前信息调查
const survey_before_trail = {
    timeline: [
        {
            type: jsPsychSurveyText,
            questions: [
                {prompt: "姓名:", required: true, name: 'name'},
                {prompt: "年龄:", required: true, name: 'age', columns: 3}
            ]
        },
        {
            type: jsPsychSurveyMultiChoice,
            questions: [
                {prompt: "性别:", options: ['男', '女'], required: true, name: 'sex'}
            ],
        }
    ],
    css_classes: ['mouse'],
}

//实验后问卷调查
const survey_after_trail = {
    timeline: [
        {
            type: jsPsychSurveyText,
            questions: [
                {
                    prompt: "你在进行视觉搜索的过程中，是否对某一个位置有偏好？",
                    required: true,
                    placeholder: '请回答是/否，并且说明是哪个位置或是怎样的位置。',
                    name: 'position-prefer'
                },
                {prompt: "你认为自己对于实验中出现的颜色哪个有偏好？", required: true, name: 'color', placeholder: '红/蓝/绿/黄/紫，可多选，没有就填"无"。'},
                {
                    prompt: "你认为自己对于实验中出现的形状哪个有偏好？",
                    required: true,
                    name: 'shape',
                    placeholder: '圆/三角/矩形/星形/六边形，可多选，没有就填"无"。'
                }
            ]
        },
    ],
    css_classes: ['mouse'],
}

//刺激物呈现前的空白
const trial_before = {
    type: jsPsychCanvasKeyboardResponse,
    stimulus: function () {
        const jspsych_content = document.getElementById("jspsych-content");
        jspsych_content.appendChild(containers);
        const stage = new Konva.Stage({
            container: 'container',
            width: width,
            height: height,
        });
        const layer_0 = new Konva.Layer();
        const group = fixtion();
        layer_0.add(group)
        stage.add(layer_0);
    },
    canvas_size: [0, 0],
    choices: "NO_KEYS",
    trial_duration: 500,
}

//实验结束后的数据下载和展示
let done = {
    type: jsPsychHtmlButtonResponse,
    choices: ['CSV', 'JSON'],
    css_classes: ['mouse'],
    stimulus: `
         <p>实验结束!</p>
         <p>点击下载数据。</p>
`,
    on_finish: function (datas) {
        // let name = data.get().filter({"trial_type": "survey-text", "trial_index": 1}).trials[0].response.name;
        let name = "ww";
        if (datas.response === 0) {
            data.get().localSave('csv', name + "_Memory-data.csv");
        }
        if (datas.response === 1) {
            data.get().localSave('json', name + '_Memory-data.json');
        }
    }
}
const show_data = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function () {
        var trial_data = data.getLastTimelineData().values();
        var trial_json = JSON.stringify(trial_data, null, 2);
        return `<p style="margin-bottom:0;"><strong>Trial data:</strong></p>
            <pre style="margin-top:0;text-align:left;">${trial_json}</pre>`;
    },
    choices: "NO_KEYS",
    css_classes: ['mouse'],
}
const exam_intro = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>实验说明：该实验根据颜色和形状各有两组，每组实验开始前会有一个眼动校准。</p>' +
        '<p>按"space"键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const shape_exam_intro = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>要求：记忆项目的形状。</p>' +
        '<p>按" "键继续，实验开始。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const color_exam_intro = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>要求：记忆项目的颜色。</p>' +
        '<p>按" "键继续，实验开始。</p>',
    choices: [' '],
    post_trial_gap: 500,
}

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

//将原来的数据打乱排序
function shuffle(array) {
    if (!Array.isArray(array)) {
        console.error("Argument to shuffle() must be an array.");
    }
    const copy_array = array.slice(0);
    let m = copy_array.length, t, i;
    while (m) {
        i = Math.floor(Math.random() * m--);
        t = copy_array[m];
        copy_array[m] = copy_array[i];
        copy_array[i] = t;
    }
    return copy_array;
}

/*
*实验流程函数
*/
let blue = "#004a9e";

//attention实验
function generateRamTrail(stimuliArray, repeat_num) {
    return {
        timeline_variables: stimuliArray,
        timeline: [
            trial_before,
            // {
            //     type: jsPsychCanvasKeyboardResponse,
            //     choices: "NO_KEYS",
            //     stimulus: function () {
            //         const jspsych_content = document.getElementById("jspsych-content");
            //         jspsych_content.appendChild(containers);
            //         const stage = new Konva.Stage({
            //             container: 'container',
            //             width: width,
            //             height: height,
            //         });
            //         const layer = new Konva.Layer();
            //         setsize = Number(timelineVariable('size'));
            //         //绘制干扰物
            //         for (let i = 0; i < setsize; i++) {
            //             let stim;
            //             stim = Stimuli('circle', 0, dist_loc2[i][0], dist_loc2[i][1]);
            //             layer.add(stim);
            //         }
            //         stage.add(layer);
            //     },
            //     canvas_size: [0, 0],
            //     trial_duration: 1000,
            //     // post_trial_gap: 900
            // },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: ['4', '6'],
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    //获取刺激set
                    setsize = Number(timelineVariable('size'))
                    let stimuli_gen = timelineVariable('v1').split(",")
                    let type = timelineVariable('type')
                    examtype = type
                    let dist, color;
                    //根据dist类型选择刺激位置
                    if (type === "dist")
                        dist = timelineVariable('dist')
                    else
                        dist = dist_loc2;
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli_gen[i].includes("_")) {
                            let hole_stim = stimuli_gen[i].split("_")
                            stim = Stimuli(hole_stim[0], 1, dist[i][0], dist[i][1])
                        } else {
                            if (stimuli_gen[i] === "circle") color = "#000099"
                            else color = "black"
                            stim = Stimuli(stimuli_gen[i], 0, dist[i][0], dist[i][1], color)
                        }
                        layer.add(stim)
                    }
                    // let stim = Stimuli('circle', 0, width / 2, height / 2)
                    // layer.add(stim)
                    stimuli = stimuli_gen
                    dist_loc = dist
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 1000,
                post_trial_gap: 1000,
                response_ends_trial: true,
                data: {
                    task: examtype,
                },
                on_finish: function (data) {
                    data.stimuli = stimuli
                    data.webgazer_targets_data = []
                    for (let i = 0; i < 2; i++) {
                        data.webgazer_targets_data.push({
                            x: dist_loc[i][0],
                            y: dist_loc[i][1],
                            width: stimWandH[stimuli[i]][0],
                            height: stimWandH[stimuli[i]][1],
                            top: dist_loc[i][1] - stimWandH[stimuli[i]][1] / 2,
                            right: dist_loc[i][0] + stimWandH[stimuli[i]][0] / 2,
                            bottom: dist_loc[i][1] + stimWandH[stimuli[i]][1] / 2,
                            left: dist_loc[i][0] - stimWandH[stimuli[i]][0] / 2
                        })
                    }
                },
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }]
            },
        ],
        randomize_order: true,
        repetitions: repeat_num,
    };
}


function generateExamProTrail(stimuliArray, repeat_num, type, dist) {
    let trail
    if (type === "recognition") {
        trail = {
            timeline_variables: stimuliArray,
            timeline: [
                trial_before,
                {
                    type: jsPsychCanvasKeyboardResponse,
                    choices: "NO_KEYS",
                    stimulus: function () {
                        const jspsych_content = document.getElementById("jspsych-content")
                        jspsych_content.appendChild(containers)
                        const stage = new Konva.Stage({
                            container: 'container',
                            width: width,
                            height: height,
                        })
                        const layer = new Konva.Layer()
                        //获取目标对象，以及他在列表中的位置，即正确答案
                        let target_index = timelineVariable('target') //形状为具体形状，颜色为位置（例如0,1,…）
                        answer = timelineVariable('ans')
                        setsize = Number(timelineVariable('size'))
                        shade = timelineVariable('shade')
                        //获取刺激set
                        stimuli = timelineVariable('v1')
                        let stim, target_color, shape;
                        //判断他是颜色不同还是形状不同
                        let shapeORcolor = timelineVariable('type')
                        if (shapeORcolor === "shape") { //形状不同
                            target = stimuli[target_index]
                            shape = target
                            target_color = "black"
                            color = ['black', 'black', 'black', 'black']
                        } else if (shapeORcolor === "color") {
                            let colorname = timelineVariable('color')
                            color = [stimColor[colorname[0]], stimColor[colorname[1]], stimColor[colorname[2]], stimColor[colorname[3]]]
                            shape = stimuli[target_index]
                            target = color[target_index]
                            target_color = target
                        }
                        console.log(shapeORcolor)
                        console.log(target, shape)
                        //绘制目标或提示
                        if (shape.includes("_")) {
                            let hole_stim = shape.split("_")
                            stim = Stimuli(hole_stim[0], Number(hole_stim[1]), width / 2, height / 2, target_color)
                        } else stim = Stimuli(shape, 0, width / 2, height / 2, target_color)
                        layer.add(stim)
                        stage.add(layer)
                    },
                    canvas_size: [0, 0],
                    trial_duration: 50,
                    post_trial_gap: 1000,
                    data: {
                        exam_type: "recognition",
                    },
                    on_finish: function (data) {
                        data.size = setsize
                        data.target = target
                        data.response_answer = answer
                        data.shade = shade
                    }
                },
                {
                    type: jsPsychCanvasKeyboardResponse,
                    choices: ['4', '8', '5', '6', '2'],
                    stimulus: function () {
                        const jspsych_content = document.getElementById("jspsych-content");
                        jspsych_content.appendChild(containers);
                        const stage = new Konva.Stage({
                            container: 'container',
                            width: width,
                            height: height,
                        });
                        const layer = new Konva.Layer()
                        //获取刺激set
                        let stimuli_gen = stimuli
                        //绘制刺激物
                        for (let i = 0; i < setsize; i++) {
                            let stim
                            if (stimuli_gen[i].includes("_")) {
                                let hole_stim = stimuli_gen[i].split("_")
                                stim = Stimuli(hole_stim[0], 1, dist[i][0], dist[i][1], color[i])
                            } else {
                                stim = Stimuli(stimuli_gen[i], 0, dist[i][0], dist[i][1], color[i])
                            }
                            layer.add(stim)
                        }
                        ans.push(answer)
                        stage.add(layer)
                    },
                    canvas_size: [0, 0],
                    trial_duration: 1000,
                    post_trial_gap: 1000,
                    response_ends_trial: true,
                    data: {
                        task: type,
                    },
                    on_finish: function (data) {
                        data.webgazer_targets_data = []
                        data.correct = !!comparekeys(data.response, answer)
                        for (let i = 0; i < dist.length; i++) {
                            data.webgazer_targets_data.push({
                                x: dist[i][0],
                                y: dist[i][1],
                                width: stimWandH[stimuli[i]][0],
                                height: stimWandH[stimuli[i]][1],
                                top: dist[i][1] - stimWandH[stimuli[i]][1] / 2,
                                right: dist[i][0] + stimWandH[stimuli[i]][0] / 2,
                                bottom: dist[i][1] + stimWandH[stimuli[i]][1] / 2,
                                left: dist[i][0] - stimWandH[stimuli[i]][0] / 2
                            })
                        }
                    },
                    extensions: [{
                        type: jsPsychExtensionWebgazer,
                        params: {targets: ['#container']}
                    }]
                },
            ],
            randomize_order: true,
            repetitions: repeat_num,
            on_finish: function (data) {
                data.ans = ans;
            }
        }
    } else {
        trail = {
            timeline_variables: stimuliArray,
            timeline: [
                trial_before,
                {
                    type: jsPsychCanvasKeyboardResponse,
                    choices: "NO_KEYS",
                    stimulus: function () {
                        const jspsych_content = document.getElementById("jspsych-content");
                        jspsych_content.appendChild(containers);
                        const stage = new Konva.Stage({
                            container: 'container',
                            width: width,
                            height: height,
                        });
                        const layer = new Konva.Layer()
                        //获取刺激set
                        answer = timelineVariable('ans')
                        shade = timelineVariable('shade')
                        setsize = Number(timelineVariable('size'))
                        //获取刺激set
                        stimuli = timelineVariable('v1')
                        let shapeORcolor = timelineVariable('type')
                        let stimuli_gen = stimuli
                        if (shapeORcolor === "shape") { //形状不同
                            color = ['black', 'black', 'black', 'black']
                        } else if (shapeORcolor === "color") {
                            let colorname = timelineVariable('color')
                            color = [stimColor[colorname[0]], stimColor[colorname[1]], stimColor[colorname[2]], stimColor[colorname[3]]]
                        }
                        //绘制刺激物
                        for (let i = 0; i < setsize; i++) {
                            let stim
                            if (stimuli_gen[i].includes("_")) {
                                let hole_stim = stimuli_gen[i].split("_")
                                stim = Stimuli(hole_stim[0], 1, dist[i][0], dist[i][1], color[i])
                            } else {
                                stim = Stimuli(stimuli_gen[i], 0, dist[i][0], dist[i][1], color[i])
                            }
                            layer.add(stim)
                        }
                        ans.push(answer)
                        stage.add(layer)
                    },
                    canvas_size: [0, 0],
                    trial_duration: 1000,
                    post_trial_gap: 1000,
                    response_ends_trial: true,
                    data: {
                        task: type,
                    },
                    on_finish: function (data) {
                        data.webgazer_targets_data = []
                        data.shade = shade
                        data.correct = !!comparekeys(data.response, answer)
                        for (let i = 0; i < dist.length; i++) {
                            data.webgazer_targets_data.push({
                                x: dist[i][0],
                                y: dist[i][1],
                                width: stimWandH[stimuli[i]][0],
                                height: stimWandH[stimuli[i]][1],
                                top: dist[i][1] - stimWandH[stimuli[i]][1] / 2,
                                right: dist[i][0] + stimWandH[stimuli[i]][0] / 2,
                                bottom: dist[i][1] + stimWandH[stimuli[i]][1] / 2,
                                left: dist[i][0] - stimWandH[stimuli[i]][0] / 2
                            })
                        }
                    },
                    extensions: [{
                        type: jsPsychExtensionWebgazer,
                        params: {targets: ['#container']}
                    }]
                },
                {
                    type: jsPsychCanvasKeyboardResponse,
                    choices: ['4', '8', '5', '6', '2'],
                    stimulus: function () {
                        const jspsych_content = document.getElementById("jspsych-content")
                        jspsych_content.appendChild(containers)
                        const stage = new Konva.Stage({
                            container: 'container',
                            width: width,
                            height: height,
                        })
                        const layer = new Konva.Layer()
                        //获取目标对象，以及他在列表中的位置，即正确答案
                        let target_index = timelineVariable('target') //形状为具体形状，颜色为位置（例如0,1,…）
                        let stim, target_color, shape;
                        //判断他是颜色不同还是形状不同
                        let shapeORcolor = timelineVariable('type')
                        if (shapeORcolor === "shape") { //形状不同
                            target = stimuli[target_index]
                            shape = target
                            target_color = "black"
                        } else if (shapeORcolor === "color") {
                            let colorname = timelineVariable('color')
                            color = [stimColor[colorname[0]], stimColor[colorname[1]], stimColor[colorname[2]], stimColor[colorname[3]]]
                            shape = stimuli[target_index]
                            target = color[target_index]
                            target_color = target
                        }
                        console.log(shapeORcolor)
                        console.log(target, shape)
                        //绘制目标或提示
                        if (shape.includes("_")) {
                            let hole_stim = shape.split("_")
                            stim = Stimuli(hole_stim[0], Number(hole_stim[1]), width / 2, height / 2, target_color)
                        } else stim = Stimuli(shape, 0, width / 2, height / 2, target_color)
                        layer.add(stim)
                        stage.add(layer)
                    },
                    canvas_size: [0, 0],
                    trial_duration: 3000,
                    post_trial_gap: 500,
                    data: {
                        exam_type: "recall",
                    },
                    on_finish: function (data) {
                        data.size = setsize
                        data.target = target
                        data.response_answer = answer
                    }
                }
            ],
            randomize_order: true,
            repetitions: repeat_num,
            on_finish: function (data) {
                data.ans = ans;
            }
        }
    }
    return trail;
}


function generateTryTrail(stimuliArray, repeat_num, dist, type, size) {
    return {
        timeline_variables: stimuliArray,
        timeline: [
            trial_before,
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer();
                    //获取刺激set
                    setsize = Number(timelineVariable('size'))
                    let stimuli_gen = timelineVariable('v1')
                    motion = Number(timelineVariable('motion'))
                    topo = Number(timelineVariable('topo'))
                    target = timelineVariable('target')
                    console.log(motion, topo, stimuli_gen, target)
                    //判断他是颜色不同还是形状不同
                    shapeORcolor = Number(timelineVariable('shapeORcolor'))
                    if (shapeORcolor === 1) color = timelineVariable('color')
                    else color = ['black', 'black', 'black', 'black']
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli_gen[i].includes("_")) {
                            let hole_stim = stimuli_gen[i].split("_")
                            if (hole_stim[0]==="ring") hole_stim[0]="circle"
                            stim = Stimuli(hole_stim[0], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        } else {
                            stim = Stimuli(stimuli_gen[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        }
                        layer.add(stim)
                    }
                    stimuli = stimuli_gen
                    ans.push(timelineVariable('ans'))
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 500,
                on_finish: function (data) {
                    if (type === "color") data.stimulus = color
                    else data.stimulus = stimuli
                    data.webgazer_targets_data = []
                    for (let i = 0; i < dist.length; i++) {
                        data.webgazer_targets_data.push({
                            x: dist[i][0],
                            y: dist[i][1],
                            width: stimWandH[stimuli[i]][0],
                            height: stimWandH[stimuli[i]][1],
                            top: dist[i][1] - stimWandH[stimuli[i]][1] / 2,
                            right: dist[i][0] + stimWandH[stimuli[i]][0] / 2,
                            bottom: dist[i][1] + stimWandH[stimuli[i]][1] / 2,
                            left: dist[i][0] - stimWandH[stimuli[i]][0] / 2
                        })
                    }
                },
                // extensions: [{
                //     type: jsPsychExtensionWebgazer,
                //     params: {targets: ['#container']}
                // }]
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: async function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    let dist1 = JSON.parse(JSON.stringify(dist))
                    let distractor1, distractor2, stimsize, target_n
                    if (motion === 0 && topo === 0) {
                        distractor2 = timelineVariable('distractor2')//topo
                        tchange = timelineVariable('dchange2')
                        distractor1 = timelineVariable('distractor1')//motion
                        mchange = timelineVariable('dchange1')
                    } else if (motion === 0 && topo === 1) {//拓扑变化为T
                        distractor1 = timelineVariable('distractor')//motion
                        mchange = timelineVariable('dchange')//motion的变化
                    } else if (motion === 1 && topo === 0) {//动态变化为T
                        target = timelineVariable('target')
                        if (shapeORcolor === 0) target_n = stimuli.indexOf(target)
                        else target_n = target
                        console.log(target_n)
                        distractor2 = timelineVariable('distractor')//topo
                        mchange = timelineVariable('tchange')
                    }
                    console.log(mchange, tchange)
                    if (mchange === "zoom") {
                        randomValue1 = Math.floor(Math.random() * 2)
                        //0不变，1缩，2放
                        stimsize = randomValue1 === 0 ? 1 : 2
                    } else if (mchange === "trans") {
                        randomValue = Math.floor(Math.random() * 2)
                        if (motion === 1 && topo === 0) {
                            if (randomValue === 0)
                                dist1[target_n] = [dist[target_n][0] - 50, dist[target_n][1]]
                            else dist1[target_n] = [dist[target_n][0], dist[target_n][1] - 50]
                        } else {
                            if (randomValue === 0)
                                dist1[distractor1] = [dist[distractor1][0] - 50, dist[distractor1][1]]
                            else dist1[distractor1] = [dist[distractor1][0], dist[distractor1][1] - 50]
                        }
                    }
                    console.log(dist1)
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli[i].includes("_")) {
                            let hole_stim = stimuli[i].split("_")
                            stim = Stimuli(hole_stim[0], Number(hole_stim[1]), dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                        } else {
                            if (i === distractor1)//motion为T
                                stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], stimsize)
                            else {
                                if (motion === 1 && topo === 0 && mchange === "zoom") {
                                    if (i === target_n) stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], stimsize)
                                    else stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                                } else
                                    stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                            }

                        }
                        layer.add(stim)
                    }
                    stage.add(layer);
                },
                canvas_size: [0, 0],
                trial_duration: 500,
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }],
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer();
                    //获取刺激set
                    setsize = Number(timelineVariable('size'))
                    let stimuli_gen = timelineVariable('v1')
                    //判断他是颜色不同还是形状不同
                    shapeORcolor = Number(timelineVariable('shapeORcolor'))
                    if (shapeORcolor === 1) color = timelineVariable('color')
                    else color = ['black', 'black', 'black', 'black']
                    let dist1 = JSON.parse(JSON.stringify(dist))
                    let distractor1, stimsize
                    if (motion === 0 && topo === 0) {
                        distractor1 = timelineVariable('distractor1')//motion
                    } else if (motion === 0 && topo === 1) {//拓扑变化为T
                        distractor1 = timelineVariable('distractor')//motion
                    } else if (motion === 1 && topo === 0) {//动态变化为T
                        if (shapeORcolor === 0) target_n = stimuli.indexOf(target)
                        else target_n = target

                    }
                    if (mchange === "zoom") {
                        //0不变，1缩，2放
                        stimsize = randomValue1 === 0 ? 1 : 2
                    } else if (mchange === "trans") {
                        if (motion === 1 && topo === 0) {
                            if (randomValue === 0)
                                dist1[target_n] = [dist[target_n][0] + 60, dist[target_n][1]]
                            else dist1[target_n] = [dist[target_n][0], dist[target_n][1] + 60]
                        } else {
                            if (randomValue === 0)
                                dist1[distractor1] = [dist[distractor1][0] + 60, dist[distractor1][1]]
                            else dist1[distractor1] = [dist[distractor1][0], dist[distractor1][1] + 60]
                        }
                    }
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli[i].includes("_")) {
                            let hole_stim = stimuli[i].split("_")
                            if (hole_stim[0]==="ring") hole_stim[0]="circle"
                            stim = Stimuli(hole_stim[0], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                        } else {
                           if (i === distractor1)//motion不为T
                                stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                            else {
                                if (motion === 1 && topo === 0 && mchange === "zoom") {
                                    if (i === target_n) stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                                    else stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                                } else
                                    stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                            }
                        }
                        layer.add(stim)
                    }

                    //绘制刺激物
                    // for (let i = 0; i < setsize; i++) {
                    //     let stim
                    //     if (stimuli_gen[i].includes("_")) {
                    //         let hole_stim = stimuli_gen[i].split("_")
                    //         stim = Stimuli(hole_stim[0], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                    //     } else {
                    //         stim = Stimuli(stimuli_gen[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                    //     }
                    //     layer.add(stim)
                    // }
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 500,
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }],
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: async function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    let dist1 = JSON.parse(JSON.stringify(dist))
                    let distractor1, stimsize
                    if (motion === 0 && topo === 0) {
                        distractor1 = timelineVariable('distractor1')//motion
                    } else if (motion === 0 && topo === 1) {//拓扑变化为T
                        distractor1 = timelineVariable('distractor')//motion
                    } else if (motion === 1 && topo === 0) {//动态变化为T
                        if (shapeORcolor === 0) target_n = stimuli.indexOf(target)
                        else target_n = target

                    }
                    if (mchange === "zoom") {
                        //0不变，1缩，2放
                        stimsize = randomValue1 === 0 ? 1 : 2
                    } else if (mchange === "trans") {
                        if (motion === 1 && topo === 0) {
                            if (randomValue === 0)
                                dist1[target_n] = [dist[target_n][0] + 60, dist[target_n][1]]
                            else dist1[target_n] = [dist[target_n][0], dist[target_n][1] + 60]
                        } else {
                            if (randomValue === 0)
                                dist1[distractor1] = [dist[distractor1][0] + 60, dist[distractor1][1]]
                            else dist1[distractor1] = [dist[distractor1][0], dist[distractor1][1] + 60]
                        }
                    }
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli[i].includes("_")) {
                            let hole_stim = stimuli[i].split("_")
                            stim = Stimuli(hole_stim[0], Number(hole_stim[1]), dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        } else {
                           if (i === distractor1)//motion为T
                                stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], stimsize)
                            else {
                                if (motion === 1 && topo === 0 && mchange === "zoom") {
                                    if (i === target_n) stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], stimsize)
                                    else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                                } else
                                    stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                            }
                        }
                        layer.add(stim)
                    }
                    stage.add(layer);

                },
                canvas_size: [0, 0],
                trial_duration: 500,
                post_trial_gap: 1000,
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }],
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: choices[size],
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    //目标刺激
                    let target_stim = timelineVariable('target')
                    answer = timelineVariable('ans')//答案
                    ans.push(answer)
                    shapeORcolor = timelineVariable('shapeORcolor')
                    let stim, target_color, shape
                    if (shapeORcolor === 0) {
                        target = target_stim
                        target_color = "black"
                        shape = target_stim //单个呈现的对象为拓扑
                    } else {
                        target = color[target_stim]
                        target_color = stimColor[target]
                        shape = stimuli[target_stim]
                    }
                    //绘制目标或提示
                    if (shape.includes("_")) {
                        let hole_stim=shape.split("_")
                        if (hole_stim[0]==="ring") hole_stim[0]="circle"
                        stim = Stimuli(hole_stim[0], 0, width / 2, height / 2, target_color, 0)
                    }
                    else stim = Stimuli(shape, 0, width / 2, height / 2, target_color, 0)
                    layer.add(stim);
                    stage.add(layer);
                },
                canvas_size: [0, 0],
                trial_duration: 3000,
                post_trial_gap: 500,
                on_finish: function (data) {
                    data.correct = !!comparekeys(data.response, answer)
                    data.response_target = target
                    data.response_answer = answer
                    data.motion = motion
                    data.topo = topo
                    data.mchange = mchange
                    data.tchange = tchange
                }
            },
            {
                timeline: [{
                    conditional_function: function () {
                        var last_trial_data1 = data.get().last(1).values()[0]
                        return last_trial_data1.correct === false
                    },
                    timeline: [{
                        type: jsPsychHtmlKeyboardResponse,
                        stimulus: '<div id="errorinfo">error</div>',
                        trial_duration: 500,
                        post_trial_gap: 500,
                    }]
                }]
            },
        ],
        randomize_order: true,
        repetitions: repeat_num,
        on_finish: function (data) {
            data.ans = ans
            data.task = "recall"
            data.ISI = 1000
            data.type = type
            data.size = size
        }
    }
}

function generateTryTrail1(stimuliArray, repeat_num, dist, type, size) {
    return {
        timeline_variables: stimuliArray,
        timeline: [
            trial_before,
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer();
                    //获取刺激set
                    setsize = Number(timelineVariable('size'))
                    let stimuli_gen = timelineVariable('v1')
                    motion = Number(timelineVariable('motion'))
                    topo = Number(timelineVariable('topo'))
                    target = timelineVariable('target')
                    console.log(motion, topo, stimuli_gen, target)
                    //判断他是颜色不同还是形状不同
                    shapeORcolor = Number(timelineVariable('shapeORcolor'))
                    if (shapeORcolor === 1) color = timelineVariable('color')
                    else color = ['black', 'black', 'black', 'black']
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli_gen[i].includes("_")) {
                            let hole_stim = stimuli_gen[i].split("_")
                            if (hole_stim[0]==="ring") hole_stim[0]="circle"
                            stim = Stimuli(hole_stim[0], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        } else {
                            stim = Stimuli(stimuli_gen[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        }
                        layer.add(stim)
                    }
                    stimuli = stimuli_gen
                    ans.push(timelineVariable('ans'))
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 500,
                on_finish: function (data) {
                    if (type === "color") data.stimulus = color
                    else data.stimulus = stimuli
                    data.webgazer_targets_data = []
                    for (let i = 0; i < dist.length; i++) {
                        data.webgazer_targets_data.push({
                            x: dist[i][0],
                            y: dist[i][1],
                            width: stimWandH[stimuli[i]][0],
                            height: stimWandH[stimuli[i]][1],
                            top: dist[i][1] - stimWandH[stimuli[i]][1] / 2,
                            right: dist[i][0] + stimWandH[stimuli[i]][0] / 2,
                            bottom: dist[i][1] + stimWandH[stimuli[i]][1] / 2,
                            left: dist[i][0] - stimWandH[stimuli[i]][0] / 2
                        })
                    }
                },
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }]
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: async function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    let dist1 = JSON.parse(JSON.stringify(dist))
                    T = Number(timelineVariable('T'))
                    let distractor1, distractor2, stimsize, target_n

                    if (motion === 1 && topo === 0) {//动态变化为T
                        if(T===1){
                            target = timelineVariable('target')
                            if (shapeORcolor === 0) target_n = stimuli.indexOf(target)
                            else target_n = target
                            console.log(target_n)
                            mchange = timelineVariable('tchange')
                        }else{
                            distractor1 = timelineVariable('distractor')
                            mchange = timelineVariable('dchange')
                        }
                    }
                    console.log(mchange)
                    if (mchange === "zoom") {
                        randomValue1 = Math.floor(Math.random() * 2)
                        //0不变，1缩，2放
                        stimsize = randomValue1 === 0 ? 1 : 2
                    } else if (mchange === "trans") {
                        randomValue = Math.floor(Math.random() * 2)
                        if (motion === 1 && topo === 0&&T===1) {
                            if (randomValue === 0)
                                dist1[target_n] = [dist[target_n][0] - 50, dist[target_n][1]]
                            else dist1[target_n] = [dist[target_n][0], dist[target_n][1] - 50]
                        } else if (motion === 1 && topo === 0&&T===0) {
                            if (randomValue === 0)
                                dist1[distractor1] = [dist[distractor1][0] - 50, dist[distractor1][1]]
                            else dist1[distractor1] = [dist[distractor1][0], dist[distractor1][1] - 50]
                        }
                    }
                    console.log(dist1)
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if(motion === 0 && topo === 1){
                            if (stimuli[i].includes("_")) {
                                let hole_stim = stimuli[i].split("_")
                                stim = Stimuli(hole_stim[0], Number(hole_stim[1]), dist[i][0], dist[i][1], stimColor[color[i]], 0)
                            }
                            else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        }
                       else if(motion === 1 && topo === 0){
                           if(mchange==="zoom"){
                               if(T===1){
                                   if (i === target_n) stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], stimsize)
                                   else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                               }else{
                                   if (i === distractor1) stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], stimsize)
                                   else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                               }
                           }else stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                        }
                        layer.add(stim)
                    }
                    stage.add(layer);
                },
                canvas_size: [0, 0],
                trial_duration: 500,
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }],
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer();
                    //获取刺激set
                    setsize = Number(timelineVariable('size'))
                    let stimuli_gen = timelineVariable('v1')
                    //判断他是颜色不同还是形状不同
                    shapeORcolor = Number(timelineVariable('shapeORcolor'))
                    if (shapeORcolor === 1) color = timelineVariable('color')
                    else color = ['black', 'black', 'black', 'black']
                    let dist1 = JSON.parse(JSON.stringify(dist))
                    let distractor1, stimsize
                    T = Number(timelineVariable('T'))
                    if (motion === 1 && topo === 0) {//动态变化为T
                        if(T===1){
                            target = timelineVariable('target')
                            if (shapeORcolor === 0) target_n = stimuli.indexOf(target)
                            else target_n = target
                            console.log(target_n)
                            mchange = timelineVariable('tchange')
                        }else{
                            distractor1 = timelineVariable('distractor')
                            mchange = timelineVariable('dchange')
                        }
                    }
                    if (mchange === "zoom") {
                        randomValue1 = Math.floor(Math.random() * 2)
                        //0不变，1缩，2放
                        stimsize = randomValue1 === 0 ? 1 : 2
                    } else if (mchange === "trans") {
                        if (motion === 1 && topo === 0&&T===1) {
                            if (randomValue === 0)
                                dist1[target_n] = [dist[target_n][0] + 50, dist[target_n][1]]
                            else dist1[target_n] = [dist[target_n][0], dist[target_n][1] + 50]
                        } else if (motion === 1 && topo === 0&&T===0) {
                            if (randomValue === 0)
                                dist1[distractor1] = [dist[distractor1][0] + 50, dist[distractor1][1]]
                            else dist1[distractor1] = [dist[distractor1][0], dist[distractor1][1] + 50]
                        }
                    }
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if(motion === 0 && topo === 1){
                            if (stimuli[i].includes("_")) {
                                let hole_stim = stimuli[i].split("_")
                                if (hole_stim[0]==="ring") hole_stim[0]="circle"
                                stim = Stimuli(hole_stim[0], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                            }
                            else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        }
                        else if(motion === 1 && topo === 0){
                            if(mchange==="zoom"){
                                  stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                            }else stim = Stimuli(stimuli[i], 0, dist1[i][0], dist1[i][1], stimColor[color[i]], 0)
                        }
                        layer.add(stim)
                    }
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 500,
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }],
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: async function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    let dist1 = JSON.parse(JSON.stringify(dist))
                    let distractor1, stimsize

                    if (motion === 1 && topo === 0) {//动态变化为T
                        if(T===1){
                            if (shapeORcolor === 0) target_n = stimuli.indexOf(target)
                            else target_n = target
                        }else{
                            distractor1 = timelineVariable('distractor')
                        }
                    }
                    if (mchange === "zoom") {
                        randomValue1 = Math.floor(Math.random() * 2)
                        //0不变，1缩，2放
                        stimsize = randomValue1 === 0 ? 1 : 2
                    }
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if(motion === 0 && topo === 1){
                            if (stimuli[i].includes("_")) {
                                let hole_stim = stimuli[i].split("_")
                                stim = Stimuli(hole_stim[0], Number(hole_stim[1]), dist[i][0], dist[i][1], stimColor[color[i]], 0)
                            }
                            else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        }
                        else if(motion === 1 && topo === 0){
                            if(mchange==="zoom"){
                                if(T===1){
                                    if (i === target_n) stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], stimsize)
                                    else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                                }else{
                                    if (i === distractor1) stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], stimsize)
                                    else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                                }
                            }else stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]], 0)
                        }
                        layer.add(stim)
                    }
                    stage.add(layer);

                },
                canvas_size: [0, 0],
                trial_duration: 500,
                post_trial_gap: 1000,
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }],
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: choices[size],
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    //目标刺激
                    let target_stim = timelineVariable('target')
                    answer = timelineVariable('ans')//答案
                    ans.push(answer)
                    shapeORcolor = timelineVariable('shapeORcolor')
                    let stim, target_color, shape
                    if (shapeORcolor === 0) {
                        target = target_stim
                        target_color = "black"
                        shape = target_stim //单个呈现的对象为拓扑
                    } else {
                        target = color[target_stim]
                        target_color = stimColor[target]
                        shape = stimuli[target_stim]
                        if (shape.includes("_")) target=target+"_"+shape.split("_")[1]
                    }
                    //绘制目标或提示
                    if (shape.includes("_")) {
                        let hole_stim=shape.split("_")
                        if (hole_stim[0]==="ring") hole_stim[0]="circle"
                        stim = Stimuli(hole_stim[0], 0, width / 2, height / 2, target_color, 0)
                    }
                    else stim = Stimuli(shape, 0, width / 2, height / 2, target_color, 0)
                    layer.add(stim);
                    stage.add(layer);
                },
                canvas_size: [0, 0],
                trial_duration: 3000,
                post_trial_gap: 500,
                on_finish: function (data) {
                    data.correct = !!comparekeys(data.response, answer)
                    data.response_target = target
                    data.response_answer = answer
                    data.motion = motion
                    data.topo = topo
                    data.mchange = mchange
                    data.tchange = tchange
                    data.T=T
                }
            },
            {
                timeline: [{
                    conditional_function: function () {
                        var last_trial_data1 = data.get().last(1).values()[0]
                        return last_trial_data1.correct === false
                    },
                    timeline: [{
                        type: jsPsychHtmlKeyboardResponse,
                        stimulus: '<div id="errorinfo">error</div>',
                        trial_duration: 500,
                        post_trial_gap: 500,
                    }]
                }]
            },
        ],
        randomize_order: true,
        repetitions: repeat_num,
        on_finish: function (data) {
            data.ans = ans
            data.task = "recall"
            data.ISI = 1000
            data.type = type
            data.size = size
        }
    }


}







/*
*type: recognition & recall
*stimuliArray: hole, no-hole, hole & no-hole
*/
function generateRecognitionTrail(stimuliArray, dist, repeat_num, ISI, target_topo, size, type) {
    return {
        timeline_variables: stimuliArray,
        timeline: [
            trial_before,
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content")
                    jspsych_content.appendChild(containers)
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    })
                    const layer = new Konva.Layer()
                    //获取目标对象，以及他在列表中的位置，即正确答案
                    let target_stim = timelineVariable('target') //形状为具体形状，颜色为位置（例如0,1,…）
                    let type = timelineVariable('type')
                    answer = timelineVariable('ans')
                    setsize = Number(timelineVariable('size'))
                    //获取刺激set
                    stimuli = timelineVariable('v1')
                    let stim, target_color, shape
                    //判断他是颜色不同还是形状不同
                    shapeORcolor = Number(timelineVariable('shapeORcolor'))
                    if (shapeORcolor === 0) { //形状不同
                        target = target_stim
                        target_color = "black"
                        color = ['black', 'black', 'black', 'black']
                        //拓扑对象作为目标情况下，单个呈现的对象为非拓扑
                        if (target_topo === 0) {
                            if (target_stim === "ring_1") shape = "circle"
                            else if (target_stim.includes("_")) shape = target_stim.split("_")[0]
                            else shape = target_stim
                        } else shape = target_stim //单个呈现的对象为拓扑
                    } else if (shapeORcolor === 1) {
                        color = timelineVariable('color')
                        if (size === 4) {
                            if (target_stim === 4) target = diff(color, stimColorName)[0]
                            else target = color[target_stim]
                            console.log(target, color)
                        } else if (size === 2) {
                            if (target_stim === 2) target = diff(color, stimColorName3)[0]
                            else target = color[target_stim]
                            console.log(target, color)
                        } else target = color[target_stim]
                        target_color = stimColor[target]
                        //拓扑对象作为目标情况下，单个呈现的对象为非拓扑
                        if (target_topo === 0) {
                            shape = "circle"
                            if (type === "hole") target = target + "_1"
                        } else {
                            if (type === "hole") {
                                shape = "ring_1"
                                target = target + "_1"
                            } else shape = "circle"
                        } //单个呈现的对象为拓扑

                    }
                    console.log(shape)
                    //绘制目标或提示
                    if (shape.includes("_")) stim = Stimuli(shape.split("_")[0], 1, width / 2, height / 2, target_color)
                    else stim = Stimuli(shape, 0, width / 2, height / 2, target_color)
                    layer.add(stim)
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 100,
                post_trial_gap: ISI,
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: choices[size],
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content")
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    //绘制刺激物,刺激set:stimuli
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli[i].includes("_")) {
                            let hole_stim = stimuli[i].split("_")
                            stim = Stimuli(hole_stim[0], 1, dist[i][0], dist[i][1], stimColor[color[i]])
                        } else {
                            stim = Stimuli(stimuli[i], 0, dist[i][0], dist[i][1], stimColor[color[i]])
                        }
                        layer.add(stim)
                    }
                    ans.push(timelineVariable('ans'))
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 3000,
                post_trial_gap: 500,
                response_ends_trial: true,
                on_finish: function (data) {
                    data.target = target
                    if (type === "color") data.stimulus = color
                    else data.stimulus = stimuli
                    data.response_answer = answer
                    data.correct = !!comparekeys(data.response, answer)
                    data.webgazer_targets_data = []
                    for (let i = 0; i < dist.length; i++) {
                        data.webgazer_targets_data.push({
                            x: dist[i][0],
                            y: dist[i][1],
                            width: stimWandH[stimuli[i]][0],
                            height: stimWandH[stimuli[i]][1],
                            top: dist[i][1] - stimWandH[stimuli[i]][1] / 2,
                            right: dist[i][0] + stimWandH[stimuli[i]][0] / 2,
                            bottom: dist[i][1] + stimWandH[stimuli[i]][1] / 2,
                            left: dist[i][0] - stimWandH[stimuli[i]][0] / 2
                        })
                    }
                },
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }]
            },
            {//error的提示界面
                timeline: [{
                    conditional_function: function () {
                        var last_trial_data1 = data.get().last(1).values()[0]
                        return last_trial_data1.correct === false
                    },
                    timeline: [{
                        type: jsPsychHtmlKeyboardResponse,
                        stimulus: '<div id="errorinfo">Error</div>',
                        trial_duration: 500,
                        post_trial_gap: 500,
                    }]
                }]
            },
        ],
        randomize_order: true,
        repetitions: repeat_num,
        on_finish: function (data) {
            data.ans = ans
            data.task = "recognition"
            data.ISI = ISI
            data.type = type
            data.size = size
        }
    }
}

function generateRecallTrail(stimuliArray, dist, repeat_num, ISI, target_topo, size, type) {
    return {
        timeline_variables: stimuliArray,
        timeline: [
            trial_before,
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: "NO_KEYS",
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    //获取刺激set
                    setsize = Number(timelineVariable('size'))
                    let stimuli_gen = timelineVariable('v1')
                    shapeORcolor = timelineVariable('shapeORcolor')
                    if (shapeORcolor === 1) color = timelineVariable('color')
                    else color = ['black', 'black', 'black', 'black']
                    //绘制刺激物
                    for (let i = 0; i < setsize; i++) {
                        let stim
                        if (stimuli_gen[i].includes("_")) {
                            let hole_stim = stimuli_gen[i].split("_")
                            stim = Stimuli(hole_stim[0], 1, dist[i][0], dist[i][1], stimColor[color[i]])
                        } else {
                            stim = Stimuli(stimuli_gen[i], 0, dist[i][0], dist[i][1], stimColor[color[i]])
                        }
                        layer.add(stim)
                    }
                    stimuli = stimuli_gen
                    ans.push(timelineVariable('ans'))
                    stage.add(layer)
                },
                canvas_size: [0, 0],
                trial_duration: 2000,
                post_trial_gap: ISI,
                response_ends_trial: true,
                on_finish: function (data) {
                    if (type === "color") data.stimulus = color
                    else data.stimulus = stimuli
                    data.webgazer_targets_data = []
                    for (let i = 0; i < dist.length; i++) {
                        data.webgazer_targets_data.push({
                            x: dist[i][0],
                            y: dist[i][1],
                            width: stimWandH[stimuli[i]][0],
                            height: stimWandH[stimuli[i]][1],
                            top: dist[i][1] - stimWandH[stimuli[i]][1] / 2,
                            right: dist[i][0] + stimWandH[stimuli[i]][0] / 2,
                            bottom: dist[i][1] + stimWandH[stimuli[i]][1] / 2,
                            left: dist[i][0] - stimWandH[stimuli[i]][0] / 2
                        })
                    }
                },
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    params: {targets: ['#container']}
                }]
            },
            {
                type: jsPsychCanvasKeyboardResponse,
                choices: choices[size],
                stimulus: function () {
                    const jspsych_content = document.getElementById("jspsych-content");
                    jspsych_content.appendChild(containers);
                    const stage = new Konva.Stage({
                        container: 'container',
                        width: width,
                        height: height,
                    });
                    const layer = new Konva.Layer()
                    let target_stim = timelineVariable('target')
                    let type = timelineVariable('type')
                    answer = timelineVariable('ans')
                    shapeORcolor = timelineVariable('shapeORcolor')
                    let stim, target_color, shape
                    if (shapeORcolor === 0) {
                        target = target_stim
                        target_color = "black"
                        if (target_topo === 0) {//拓扑对象作为目标情况下，单个呈现的对象为非拓扑
                            if (target_stim === "ring_1") shape = "circle"
                            else if (target_stim.includes("_")) shape = target_stim.split("_")[0]
                            else shape = target_stim
                        } else shape = target_stim //单个呈现的对象为拓扑
                    } else {
                        if (size === 4) {
                            if (target_stim === 4) target = diff(color, stimColorName)[0]
                            else target = color[target_stim]
                        } else if (size === 2) {
                            if (target_stim === 2) target = diff(color, stimColorName3)[0]
                            else target = color[target_stim]
                        } else target = color[target_stim]
                        target_color = stimColor[target]
                        //拓扑对象作为目标情况下，单个呈现的对象为非拓扑
                        if (target_topo === 0) {
                            shape = "circle"
                            if (type === "hole") target = target + "_1"
                        } else {
                            if (type === "hole") {
                                shape = "ring_1"
                                target = target + "_1"
                            } else shape = "circle"
                        } //单个呈现的对象为拓扑

                    }
                    //绘制目标或提示
                    if (shape.includes("_")) stim = Stimuli(shape.split("_")[0], 1, width / 2, height / 2, target_color)
                    else stim = Stimuli(shape, 0, width / 2, height / 2, target_color)
                    layer.add(stim);
                    stage.add(layer);
                },
                canvas_size: [0, 0],
                trial_duration: 3000,
                post_trial_gap: 500,
                on_finish: function (data) {
                    data.correct = !!comparekeys(data.response, answer)
                    data.response_target = target
                    data.response_answer = answer
                }
            },
            {
                timeline: [{
                    conditional_function: function () {
                        var last_trial_data1 = data.get().last(1).values()[0]
                        return last_trial_data1.correct === false
                    },
                    timeline: [{
                        type: jsPsychHtmlKeyboardResponse,
                        stimulus: '<div id="errorinfo">error</div>',
                        trial_duration: 500,
                        post_trial_gap: 500,
                    }]
                }]
            },
        ],
        randomize_order: true,
        repetitions: repeat_num,
        on_finish: function (data) {
            data.ans = ans
            data.task = "recall"
            data.ISI = ISI
            data.type = type
            data.size = size
        }
    }
}

function comparekeys(key1, key2) {
    if ((typeof key1 !== "string" && key1 !== null) ||
        (typeof key2 !== "string" && key2 !== null)) {
        console.error("Error in jsPsych.pluginAPI.compareKeys: arguments must be key strings or null.");
        return undefined;
    }
    if (typeof key1 === "string" && typeof key2 === "string") {
        return this.areResponsesCaseSensitive
            ? key1 === key2
            : key1.toLowerCase() === key2.toLowerCase();
    }
    return key1 === null && key2 === null;
}


//将除指定目标位置外的数组重新排序
function RandomArray(array, index, type, target) {
    if (!Array.isArray(array))
        console.error("Argument to RandomArray() must be an array.")
    let copy_array = array.slice()
    let temp, t
    if (type === "hole") {
        for (let i = 0; i < array.length; i++) {
            if (array[i] === target) {
                if (target === "circle") {
                    temp = "ring_1"
                } else temp = array[i].toString() + "_1"
                t = i
            }
        }
    }
    if (type === "no-hole") {
        for (let i = 0; i < array.length; i++) {
            if (array[i] === target) {
                temp = array[i]
                t = i
            }
        }
    }
    if (type === "hole-no-hole") {
        for (let i = 0; i < array.length; i++) {
            if (array[i] === target) {
                temp = array[i]
                t = i
            }
        }
    }
    copy_array.splice(t, 1)
    copy_array = shuffle(copy_array)
    for (let j = array.length - 1; j >= 0; j--) {
        if (index !== j)
            copy_array[j] = copy_array[j - 1]
        else {
            copy_array[j] = temp
            break
        }
    }
    return copy_array
}

//获得除指定数外的随机整数，以确保三分之一的概率
function GetRandomNum(num) {
    let number = Math.floor(Math.random() * 4)
    while (number === num) number = Math.floor(Math.random() * 4)
    return number
}

//生成随机刺激数列，一组16个
function generateStimArray(type, shapeORcolor) {
    let timeline_variables = [], target;
    const stimArray = ["rect", "triangle", "circle", "star", "hexagram"]
    const stimColor = {
        "green": "#00a600", "yellow": "#a6a600", "blue": "#0000a6", "purple": "#a600a6",
        "red": "#a60000"
    }
    let stimColorName = ["green", "yellow", "blue", "purple", "red"]
    let ans = ["4", "8", "6", "2"]
    if (shapeORcolor === 0) {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < stimArray.length; j++) {
                let stimCopy = ["rect", "triangle", "circle", "star", "hexagram"]
                stimCopy.splice(j, 1)
                let stim = getArrayItems(stimCopy, 3)
                stim[3] = stimArray[j]
                //当target是hole时，20个每组
                if (type === "hole") {
                    if (stimArray[j] === "circle") target = "ring_1"
                    else target = stimArray[j] + "_1"
                    timeline_variables.push({
                        size: '4',
                        v1: RandomArray(stim, i, type, stimArray[j]),
                        target: target,
                        ans: ans[i],
                        type: type,
                        shapeORcolor: 0
                    })
                }
                //或当target是no-hole时,刺激列里不存在hole
                if (type === "no-hole") {
                    timeline_variables.push({
                        size: '4',
                        v1: RandomArray(stim, i, type, stimArray[j]),
                        target: stimArray[j],
                        ans: ans[i],
                        type: type,
                        shapeORcolor: 0
                    })
                }
                //当target是no-hole时,刺激列存在hole 60个？
                if (type === "hole-no-hole") {
                    let distractor_num = 0
                    for (let k = 0; k < 3; k++) {
                        if (i === 0) distractor_num = k + 1
                        else if (i === 1) {
                            if (k < 1) distractor_num = 0
                            else distractor_num = k + 1
                        } else if (i === 2) {
                            if (k < 2) distractor_num = k
                            else distractor_num = k + 1
                        } else distractor_num = k
                        let v = RandomArray(stim, i, type, stimArray[j])
                        if (v[distractor_num] === "circle") v[distractor_num] = "ring_1"
                        else v[distractor_num] = v[distractor_num] + "_1"
                        timeline_variables.push({
                            size: '4',
                            v1: v,
                            target: stimArray[j],
                            ans: ans[i],
                            type: type,
                            distractor: v[distractor_num],
                            distractor_dist: ans[distractor_num],
                            shapeORcolor: 0
                        })
                    }
                    // timeline_variables = f4(hole_no_hole_TopoVSShape)
                }
            }
        }
    } else {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < stimColorName.length; j++) {
                let color = []
                let stim = ["green", "yellow", "blue", "purple", "red"]
                stim.splice(j, 1)
                color = getArrayItems(stim, 3);
                // for (let k = 0; k < stim.length; k++) color[k] = stimColor[stim[k]]
                color.splice(i, 0, stimColorName[j])
                let array = ["circle", "circle", "circle", "circle"]
                //24个每组
                if (type === "hole") {
                    array[i] = "ring_1"
                    timeline_variables.push({
                        size: '4',
                        v1: array,
                        color: color,
                        target: i,
                        ans: ans[i],
                        type: type,
                        shapeORcolor: 1
                    })
                }
                if (type === "no-hole") {
                    timeline_variables.push({
                        size: '4',
                        v1: array,
                        color: color,
                        target: i,
                        ans: ans[i],
                        type: type,
                        shapeORcolor: 1
                    })
                }
                //60个
                if (type === "hole-no-hole") {
                    for (let k = 0; k < 3; k++) {
                        let distractornum = 0
                        let array = ["circle", "circle", "circle", "circle"]
                        if (i === 0) distractornum = k + 1
                        else if (i === 1) {
                            if (k < 1) distractornum = 0
                            else distractornum = k + 1
                        } else if (i === 2) {
                            if (k < 2) distractornum = k
                            else distractornum = k + 1
                        } else distractornum = k
                        array[distractornum] = "ring_1"
                        timeline_variables.push({
                            size: '4',
                            v1: array,
                            color: color,
                            target: i,
                            type: "hole-no-hole",
                            ans: ans[i],
                            distractor: distractornum,
                            distractor_dist: ans[distractornum],
                            shapeORcolor: 1
                        })
                    }
                    // timeline_variables = f5(hole_no_hole_ColorVSShape)
                }
            }
        }
    }
    return timeline_variables
}

function split_Array(array) {
    let arr1 = [], arr2 = [], j = 0, k = 0
    for (let i = 0; i < array.length / 2; i++) {
        if (i % 2 === 0) arr1[j++] = array[i]
        else arr2[k++] = array[i]
    }
    for (let i = Math.floor(array.length / 2); i < array.length; i++) {
        if (i % 2 === 0) arr2[k++] = array[i]
        else arr1[j++] = array[i]
    }
    return [arr1, arr2]
}

function group(array, subGroupLength) {
    let index = 0;
    let newArray = [];
    while (index < array.length) {
        newArray.push(array.slice(index, index += subGroupLength));
    }
    return newArray;
}

//获取数组的差
function diff(array, array1) {
    let diff = array1.slice(), arr1 = array.slice()
    for (let i = 0, len = array.length; i < len; i++) {
        for (let j = 0, length = array1.length; j < length; j++) {
            if (arr1[i].includes("_")) arr1[i] = arr1[i].split("_")[0]
            if (arr1[i] === "ring") arr1[i] = "circle"
            if (arr1[i] === array1[j]) {
                diff.splice(diff.findIndex(item => item === arr1[i]), 1)
            }
        }
    }
    return diff
}

//按照属性名为数组排序
function compareNames(a, b) {
    // 将字符串转换为小写,比较忽略大写和小写
    let nameA = a.target
    let nameB = b.target
    if (nameA < nameB) {
        return -1;
    }
    if (nameA > nameB) {
        return 1;
    }
    // 名称必须相同
    return 0;
}