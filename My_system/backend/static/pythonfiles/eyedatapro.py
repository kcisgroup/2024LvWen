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
def dictDefine(webgazer_data, stimuli, webgazer_targets_data, num):
    dots = []
    for j in range(len(stimuli)):
        nums = 0
        for i in range(len(webgazer_data)):
            dicts = math.sqrt(
                math.pow(webgazer_data[i]["x"] - webgazer_targets_data[j]["x"], 2)
                + math.pow(webgazer_data[i]["y"] - webgazer_targets_data[j]["y"], 2)
            )
            if dicts < Dicts[num]:
                nums = nums + 1
        dots.append({stimuli[j]: nums})
    return dots


# 获取落在目标刺激范围内的注视点
def dictDefine1(webgazer_data, target, webgazer_targets_data, num):
    dots = {}
    dot = []
    for i in range(len(webgazer_data)):
        dicts = math.sqrt(
            math.pow(webgazer_data[i]["x"] - webgazer_targets_data["x"], 2)
            + math.pow(webgazer_data[i]["y"] - webgazer_targets_data["y"], 2)
        )
        if dicts < Dicts[num]:
            dot.append(webgazer_data[i])
    if len(dot) > 0:
        dots[target] = len(dot)
    return dots


# 处理收集到的眼动数据
def eyeDataProcess(webgazer_data, canvas_data):
    target_canvas_data_x = canvas_data["#container"]["x"]
    target_canvas_data_y = canvas_data["#container"]["y"]
    for i in range(len(webgazer_data)):
        webgazer_data[i]["x"] = webgazer_data[i]["x"] - target_canvas_data_x
        webgazer_data[i]["y"] = webgazer_data[i]["y"] - target_canvas_data_y
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
def eyeData1(paths):
    files = os.listdir(paths)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)

        num = re.findall(r"_(\d+)_\d+", file_name)[0]
        dt_rt, df = process_data(paths + "\\" + f)
        # 添加一个空列
        # 重置索引
        df = df.reset_index()
        df["fixation"] = None
        df["fixation_target"] = None
        df["first_dot"] = None
        # 迭代DataFrame的行
        for index, row in df.iterrows():
            if pd.notnull(row["answer"]) and row["answer"] != 5:
                webgazer_data = json.loads(row["webgazer_data"])
                canvas_data = json.loads(row["canvas_data"])
                stimuli = json.loads(row["stimulus"])
                target = row["target"]
                eyeDataProcess(webgazer_data, canvas_data)
                target_id = int(ans_index[num][str(int(row["answer"]))])
                target_data = json.loads(row["webgazer_targets_data"])
                dots = dictDefine(webgazer_data, stimuli, target_data, num)
                first_dot = findTaggedKeys(dots)
                dots_target = dictDefine1(
                    webgazer_data, target, target_data[target_id], num
                )
                print("dots:", dots)
                print("dots_target:", dots_target)
                print("first_target:", first_dot)
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
            else:
                continue
        df.to_csv(
            paths + "/eyedata/num/" + file_name + "_eyedatanum.csv",
            index=False,
            encoding="utf-8",
        )


paths = r"E:\数据汇总\实验一"


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


