//size=6
const {data, run, timelineVariable} = initJsPsych({
    extensions: [
        {type: jsPsychExtensionWebgazer}
    ],
});

const Recognition_exam_intro = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>识别实验（6个刺激物）：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是100毫秒的单个项目展示，' + ISI[0] + '毫秒的空白间隔后，会呈现一个六个项目的阵列。</p> ' +
        '<p>要求：记忆单个项目，并在多个项目阵列中快速找到，并根据数字键盘的 "4", "7", "9", "6", "3", "1" 进行选择响应，如果不记得或者不存在选择 "5"。</p>' +
        '<p>按"space"键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}

const Recall_exam_intro = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>回忆实验（6个刺激物）：试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是 2500 毫秒的样本展示，' + ISI[0] + '毫秒的空白间隔后，会有一个目标刺激的提示。</p> ' +
        '<p>要求：记忆所呈现刺激物和其对应的位置，根据目标提示选择对应刺激的位置，根据数字键盘的 "4", "7", "9", "6", "3", "1" 进行选择响应，如果不记得或者不存在选择"5"。</p>' +
        '<p>按"space"键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}



//六个刺激物
//处理获得的刺激数组（6个），各36
//形状不一，颜色统一
let shape_variables_6_T = generatestim("hole", stimArray6,anss7,6,0)
let shape_variables_6_D = generatestim("hole-no-hole", stimArray6,anss7,6,0)
//颜色不一，形状统一
let color_variables_6_T = generatestim("hole", stimColorName6 ,anss7,6,1)
let color_variables_6_D = generatestim("hole-no-hole", stimColorName6 ,anss7,6,1)

let recognition_shape = [], recall_shape = [], recognition_color = [], recall_color = []
recognition_shape.push.apply(recognition_shape, shape_variables_6_T)
recognition_shape.push.apply(recognition_shape, shape_variables_6_D)//topo作为非目标对象特征
recognition_color.push.apply(recognition_color, color_variables_6_T)
recognition_color.push.apply(recognition_color, color_variables_6_D)//topo作为非目标对象特征
recall_shape.push.apply(recall_shape, shape_variables_6_T)
recall_shape.push.apply(recall_shape, shape_variables_6_D)//topo作为非目标
recall_color.push.apply(recall_color, color_variables_6_T)
recall_color.push.apply(recall_color, color_variables_6_D)

//生成识别和回忆实验
// const recognition_shape_exam= generateRecognitionTrail(recognition_shape, dist_loc6,1,ISI[0],1,6,"shape")//36
const recognition_color_exam = generateRecognitionTrail(recognition_color, dist_loc6,1,ISI[0],1,6,"color")

// const recall_shape_exam = generateRecallTrail(recall_shape, dist_loc6,1,ISI[0],1,6,"shape")//36
const recall_color_exam = generateRecallTrail(recall_color, dist_loc6,1,ISI[0],1,6,"color")

// const recognition_node_timeline_shape = {
//     timeline: [
//         recognition_exam_intro,
//         shape_exam_intro,
//         recognition_shape_exam
//     ]
// }
// const recognition_node_timeline_color = {
//     timeline: [
//         recognition_exam_intro,
//         color_exam_intro,
//         recognition_color_exam
//     ]
// }
// const recall_node_timeline_shape = {
//     timeline: [
//         recall_exam_intro,
//         shape_exam_intro,
//         recall_shape_exam,
//     ]
// }
// const recall_node_timeline_color = {
//     timeline: [
//         recall_exam_intro,
//         color_exam_intro,
//         recall_color_exam
//     ]
// }
let exam_done = {
    type: jsPsychHtmlButtonResponse,
    choices: ['CSV'],
    css_classes: ['mouse'],
    stimulus: `
         <p>实验结束!</p>
         <p>点击下载数据。</p>
`,
    on_finish: function (datas) {
        let name = data.get().filter({"trial_type": "survey-text", "trial_index": 2}).trials[0].response.name
        let exam_type = data.get().filter({"trial_type": "canvas-keyboard-response"}).trials[0].task
        let ISI = data.get().filter({"trial_type": "canvas-keyboard-response"}).trials[0].ISI
        let type = data.get().filter({"trial_type": "canvas-keyboard-response"}).trials[0].type
        if (datas.response === 0) {
            data.get().localSave('csv', name + "_" + exam_type + "_" + ISI + "_6_" + type + "_Exam_Memory-data.csv")
        }
    }
}


let stimArr = {
    "Recognition": {
        "shape": recognition_shape,     
        "color": recognition_color
    },
    "Recall": {
        "shape": recall_shape,
        "color": recall_color
    }
}

function f1(ISIs, TaskType, StudyAttribute) {
    isi = Number(ISIs)
    let intro = eval(TaskType + '_exam_intro')
    console.log(isi,TaskType,StudyAttribute)


    const timeline = []
    timeline.push(enter_fullscreen)
    timeline.push(preload)
    timeline.push(survey_before_trail)
    timeline.push(init_camera)
    timeline.push(calibration_timeline)
    timeline.push(intro)

    if (TaskType === "Recognition") {
        if (StudyAttribute === "颜色") {
            let stim = stimArr[TaskType]["color"]
            exam = generateRecognitionTrail(stim, dist_loc6, 1, isi, 1, 6, "color")
            timeline.push(color_exam_intro)
            timeline.push(exam)
        } else if (StudyAttribute === "形状") {
            let stim = stimArr[TaskType]["shape"]
            exam = generateRecognitionTrail(stim, dist_loc6, 1, isi, 1, 6, "shape")
            timeline.push(shape_exam_intro)
            timeline.push(exam)
        } 
    } else {
        if (StudyAttribute === "颜色") {
            let stim = stimArr[TaskType]["color"]
            exam = generateRecallTrail(stim, dist_loc6, 1, isi, 1, 6, "color")
            timeline.push(color_exam_intro)
            timeline.push(exam)
        } else if (StudyAttribute === "形状"){
            let stim = stimArr[TaskType]["shape"]
            exam = generateRecallTrail(stim, dist_loc6, 1, isi, 1, 6, "shape")
            timeline.push(shape_exam_intro)
            timeline.push(exam)
        } 
    }
    timeline.push(exit_fullscreen)
    timeline.push(exam_done)
    timeline.push(show_data)
    console.log(timeline)
    run(timeline)
}