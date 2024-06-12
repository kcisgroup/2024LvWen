import json
import math
import os
import re
from typing import Dict, List
import io
import base64
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import kruskal

from static.pythonfiles.datafunc import process_data, namefun, preprocess_value
import statsmodels.formula.api as smf

# 设置刺激的范围
Dicts = {"2": 200, "4": 200, "6": 150}


# 获取落在范围内的注视点，并且为落在范围的第一个刺激标记
def dictDefine(
    webgazer_data,
    stimuli,
    webgazer_targets_data,
    num,
    target,
    target_id,
    motion,
    mchange,
):
    dots = []
    for j in range(len(stimuli)):
        do = []
        if motion == 1.0 and mchange == "trans" and j == target_id:
            dist = Dicts[num] + 50
        else:
            dist = Dicts[num]
        for i in range(len(webgazer_data)):
            dot = []
            min_t = float("inf")  # 初始化为正无穷大
            for n in range(len(webgazer_data[i])):
                dicts = math.sqrt(
                    math.pow(
                        webgazer_data[i][n]["x"] - webgazer_targets_data[j]["x"], 2
                    )
                    + math.pow(
                        webgazer_data[i][n]["y"] - webgazer_targets_data[j]["y"], 2
                    )
                )
                if dicts < dist:
                    if webgazer_data[i][n]["t"] < min_t:
                        if j > 0:
                            for m in range(len(dots)):
                                for item in dots[m].keys():
                                    # print(dots[m][item][i])
                                    if len(dots[m][item][i]) > 0:
                                        dots[m][item][i][0]["tagged"] = False
                        # 更新最小t值
                        min_t = webgazer_data[i][n]["t"]
                        webgazer_data[i][n]["tagged"] = True
                        if len(dot) > 0:
                            webgazer_data[i][n]["tagged"] = False
                    else:
                        webgazer_data[i][n]["tagged"] = False
                    dot.append(webgazer_data[i][n])  # 把合适的眼动数据点放入dot
            do.append(dot)
        if len(do) > 0:
            dots.append({stimuli[j]: do})
    # print(dots)
    return dots


# 获取第二段数据的注视点运动轨迹
def dictDefine2(
    webgazer_data,
    stimuli,
    webgazer_targets_data,
    num,
    target,
    target_id,
    motion,
    mchange,
):
    dots = []
    for i in range(len(webgazer_data)):  # 4
        dot = []
        for j in range(len(stimuli)):
            if motion == 1.0 and mchange == "trans" and j == target_id:
                dist = Dicts[num] + 50
            else:
                dist = Dicts[num]
            min_t = float("inf")  # 初始化为正无穷大
            for n in range(len(webgazer_data[i])):
                dicts = math.sqrt(
                    math.pow(
                        webgazer_data[i][n]["x"] - webgazer_targets_data[j]["x"], 2
                    )
                    + math.pow(
                        webgazer_data[i][n]["y"] - webgazer_targets_data[j]["y"], 2
                    )
                )
                if dicts < dist:
                    if webgazer_data[i][n]["t"] < min_t:
                        # 更新最小t值
                        min_t = webgazer_data[i][n]["t"]
            dot.append({stimuli[j]: min_t})  # 把合适的眼动数据点放入dot
        dots.append(sorted(dot, key=lambda d: list(d.values())[0]))
    # print(dots)
    filtered_data = [
        [d for d in sublist if list(d.values())[0] != float("inf")] for sublist in dots
    ]
    return filtered_data


# 获取落在目标刺激范围内的注视点
def dictDefine1(webgazer_data, target, webgazer_targets_data, num, motion, mchange):
    dots = {}
    do = []
    if motion == 1.0 and mchange == "trans":
        dist = Dicts[num] + 50
    else:
        dist = Dicts[num]
    for i in range(len(webgazer_data)):
        dot = []
        for j in range(len(webgazer_data[i])):
            dicts = math.sqrt(
                math.pow(webgazer_data[i][j]["x"] - webgazer_targets_data["x"], 2)
                + math.pow(webgazer_data[i][j]["y"] - webgazer_targets_data["y"], 2)
            )
            if dicts < dist:
                dot.append(webgazer_data[i][j])
        if len(dot) > 0:
            do.append(dot)
    if len(do) > 0:
        dots[target] = do
    return dots