# 绘制首个注视点落在目标和非目标的注视点数量的箱线图,实验一
def draw(df, df_not, num):
    df = df[df["NUM"] == num]
    df_not = df_not[df_not["NUM"] == num]
    dt_s = fun(df[df["TYPE"] == "shape"])
    dt_c = fun(df[df["TYPE"] == "color"])
    dt_not_s = fun(df_not[df_not["TYPE"] == "shape"])
    dt_not_c = fun(df_not[df_not["TYPE"] == "color"])
    combined_counts = pd.concat(
        [dt_s, dt_c, dt_not_s, dt_not_c], axis=1, keys=["T_S", "T_C", "D_S", "D_C"]
    )
    dt = fun(df)
    dt_not = fun(df_not)
    combined_counts = pd.concat([dt, dt_not], axis=1, keys=["T", "D"])
    #
    # # 合并一级列索引和二级列索引
    combined_counts.columns = ["_".join(col) for col in combined_counts.columns]
    print(combined_counts)
    # 使用 pd.melt() 函数将列转换为标识和值的列
    melted_df = pd.melt(combined_counts, var_name="Label", value_name="Value")

    # 创建1行2列的子图布局
    fig = plt.subplots(figsize=(5, 4), sharey=True, sharex=True)
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.xticks(fontname="Times New Roman")
    plt.yticks(fontname="Times New Roman")
    # 创建自定义调色板
    my_palette = sns.color_palette(["#1597a5", "#0e606b", "#fff4f2", "#feb3ae"])
    sns.boxplot(data=melted_df, palette=my_palette, x="Label", y="Value", width=0.5)
    # # 绘制recognition子图
    # sns.boxplot(ax=axes[1], data=combined_counts['df_not'], orient='v')
    plt.ylabel("eyedata", fontname="Times New Roman", fontsize=12)
    plt.xlabel(str(num) + "_eyedata", fontname="Times New Roman", fontsize=12)
    # 调整子图布局
    plt.tight_layout()
    # 保存为svg格式
    # plt.savefig(r'E:\数据汇总\实验一\eyedata\num\pic\\' + str(num) + '_eyedot.svg', format='svg')
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\静态P\\" + str(num) + "_eyedot.jpg",
    #     format="jpg",
    #     dpi=1000,
    # )
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode("utf-8")
    return image_data


# 绘制首个注视点落在目标和非目标的注视点数量的箱线图
def drawTopo(tt, tt_not, dd, dd_not):
    # tt_s = tt[tt['TYPE'] == "shape"]
    # tt_c = tt[tt['TYPE'] == "color"]
    # tt_not_s = tt_not[tt_not['TYPE'] == "shape"]
    # tt_not_c = tt_not[tt_not['TYPE'] == "color"]
    # dd_s = dd[dd['TYPE'] == "shape"]
    # dd_c = dd[dd['TYPE'] == "color"]
    # dd_not_s = dd_not[dd_not['TYPE'] == "shape"]
    # dd_not_c =dd_not[dd_not['TYPE'] == "color"]
    for i, num in enumerate([2, 4, 6]):
        tt_num = fun(tt[tt["NUM"] == num])
        tt_not_num = fun(tt_not[tt_not["NUM"] == num])
        dd_num = fun(dd[dd["NUM"] == num])
        dd_not_num = fun(dd_not[dd_not["NUM"] == num])
        combined_counts = pd.concat(
            [tt_num, tt_not_num, dd_num, dd_not_num],
            axis=1,
            keys=["TT", "TD", "DT", "DD"],
        )
        # tt_s_num = fun(tt_s[tt_s['NUM'] == num])
        # tt_c_num = fun(tt_c[tt_c['NUM'] == num])
        # tt_not_s_num = fun(tt_not_s[tt_not_s['NUM'] == num])
        # tt_not_c_num = fun(tt_not_c[tt_not_c['NUM'] == num])
        # dd_s_num =fun(dd_s[dd_s['NUM'] == num])
        # dd_c_num = fun(dd_c[dd_c['NUM'] == num])
        # dd_not_s_num = fun(dd_not_s[dd_not_s['NUM'] == num])
        # dd_not_c_num = fun(dd_not_c[dd_not_c['NUM'] == num])
        # combined_counts = pd.concat(
        #     [tt_s_num, tt_c_num, tt_not_s_num, tt_not_c_num, dd_s_num, dd_c_num, dd_not_s_num, dd_not_c_num], axis=1,
        #     keys=['TT_S', 'TT_C', 'TD_S', 'TD_C', 'DT_S', 'DT_C', 'DD_S', 'DD_C'])
        # 合并一级列索引和二级列索引
        combined_counts.columns = ["_".join(col) for col in combined_counts.columns]
        # print(combined_counts)
        # 使用 pd.melt() 函数将列转换为标识和值的列
        melted_df = pd.melt(combined_counts, var_name="Label", value_name="Value")

        # 创建1行2列的子图布局
        fig = plt.subplots(figsize=(6, 4), sharey=True, sharex=True)
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = ["Times New Roman"]
        plt.xticks(fontname="Times New Roman")
        plt.yticks(fontname="Times New Roman")
        # 创建自定义调色板
        my_palette = sns.color_palette(
            [
                "#1597a5",
                "#1597a5",
                "#0e606b",
                "#0e606b",
                "#fff4f2",
                "#fff4f2",
                "#feb3ae",
                "#feb3ae",
            ]
        )
        sns.boxplot(data=melted_df, palette=my_palette, x="Label", y="Value", width=0.5)
        # # 绘制recognition子图
        # sns.boxplot(ax=axes[1], data=combined_counts['df_not'], orient='v')
        plt.ylabel("eyedata", fontname="Times New Roman")
        plt.xlabel(str(num) + "_eyedata", fontname="Times New Roman")
        # 调整子图布局
        plt.tight_layout()
        # plt.savefig(r'E:\数据汇总\实验二\eyedata\num\pic\\' + str(num) + '_eyedot_s_c.svg', format='svg')
        # plt.show()


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


