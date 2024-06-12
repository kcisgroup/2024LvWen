const { data, run, timelineVariable } = initJsPsych({
    extensions: [
        { type: jsPsychExtensionWebgazer }
    ],
})
const introduce_trail_2 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: '<p>正式试验：试验都以 500 毫秒的固定时间开始，然后会有一个 2000 ms的样本显示，然后是 1000 毫秒的空白间隔。</p> ' +
        '<p style="font-weight: bold">要求：记忆所呈现刺激物和其对应的位置，根据目标提示选择对应刺激的位置,并根据数字键盘的 "4" ,"6" 进行选择响应。</p>',
    choices: ['开始'],
    css_classes: ['mouse'],
    post_trial_gap: 500
}

const introduce_trail_4 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: '<p>正式试验：试验都以 500 毫秒的固定时间开始，然后会有一个 2000 ms的样本显示，然后是 1000 毫秒的空白间隔。</p> ' +
        '<p style="font-weight: bold">要求：记忆所呈现刺激物和其对应的位置，根据目标提示选择对应刺激的位置,并根据数字键盘的 "4" ,"8" ,"6" ,"2" 进行选择响应。</p>',
    choices: ['开始'],
    css_classes: ['mouse'],
    post_trial_gap: 500
}


const introduce_trail_5 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: '<p>正式试验：试验都以 500 毫秒的固定时间开始，然后会有一个 2000 ms的样本显示，然后是 1000 毫秒的空白间隔。</p> ' +
        '<p style="font-weight: bold">要求：记忆所呈现刺激物和其对应的位置，根据目标提示选择对应刺激的位置,并根据数字键盘的 "7", "9", "6", "2", "4" 进行选择响应。</p>',
    choices: ['开始'],
    css_classes: ['mouse'],
    post_trial_gap: 500
}

const introduce_trail_6 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: '<p>正式试验：试验都以 500 毫秒的固定时间开始，然后会有一个 2000 ms的样本显示，然后是 1000 毫秒的空白间隔。</p> ' +
        '<p style="font-weight: bold">要求：记忆所呈现刺激物和其对应的位置，根据目标提示选择对应刺激的位置,并根据数字键盘的"4", "7", "9", "6", "3", "1"进行选择响应。</p>',
    choices: ['开始'],
    css_classes: ['mouse'],
    post_trial_gap: 500
}

const stim_dist = [[width / 2 - 300, height / 2], [width / 2, height / 2 - 300],
[width / 2 + 300, height / 2], [width / 2, height / 2 + 300]]
let dist_loc5 = [
    [width / 2 - 300 * Math.sin(36 * (Math.PI / 180)), height / 2 - 300 * Math.sin(54 * (Math.PI / 180))],
    [width / 2 + 300 * Math.sin(36 * (Math.PI / 180)), height / 2 - 300 * Math.sin(54 * (Math.PI / 180))],
    [width / 2 + 300 * Math.sin(72 * (Math.PI / 180)), height / 2 + 300 * Math.sin(18 * (Math.PI / 180))],
    [width / 2, height / 2 + 300],
    [width / 2 - 300 * Math.sin(72 * (Math.PI / 180)), height / 2 + 300 * Math.sin(18 * (Math.PI / 180))],
]

let arr4 = DynamicStim(4, "shape", 0, 0)
let arr5 = DynamicStim(5, "shape", 0, 0)
let arr6 = DynamicStim(6, "shape", 0, 0)
console.log(arr4, arr5, arr6)
let Tarr2 = DynamicStim(2, "shape", 0, 1)
let Tarr4 = DynamicStim(4, "shape", 0, 1)
let Tarr5 = DynamicStim(5, "shape", 0, 1)
let Tarr6 = DynamicStim(6, "shape", 0, 1)
console.log(Tarr2, Tarr4, Tarr5, Tarr6)
let Marr2 = DynamicStim(2, "shape", 1, 0)
let Marr4 = DynamicStim(4, "shape", 1, 0)
let Marr5 = DynamicStim(5, "shape", 1, 0)
let Marr6 = DynamicStim(6, "shape", 1, 0)
console.log(Marr2, Marr4, Marr5, Marr6)