# 处理收集到的眼动数据
def eyeDataProcess(webgazer_data, canvas_data):
    target_canvas_data_x = canvas_data["#container"]["x"]
    target_canvas_data_y = canvas_data["#container"]["y"]
    for i in range(len(webgazer_data)):
        for j in range(len(webgazer_data[i])):
            webgazer_data[i][j]["x"] = webgazer_data[i][j]["x"] - target_canvas_data_x
            webgazer_data[i][j]["y"] = webgazer_data[i][j]["y"] - target_canvas_data_y
    return webgazer_data


# 获取标记好的刺激
def findTaggedKeys(dots):
    tagged_keys = ["", "", "", ""]
    for item in dots:
        # print(item.items())
        for key, values in item.items():
            for i in range(len(values)):
                if any(value["tagged"] for value in values[i]):
                    tagged_keys[i] = key
    # print(tagged_keys)
    return tagged_keys


# 不同刺激数目下，目标对应的位置
ans_index = {
    "2": {"4": 0, "6": 1},
    "4": {"4": 0, "8": 1, "6": 2, "2": 3},
    "6": {"4": 0, "7": 1, "9": 2, "6": 3, "3": 4, "1": 5},
}


# 筛选并处理眼动数据，寻找首个注视的刺激
def eyeDatady(paths):
    files = os.listdir(paths)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)
        num = re.findall(r"_(\d+)_", file_name)[0]
        # num = "4"
        dt_rt, df = process_data(paths + "\\" + f)
        # 添加一个空列
        # 重置索引
        df = df.reset_index()
        df["fixation"] = None
        df["fixation_target"] = None
        df["first_dot"] = None
        df["movement"] = None
        df["first"] = None
        # 迭代DataFrame的行
        for index, row in df.iterrows():
            if pd.notnull(row["answer"]) and row["answer"] != 5:
                webgazer_data = json.loads("[" + row["webgazer_data"] + "]")

                canvas_data = json.loads(row["canvas_data"])
                stimuli = json.loads(row["stimulus"])
                target = row["target"]
                motion = row["motion"]
                mchange = row["mchange"]
                eyeDataProcess(webgazer_data, canvas_data)
                target_id = int(ans_index[num][str(int(row["answer"]))])
                target_data = json.loads(row["webgazer_targets_data"])
                dots = dictDefine(
                    webgazer_data,
                    stimuli,
                    target_data,
                    num,
                    target,
                    target_id,
                    motion,
                    mchange,
                )
                first_dot = findTaggedKeys(dots)
                dots_target = dictDefine1(
                    webgazer_data, target, target_data[target_id], num, motion, mchange
                )

                if len(dots) > 0:
                    df.loc[index, "fixation"] = str(dots)
                    if len(dots_target) > 0:
                        df.loc[index, "fixation_target"] = str(dots_target)
                    # if len(first_dot) > 0:
                    #     if (target == str(first_dot[0])) or (target.split("_")[0] == str(first_dot[0])):
                    #         df.loc[index, "first_dot"] = target
                    #     else:
                    df.loc[index, "first_dot"] = str(first_dot)
                    move = dictDefine2(
                        webgazer_data,
                        stimuli,
                        target_data,
                        num,
                        target,
                        target_id,
                        motion,
                        mchange,
                    )
                    df.loc[index, "movement"] = str(move)
                    if len(move[1]) > 0:  # 第二段数据存在
                        # 第一个数据是目标
                        if (target == str(list(move[1][0].keys())[0])) or (
                            target.split("_")[0] == str(list(move[1][0].keys())[0])
                        ):
                            df.loc[index, "first"] = target
                        else:  # 第一个数据不是目标
                            # 第二段数据长度为1，
                            if len(move[1]) == 1:
                                # 第一段数据最后一个和第二段的数据相同
                                if len(move[0]) > 0 and (
                                    str(list(move[0][-1].keys())[0])
                                    == str(list(move[1][0].keys())[0])
                                ):
                                    if (
                                        len(move[2]) > 0
                                    ):  # 第三段存在，选第三段数据的第一个
                                        if (
                                            target == str(list(move[2][0].keys())[0])
                                        ) or (
                                            target.split("_")[0]
                                            == str(list(move[2][0].keys())[0])
                                        ):
                                            df.loc[index, "first"] = target
                                        else:  # 第一个不是目标
                                            # 第三段为1，且三段数据相同，选第四段第一个
                                            if (
                                                len(move[2]) == 1
                                                and len(move[3]) > 0
                                                and (
                                                    str(list(move[1][0].keys())[0])
                                                    == str(list(move[2][0].keys())[0])
                                                )
                                            ):
                                                if (
                                                    target
                                                    == str(list(move[3][0].keys())[0])
                                                ) or (
                                                    target.split("_")[0]
                                                    == str(list(move[3][0].keys())[0])
                                                ):
                                                    df.loc[index, "first"] = target
                                            # 第三段大于1，且三段数据第一个相同，选第三段第二个
                                            if (
                                                len(move[2]) > 1
                                                and (
                                                    str(list(move[1][0].keys())[0])
                                                    == str(list(move[2][0].keys())[0])
                                                )
                                                and (
                                                    (
                                                        target
                                                        == str(
                                                            list(move[2][1].keys())[0]
                                                        )
                                                    )
                                                    or (
                                                        target.split("_")[0]
                                                        == str(
                                                            list(move[2][1].keys())[0]
                                                        )
                                                    )
                                                )
                                            ):
                                                df.loc[index, "first"] = target
                            # 第二个数据是目标
                            if len(move[1]) > 1:
                                if len(move[0]) > 0 and (
                                    str(list(move[0][-1].keys())[0])
                                    == str(list(move[1][0].keys())[0])
                                ):
                                    if (target == str(list(move[1][1].keys())[0])) or (
                                        target.split("_")[0]
                                        == str(list(move[1][1].keys())[0])
                                    ):
                                        df.loc[index, "first"] = target
                    else:
                        # 第二段不存在，第三段存在
                        if len(move[2]) > 0:
                            if (target == str(list(move[2][0].keys())[0])) or (
                                target.split("_")[0] == str(list(move[2][0].keys())[0])
                            ):
                                df.loc[index, "first"] = target
                        else:
                            # 第三段不存在，第四段存在
                            if len(move[3]) > 0:
                                if (target == str(list(move[3][0].keys())[0])) or (
                                    target.split("_")[0]
                                    == str(list(move[3][0].keys())[0])
                                ):
                                    df.loc[index, "first"] = target
                            # else:
                            #     if len(move[1]) > 1:
                            #         if (target == str(list(move[1][1].keys())[0])) or (
                            #                 target.split("_")[0] == str(list(move[1][1].keys())[0])):
                            #             df.loc[index, "first"] = target
            else:
                continue
        df.to_csv(
            paths + "\\eyedata\\" + file_name + "_eyedata.csv",
            index=False,
            encoding="utf-8",
        )


