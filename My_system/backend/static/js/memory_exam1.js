/*
实验一：图形特征（形状和颜色）
研究目的：1、探讨人眼是否对某个形状有偏好，每个图形都不同，也可以探讨对角的数量
        2、研究人眼是否对某个颜色有偏好
        3、同时研究他们在回忆和识别时，对记忆的影响
实验变量：1、形状：["rect", "triangle", "circle", "star", "hexagram"]
        2、颜色：{"green": "#00a600", "yellow": "#a6a600", "blue": "#0000a6",
        "purple": "#a600a6","red": "#a60000"}
实验设计：1、为了排除人眼对于位置记忆的影响，我们将位置随机化，即每个目标出现在各个位置的概率相同
        2、实验利用正交设计分别生成在两个特征下的变量，分别有 24 种（形状/颜色*位置）
        3、在实验过程中穿插眼动校准，以确保眼动的准确性
G*Power样本量：1、计算2(颜色、形状)*4(位置)*5(形状/颜色)的重复测量方差分析（within_between），
                    被试间变量       试间变量
              得出10名参与者得出0.8的power，12名参与者得出0.95的power
              2、如果是2(识别、召回)*2(颜色、形状)*4(位置)*5(形状/颜色)
                       被试间变量             试间变量
              得出6名参与者得出0.8的power，8名参与者得出0.95的power
              最好将识别和召回分成两组人，这样至少需要20人
              3、探讨人眼是否对某个形状有偏好,研究人眼是否对某个颜色有偏好,属于被试内实验，预计15个人，保险起见一组20个
*/

//初始化JsPsych组件
const { data, run, timelineVariable } = initJsPsych({
    extensions: [
        { type: jsPsychExtensionWebgazer }
    ],
});

const Recognition_exam_intro_2 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>识别实验：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是100毫秒的单个项目展示，1000毫秒的空白间隔后，会呈现一个2个项目的阵列。</p> ' +
        '<p>要求：记忆单个项目，并在多个项目阵列中快速找到，并根据数字键盘的 " 4 " ," 6 ",进行选择响应,如果不记得或者不存在选择"5"。</p>' +
        '<p>按" "键继续，实验开始。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const Recall_exam_intro_2 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>回忆实验：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是 2500 毫秒的样本展示，1000毫秒的空白间隔后，会有一个目标刺激的提示。</p> ' +
        '<p>要求：记忆所呈现刺激物的位置，根据提示选择对应刺激的位置，根据数字键盘的 " 4 " ," 6 " 进行选择响应,如果不记得或者不存在选择"5"。</p>' +
        '<p>按" "键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const Recognition_exam_intro_4 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>识别实验：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是100毫秒的单个项目展示，1000毫秒的空白间隔后，会呈现一个四个项目的阵列。</p> ' +
        '<p>要求：记忆单个项目，并在多个项目阵列中快速找到，并根据数字键盘的 " 4 " ," 8 "," 6 "," 2 " 进行选择响应,如果不记得或者不存在选择"5"。</p>' +
        '<p>按" "键继续，实验开始。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const Recall_exam_intro_4 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>回忆实验：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是 2500 毫秒的样本展示，1000毫秒的空白间隔后，会有一个目标刺激的提示。</p> ' +
        '<p>要求：记忆所呈现刺激物的位置，根据提示选择对应刺激的位置，根据数字键盘的 " 4 " ," 8 "," 6 "," 2 " 进行选择响应,如果不记得或者不存在选择"5"。</p>' +
        '<p>按" "键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const Recognition_exam_intro_6 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>识别实验：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是100毫秒的单个项目展示，1000毫秒的空白间隔后，会呈现一个6个项目的阵列。</p> ' +
        '<p>要求：记忆单个项目，并在多个项目阵列中快速找到，并根据数字键盘的 " 1 "," 4 " ," 7 "," 9 "," 6 "," 3 " 进行选择响应,如果不记得或者不存在选择"5"。</p>' +
        '<p>按" "键继续，实验开始。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const Recall_exam_intro_6 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>回忆实验：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是 2500 毫秒的样本展示，1000毫秒的空白间隔后，会有一个目标刺激的提示。</p> ' +
        '<p>要求：记忆所呈现刺激物的位置，根据提示选择对应刺激的位置，根据数字键盘的  " 1 "," 4 " ," 7 "," 9 "," 6 "," 3 " 进行选择响应,如果不记得或者不存在选择"5"。</p>' +
        '<p>按" "键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}

const stim_dist = [[width / 2 - 300, height / 2], [width / 2, height / 2 - 300],
[width / 2 + 300, height / 2], [width / 2, height / 2 + 300]]

//处理获得的刺激数组（4个），各20+5
//形状不一，颜色统一
let shape_variables_4 = generateStimArray("no-hole", 0)
shape_variables_4.push.apply(shape_variables_4, f7(shape_variables_4, 4))
//颜色不一，形状统一
let color_variables_4 = generateStimArray("no-hole", 1)
color_variables_4.push.apply(color_variables_4, f7(color_variables_4, 4))

