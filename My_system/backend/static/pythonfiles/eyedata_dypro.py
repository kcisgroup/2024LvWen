import json
import math
import os
import re
from typing import Dict, List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from static.pythonfiles.datafunc import process_data, namefun
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
        nums = 0
        if motion == 1.0 and mchange == "trans" and j == target_id:
            dist = Dicts[num] + 50
        else:
            dist = Dicts[num]
        for i in range(len(webgazer_data)):
            if i != 0:
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
                        nums = nums + 1
            else:
                continue
        dots.append({stimuli[j]: nums})
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
    nums = 0
    if motion == 1.0 and mchange == "trans":
        dist = Dicts[num] + 50
    else:
        dist = Dicts[num]
    for i in range(len(webgazer_data)):
        if i != 0:
            for j in range(len(webgazer_data[i])):
                dicts = math.sqrt(
                    math.pow(webgazer_data[i][j]["x"] - webgazer_targets_data["x"], 2)
                    + math.pow(webgazer_data[i][j]["y"] - webgazer_targets_data["y"], 2)
                )
                if dicts < dist:
                    nums = nums + 1
        else:
            continue
    dots[target] = nums
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
    max_stimulus = max(dots, key=lambda x: list(x.values())[0])  # 获取数量最多的刺激
    return max_stimulus


# 不同刺激数目下，目标对应的位置
ans_index = {
    "2": {"4": 0, "6": 1},
    "4": {"4": 0, "8": 1, "6": 2, "2": 3},
    "6": {"4": 0, "7": 1, "9": 2, "6": 3, "3": 4, "1": 5},
}


# 筛选并处理眼动数据，寻找首个注视的刺激
def eyeDatadyp(paths):
    files = os.listdir(paths)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)
        # num = re.findall(r'_(\d+)_', file_name)[0]
        num = "4"
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
                    if len(first_dot) > 0:
                        if (target == str(list(first_dot)[0])) or (
                            target.split("_")[0] == str(list(first_dot)[0])
                        ):
                            df.loc[index, "first_dot"] = target
                        else:
                            df.loc[index, "first_dot"] = str(list(first_dot)[0])
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
                    # df.loc[index, "movement"] = str(move)
                    # if len(move[1]) > 0:  # 第二段数据存在
                    #     # 第一个数据是目标
                    #     if (target == str(list(move[1][0].keys())[0])) or (
                    #             target.split("_")[0] == str(list(move[1][0].keys())[0])):
                    #         df.loc[index, "first"] = target
                    #     else:  # 第一个数据不是目标
                    #         # 第二段数据长度为1，
                    #         if len(move[1]) == 1:
                    #             # 第一段数据最后一个和第二段的数据相同
                    #             if len(move[0]) > 0 and (
                    #                     str(list(move[0][-1].keys())[0]) == str(list(move[1][0].keys())[0])):
                    #                 if len(move[2]) > 0:  # 第三段存在，选第三段数据的第一个
                    #                     if (target == str(list(move[2][0].keys())[0])) or (
                    #                             target.split("_")[0] == str(list(move[2][0].keys())[0])):
                    #                         df.loc[index, "first"] = target
                    #                     else:  # 第一个不是目标
                    #                         # 第三段为1，且三段数据相同，选第四段第一个
                    #                         if len(move[2]) == 1 and len(move[3]) > 0 and (
                    #                                 str(list(move[1][0].keys())[0]) == str(list(move[2][0].keys())[0])):
                    #                             if (target == str(list(move[3][0].keys())[0])) or (
                    #                                     target.split("_")[0] == str(list(move[3][0].keys())[0])):
                    #                                 df.loc[index, "first"] = target
                    #                         # 第三段大于1，且三段数据第一个相同，选第三段第二个
                    #                         if len(move[2]) > 1 and (
                    #                                 str(list(move[1][0].keys())[0]) == str(
                    #                             list(move[2][0].keys())[0])) and (
                    #                                 (target == str(list(move[2][1].keys())[0])) or (
                    #                                 target.split("_")[0] == str(list(move[2][1].keys())[0]))):
                    #                             df.loc[index, "first"] = target
                    #         # 第二个数据是目标
                    #         if len(move[1]) > 1:
                    #             if len(move[0]) > 0 and (
                    #                     str(list(move[0][-1].keys())[0]) == str(list(move[1][0].keys())[0])):
                    #                 if (target == str(list(move[1][1].keys())[0])) or (
                    #                         target.split("_")[0] == str(list(move[1][1].keys())[0])):
                    #                     df.loc[index, "first"] = target
                    # else:
                    #     # 第二段不存在，第三段存在
                    #     if len(move[2]) > 0:
                    #         if (target == str(list(move[2][0].keys())[0])) or (
                    #                 target.split("_")[0] == str(list(move[2][0].keys())[0])):
                    #             df.loc[index, "first"] = target
                    #     else:
                    #         # 第三段不存在，第四段存在
                    #         if len(move[3]) > 0:
                    #             if (target == str(list(move[3][0].keys())[0])) or (
                    #                     target.split("_")[0] == str(list(move[3][0].keys())[0])):
                    #                 df.loc[index, "first"] = target
                    # else:
                    #     if len(move[1]) > 1:
                    #         if (target == str(list(move[1][1].keys())[0])) or (
                    #                 target.split("_")[0] == str(list(move[1][1].keys())[0])):
                    #             df.loc[index, "first"] = target
            else:
                continue
        df.to_csv(
            paths + "\\eyedata\\num\\" + file_name + "_eyedata.csv",
            index=False,
            encoding="utf-8",
        )