paths = r"E:\数据汇总\dynamic"


# eyeData(paths)


# 将识别和回忆的眼动数据分割，并计数
def fun(df):
    dt = pd.DataFrame()
    # 按照Examtype分割数据为recall和recognition两个子集
    recall_data = df[df["Examtype"] == "recall"]
    recognition_data = df[df["Examtype"] == "recognition"]
    # 统计每个name的计数
    recall_counts = recall_data["name"].value_counts()
    recognition_counts = recognition_data["name"].value_counts()
    combined_counts = pd.concat(
        [recall_counts, recognition_counts], axis=1, keys=["A", "O"]
    )
    dt = pd.concat([dt, combined_counts], axis=1)
    # print(dt)
    return dt


# 绘制不同数量下注视点数量的箱线图
def draw(df, df_not, num):
    dt_s = fun(df[df["TYPE"] == "shape"])
    dt_c = fun(df[df["TYPE"] == "color"])
    dt_not_s = fun(df_not[df_not["TYPE"] == "shape"])
    dt_not_c = fun(df_not[df_not["TYPE"] == "color"])
    combined_counts = pd.concat(
        [dt_s, dt_c, dt_not_s, dt_not_c], axis=1, keys=["T_S", "T_C", "D_S", "D_C"]
    )
    # dt = fun(df)
    # dt_not = fun(df_not)
    # combined_counts = pd.concat([dt, dt_not], axis=1, keys=['T', 'D'])

    # 合并一级列索引和二级列索引
    combined_counts.columns = ["_".join(col) for col in combined_counts.columns]
    print(combined_counts)
    # 使用 pd.melt() 函数将列转换为标识和值的列
    melted_df = pd.melt(combined_counts, var_name="Label", value_name="Value")

    # 创建1行2列的子图布局
    fig = plt.subplots(figsize=(8, 5), sharey=True, sharex=True)
    # 创建自定义调色板
    my_palette = sns.color_palette(["white", "gray"])
    sns.boxplot(data=melted_df, palette=my_palette, x="Label", y="Value")
    # # 绘制recognition子图
    # sns.boxplot(ax=axes[1], data=combined_counts['df_not'], orient='v')
    plt.ylabel("eyedata")
    plt.xlabel(num + "_eyedata")
    # 调整子图布局
    plt.tight_layout()
    # 保存为svg格式
    plt.savefig(
        r"E:\数据汇总\dynamic\eyedata\pic\\" + num + "_eyedot.svg", format="svg"
    )