# 注视点落在每一个不同形状\颜色的数量的箱线图
# 以及每一个形状\颜色对注视点数量的显著性分析
def drawStim(df, num):
    ds = df[df["TYPE"] == "shape"]
    dc = df[df["TYPE"] == "color"]
    df_s = pd.DataFrame()
    df_c = pd.DataFrame()
    for i in range(len(arr_shape[num])):
        ds_recall = ds[
            (ds["target"] == arr_shape[num][i]) & (ds["Examtype"] == "recall")
        ].reset_index(drop=True)
        ds_recognition = ds[
            (ds["target"] == arr_shape[num][i]) & (ds["Examtype"] == "recognition")
        ].reset_index(drop=True)
        recall_counts = ds_recall["name"].value_counts()
        recognition_counts = ds_recognition["name"].value_counts()
        combined_counts = pd.concat(
            [recall_counts, recognition_counts],
            axis=1,
            keys=[f"S_{arr_shape[num][i]}_A", f"S_{arr_shape[num][i]}_O"],
        )
        # print(recall_counts, recognition_counts)
        df_s = pd.concat([df_s, combined_counts], axis=1)
        # print(df_s)
    #
    for i in range(len(arr_color[num])):
        dc_recall = dc[
            (dc["target"] == arr_color[num][i]) & (dc["Examtype"] == "recall")
        ].reset_index(drop=True)
        dc_recognition = dc[
            (dc["target"] == arr_color[num][i]) & (dc["Examtype"] == "recognition")
        ].reset_index(drop=True)
        recall_counts = dc_recall["name"].value_counts()
        recognition_counts = dc_recognition["name"].value_counts()
        combined_counts = pd.concat(
            [recall_counts, recognition_counts],
            axis=1,
            keys=[f"C_{arr_color[num][i]}_A", f"C_{arr_color[num][i]}_O"],
        )
        df_c = pd.concat(
            [df_c, combined_counts],
            axis=1,
        )
    # print(df_s, df_c)

    # 使用 pd.melt() 函数将列转换为标识和值的列
    melted_df_s = pd.melt(df_s, var_name="Label", value_name="Value")
    melted_df_c = pd.melt(df_c, var_name="Label", value_name="Value")
    my_palette = sns.color_palette(["white"])

    fig = plt.subplots(figsize=(12, 6), sharey=True, sharex=True)
    # 创建自定义调色板

    sns.boxplot(data=melted_df_s, palette=my_palette, x="Label", y="Value")
    plt.ylabel("eyedata")
    plt.xlabel(num + "_eyedata")
    fig = plt.subplots(figsize=(12, 6), sharey=True, sharex=True)
    sns.boxplot(data=melted_df_c, palette=my_palette, x="Label", y="Value")
    plt.ylabel("eyedata")
    plt.xlabel(num + "_eyedata")
    # 调整子图布局
    plt.tight_layout()


