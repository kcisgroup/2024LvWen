const {data, run, timelineVariable} = initJsPsych({});

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

//实验前信息调查
const survey_before_trail = {
    timeline: [
        {
            type: jsPsychSurveyText,
            questions: [
                {prompt: "姓名:", required: true, name: 'name'},
            ]
        },
    ],
    css_classes: ['mouse'],
}
const exam_intro = {
    type: jsPsychHtmlButtonResponse,
    stimulus: '<p>根据自己对网页的印象，完成问卷。</p> ',
    choices: ['确定'],
    post_trial_gap: 500,
}
const exam_intro1 = {
    type: jsPsychImageButtonResponse,
    stimulus: './img/Booking.png',
    stimulus_width:1100,
    maintain_aspect_ration:true,
    choices: ['确定'],
    post_trial_gap: 500,
}
const exam_intro2 = {
    type: jsPsychImageButtonResponse,
    stimulus: './img/tuniu.png',
    stimulus_width:1100,
    maintain_aspect_ration:true,
    choices: ['确定'],
    post_trial_gap: 500,
}

var likert_scale = [
    "1(非常不满意)",
    "2",
    "3",
    "4",
    "5(非常满意)"
];

var trial1 = {
    type: jsPsychSurveyLikert,
    questions: [
        {prompt: "1、网站的整体外观和布局：", name: '1', labels: likert_scale},
        {prompt: "2、网站的颜色和图像选择：", name: '2', labels: likert_scale},
        {prompt: "3、信息的呈现方式和清晰度：", name: '3', labels: likert_scale},
        {prompt: "4、网站的导航菜单和链接的可见性和易用性：", name: '4', labels: likert_scale},
        {prompt: "5、对网站的整体印象：", name: '5', labels: likert_scale},
        {prompt: "6、是否愿意使用这个网站进行门票预定：", name: '6', labels: likert_scale},
    ],
};

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
        let name = data.get().filter({"trial_type": "survey-text", "trial_index": 1}).trials[0].response.name
        if (datas.response === 0) {
            data.get().localSave('csv', name + "_survey.csv")
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

let block={
    timeline:[exam_intro1,trial1,exam_intro2,trial1]
}

let preload_block={
    type:jsPsychPreload,
    trails:[block]
}

function f1(){
    let timeline = []
    timeline.push(enter_fullscreen)
    timeline.push(survey_before_trail)
    timeline.push(preload_block)
    timeline.push(exam_intro)
    timeline.push(block)
    timeline.push(exit_fullscreen)
    timeline.push(exam_done)
    timeline.push(show_data)
    run(timeline)
}