arr_shape: Dict[str, List[str]] = {
    "6": ["rect", "triangle", "circle", "star", "hexagram", "diamond"],
    "4": ["rect", "triangle", "circle", "star", "hexagram"],
    "2": ["rect", "triangle", "circle"],
}
arr_color = {
    "6": ["green", "yellow", "blue", "purple", "red", "cyan"],
    "4": ["green", "yellow", "blue", "purple", "red"],
    "2": ["green", "blue", "red"],
}


# Formal experiment
# 运动变化和拓扑变化的首次注视点
def drawStim(df):
    ds_t = df[(df["TYPE"] == "shape") & (df["Target"] == "topo")]["eyedata"]
    ds_m = df[(df["TYPE"] == "shape") & (df["Target"] == "motion")]["eyedata"]
    dc_t = df[(df["TYPE"] == "color") & (df["Target"] == "topo")]["eyedata"]
    dc_m = df[(df["TYPE"] == "color") & (df["Target"] == "motion")]["eyedata"]
    combined_counts = pd.concat(
        [ds_t, ds_m, dc_t, dc_m],
        axis=1,
        keys=["T_shape", "M_shape", "T_color", "M_color"],
    )
    # 使用 pd.melt() 函数将列转换为标识和值的列
    # 创建自定义调色板
    melted_df = pd.melt(combined_counts, var_name="Label", value_name="Value")
    my_palette = sns.color_palette(["#1597a5", "#0e606b", "#fff4f2", "#feb3ae"])
    fig = plt.subplots(figsize=(4, 3.3), sharey=True, sharex=True)
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.xticks(fontname="Times New Roman")
    plt.yticks(fontname="Times New Roman")
    sns.boxplot(data=melted_df, palette=my_palette, x="Label", y="Value", width=0.4)

    plt.ylabel("eyedata", fontname="Times New Roman", fontsize=11)
    plt.xlabel("first-eyedata", fontname="Times New Roman", fontsize=11)
    # 调整子图布局
    plt.tight_layout()
    # plt.savefig(r'E:\数据汇总\dynamic\4\汇总\compare_data.svg', format='svg')
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\动态A\\compare_data" + ".jpg",
    #     format="jpg",
    #     dpi=1000,
    # )
    # plt.show()
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    res = base64.b64encode(buffer.read()).decode("utf-8")
    return res