# 在不同刺激数目的背景下画折线图
def drawtopo(df, num):
    df = df[df["NUM"] == num]
    df = df[df["target"] == df["first_dot"]]
    df_recall = pd.DataFrame()
    df_recognition = pd.DataFrame()
    dfs = {}
    # mask = df["first_dot"].str.contains("_1").fillna(False)
    for k, type in enumerate(["shape", "color"]):
        for i, col in enumerate(["topo", "no_topo"]):
            for j, f in enumerate(["recall", "recognition"]):
                for m, isi in enumerate([500, 1000, 1500]):
                    if i == 0:
                        dfs[col] = df[
                            (df["Target"] == col)
                            & (df["Examtype"] == f)
                            & (df["ISI"] == isi)
                            & (df["TYPE"] == type)
                        ].reset_index(drop=True)
                    else:
                        dfs[col] = df[
                            (df["Target"] == col)
                            & (df["Examtype"] == f)
                            & (df["ISI"] == isi)
                            & (df["TYPE"] == type)
                        ].reset_index(drop=True)
                    # counts = dfs[col]['name'].value_counts()
                    # dfs[col] = dfs[col].loc[:, ['eyedata']]

                    print(dfs[col]["first_dot"])
                    if j == 0:
                        if i == 1:
                            df_recall.insert(
                                df_recall.shape[1],
                                f + "_eyedata_nopo_" + str(isi) + "_" + type,
                                pd.Series(len(dfs[col]["first_dot"])),
                            )
                        else:
                            df_recall.insert(
                                df_recall.shape[1],
                                f + "_eyedata_" + col + "_" + str(isi) + "_" + type,
                                pd.Series(len(dfs[col]["first_dot"])),
                            )
                    else:
                        if i == 1:
                            df_recognition.insert(
                                df_recognition.shape[1],
                                f + "_eyedata_nopo_" + str(isi) + "_" + type,
                                pd.Series(len(dfs[col]["first_dot"])),
                            )
                        else:
                            df_recognition.insert(
                                df_recognition.shape[1],
                                f + "_eyedata_" + col + "_" + str(isi) + "_" + type,
                                pd.Series(len(dfs[col]["first_dot"])),
                            )

        print(df_recall)

        df_topo = []
        df_notopo = []
        colors = ["#fe817d", "#81b8df"]
        col = [type + "_500", type + "_1000", type + "_1500"]
        # 绘制每个子图的实线和虚线折线图

        #  创建画布
        fig, ax = plt.subplots(figsize=(5, 4))
        plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
        for i, dfs in enumerate([df_recall, df_recognition]):
            nums = [int(re.findall(r"_(\d+)", col)[0]) for col in dfs.columns]
            sorted_col_name = [
                dfs.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
            ]
            df_topo.append([col for col in sorted_col_name if "topo" in col])
            df_notopo.append([col for col in sorted_col_name if "nopo" in col])
        print(df_topo, df_notopo)
        for i, dfs in enumerate([df_recall, df_recognition]):
            ax.plot(
                col,
                dfs[df_topo[i]].values[0],
                label=f"{'recall_' if i == 0 else 'recognition_'}topo",
                linestyle="-",
                color=colors[i],
            )
            ax.plot(
                col,
                dfs[df_notopo[i]].values[0],
                label=f"{'recall_' if i == 0 else 'recognition_'}no-topo",
                linestyle="--",
                color=colors[i],
            )
        df_topo = []
        df_notopo = []
        # 添加图例和横纵轴标签
        # 设置中文字体
        ax.legend(loc="upper right")
        ax.set_xlabel("ISI")
        ax.set_ylabel("eyedata")
        # 添加整个图形的标题
        fig.suptitle(type + "_" + str(num) + "_eyedata")
        # 显示图形
        plt.show()
        plt.savefig(
            r"E:\数据汇总\实验二\eyedata\num\pic\\topo_"
            + type
            + "_"
            + str(num)
            + "_eyedata"
            + ".svg",
            format="svg",
            dpi=500,
        )
        df_recall = pd.DataFrame()
        df_recognition = pd.DataFrame()
        dfs = {}


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


