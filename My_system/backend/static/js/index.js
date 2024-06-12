const { data, run, timelineVariable } = initJsPsych({
    extensions: [
        { type: jsPsychExtensionWebgazer }
    ],
});
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
                { prompt: "姓名:", required: true, name: 'name' },
            ]
        },
    ],
    css_classes: ['mouse'],
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
    calibration_points: [
        [15, 15],
        [15, 50],
        [15, 85],
        [50, 15],
        [50, 50],
        [50, 85],
        [85, 15],
        [85, 50],
        [85, 85]
    ],
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
        [15, 15],
        // [10, 50],
        [15, 85],
        // [50, 10],
        [50, 50],
        // [50, 90],
        [85, 15],
        // [90, 50],
        [85, 85],
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
        var validation_data = data.get().filter({ task: 'validate' }).values()[0];
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
        var validation_data = data.getLastTrialData().filter({ task: 'validate' }).values()[0];
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

const exam_intro = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<p>自由浏览网页，完成后按”0“退出，下载数据；</p> ' +
        '按下空格键继续实验。',
    choices: [' '],
    post_trial_gap: 500,
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
        // 1. 从原始数据中提取webgazer_data
        console.log(data.get().filter({ "trial_type": "html-keyboard-response", "response": "0" }))
        let webgazerData = data.get().filter({
            "trial_type": "html-keyboard-response",
            "response": "0"
        }).trials[0].webgazer_data;
        console.log(webgazerData)
        let webgazerDataCSV = "";
        let webgazerDataCSV1 = "";// 根据 webgazer 数据的结构创建 CSV 头
        for (let i = 0; i < webgazerData.length; i++) {
            webgazerDataCSV1 += webgazerData[i].x + "," + webgazerData[i].y + "," + webgazerData[i].t + "\n";
            webgazerDataCSV += webgazerData[i].x + "," + webgazerData[i].y + "\n";
        }
        if (datas.response === 0) {
            let webgazerDataFilename = name + "-webgazer-data.csv";
            let blob = new Blob([webgazerDataCSV], { type: 'text/csv' });
            saveAs(blob, webgazerDataFilename);
            let webgazerDataFilename1 = name + "-webgazer-data.csv";
            let blob1 = new Blob([webgazerDataCSV1], { type: 'text/csv' });
            saveAs(blob1, webgazerDataFilename1);

            // 4. 更新原始数据以包含webgazer_data的文件地址
            data.get().filter({
                "trial_type": "html-keyboard-response",
                "response": "0"
            }).trials[0].webgazer_data = webgazerDataFilename
            data.get().localSave('csv', name + "-eye-data.csv")
        }
    }
}


function f1(exam_url) {
    var externalHtmlContent, virtualElement; // 用于存储外部 HTML 内容
    // 使用 fetch 获取外部 HTML 内容
    fetch('/get_qian_html')
        .then(response => response.text())
        .then(data => {
            externalHtmlContent = data; // 存储 HTML 内容
            console.log(externalHtmlContent)
            // 修改 HTML 内容中某个元素的 src 属性
            virtualElement = document.createElement('div');
            virtualElement.innerHTML = externalHtmlContent;
            var targetElement = virtualElement.querySelector('#consent');
            if (exam_url == "tuniu") targetElement.src = 'http://127.0.0.1:5500/backend/templates/tuniu.html';
            else targetElement.src = 'http://127.0.0.1:5500/backend/templates/Booking.html';
            externalHtmlContent = virtualElement.innerHTML
            console.log(externalHtmlContent)

            // 定义实验块，用于呈现外部 HTML 内容
            var externalHtmlTrial = {
                type: jsPsychHtmlKeyboardResponse,
                choices: ['0'],
                stimulus: function () {
                    return externalHtmlContent; // 使用预先加载的 HTML 内容
                },
                extensions: [{
                    type: jsPsychExtensionWebgazer,
                    initialize: function (params) {
                        // 在外部 HTML 加载完成后启动眼动数据收集
                        webgazer.resume();
                    },
                    params: { targets: ['#consent'] }
                }],

                on_finish: function (data) {
                    window.parent.postMessage({ type: 'exitExternalPage' }, '*');
                },
            };

            let timeline = []
            timeline.push(enter_fullscreen)
            timeline.push(survey_before_trail)
            timeline.push(exam_intro)
            timeline.push(init_camera)
            timeline.push(calibration_timeline)
            timeline.push(externalHtmlTrial)
            timeline.push(exit_fullscreen)
            timeline.push(exam_done)
            run(timeline)
        })
        .catch(error => {
            console.error('Error fetching HTML content:', error);
        });

}