paths = r"E:\数据汇总\dynamic\4"


# eyeData(paths)


# 每一个每一个不同形状\颜色的注视点对比
def eyeDataProcessSAVE(paths):
    files = os.listdir(paths)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 创建一个空字典
    # dfs = {"shape": {"2": {}, "4": {}, "6": {}}, "color": {"2": {}, "4": {}, "6": {}}}
    dfs = {"shape": {"motion": {}, "topo": {}}, "color": {"motion": {}, "topo": {}}}

    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)
        # num = re.findall(r'_(\d+)__', file_name)[0]
        num = "4"
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
        mask_topo = df["target"].str.contains("_").fillna(False)
        mask_motion = (df["motion"] == 1.0) & (df["topo"] == 0.0)
        mask_none = (df["motion"] == 0.0) & (df["topo"] == 0.0)
        for m, col in enumerate(arr):
            if "shape" in file_name:
                if col in file_name:
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
                            "first_dot",
                            "T",
                        ],
                    ]
                # dfs["shape"][num][col] = df[(df["answer"].notna()) & (df["fixation"].notna()) & (
                #     mask_topo if m == 0 else mask_motion if m == 1 else mask_none)].reset_index(drop=True)
                # dfs["shape"][num][col] = dfs["shape"][num][col].loc[:,
                #                          ['name', 'rt', 'correct', 'target', 'motion', 'topo', 'mchange',
                #                           'tchange', 'fixation', 'fixation_target', 'first_dot']]
            else:
                # dfs["color"][num][col] = df[(df["answer"].notna()) & (df["fixation"].notna()) & (
                #     mask_topo if m == 0 else mask_motion if m == 1 else mask_none)].reset_index(drop=True)
                # dfs["color"][num][col] = dfs["color"][num][col].loc[:,
                #                          ['name', 'rt', 'correct', 'target', 'motion', 'topo', 'mchange',
                #                           'tchange', 'fixation', 'fixation_target', 'first_dot']]
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
                            "first_dot",
                            "T",
                        ],
                    ]

    # 将原始数据集转换为长格式

    for n, arr in enumerate(["shape", "color"]):
        # for i, num in enumerate(["2", "4", "6"]):
        #     dfs[arr][num] = pd.concat([v.assign(Target=k) for k, v in dfs[arr][num].items()])
        dfs[arr] = pd.concat([v.assign(Target=k) for k, v in dfs[arr].items()])
        # dfs[arr] = pd.concat([v.assign(NUM=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    print(data_long)
    data_long.to_csv(
        r"E:\数据汇总\dynamic\4\eyedata\num\汇总\eyedata.csv",
        index=False,
        encoding="utf-8",
    )


eyedata_paths = r"E:\数据汇总\dynamic\4\eyedata\num"