# 运动变化和拓扑变化的首次注视点(详细）
def drawStim1(dfs, typess):
    res = {}
    for i, types in enumerate(["shape", "color"]):
        df = dfs[dfs["TYPE"] == types]
        ds_t = df[(df["Change"] == "single") & (df["Target"] == "topo")]["eyedata"]
        ds_m = df[(df["Change"] == "zoom") & (df["Target"] == "motion")]["eyedata"]
        dc_t = df[(df["Change"] == "double") & (df["Target"] == "topo")]["eyedata"]
        dc_m = df[(df["Change"] == "trans") & (df["Target"] == "motion")]["eyedata"]
        combined_counts = pd.concat(
            [ds_t, dc_t, ds_m, dc_m],
            axis=1,
            keys=["T_single", "T_double", "M_scaling", "M_trans"],
        )
        # 使用 pd.melt() 函数将列转换为标识和值的列
        # 创建自定义调色板
        melted_df = pd.melt(combined_counts, var_name="Label", value_name="Value")
        my_palette = sns.color_palette(["#1597a5", "#0e606b", "#fff4f2", "#feb3ae"])
        fig = plt.subplots(figsize=(4, 3.3), sharey=True, sharex=True)
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = ["Times New Roman"]
        plt.xticks(fontname="Times New Roman")
        plt.yticks(fontname="Times New Roman")
        sns.boxplot(data=melted_df, palette=my_palette, x="Label", y="Value", width=0.4)
        plt.ylabel("eyedata", fontname="Times New Roman", fontsize=11)
        plt.xlabel(types + "_first-eyedata", fontname="Times New Roman", fontsize=11)
        # 调整子图布局
        plt.tight_layout()
        # plt.savefig(r'E:\数据汇总\dynamic\4\汇总\compare_data_' + types + '.svg', format='svg')
        # plt.savefig(
        #     r"E:\小论文\小论文图\数据图\动态A\\compare_data_" + types + ".jpg",
        #     format="jpg",
        #     dpi=1000,
        # )
        # plt.show()
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=1000)
        buffer.seek(0)
        res[types] = base64.b64encode(buffer.read()).decode("utf-8")
    return res[typess]


# 计算注视点的命中率
def process(d, df, num):
    # d为目标和首次注视点集,df是完整注视集
    d_a = d[d["Examtype"] == "recall"]
    df_a = df[df["Examtype"] == "recall"]
    d_o = d[d["Examtype"] == "recognition"]
    df_o = df[df["Examtype"] == "recognition"]
    print("recall", d_a.shape[0] / df_o.shape[0])
    print("recognition", d_o.shape[0] / df_a.shape[0])
    for i, arrs in enumerate([arr_shape[num], arr_color[num]]):
        for j, arr in enumerate(arrs):
            d_count = d_a["target"].value_counts()[arr]
            df_count = df_a["target"].value_counts()[arr]
            print(arr, "_recall:", d_count, df_count, d_count / df_count)
            d_count = d_o["target"].value_counts()[arr]
            df_count = df_o["target"].value_counts()[arr]
            print(arr, "_recognition:", d_count, df_count, d_count / df_count)