# 分析不同变量对眼动数据的显著性影响
def analy(df):
    data = []
    for i, num in enumerate([2, 4, 6]):
        df_n = df[df["NUM"] == num]
        # 创建一个空字典
        dfs_recall = {
            "shape": {"500": {}, "1000": {}, "1500": {}},
            "color": {"500": {}, "1000": {}, "1500": {}},
        }
        dfs_recognition = {
            "shape": {"500": {}, "1000": {}, "1500": {}},
            "color": {"500": {}, "1000": {}, "1500": {}},
        }
        for j, ISI in enumerate([500, 1000, 1500]):
            df_i = df_n[df_n["ISI"] == ISI]
            for k, examtype in enumerate(["recall", "recognition"]):
                df_t = df_i[df_i["Examtype"] == examtype]
                for m, type in enumerate(["shape", "color"]):
                    df_m = df_t[df_t["TYPE"] == type]
                    df_tt = df_m[df_m["target"] == df_m["first_dot"]]
                    counts = df_tt["name"].value_counts()
                    if k == 0:
                        dfs_recall[type][str(ISI)] = pd.DataFrame({"eyedata": counts})
                    else:
                        dfs_recognition[type][str(ISI)] = pd.DataFrame(
                            {"eyedata": counts}
                        )
        # print(dfs_recall, dfs_recognition)
        dfs = {"recall": dfs_recall, "recognition": dfs_recognition}

        # 将原始数据集转换为长格式
        for m, type in enumerate(["recall", "recognition"]):
            for m, arr in enumerate(["shape", "color"]):
                dfs[type][arr] = pd.concat(
                    [v.assign(ISI=k) for k, v in dfs[type][arr].items()]
                )
            dfs[type] = pd.concat([v.assign(TYPE=k) for k, v in dfs[type].items()])
        data_long = pd.concat([v.assign(Examtype=k) for k, v in dfs.items()])

        # print(data_long)

        new_df = data_long.reset_index()
        # new_df=new_df[(new_df["Examtype"]=="recognition")]
        md = smf.mixedlm("eyedata ~ ISI*TYPE*Examtype", new_df, groups=new_df["index"])
        mdf = md.fit()
        # 查看模型结果
        # print(mdf.summary())
        data.append({num: mdf.summary()})
    return data