//处理获得的刺激数组（6个），各36
//形状不一，颜色统一
let shape_variables_6 = generatestim("no-hole", stimArray6, anss7, 6, 0)
// shape_variables_6.push.apply(shape_variables_6 ,f7(shape_variables_6 ))
//颜色不一，形状统一
let color_variables_6 = generatestim("no-hole", stimColorName6, anss7, 6, 1)
// color_variables_6.push.apply(color_variables_6,f7(color_variables_6))

//处理获得的刺激数组（2个），各6+3
//形状不一，颜色统一
let shape_variables_2 = generatestim("no-hole", stimArray3, anss3, 2, 0)
shape_variables_2.push.apply(shape_variables_2, f7(shape_variables_2, 2))
//颜色不一，形状统一
let color_variables_2 = generatestim("no-hole", stimColorName3, anss3, 2, 1)
color_variables_2.push.apply(color_variables_2, f7(color_variables_2, 2))

console.log(shape_variables_2, color_variables_2)
console.log(shape_variables_4, color_variables_4)
console.log(shape_variables_6, color_variables_6)


let recognition_shape_2 = [], recall_shape_2 = [], recognition_color_2 = [], recall_color_2 = []
let recognition_shape_4 = [], recall_shape_4 = [], recognition_color_4 = [], recall_color_4 = []
let recognition_shape_6 = [], recall_shape_6 = [], recognition_color_6 = [], recall_color_6 = []
recognition_shape_2.push.apply(recognition_shape_2, shape_variables_2)
recognition_color_2.push.apply(recognition_color_2, color_variables_2)
recall_shape_2.push.apply(recall_shape_2, shape_variables_2)
recall_color_2.push.apply(recall_color_2, color_variables_2)
recognition_shape_4.push.apply(recognition_shape_4, shape_variables_4)
recognition_color_4.push.apply(recognition_color_4, color_variables_4)
recall_shape_4.push.apply(recall_shape_4, shape_variables_4)
recall_color_4.push.apply(recall_color_4, color_variables_4)
recognition_shape_6.push.apply(recognition_shape_6, shape_variables_6)
recognition_color_6.push.apply(recognition_color_6, color_variables_6)
recall_shape_6.push.apply(recall_shape_6, shape_variables_6)
recall_color_6.push.apply(recall_color_6, color_variables_6)

//生成识别和回忆实验
const recognition_shape_exam_2 = generateRecognitionTrail(recognition_shape_2, dist_loc2, 2, ISI[0], 1, 2, "shape")//18
const recognition_color_exam_2 = generateRecognitionTrail(recognition_color_2, dist_loc2, 2, ISI[0], 1, 2, "color")
const recognition_shape_exam_4 = generateRecognitionTrail(recognition_shape_4, stim_dist, 1, ISI[0], 1, 4, "shape")
const recognition_color_exam_4 = generateRecognitionTrail(recognition_color_4, stim_dist, 1, ISI[0], 1, 4, "color")
const recognition_shape_exam_6 = generateRecognitionTrail(recognition_shape_6, dist_loc6, 1, ISI[0], 1, 6, "shape")
const recognition_color_exam_6 = generateRecognitionTrail(recognition_color_6, dist_loc6, 1, ISI[0], 1, 6, "color")

const recall_shape_exam_2 = generateRecallTrail(recall_shape_2, dist_loc2, 2, ISI[0], 1, 2, "shape")
const recall_color_exam_2 = generateRecallTrail(recall_color_2, dist_loc2, 2, ISI[0], 1, 2, "color")
const recall_shape_exam_4 = generateRecallTrail(recall_shape_4, stim_dist, 1, ISI[0], 1, 4, "shape")
const recall_color_exam_4 = generateRecallTrail(recall_color_4, stim_dist, 1, ISI[0], 1, 4, "color")
const recall_shape_exam_6 = generateRecallTrail(recall_shape_6, dist_loc6, 1, ISI[0], 1, 6, "shape")
const recall_color_exam_6 = generateRecallTrail(recall_color_6, dist_loc6, 1, ISI[0], 1, 6, "color")

//两组实验过程中重新进行眼动校准
const recognition_node_timeline_2 = {
    timeline: [
        Recognition_exam_intro_2,
        recognition_shape_exam_2,
        recognition_color_exam_2,
    ]
}

const recognition_node_timeline_4 = {
    timeline: [
        Recognition_exam_intro_4,
        recognition_shape_exam_4,
        Recognition_exam_intro_4,
        recognition_color_exam_4,
    ]
}

const recognition_node_timeline_6_shape = {
    timeline: [
        Recognition_exam_intro_6,
        recognition_shape_exam_6,
    ]
}
const recognition_node_timeline_6_color = {
    timeline: [
        Recognition_exam_intro_6,
        recognition_color_exam_6
    ]
}


