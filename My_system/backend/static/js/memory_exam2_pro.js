const {data, run, timelineVariable} = initJsPsych({
    extensions: [
        {type: jsPsychExtensionWebgazer}
    ],

});
const Recognition_introduce_exam = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>识别实验（两个刺激物）：每个试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是100毫秒的单个项目展示，' + ISI[0] + '毫秒的空白间隔后，会呈现一个两个项目的阵列。</p> ' +
        '<p>实验要求：记忆单个项目，根据其' + '<b>形状（该条件下，颜色为黑色）</b>' + '或者' + '<b>颜色（该条件下，形状为圆且颜色不为黑）</b>' + '，忽略其拓扑特征，在多个项目阵列中快速找到，通过数字键盘的 "4","6" 响应，不记得或者不存在选择"5" 。</p>' +
        '<p>按"space"键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}
const Recall_introduce_exam = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>回忆实验（两个刺激物）：每个试验都以 500 毫秒的固定时间开始，然后会有一个 500 毫秒的fixation，接下来是 2500 毫秒的样本展示，' + ISI[0] + '毫秒的空白间隔后，会有一个目标刺激的提示。</p> ' +
        '<p>实验要求：记忆所呈现刺激物和其对应的位置，根据目标提示的' + '<b>形状（该条件下，颜色为黑色）</b>' + '或者' + '<b>颜色（该条件下，形状为圆且颜色不为黑）</b>' + '，忽略其拓扑特征，' +
        '选择对应刺激的位置，左边按数字键盘的 "4" ,右边按 "6" ，不记得或者不存在选择 "5" 。</p>' +
        '<p>按"space"键继续。</p>',
    choices: [' '],
    post_trial_gap: 500,
}

//处理获得的刺激数组（2个），各6+3
//T
let shape_variables_2_T= generatestim("hole", stimArray3,anss3,2,0)//形状
shape_variables_2_T.push.apply(shape_variables_2_T ,f7(shape_variables_2_T,2))//目标不存在的情况
let color_variables_2_T = generatestim("hole", stimColorName3 ,anss3,2,1)//颜色
color_variables_2_T.push.apply(color_variables_2_T,f7(color_variables_2_T,2))//目标不存在的情况
//D
let shape_variables_2_D= generatestim("hole-no-hole", stimArray3,anss3,2,0)//形状
shape_variables_2_D.push.apply(shape_variables_2_D ,f7(shape_variables_2_D,2))//目标不存在的情况
let color_variables_2_D = generatestim("hole-no-hole", stimColorName3 ,anss3,2,1)//颜色
color_variables_2_D.push.apply(color_variables_2_D,f7(color_variables_2_D,2))//目标不存在的情况

console.log(shape_variables_2_T,color_variables_2_T,shape_variables_2_D,color_variables_2_D)

let recognition_shape = [], recall_shape = [], recognition_color = [], recall_color = []

recognition_shape.push.apply(recognition_shape, shape_variables_2_T)
recognition_shape.push.apply(recognition_shape, shape_variables_2_D)//topo作为非目标
recognition_color.push.apply(recognition_color, color_variables_2_T)
recognition_color.push.apply(recognition_color, color_variables_2_D)//topo作为非目标
recall_shape.push.apply(recall_shape, shape_variables_2_T)
recall_shape.push.apply(recall_shape, shape_variables_2_D)//topo作为非目标
recall_color.push.apply(recall_color, color_variables_2_T)
recall_color.push.apply(recall_color, color_variables_2_D)

//生成识别和回忆实验
// const recognition_shape_exam= generateRecognitionTrail(recognition_shape, dist_loc2,2,ISI[0],0,2,"shape")//18
const recognition_color_exam = generateRecognitionTrail(recognition_color, dist_loc2,2,ISI[0],0,2,"color")

// const recall_shape_exam = generateRecallTrail(recall_shape, dist_loc2,2,ISI[0],0,2,"shape")//18
const recall_color_exam = generateRecallTrail(recall_color, dist_loc2,2,ISI[0],0,2,"color")

const recognition_node_timeline = {
    timeline: [
         // shape_exam_intro,
        // recognition_shape_exam,
        color_exam_intro,
        recognition_color_exam
    ]
}

const recall_node_timeline = {
    timeline: [
        Recall_introduce_exam,
        // shape_exam_intro,
        // recall_shape_exam,
        color_exam_intro,
        recall_color_exam
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
        let name = data.get().filter({"trial_type": "survey-text", "trial_index": 2}).trials[0].response.name
        let exam_type = data.get().filter({"trial_type": "canvas-keyboard-response"}).trials[0].task
        let ISI = data.get().filter({"trial_type": "canvas-keyboard-response"}).trials[0].ISI
        if (datas.response === 0) {
            data.get().localSave('csv', name + "_" + exam_type + "_" + ISI + "_2_shape and color_Exam_pro_Memory-data.csv")
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
    let intro = eval(TaskType + '_introduce_exam')
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
            exam = generateRecognitionTrail(stim, dist_loc2, 2, isi, 0, 2, "color")
            timeline.push(color_exam_intro)
            timeline.push(exam)
        } else if (StudyAttribute === "形状") {
            let stim = stimArr[TaskType]["shape"]
            exam = generateRecognitionTrail(stim, dist_loc2, 2, isi, 0, 2, "shape")
            timeline.push(shape_exam_intro)
            timeline.push(exam)
        } 
    } else {
        if (StudyAttribute === "颜色") {
            let stim = stimArr[TaskType]["color"]
            exam = generateRecallTrail(stim, dist_loc2, 2, isi, 0, 2, "color")
            timeline.push(color_exam_intro)
            timeline.push(exam)
        } else if (StudyAttribute === "形状"){
            let stim = stimArr[TaskType]["shape"]
            exam = generateRecallTrail(stim, dist_loc2, 2, isi, 0, 2, "shape")
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