# 分析不同变量对眼动数据的显著性影响，实验二、三
def analyTopo(df):
    for i, num in enumerate([2, 4, 6]):
        df_n = df[df["NUM"] == num]
        # 创建一个空字典
        dfs_recall = {
            "shape": {
                "500": {"topo": {}, "no_topo": {}},
                "1000": {"topo": {}, "no_topo": {}},
                "1500": {"topo": {}, "no_topo": {}},
            },
            "color": {
                "500": {"topo": {}, "no_topo": {}},
                "1000": {"topo": {}, "no_topo": {}},
                "1500": {"topo": {}, "no_topo": {}},
            },
        }
        dfs_recognition = {
            "shape": {
                "500": {"topo": {}, "no_topo": {}},
                "1000": {"topo": {}, "no_topo": {}},
                "1500": {"topo": {}, "no_topo": {}},
            },
            "color": {
                "500": {"topo": {}, "no_topo": {}},
                "1000": {"topo": {}, "no_topo": {}},
                "1500": {"topo": {}, "no_topo": {}},
            },
        }
        for j, ISI in enumerate([500, 1000, 1500]):
            df_i = df_n[df_n["ISI"] == ISI]
            for k, examtype in enumerate(["recall", "recognition"]):
                df_t = df_i[df_i["Examtype"] == examtype]
                for m, type in enumerate(["shape", "color"]):
                    df_m = df_t[df_t["TYPE"] == type]
                    for n, target in enumerate(["topo", "no_topo"]):
                        # df_tt = df_m[df_m["Target"] == "topo"]
                        df_tt = df_m[df_m["Target"] == target]
                        # mask = df_m["first_dot"].str.contains("_1").fillna(False)
                        df_tt = df_tt[df_tt["target"] == df_tt["first_dot"]]
                        # if(n==0):
                        #     df_tt = df_m[mask]
                        #     # df_tt = df_tt[df_tt["target"] == df_tt["first_dot"]]
                        # else:
                        #     df_tt = df_m[~mask]
                        # df_tt = df_tt[df_tt["target"] != df_tt["first_dot"]]
                        counts = df_tt["name"].value_counts()
                        if k == 0:
                            dfs_recall[type][str(ISI)][target] = pd.DataFrame(
                                {"eyedata": counts}
                            )
                        else:
                            dfs_recognition[type][str(ISI)][target] = pd.DataFrame(
                                {"eyedata": counts}
                            )

        dfs = {"recall": dfs_recall, "recognition": dfs_recognition}

        # 将原始数据集转换为长格式
        for m, type in enumerate(["recall", "recognition"]):
            for m, arr in enumerate(["shape", "color"]):
                for j, ISI in enumerate(["500", "1000", "1500"]):
                    dfs[type][arr][ISI] = pd.concat(
                        [v.assign(Target=k) for k, v in dfs[type][arr][ISI].items()]
                    )
                dfs[type][arr] = pd.concat(
                    [v.assign(ISI=k) for k, v in dfs[type][arr].items()]
                )
            dfs[type] = pd.concat([v.assign(TYPE=k) for k, v in dfs[type].items()])
        data_long = pd.concat([v.assign(Examtype=k) for k, v in dfs.items()])

        print(data_long)
        # data_long.to_csv(r'E:\数据汇总\实验二\eyedata\num\data_' + str(num) + '.csv', index=False, encoding='utf-8')
        # # drawtopo(data_long, num)
        new_df = data_long.reset_index()
        new_df = new_df[(new_df["TYPE"] == "color")]
        # new_df = new_df[(new_df["Examtype"] == "recognition")]
        md = smf.mixedlm(
            "eyedata ~ ISI*Target*Examtype*TYPE", new_df, groups=new_df["index"]
        )
        mdf = md.fit()
        # 查看模型结果
        print(mdf.summary())