# 每一个每一个不同形状\颜色的注视点对比
def eyeDataAnalysisSave(paths):
    files = os.listdir(paths)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 创建一个空字典
    # dfs = {"shape": {"2": {}, "4": {}, "6": {}}, "color": {"2": {}, "4": {}, "6": {}}}
    dfs = {"shape": {"motion": {}, "topo": {}}, "color": {"motion": {}, "topo": {}}}
    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)
        # num = re.findall(r'_(\d+)__', file_name)[0]
        # if num == "2":
        #     arr = ["topo", "motion"]
        # else:
        #     arr = ["topo", "motion", "none"]
        arr = ["topo", "motion"]
        df = pd.read_csv(
            paths + "\\" + f, encoding="utf-8", engine="python", on_bad_lines="warn"
        )
        # 重置索引
        df = df.reset_index()
        df = namefun(df)
        df["name"].fillna(method="ffill", inplace=True)
        # mask_topo = df["target"].str.contains("_").fillna(False)
        # mask_motion = (df["motion"] == 1.0) & (df["topo"] == 0.0)
        # mask_none = (df["motion"] == 0.0) & (df["topo"] == 0.0)
        for m, col in enumerate(arr):
            if "shape" in file_name:
                # 列fixation不为空的有效注视点
                if col in file_name:
                    # dfs["shape"][num][col] = df[(df["answer"].notna()) & (df["fixation"].notna()) & (
                    #     mask_topo if m == 0 else mask_motion if m == 1 else mask_none)].reset_index(drop=True)
                    # dfs["shape"][num][col] = dfs["shape"][num][col].loc[:,
                    #                          ['name', 'rt', 'correct', 'target', 'motion', 'topo', 'mchange', 'tchange',
                    #                           'first']]
                    dfs["shape"][col] = df[
                        (df["answer"].notna()) & (df["fixation"].notna())
                    ].reset_index(drop=True)
                    dfs["shape"][col] = dfs["shape"][col].loc[
                        :,
                        [
                            "name",
                            "rt",
                            "correct",
                            "target",
                            "mchange",
                            "tchange",
                            "first",
                            "T",
                        ],
                    ]
            else:
                # dfs["color"][num][col] = df[(df["answer"].notna()) & (df["fixation"].notna()) & (
                #     mask_topo if m == 0 else mask_motion if m == 1 else mask_none)].reset_index(drop=True)
                # dfs["color"][num][col] = dfs["color"][num][col].loc[:,
                #                          ['name', 'rt', 'correct', 'target', 'motion', 'topo', 'mchange', 'tchange',
                #                           'first']]
                if col in file_name:
                    dfs["color"][col] = df[
                        (df["answer"].notna()) & (df["fixation"].notna())
                    ].reset_index(drop=True)
                    dfs["color"][col] = dfs["color"][col].loc[
                        :,
                        [
                            "name",
                            "rt",
                            "correct",
                            "target",
                            "mchange",
                            "tchange",
                            "first",
                            "T",
                        ],
                    ]

    print(dfs)

    # 将原始数据集转换为长格式
    for n, arr in enumerate(["shape", "color"]):
        # for i, num in enumerate(["2", "4", "6"]):
        #     dfs[arr][num] = pd.concat([v.assign(Target=k) for k, v in dfs[arr][num].items()])
        dfs[arr] = pd.concat([v.assign(Target=k) for k, v in dfs[arr].items()])
    # dfs[arr] = pd.concat([v.assign(NUM=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    print(data_long)
    data_long.to_csv(
        r"E:\数据汇总\dynamic\4\汇总\eyedata.csv", index=False, encoding="utf-8"
    )


eyedata_paths = r"E:\数据汇总\dynamic\4\eyedata"


# eyeDataAnalysisSave(eyedata_paths)


# Additional experiment
# 运动变化和拓扑变化和none的首次注视点
def drawStimHUN(dfs, Factor):
    res = {}
    for i, num in enumerate([2, 4, 6]):
        print(num)
        df = dfs[dfs["NUM"] == num]
        ds_t = df[(df["TYPE"] == "shape") & (df["Target"] == "topo")]["eyedata"]
        ds_m = df[(df["TYPE"] == "shape") & (df["Target"] == "motion")]["eyedata"]
        dc_t = df[(df["TYPE"] == "color") & (df["Target"] == "topo")]["eyedata"]
        dc_m = df[(df["TYPE"] == "color") & (df["Target"] == "motion")]["eyedata"]
        combined_counts = pd.concat(
            [ds_t, ds_m, dc_t, dc_m],
            axis=1,
            keys=["T_shape", "M_shape", "T_color", "M_color"],
        )
        if num == 4 or num == 6:
            ds_n = df[(df["TYPE"] == "shape") & (df["Target"] == "none")]["eyedata"]
            dc_n = df[(df["TYPE"] == "color") & (df["Target"] == "none")]["eyedata"]
            combined_counts = pd.concat(
                [ds_t, ds_m, ds_n, dc_t, dc_m, dc_n],
                axis=1,
                keys=["T_shape", "M_shape", "N_shape", "T_color", "M_color", "N_color"],
            )

        # 使用 pd.melt() 函数将列转换为标识和值的列
        # 创建自定义调色板
        melted_df = pd.melt(combined_counts, var_name="Label", value_name="Value")
        my_palette = sns.color_palette(
            ["#81b8df", "#1597a5", "#0e606b", "#fff4f2", "#feb3ae", "#f7723d"]
        )
        fig = plt.subplots(figsize=(5, 4), sharey=True, sharex=True)
        sns.boxplot(data=melted_df, palette=my_palette, x="Label", y="Value", width=0.5)
        plt.ylabel("eyedata")
        plt.title(str(num) + "_first-eyedata")
        # 调整子图布局
        plt.tight_layout()
        # plt.savefig(r"E:\数据汇总\dynamic\汇总\compare_data.svg", format="svg")
        # plt.show()
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=1000)
        buffer.seek(0)
        res[num] = base64.b64encode(buffer.read()).decode("utf-8")
    return res[Factor]