eyeDataProcessSAVE(eyedata_paths)


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
    fig = plt.subplots(figsize=(5, 4), sharey=True, sharex=True)

    sns.boxplot(data=melted_df, palette=my_palette, x="Label", y="Value", width=0.5)

    plt.ylabel("eyedata")
    plt.title("first-eyedata")
    # 调整子图布局
    plt.tight_layout()
    plt.savefig(r"E:\数据汇总\dynamic\汇总\num-compare_data.svg", format="svg")
    plt.show()


# 混合num
def eyeDataAnalysis(paths):
    data_long = pd.read_csv(
        paths, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    # 获取含有首次注注视点的数据
    data_fix = data_long[data_long["first_dot"].notna()]
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
                counts = df_tt["name"].value_counts()
                dfs[type][num][target] = pd.DataFrame({"eyedata": counts})
    print(dfs)

    # 将原始数据集转换为长格式
    for m, arr in enumerate(["shape", "color"]):
        for i, num in enumerate([2, 4, 6]):
            dfs[arr][num] = pd.concat(
                [v.assign(Target=k) for k, v in dfs[arr][num].items()]
            )
        dfs[arr] = pd.concat([v.assign(NUM=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    new_df = data_long.reset_index()
    # new_df = new_df[(new_df["NUM"] == 2)& (new_df["TYPE"] == "shape")]
    new_df = new_df[(new_df["NUM"] != 2)]
    # drawStim(new_df)
    md = smf.mixedlm("eyedata ~ Target*TYPE*NUM", new_df, groups=new_df["index"])
    mdf = md.fit()
    # 查看模型结果
    print(mdf.summary())


pathscv = r"E:\数据汇总\dynamic\eyedata\num\汇总\eyedata.csv"
# eyeDataAnalysis(pathscv)


def eyeDataProcessdy(paths):
    data_res = []
    data_long = pd.read_csv(
        paths + "/eyedata.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    for m, arr in enumerate(["shape", "color"]):
        df_m = data_long[data_long["TYPE"] == arr]
        for i, num in enumerate([2, 4, 6]):
            if num == 2:
                arrs = ["topo", "motion"]
            else:
                arrs = ["topo", "motion", "none"]
            df_n = df_m[df_m["NUM"] == num]
            for j, target in enumerate(arrs):
                df_i = df_n[df_n["Target"] == target]
                sum = df_i.shape[0]
                # count = len(df_i[df_i["first_dot"].str.contains("_")])
                count = len(df_i[df_i["first_dot"] == df_i["target"]])
                hit_rate = count / sum
                data_res.append(
                    {
                        "target": target,
                        "arr": arr,
                        "num": num,
                        "hit_rate": hit_rate,
                    }
                )
    return data_res


pathss = r"E:\数据汇总\dynamic\eyedata\num\汇总\eyedata.csv"


# eyeDataProcess(pathss)


# 单独的4
def eyeDataAnalysis1(paths):
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
    print(dfs)
    # 将原始数据集转换为长格式
    for m, arr in enumerate(["shape", "color"]):
        dfs[arr] = pd.concat([v.assign(Target=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    new_df = data_long.reset_index()
    # drawStim(new_df)
    new_df = new_df[(new_df["TYPE"] == "color")]
    md = smf.mixedlm("eyedata ~ TYPE*Target", new_df, groups=new_df["index"])
    mdf = md.fit()
    # 查看模型结果
    print(mdf.summary())


pathscv1 = r"E:\数据汇总\dynamic\4\eyedata\num\汇总\eyedata.csv"


# eyeDataAnalysis1(pathscv1)


def eyeDataProcessdyp(paths):
    data_res = []
    data_long = pd.read_csv(
        paths + "/eyedata.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    for m, arr in enumerate(["shape", "color"]):
        df_m = data_long[data_long["TYPE"] == arr]
        arrs = ["topo", "motion"]
        for j, target in enumerate(arrs):
            df_i = df_m[df_m["Target"] == target]
            sum = df_i.shape[0]
            # count = len(df_i[df_i["first_dot"].str.contains("_")])
            count = len(df_i[df_i["first_dot"] == df_i["target"]])
            hit_rate = count / sum
            data_res.append(
                {
                    "target": target,
                    "arr": arr,
                    "hit_rate": hit_rate,
                }
            )
    return data_res


# pathss1 = r'E:\数据汇总\dynamic\4\eyedata\num\汇总\eyedata.csv'
# eyeDataProcess1(pathss1)