# 每一个每一个不同形状\颜色的注视点对比
def eyeDataProcessSAVE(paths):
    files = os.listdir(paths)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选识别和回忆文件
    recall_files = [f for f in csv_files if "recall" in f]
    recognition_files = [f for f in csv_files if "recognition" in f]
    # 创建一个空字典
    dfs_recall = {
        "shape": {"2": {}, "4": {}, "6": {}},
        "color": {"2": {}, "4": {}, "6": {}},
    }
    dfs_recognition = {
        "shape": {"2": {}, "4": {}, "6": {}},
        "color": {"2": {}, "4": {}, "6": {}},
    }
    # selected_files = [f for f in csv_files if "4" in f and "shape" in f and "1000" in f and "recall" in f]
    for i, fs in enumerate([recall_files, recognition_files]):
        for f in fs:
            file_name, file_ext = os.path.splitext(f)
            num = re.findall(r"_(\d+)_\d+", file_name)[0]
            ISI = re.findall(r"_\d+_(\d+)", file_name)[0]
            df = pd.read_csv(
                paths + "\\" + f, encoding="utf-8", engine="python", on_bad_lines="warn"
            )
            # 重置索引
            df = df.reset_index()
            df = namefun(df)
            df["name"].fillna(method="ffill", inplace=True)
            if "shape" in file_name:
                if i == 0:
                    dfs_recall["shape"][num][ISI] = df[
                        (df["answer"].notna())
                        & (df["answer"] != 5)
                        & (df["fixation"].notna())
                    ].reset_index(drop=True)
                    dfs_recall["shape"][num][ISI] = dfs_recall["shape"][num][ISI].loc[
                        :,
                        [
                            "name",
                            "rt",
                            "correct",
                            "target",
                            "fixation",
                            "fixation_target",
                            "first_dot",
                        ],
                    ]
                else:
                    dfs_recognition["shape"][num][ISI] = df[
                        (df["answer"].notna())
                        & (df["answer"] != 5)
                        & (df["fixation"].notna())
                    ].reset_index(drop=True)
                    dfs_recognition["shape"][num][ISI] = dfs_recognition["shape"][num][
                        ISI
                    ].loc[
                        :,
                        [
                            "name",
                            "rt",
                            "correct",
                            "target",
                            "fixation",
                            "fixation_target",
                            "first_dot",
                        ],
                    ]
            else:
                if i == 0:
                    dfs_recall["color"][num][ISI] = df[
                        (df["answer"].notna())
                        & (df["answer"] != 5)
                        & (df["fixation"].notna())
                    ].reset_index(drop=True)
                    dfs_recall["color"][num][ISI] = dfs_recall["color"][num][ISI].loc[
                        :,
                        [
                            "name",
                            "rt",
                            "correct",
                            "target",
                            "fixation",
                            "fixation_target",
                            "first_dot",
                        ],
                    ]
                else:
                    dfs_recognition["color"][num][ISI] = df[
                        (df["answer"].notna())
                        & (df["answer"] != 5)
                        & (df["fixation"].notna())
                    ].reset_index(drop=True)
                    dfs_recognition["color"][num][ISI] = dfs_recognition["color"][num][
                        ISI
                    ].loc[
                        :,
                        [
                            "name",
                            "rt",
                            "correct",
                            "target",
                            "fixation",
                            "fixation_target",
                            "first_dot",
                        ],
                    ]
    # 列fixation不为空的有效注视点
    dfs = {"recall": dfs_recall, "recognition": dfs_recognition}

    # 将原始数据集转换为长格式
    for m, type in enumerate(["recall", "recognition"]):
        for m, arr in enumerate(["shape", "color"]):
            for i, num in enumerate(["2", "4", "6"]):
                dfs[type][arr][num] = pd.concat(
                    [v.assign(ISI=k) for k, v in dfs[type][arr][num].items()]
                )
            dfs[type][arr] = pd.concat(
                [v.assign(NUM=k) for k, v in dfs[type][arr].items()]
            )
        dfs[type] = pd.concat([v.assign(TYPE=k) for k, v in dfs[type].items()])
    data_long = pd.concat([v.assign(Examtype=k) for k, v in dfs.items()])
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    print(data_long)
    # analy(data_long)
    data_long.to_csv(
        r"E:\数据汇总\实验三\eyedata\data3.csv", index=False, encoding="utf-8"
    )
    # 如果含义拓扑特性
    mask = data_long["target"].str.contains("_1").fillna(False)
    df_topo = {"topo": data_long[mask], "no_topo": data_long[~mask]}
    data_long = pd.concat([v.assign(Target=k) for k, v in df_topo.items()])
    print(data_long)
    # data_long.to_csv(r'E:\数据汇总\实验二\eyedata\num\data2.csv', index=False, encoding='utf-8')

    # analyTopo(data_long)
    #
    # analyTopo(data_long[(data_long["target"] == data_long["first_dot"])])
    # TOPO作为target，且命中
    TT_dot = data_long[
        (data_long["Target"] == "topo")
        & (data_long["target"] == data_long["first_dot"])
    ].reset_index(drop=True)
    # TOPO作为非target，且target命中
    TD_dot = data_long[
        (data_long["Target"] == "no_topo")
        & (data_long["target"] == data_long["first_dot"])
    ].reset_index(drop=True)
    # TOPO作为target，没命中
    DT_dot = data_long[
        (data_long["Target"] == "topo")
        & (data_long["target"] != data_long["first_dot"])
    ].reset_index(drop=True)
    # TOPO作为非target，target没命中
    DD_dot = data_long[
        (data_long["Target"] == "no_topo")
        & (data_long["target"] != data_long["first_dot"])
    ].reset_index(drop=True)

    # drawTopo(TT_dot, DT_dot, TD_dot, DD_dot)
    # plt.show()

    # 目标和首个注视点一致的形状/颜色
    df_target_dot = data_long[
        (data_long["target"] == data_long["first_dot"])
    ].reset_index(drop=True)
    # 目标和首个注视点不一致的形状/颜色
    df_target_dot_not = data_long[
        (data_long["target"] != data_long["first_dot"])
    ].reset_index(drop=True)

    plt.show()