let arr4c = DynamicStim(4, "color", 0, 0)
let arr5c = DynamicStim(5, "color", 0, 0)
let arr6c = DynamicStim(6, "color", 0, 0)
console.log(arr4c, arr5c, arr6c)
let Tarr2c = DynamicStim(2, "color", 0, 1)
let Tarr4c = DynamicStim(4, "color", 0, 1)
let Tarr5c = DynamicStim(5, "color", 0, 1)
let Tarr6c = DynamicStim(6, "color", 0, 1)
console.log(Tarr2c, Tarr4c, Tarr5c, Tarr6c)
let Marr2c = DynamicStim(2, "color", 1, 0)
let Marr4c = DynamicStim(4, "color", 1, 0)
let Marr5c = DynamicStim(5, "color", 1, 0)
let Marr6c = DynamicStim(6, "color", 1, 0)
console.log(Marr2c, Marr4c, Marr5c, Marr6c)

//运动变化  T代表是否作为目标
let Marray4T = DynamicStim1(4, "shape", 1, 0, 1)
let Marray4 = DynamicStim1(4, "shape", 1, 0, 0)
let Marray4cT = DynamicStim1(4, "color", 1, 0, 1)
let Marray4c = DynamicStim1(4, "color", 1, 0, 0)
//拓扑变化
let Tarray4T = DynamicStim1(4, "shape", 0, 1, 1)
let Tarray4 = DynamicStim1(4, "shape", 0, 1, 0)
let Tarray4cT = DynamicStim1(4, "color", 0, 1, 1)
let Tarray4c = DynamicStim1(4, "color", 0, 1, 0)
console.log(Marray4T, Marray4, Marray4cT, Marray4c)
console.log(Tarray4T, Tarray4, Tarray4cT, Tarray4c)


//额外实验(单独的拓扑变化和运动变化)
let shape_4_a = [], color_4_a = [],shape_4_a_T = [], color_4_a_T = []
shape_4_a.push.apply(shape_4_a, Marray4T)
shape_4_a.push.apply(shape_4_a, Marray4)
shape_4_a_T.push.apply(shape_4_a_T, Tarray4T)
shape_4_a_T.push.apply(shape_4_a_T, Tarray4)
color_4_a.push.apply(color_4_a, Marray4cT)
color_4_a.push.apply(color_4_a, Marray4c)
color_4_a_T.push.apply(color_4_a_T, Tarray4cT)
color_4_a_T.push.apply(color_4_a_T, Tarray4c)
const color_exam44 = generateTryTrail1(color_4_a, 1, stim_dist, "color", 4)
const shape_exam44 = generateTryTrail1(shape_4_a, 1, stim_dist, "shape", 4)
const color_exam44_T = generateTryTrail1(color_4_a_T, 1, stim_dist, "color", 4)
const shape_exam44_T = generateTryTrail1(shape_4_a_T, 1, stim_dist, "shape", 4)
const timeline_shape_4 = {
    timeline: [
        introduce_trail_4,
        shape_exam44,
        color_exam44

    ]
}
const timeline_color_4 = {
    timeline: [
        introduce_trail_4,
        color_exam44
    ]
}


//处理获得的刺激数组，各25
let shape_2 = [], shape_4 = [], shape_5 = [], shape_6 = [], color_2 = [], color_4 = [], color_5 = [], color_6 = []
shape_2.push.apply(shape_2, Tarr2)
shape_2.push.apply(shape_2, Marr2)
shape_4.push.apply(shape_4, arr4)
shape_4.push.apply(shape_4, Tarr4)
shape_4.push.apply(shape_4, Marr4)
shape_5.push.apply(shape_5, arr5)
shape_5.push.apply(shape_5, Tarr5)
shape_5.push.apply(shape_5, Marr5)
shape_6.push.apply(shape_6, arr6)
shape_6.push.apply(shape_6, Tarr6)
shape_6.push.apply(shape_6, Marr6)
color_2.push.apply(color_2, Tarr2c)
color_2.push.apply(color_2, Marr2c)
color_4.push.apply(color_4, arr4c)
color_4.push.apply(color_4, Tarr4c)
color_4.push.apply(color_4, Marr4c)
color_5.push.apply(color_5, arr5c)
color_5.push.apply(color_5, Tarr5c)
color_5.push.apply(color_5, Marr5c)
color_6.push.apply(color_6, arr6c)
color_6.push.apply(color_6, Tarr6c)
color_6.push.apply(color_6, Marr6c)
let types = ["shape", "color", "shapeAndcolor"]
const shape_exam2 = generateTryTrail(shape_2, 2, dist_loc2, "shape", 2)
const shape_exam4 = generateTryTrail(shape_4, 1, stim_dist, "shape", 4)
const shape_exam5 = generateTryTrail(shape_5, 1, dist_loc5, "shape", 5)
const shape_exam6 = generateTryTrail(shape_6, 1, dist_loc6, "shape", 6)
const color_exam2 = generateTryTrail(color_2, 2, dist_loc2, "color", 2)
const color_exam4 = generateTryTrail(color_4, 1, stim_dist, "color", 4)
const color_exam5 = generateTryTrail(color_5, 1, dist_loc5, "color", 5)
const color_exam6 = generateTryTrail(color_6, 1, dist_loc6, "color", 6)