# 混合num
def eyeDataAnalysis(paths, Nums, types, Factor, inde):
    data_long = pd.read_csv(
        paths, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    # 获取含有首次注注视点的数据
    data_fix = data_long[data_long["first"].notna()]
    # print(data_fix)
    # 创建一个空字典
    dfs = {"shape": {2: {}, 4: {}, 6: {}}, "color": {2: {}, 4: {}, 6: {}}}
    for i, num in enumerate([2, 4, 6]):
        df_n = data_fix[data_fix["NUM"] == num]
        if num == 2:
            arr = ["topo", "motion"]
        else:
            arr = ["topo", "motion", "none"]
        for m, type in enumerate(["shape", "color"]):
            df_m = df_n[df_n["TYPE"] == type]
            for n, target in enumerate(arr):
                df_tt = df_m[df_m["Target"] == target]
                # print(df_tt)
                counts = df_tt["name"].value_counts()
                dfs[type][num][target] = pd.DataFrame({"eyedata": counts})
    # print(dfs)

    # 将原始数据集转换为长格式
    for m, arr in enumerate(["shape", "color"]):
        for i, num in enumerate([2, 4, 6]):
            dfs[arr][num] = pd.concat(
                [v.assign(Target=k) for k, v in dfs[arr][num].items()]
            )
        dfs[arr] = pd.concat([v.assign(NUM=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    new_df = data_long.reset_index()

    if inde == 0:
        new_df = new_df[(new_df["NUM"] == Nums) & (new_df["TYPE"] == types)]
        # new_df = new_df[(new_df["NUM"]  == 6) & (new_df["TYPE"] == "shape")]
        md = smf.mixedlm("eyedata ~ Target", new_df, groups=new_df["index"])
        mdf = md.fit()
        # 查看模型结果
        # print(mdf.summary())
        return mdf.summary()
    elif inde == 1:
        return drawStimHUN(new_df, Factor)


pathscv = r"E:\数据汇总\dynamic\汇总\eyedata.csv"
# eyeDataAnalysis(pathscv)


# 单独的4
def eyeDataAnalysis1(paths, types, inde):
    data_long = pd.read_csv(
        paths, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    # 获取含有首次注注视点的数据
    data_fix = data_long[(data_long["first"].notna()) & (data_long["T"] == 1)]
    # print(data_fix)
    # 创建一个空字典
    dfs = {"shape": {}, "color": {}}
    arr = ["topo", "motion"]
    for m, type in enumerate(["shape", "color"]):
        df_m = data_fix[data_fix["TYPE"] == type]
        for n, target in enumerate(arr):
            df_tt = df_m[df_m["Target"] == target]
            print(df_tt)
            counts = df_tt["name"].value_counts()
            dfs[type][target] = pd.DataFrame({"eyedata": counts})
    # print(dfs)
    # 将原始数据集转换为长格式
    for m, arr in enumerate(["shape", "color"]):
        dfs[arr] = pd.concat([v.assign(Target=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    new_df = data_long.reset_index()
    if inde == 0:
        new_df = new_df[(new_df["TYPE"] == types)]
        md = smf.mixedlm("eyedata ~ TYPE*Target", new_df, groups=new_df["index"])
        mdf = md.fit()
        # 查看模型结果
        # print(mdf.summary())
        return mdf.summary()
    else:
        return drawStim(new_df)


pathscv1 = r"E:\数据汇总\dynamic\4\汇总\eyedata.csv"
# eyeDataAnalysis1(pathscv1)


def eyeDataAnalysisTandM(paths, types, inde):
    data_long = pd.read_csv(
        paths, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    # 获取含有首次注注视点的数据
    data_fix = data_long[(data_long["first"].notna()) & (data_long["T"] == 1)]
    # print(data_fix)
    # 创建一个空字典
    dfs = {"shape": {"topo": {}, "motion": {}}, "color": {"topo": {}, "motion": {}}}
    arr = ["topo", "motion"]
    arrs = {"topo": ["single", "double"], "motion": ["trans", "zoom"]}
    for m, type in enumerate(["shape", "color"]):
        df_m = data_fix[data_fix["TYPE"] == type]
        for n, target in enumerate(arr):
            df_tt = df_m[df_m["Target"] == target]
            for i, change in enumerate(arrs[target]):
                if n == 0:
                    df_tc = df_tt[df_tt["tchange"] == change]
                else:
                    df_tc = df_tt[df_tt["mchange"] == change]
                print(df_tc)
                counts = df_tc["name"].value_counts()
                dfs[type][target][change] = pd.DataFrame({"eyedata": counts})
    # print(dfs)
    # 将原始数据集转换为长格式
    for m, arr in enumerate(["shape", "color"]):
        for m, type in enumerate(["topo", "motion"]):
            dfs[arr][type] = pd.concat(
                [v.assign(Change=k) for k, v in dfs[arr][type].items()]
            )
        dfs[arr] = pd.concat([v.assign(Target=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    new_df = data_long.reset_index()
    if inde == 0:
        # new_df = new_df[(new_df["TYPE"] == "color")]
        md = smf.mixedlm("eyedata ~ Change*TYPE", new_df, groups=new_df["index"])
        mdf = md.fit()
        # 查看模型结果
        # print(mdf.summary())
        return mdf.summary()
    else:
        return drawStim1(new_df, types)
    #


# eyeDataAnalysisTandM(pathscv1)


# 混合num
def eyeDataAnalysisTM(paths):
    data_long = pd.read_csv(
        paths, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    # 获取含有首次注注视点的数据
    data_fix = data_long[data_long["first"].notna()]
    # print(data_fix)
    # 创建一个空字典
    dfs = {
        "shape": {
            2: {"topo": {}, "motion": {}},
            4: {"topo": {}, "motion": {}},
            6: {"topo": {}, "motion": {}},
        },
        "color": {
            2: {"topo": {}, "motion": {}},
            4: {"topo": {}, "motion": {}},
            6: {"topo": {}, "motion": {}},
        },
    }
    arrs = {"topo": ["single", "double"], "motion": ["trans", "zoom"]}
    for i, num in enumerate([2, 4, 6]):
        df_n = data_fix[data_fix["NUM"] == num]
        arr = ["topo", "motion"]
        for m, type in enumerate(["shape", "color"]):
            df_m = df_n[df_n["TYPE"] == type]
            for n, target in enumerate(arr):
                df_tt = df_m[df_m["Target"] == target]
                for j, change in enumerate(arrs[target]):
                    if n == 0:
                        df_tc = df_tt[df_tt["tchange"] == change]
                    else:
                        df_tc = df_tt[df_tt["mchange"] == change]
                    print(df_tt)
                    counts = df_tc["name"].value_counts()
                    dfs[type][num][target][change] = pd.DataFrame({"eyedata": counts})
    # print(dfs)

    # 将原始数据集转换为长格式
    for m, arr in enumerate(["shape", "color"]):
        for i, num in enumerate([2, 4, 6]):
            for j, target in enumerate(["topo", "motion"]):
                dfs[arr][num][target] = pd.concat(
                    [v.assign(Change=k) for k, v in dfs[arr][num][target].items()]
                )
            dfs[arr][num] = pd.concat(
                [v.assign(Target=k) for k, v in dfs[arr][num].items()]
            )
        dfs[arr] = pd.concat([v.assign(NUM=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    new_df = data_long.reset_index()
    new_df = new_df[(new_df["TYPE"] == "shape")]
    # drawStim(new_df)
    md = smf.mixedlm("eyedata ~ NUM*Change", new_df, groups=new_df["index"])
    mdf = md.fit()
    # 查看模型结果
    # print(mdf.summary())
    return mdf.summary()


# eyeDataAnalysisTM(pathscv)