const recall_node_timeline_2 = {
    timeline: [
        Recall_exam_intro_2,
        recall_shape_exam_2,
        recall_color_exam_2,
    ]
}

const recall_node_timeline_4 = {
    timeline: [
        Recall_exam_intro_4,
        recall_shape_exam_4,
        Recall_exam_intro_4,
        recall_color_exam_4,
    ]
}

const recall_node_timeline_6_shape = {
    timeline: [
        Recall_exam_intro_6,
        recall_shape_exam_6,
    ]
}
const recall_node_timeline_6_color = {
    timeline: [
        Recall_exam_intro_6,
        recall_color_exam_6
    ]
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
        let name = data.get().filter({ "trial_type": "survey-text", "trial_index": 2 }).trials[0].response.name
        let exam_type = data.get().filter({ "trial_type": "canvas-keyboard-response" }).trials[0].task
        let ISI = data.get().filter({ "trial_type": "canvas-keyboard-response" }).trials[0].ISI
        let size = data.get().filter({ "trial_type": "canvas-keyboard-response" }).trials[0].size
        let type = data.get().filter({ "trial_type": "canvas-keyboard-response" }).trials[0].type
        if (size !== 6) type = "shape and color"
        console.log(exam_type)
        if (datas.response === 0) {
            data.get().localSave('csv', "../file/"+name + "_" + exam_type + "_" + ISI + "_" + size + "_" + type + "_Exam1_Memory-data.csv")
            
        }
    }
};

let stimArr = {
    "Recognition": {
        "shape": {
            2: recognition_shape_2,
            4: recognition_shape_4,
            6: recognition_shape_6,
        },
        "color": {
            2: recognition_color_2,
            4: recognition_color_4,
            6: recognition_color_6,
        },
    },
    "Recall": {
        "shape": {
            2: recall_shape_2,
            4: recall_shape_4,
            6: recall_shape_6,
        },
        "color": {
            2: recall_color_2,
            4: recall_color_4,
            6: recall_color_6,
        },
    }

}


function f1(ISIs, TaskType, Stimnumber, StudyAttribute) {
    isi = Number(ISIs)
    stimnum = Number(Stimnumber)
    let rep = stimnum === 2 ? 2 : 1;
    let dist = (stimnum === 2) ? dist_loc2 : ((stimnum === 4) ? stim_dist : dist_loc6);
    let intro = eval(TaskType + '_exam_intro_' + Stimnumber)
    console.log(isi,stimnum,TaskType,StudyAttribute)


    const timeline = []
    timeline.push(enter_fullscreen)
    timeline.push(preload)
    timeline.push(survey_before_trail)
    timeline.push(init_camera)
    timeline.push(calibration_timeline)
    timeline.push(intro)

    if (TaskType === "Recognition") {
        if (StudyAttribute === "颜色") {
            let stim = stimArr[TaskType]["color"][stimnum]
            exam = generateRecognitionTrail(stim, dist, rep, isi, 1, stimnum, "color")
            timeline.push(exam)
        } else if (StudyAttribute === "形状") {
            let stim = stimArr[TaskType]["shape"][stimnum]
            exam = generateRecognitionTrail(stim, dist, rep, isi, 1, stimnum, "shape")
            timeline.push(exam)
        }else {
            let exam1, exam2, stim1, stim2
            stim1 = stimArr[TaskType]["shape"][stimnum]
            stim2 = stimArr[TaskType]["color"][stimnum]
            exam1 = generateRecognitionTrail(stim1, dist, rep, isi, 1, stimnum, "shape")
            exam2 = generateRecognitionTrail(stim2, dist, rep, isi, 1, stimnum, "color")
            timeline.push(exam1)
            
            timeline.push(exam2)
        }  
    } else {
        if (StudyAttribute === "颜色") {
            let stim = stimArr[TaskType]["color"][stimnum]
            exam = generateRecallTrail(stim, dist, rep, isi, 1, stimnum, "color")
            timeline.push(exam)
        } else if (StudyAttribute === "形状"){
            let stim = stimArr[TaskType]["shape"][stimnum]
            exam = generateRecallTrail(stim, dist, rep, isi, 1, stimnum, "shape")
            timeline.push(exam)
        } else {
            let exam1, exam2, stim1, stim2
            stim1 = stimArr[TaskType]["shape"][stimnum]
            stim2 = stimArr[TaskType]["color"][stimnum]
            exam1 = generateRecallTrail(stim1, dist, rep, isi, 1, stimnum, "shape")
            exam2 = generateRecallTrail(stim2, dist, rep, isi, 1, stimnum, "color")
            timeline.push(exam1)
            timeline.push(exam2)
        }  
    }
    timeline.push(exit_fullscreen)
    timeline.push(exam_done)
    timeline.push(show_data)
    console.log(timeline)
    run(timeline)
}