const timeline_shapeAndcolor_2 = {
    timeline: [
        introduce_trail_2,
        shape_exam2,
        color_exam2
    ]
}

const timeline_shapeAndcolor_4 = {
    timeline: [
        introduce_trail_4,
        shape_exam4,
        color_exam4
    ]
}
const timeline_shape_5 = {
    timeline: [
        introduce_trail_5,
        shape_exam5,
    ]
}
const timeline_color_5 = {
    timeline: [
        // recognition_exam_intro,
        // recognition_shape_exam_intro,
        color_exam5
    ]
}
const timeline_shape_6 = {
    timeline: [
        introduce_trail_6,
        shape_exam6,

    ]
}
const timeline_color_6 = {
    timeline: [
        introduce_trail_6,
        color_exam6
    ]
}




let ExamArr = {
    "formal": {
        2: {
            "shape": shape_exam2,
            "color": color_exam2
        },

        4: {
            "shape": shape_exam4,
            "color": color_exam4
        },
        6: {
            "shape": shape_exam6,
            "color": color_exam6
        },
    },
    "pro": {
        4: {
            "shape": {
                "motion":shape_exam44,
                "topo":shape_exam44_T},
            "color": {
                "motion":color_exam44,
                "topo":color_exam44_T}
        },
    }
}

function f1(Exam_Type, Stimnumber, StudyAttribute, ChangeType) {
    let intro = eval('introduce_trail_' + Stimnumber)
    stimnum = Number(Stimnumber)
    console.log(Exam_Type, stimnum, StudyAttribute)
    let num=0,mm=""

    const timeline = []
    timeline.push(enter_fullscreen)
    timeline.push(preload)
    timeline.push(survey_before_trail)
    timeline.push(init_camera)
    timeline.push(calibration_timeline)
    timeline.push(intro)

    if (Exam_Type==1){
        let exam
        mm="_"+ChangeType
        if (StudyAttribute === "颜色") {
            exam=ExamArr["pro"][4]["color"][ChangeType]
            num=1
        }else {
            exam=ExamArr["pro"][4]["shape"][ChangeType]
            num=0
        }
        timeline.push(exam)
    }else{
        let exam1 = ExamArr["formal"][stimnum]["shape"]
        let exam2 = ExamArr["formal"][stimnum]["color"]
        if (StudyAttribute === "颜色") {
            timeline.push(exam2)
            num=1
        }else if (StudyAttribute === "形状") {
            timeline.push(exam1)
            num=0
        } else {
            num=2
            timeline.push(exam1)
            timeline.push(exam2)
        }
    }
    let exam_done = {
        type: jsPsychHtmlButtonResponse,
        choices: ['CSV'],
        css_classes: ['mouse'],
        stimulus: `
             <p>实验结束!</p>
             <p>点击下载数据。</p>
    `,
        on_finish: function (datas) {
            console.log(data.get())
            let name = data.get().filter({ "trial_type": "survey-text", "trial_index": 1 }).trials[0].response.name
            let size = data.get().filter({ "trial_type": "canvas-keyboard-response" }).trials[0].size
            if (datas.response === 0) {
                data.get().localSave('csv', name + "_" + size + "_" + types[num] + mm + "_Exam_Memory-data.csv")
            }
        }
    }

    timeline.push(exit_fullscreen)
    timeline.push(exam_done)
    timeline.push(show_data)
    console.log(timeline)
    run(timeline)
}