eyedata_paths = r"E:\数据汇总\实验三\eyedata\num"


# eyeDataProcessSAVE(eyedata_paths)


#


def eyeDataProcess1(paths):
    data_long = pd.read_csv(
        paths, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    # drawtopo(data_long, 6)
    # analyTopo(data_long)
    # TOPO作为target，且命中
    TT_dot = data_long[
        (data_long["Target"] == "topo")
        & (data_long["target"] == data_long["first_dot"])
    ].reset_index(drop=True)
    # TOPO作为非target，且target命中
    TD_dot = data_long[
        (data_long["Target"] == "no_topo")
        & (data_long["target"] == data_long["first_dot"])
    ].reset_index(drop=True)
    # TOPO作为target，没命中
    DT_dot = data_long[
        (data_long["Target"] == "topo")
        & (data_long["target"] != data_long["first_dot"])
    ].reset_index(drop=True)
    # TOPO作为非target，target没命中
    DD_dot = data_long[
        (data_long["Target"] == "no_topo")
        & (data_long["target"] != data_long["first_dot"])
    ].reset_index(drop=True)

    drawTopo(TT_dot, DT_dot, TD_dot, DD_dot)

    draw(
        data_long[(data_long["first_dot"] == data_long["target"])],
        data_long[(data_long["first_dot"] != data_long["target"])],
        6,
    )
    for m, type in enumerate(["recall", "recognition"]):
        # df_t = data_long[(data_long["Examtype"] == type)&(data_long["Target"] == "topo")]
        df_t = data_long[(data_long["Examtype"] == type)]
        for m, arr in enumerate(["shape", "color"]):
            df_m = df_t[df_t["TYPE"] == arr]
            for i, num in enumerate([2, 4, 6]):
                df_n = df_m[df_m["NUM"] == num]
                for j, ISI in enumerate([500, 1000, 1500]):
                    df_i = df_n[(df_n["ISI"] == ISI)]
                    sum = df_i.shape[0]
                    # count = len(df_i[df_i["first_dot"].str.contains("_")])
                    count = len(df_i[df_i["first_dot"] == df_i["target"]])
                    print(type, arr, num, ISI, count / sum)
    data_long = data_long[(data_long["Target"] == "topo")]
    analy(data_long)


pathss = r"E:\数据汇总\实验二\eyedata\num\data2.csv"
# eyeDataProcess1(pathss)


def eyeDataProcessStatic(paths, Etype):
    data_long = pd.read_csv(
        paths + "/data.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_res = []
    for m, type in enumerate(["recall", "recognition"]):
        if Etype == "静态":
            df_t = data_long[
                (data_long["Examtype"] == type) & (data_long["Target"] == "topo")
            ]

        elif Etype == "预实验":
            df_t = data_long[(data_long["Examtype"] == type)]

        for m, arr in enumerate(["shape", "color"]):
            df_m = df_t[df_t["TYPE"] == arr]

            for i, num in enumerate([2, 4, 6]):
                df_n = df_m[df_m["NUM"] == num]

                for j, ISI in enumerate([500, 1000, 1500]):
                    df_i = df_n[(df_n["ISI"] == ISI)]
                    sum = df_i.shape[0]
                    # count = len(df_i[df_i["first_dot"].str.contains("_")])
                    count = len(df_i[df_i["first_dot"] == df_i["target"]])

                    hit_rate = count / sum
                    data_res.append(
                        {
                            "type": type,
                            "arr": arr,
                            "num": num,
                            "ISI": ISI,
                            "hit_rate": hit_rate,
                        }
                    )
    return data_res
