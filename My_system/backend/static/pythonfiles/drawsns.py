import os
import re
import io
import base64
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy.stats import shapiro
from matplotlib.font_manager import FontProperties
from static.pythonfiles.datafunc import (
    process_data,
    drawboxplot,
    drawSumboxplot,
    drawSumplot,
)


# 计算响应时间和准确率并保存，且进行绘图
def data_process(path_all, num, type):
    files = os.listdir(path_all)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 回忆
    selected_file = [f for f in csv_files if type in f]
    # 筛选包含数字num的文件名
    selected_files = [f for f in selected_file if num in f]
    df_rt_sum = pd.DataFrame()
    df_rt_s = pd.DataFrame()
    dt_correct = pd.DataFrame()
    for f in selected_files:
        # 获取文件名和后缀
        file_name, file_ext = os.path.splitext(os.path.basename(path_all + "\\" + f))
        dt_rt, df = process_data(path_all + "\\" + f)
        # 处理准确率
        # 计算非空行数
        non_null_count = df["correct"].notnull().sum()
        # 计算值为 True 的行数
        true_count = (df["correct"] == True).sum()
        # 计算每个实验的准确率
        accuracy = true_count / non_null_count
        dt_correct.insert(dt_correct.shape[1], file_name, pd.Series(accuracy))

        # 处理rt
        # 计算均值和标准差
        mean = pd.DataFrame(dt_rt.mean(), columns=[file_name + "_mean"])
        std = pd.DataFrame(dt_rt.std(), columns=[file_name + "_std"])
        # 将对应的“rt”列单独提取，以样本名作为列名，生成一个新的dt
        df_rt_sum = pd.concat([df_rt_sum, mean], axis=1)
        # 根据列(即ISI间隔不同)计算该列的整体均值以及方差，插入最后一行
        df_rt_s.at[-1, file_name + "_mean"] = df_rt_sum[file_name + "_mean"].mean()
        df_rt_sum = pd.concat([df_rt_sum, std], axis=1)
        df_rt_s.at[-1, file_name + "_std"] = df_rt_sum[file_name + "_mean"].std()

    # 将数据保存
    df_rt_sum = pd.concat([df_rt_sum, df_rt_s])
    df_rt_sum.to_csv(
        path_all + "\\汇总\\" + type + "_" + num + "_rt.csv",
        index=False,
        encoding="utf-8",
    )
    dt_correct.to_csv(
        path_all + "\\汇总\\" + type + "_" + num + "_correct.csv",
        index=False,
        encoding="utf-8",
    )
    print(df_rt_s)
    # rt绘图准备
    # 将列名根据ISI重新排序,定义正则表达式提取数字
    nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df_rt_sum.columns]
    sorted_col_names = [
        df_rt_sum.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
    ]
    print(sorted_col_names)
    # 检索含有shape和mean的列
    shape_cols_mean = [
        col for col in sorted_col_names if "shape" in col and "mean" in col
    ]
    shape_cols_std = [
        col for col in sorted_col_names if "shape" in col and "std" in col
    ]
    # 检索含有color和mean的列
    color_cols_mean = [
        col for col in sorted_col_names if "color" in col and "mean" in col
    ]
    color_cols_std = [
        col for col in sorted_col_names if "color" in col and "std" in col
    ]
    # 绘图
    drawSumboxplot(
        df_rt_sum, shape_cols_mean, shape_cols_std, "shape", type, path_all, num
    )
    drawSumboxplot(
        df_rt_sum, color_cols_mean, color_cols_std, "color", type, path_all, num
    )
    drawSumplot(df_rt_sum, shape_cols_mean, color_cols_mean, num, type, "RT", path_all)
    shape_cols = [
        re.sub(r"(_[^_]+)$", "", shape_cols_mean[i])
        for i in range(len(shape_cols_mean))
    ]
    color_cols = [
        re.sub(r"(_[^_]+)$", "", color_cols_mean[i])
        for i in range(len(color_cols_mean))
    ]
    drawSumplot(dt_correct, shape_cols, color_cols, num, type, "Accuracy", path_all)


path_all = r"E:\数据汇总\实验二"


# data_process(path_all, '6', "recognition")


# 将三个实验的结果放到一起来对比
def SumData(num, assessment, type):
    # 同一刺激数，不同实验，列名都一样
    path1 = r"E:\数据汇总\实验一\汇总\\" + type + "_" + num + "_" + assessment + ".csv"
    path2 = r"E:\数据汇总\实验二\汇总\\" + type + "_" + num + "_" + assessment + ".csv"
    path3 = r"E:\数据汇总\实验三\汇总\\" + type + "_" + num + "_" + assessment + ".csv"
    # 读取文件
    df1 = pd.read_csv(path1, encoding="utf-8", engine="python", on_bad_lines="warn")
    df2 = pd.read_csv(path2, encoding="utf-8", engine="python", on_bad_lines="warn")
    df3 = pd.read_csv(path3, encoding="utf-8", engine="python", on_bad_lines="warn")
    last_low1 = df1.iloc[-1]
    last_low2 = df2.iloc[-1]
    last_low3 = df3.iloc[-1]

    #  创建一个包含三个子图的画布
    fig, ax = plt.subplots()
    df_shape = []
    df_color = []
    colors = ["#f7723d", "#4d85bd", "#59a95a"]
    # 绘制每个子图的实线和虚线折线图
    for i, df in enumerate([df1, df2, df3]):
        nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df.columns]
        sorted_col_name = [
            df.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
        ]
        if assessment == "rt":
            df_shape.append(
                [col for col in sorted_col_name if "shape" in col and "mean" in col]
            )
            df_color.append(
                [col for col in sorted_col_name if "color" in col and "mean" in col]
            )
        if assessment == "correct":
            df_shape.append([col for col in sorted_col_name if "shape" in col])
            df_color.append([col for col in sorted_col_name if "color" in col])
    print(df_shape)
    col = [
        type + "_" + num + "_500",
        type + "_" + num + "_1000",
        type + "_" + num + "_1500",
    ]
    for i, df in enumerate([last_low1, last_low2, last_low3]):
        ax.plot(
            col,
            df[df_shape[i]],
            label=f"exam{i + 1} shape",
            linestyle="-",
            color=colors[i],
        )
    for i, df in enumerate([last_low1, last_low2, last_low3]):
        ax.plot(
            col,
            df[df_color[i]],
            label=f"exam{i + 1} color",
            linestyle="--",
            color=colors[i],
        )
    # 添加图例和横纵轴标签
    # 设置中文字体
    ax.legend(loc="upper right")
    ax.set_xlabel("ISI")
    ax.set_ylabel(assessment)
    # 添加整个图形的标题
    fig.suptitle("Line Plots")
    # 显示图形
    plt.show()
    plt.savefig(r"E:\数据汇总\\" + type + "_" + num + "_" + assessment + ".png")


# SumData("4", "rt", "recall")


# 将同一实验的不同刺激数目进行比较
def SumData1(path, num, assessment, type):
    # path1 = r"E:\数据汇总\实验" + num + "\汇总\\" + type + "_2_" + assessment + ".csv"
    # path2 = r"E:\数据汇总\实验" + num + "\汇总\\" + type + "_4_" + assessment + ".csv"
    # path3 = r"E:\数据汇总\实验" + num + "\汇总\\" + type + "_6_" + assessment + ".csv"
    path1 = path + "\\" + type + "_2_" + assessment + ".csv"
    path2 = path + "\\" + type + "_4_" + assessment + ".csv"
    path3 = path + "\\" + type + "_6_" + assessment + ".csv"
    # 读取文件
    df1 = pd.read_csv(path1, encoding="utf-8", engine="python", on_bad_lines="warn")
    df2 = pd.read_csv(path2, encoding="utf-8", engine="python", on_bad_lines="warn")
    df3 = pd.read_csv(path3, encoding="utf-8", engine="python", on_bad_lines="warn")
    last_low1 = df1.iloc[-1]
    last_low2 = df2.iloc[-1]
    last_low3 = df3.iloc[-1]

    #  创建画布
    fig, ax = plt.subplots(figsize=(5, 4))
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.xticks(fontname="Times New Roman")
    plt.yticks(fontname="Times New Roman")
    df_shape = []
    df_color = []
    colors = ["#f7723d", "#4d85bd", "#ffc24b"]
    # 绘制每个子图的实线和虚线折线图
    for i, df in enumerate([df1, df2, df3]):
        nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df.columns]
        sorted_col_name = [
            df.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
        ]
        if assessment == "rt":
            df_shape.append(
                [col for col in sorted_col_name if "shape" in col and "mean" in col]
            )
            df_color.append(
                [col for col in sorted_col_name if "color" in col and "mean" in col]
            )
        if assessment == "accuracy":
            df_shape.append([col for col in sorted_col_name if "shape" in col])
            df_color.append([col for col in sorted_col_name if "color" in col])
    print(df_shape)
    col = [type + "_500", type + "_1000", type + "_1500"]
    for i, df in enumerate([last_low1, last_low2, last_low3]):
        ax.plot(
            col,
            df[df_shape[i]],
            label=f"{2 * (i + 1)}_shape",
            linestyle="-",
            color=colors[i],
        )
    for i, df in enumerate([last_low1, last_low2, last_low3]):
        ax.plot(
            col,
            df[df_color[i]],
            label=f"{2 * (i + 1)}_color",
            linestyle="--",
            color=colors[i],
        )
    # 添加图例和横纵轴标签
    # 设置中文字体
    ax.legend(loc="upper right")
    ax.set_xlabel("ISI", fontname="Times New Roman")
    ax.set_ylabel(assessment, fontname="Times New Roman")
    # 添加整个图形的标题
    fig.suptitle("Pre-Experiment")
    # Save the generated image to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    # Convert the image buffer to base64 encoding
    image_data = base64.b64encode(buffer.read()).decode("utf-8")
    return image_data
    # 显示图形
    # plt.show()
    # plt.savefig(r'E:\数据汇总\实验' + num + '\汇总\\' + type + "_" + assessment + '.svg', format='svg')
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\静态P\\" + type + "_" + assessment + ".jpg",
    #     format="jpg",
    #     dpi=1000,
    # )


# SumData1("一", "rt", "recognition")


# 将同一实验的不同刺激数目进行比较topo和no_topo，实验二
def SumData2(urlpath, num, assessment, Ttype, stimtype):
    # path_csv = r"E:\数据汇总\实验" + num
    files = os.listdir(urlpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    selected_file = [f for f in csv_files if stimtype in f]
    # 区分识别和回忆
    selected_file_recall = [
        f for f in selected_file if "recall" in f
    ]  # 500\1000\1500\2,4,6
    selected_file_recognition = [
        f for f in selected_file if "recognition" in f
    ]  # 500\1000\1500\2,4,6
    df_recall_2 = pd.DataFrame()
    df_recall_4 = pd.DataFrame()
    df_recall_6 = pd.DataFrame()
    df_recognition_2 = pd.DataFrame()
    df_recognition_4 = pd.DataFrame()
    df_recognition_6 = pd.DataFrame()
    for j, fs in enumerate([selected_file_recall, selected_file_recognition]):
        for f in fs:
            # 获取文件名和后缀
            file_name, file_ext = os.path.splitext(f)
            dt_rt, df = process_data(urlpath + "\\" + f)
            mask_recall = df["target"].str.contains("_1").fillna(False)
            dfs = {}
            for i, col in enumerate(["topo", "nopo"]):
                dfs[col] = df[
                    (df["answer"].notna())
                    & (df["answer"] != 5)
                    & (mask_recall if i == 0 else ~mask_recall)
                ].reset_index(drop=True)
                dfs[col] = dfs[col].loc[:, ["rt", "correct"]]
                # 处理准确率
                # 计算非空行数
                non_null_count = dfs[col]["correct"].notnull().sum()
                # 计算值为 True 的行数
                true_count = (dfs[col]["correct"] == True).sum()
                # 计算每个实验的准确率
                accuracy = true_count / non_null_count
                if j == 0:
                    if "2" in file_name:
                        df_recall_2.insert(
                            df_recall_2.shape[1],
                            file_name + "_rt_" + col,
                            pd.Series(dfs[col]["rt"].mean()),
                        )
                        df_recall_2.insert(
                            df_recall_2.shape[1],
                            file_name + "_accuracy_" + col,
                            pd.Series(accuracy),
                        )
                    if "4" in file_name:
                        df_recall_4.insert(
                            df_recall_4.shape[1],
                            file_name + "_rt_" + col,
                            pd.Series(dfs[col]["rt"].mean()),
                        )
                        df_recall_4.insert(
                            df_recall_4.shape[1],
                            file_name + "_accuracy_" + col,
                            pd.Series(accuracy),
                        )
                    if "6" in file_name:
                        df_recall_6.insert(
                            df_recall_6.shape[1],
                            file_name + "_rt_" + col,
                            pd.Series(dfs[col]["rt"].mean()),
                        )
                        df_recall_6.insert(
                            df_recall_6.shape[1],
                            file_name + "_accuracy_" + col,
                            pd.Series(accuracy),
                        )
                else:
                    if "2" in file_name:
                        df_recognition_2.insert(
                            df_recognition_2.shape[1],
                            file_name + "_rt_" + col,
                            pd.Series(dfs[col]["rt"].mean()),
                        )
                        df_recognition_2.insert(
                            df_recognition_2.shape[1],
                            file_name + "_accuracy_" + col,
                            pd.Series(accuracy),
                        )
                    if "4" in file_name:
                        df_recognition_4.insert(
                            df_recognition_4.shape[1],
                            file_name + "_rt_" + col,
                            pd.Series(dfs[col]["rt"].mean()),
                        )
                        df_recognition_4.insert(
                            df_recognition_4.shape[1],
                            file_name + "_accuracy_" + col,
                            pd.Series(accuracy),
                        )
                    if "6" in file_name:
                        df_recognition_6.insert(
                            df_recognition_6.shape[1],
                            file_name + "_rt_" + col,
                            pd.Series(dfs[col]["rt"].mean()),
                        )
                        df_recognition_6.insert(
                            df_recognition_6.shape[1],
                            file_name + "_accuracy_" + col,
                            pd.Series(accuracy),
                        )
            print(df_recall_2, df_recognition_2)

    df_topo = []
    df_notopo = []
    colors = ["#f7723d", "#4d85bd", "#ffc24b"]
    col = [stimtype + "_500", stimtype + "_1000", stimtype + "_1500"]
    # # 绘制每个子图的实线和虚线折线图

    # 获取上一级路径
    parent_path = os.path.dirname(urlpath)
    # 进入上一级路径的预实验文件夹
    pre_experiment_folder = os.path.join(parent_path, "预实验")
    # 进入 "汇总文件夹"
    summary_folder = os.path.join(pre_experiment_folder, "汇总")
    path1 = summary_folder + "/recall_2_" + assessment + ".csv"
    path2 = summary_folder + "/recall_4_" + assessment + ".csv"
    path3 = summary_folder + "/recall_6_" + assessment + ".csv"
    # 读取文件
    df1 = pd.read_csv(path1, encoding="utf-8", engine="python", on_bad_lines="warn")
    df2 = pd.read_csv(path2, encoding="utf-8", engine="python", on_bad_lines="warn")
    df3 = pd.read_csv(path3, encoding="utf-8", engine="python", on_bad_lines="warn")
    last_low1 = df1.iloc[-1]
    last_low2 = df2.iloc[-1]
    last_low3 = df3.iloc[-1]
    df_type = []
    for i, df in enumerate([df1, df2, df3]):
        nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df.columns]
        sorted_col_name = [
            df.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
        ]
        if assessment == "rt":
            df_type.append(
                [col for col in sorted_col_name if stimtype in col and "mean" in col]
            )
        if assessment == "accuracy":
            df_type.append([col for col in sorted_col_name if stimtype in col])
    #  创建画布
    fig, ax = plt.subplots(figsize=(5, 4))
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.xticks(fontname="Times New Roman")
    plt.yticks(fontname="Times New Roman")
    for i, df in enumerate([df_recall_2, df_recall_4, df_recall_6]):
        nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df.columns]
        sorted_col_name = [
            df.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
        ]
        df_topo.append(
            [col for col in sorted_col_name if "topo" in col and str(assessment) in col]
        )
        df_notopo.append(
            [col for col in sorted_col_name if "nopo" in col and str(assessment) in col]
        )
    # print(df_topo)
    for i, df in enumerate([last_low1, last_low2, last_low3]):
        ax.plot(
            col,
            df[df_type[i]],
            label=f"{2 * (i + 1)}_Pre",
            linestyle="-.",
            color=colors[i],
        )
    for i, df in enumerate([df_recall_2, df_recall_4, df_recall_6]):
        ax.plot(
            col,
            df[df_topo[i]].values[0],
            label=f"{2 * (i + 1)}_T",
            linestyle="-",
            color=colors[i],
        )
    for i, df in enumerate([df_recall_2, df_recall_4, df_recall_6]):
        ax.plot(
            col,
            df[df_notopo[i]].values[0],
            label=f"{2 * (i + 1)}_D",
            linestyle="--",
            color=colors[i],
        )
    df_topo = []
    df_notopo = []
    # 添加图例和横纵轴标签
    # 设置中文字体
    ax.legend(loc="upper right")
    ax.set_xlabel("ISI")
    ax.set_ylabel(assessment)
    # 添加整个图形的标题
    fig.suptitle("Recall_" + assessment)
    # 显示图形
    # plt.show()
    # plt.savefig(r'E:\数据汇总\实验' + num + '\汇总\\topo_recall_' + stimtype + "_" + assessment + '.svg', format='svg')
    if Ttype == "recall":
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=1000)
        buffer.seek(0)
        # Convert the image buffer to base64 encoding
        image_data = base64.b64encode(buffer.read()).decode("utf-8")

    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\静态F\\topo_recall_"
    #     + stimtype
    #     + "_"
    #     + assessment
    #     + ".jpg",
    #     format="jpg",
    #     dpi=1000,
    # )

    # recognition
    #  创建画布
    path1 = summary_folder + "/recognition_2_" + assessment + ".csv"
    path2 = summary_folder + "/recognition_4_" + assessment + ".csv"
    path3 = summary_folder + "/recognition_6_" + assessment + ".csv"
    # 读取文件
    df1 = pd.read_csv(path1, encoding="utf-8", engine="python", on_bad_lines="warn")
    df2 = pd.read_csv(path2, encoding="utf-8", engine="python", on_bad_lines="warn")
    df3 = pd.read_csv(path3, encoding="utf-8", engine="python", on_bad_lines="warn")
    last_low1 = df1.iloc[-1]
    last_low2 = df2.iloc[-1]
    last_low3 = df3.iloc[-1]
    df_type = []
    for i, df in enumerate([df1, df2, df3]):
        nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df.columns]
        sorted_col_name = [
            df.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
        ]
        if assessment == "rt":
            df_type.append(
                [col for col in sorted_col_name if stimtype in col and "mean" in col]
            )
        if assessment == "accuracy":
            df_type.append([col for col in sorted_col_name if stimtype in col])
    fig, ax = plt.subplots(figsize=(5, 4))
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.xticks(fontname="Times New Roman")
    plt.yticks(fontname="Times New Roman")
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
    for i, df in enumerate([df_recognition_2, df_recognition_4, df_recognition_6]):
        nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df.columns]
        sorted_col_name = [
            df.columns[i] for i in sorted(range(len(nums)), key=lambda k: nums[k])
        ]
        df_topo.append(
            [col for col in sorted_col_name if "topo" in col and str(assessment) in col]
        )
        df_notopo.append(
            [col for col in sorted_col_name if "nopo" in col and str(assessment) in col]
        )
    # print(df_topo)
    for i, df in enumerate([last_low1, last_low2, last_low3]):
        ax.plot(
            col,
            df[df_type[i]],
            label=f"{2 * (i + 1)}_Pre",
            linestyle="-.",
            color=colors[i],
        )
    for i, df in enumerate([df_recognition_2, df_recognition_4, df_recognition_6]):
        ax.plot(
            col,
            df[df_topo[i]].values[0],
            label=f"{2 * (i + 1)}_T",
            linestyle="-",
            color=colors[i],
        )
    for i, df in enumerate([df_recognition_2, df_recognition_4, df_recognition_6]):
        ax.plot(
            col,
            df[df_notopo[i]].values[0],
            label=f"{2 * (i + 1)}_D",
            linestyle="--",
            color=colors[i],
        )
    df_topo = []
    df_notopo = []
    # 添加图例和横纵轴标签
    # 设置中文字体
    ax.legend(loc="upper right")
    ax.set_xlabel("ISI")
    ax.set_ylabel(assessment)
    # 添加整个图形的标题
    fig.suptitle("Recognition_" + assessment)
    # 显示图形
    # plt.show()
    # # plt.savefig(r'E:\数据汇总\实验' + num + '\汇总\\topo_recognition_' + stimtype + "_" + assessment + '.svg', format='svg')
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\静态F\\topo_recognition_"
    #     + stimtype
    #     + "_"
    #     + assessment
    #     + ".jpg",
    #     format="jpg",
    #     dpi=1000,
    # )
    if Ttype == "recognition":
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=1000)
        buffer.seek(0)
        # Convert the image buffer to base64 encoding
        image_data = base64.b64encode(buffer.read()).decode("utf-8")
    return image_data


# SumData2("二", "shape")
#
arr_shape = {
    "6": ["rect", "triangle", "circle", "star", "hexagram", "diamond"],
    "4": ["rect", "triangle", "circle", "star", "hexagram"],
    "2": ["rect", "triangle", "circle"],
}
arr_color = {
    "6": ["green", "yellow", "blue", "purple", "red", "cyan"],
    "4": ["green", "yellow", "blue", "purple", "red"],
    "2": ["green", "blue", "red"],
}


# 将实验一的不同目标刺激进行比较
def SumData3(stimtype):
    path_csv = r"E:\数据汇总\实验一"
    files = os.listdir(path_csv)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    selected_file = [f for f in csv_files if stimtype in f]
    # 区分识别和回忆
    selected_file_recall = [
        f for f in selected_file if "recall" in f
    ]  # 500\1000\1500\2,4,6
    selected_file_recognition = [
        f for f in selected_file if "recognition" in f
    ]  # 500\1000\1500\2,4,6
    df_recall_2 = pd.DataFrame()
    df_recall_4 = pd.DataFrame()
    df_recall_6 = pd.DataFrame()
    df_recognition_2 = pd.DataFrame()
    df_recognition_4 = pd.DataFrame()
    df_recognition_6 = pd.DataFrame()
    if stimtype == "shape":
        arr = arr_shape
    else:
        arr = arr_color
    for j, fs in enumerate([selected_file_recall, selected_file_recognition]):
        for f in fs:
            # 获取文件名和后缀
            file_name, file_ext = os.path.splitext(f)
            num = re.findall(r"_(\d+)_\d+", file_name)[0]
            dt_rt, df = process_data(path_csv + "\\" + f)
            dfs = {}
            for i in range(len(arr[num])):
                dfs[arr[num][i]] = df[
                    (df["answer"].notna())
                    & (df["answer"] != 5)
                    & (df["target"] == arr[num][i])
                ].reset_index(drop=True)
                dfs[arr[num][i]] = dfs[arr[num][i]].loc[:, ["rt", "correct"]]
                # 处理准确率
                # 计算非空行数
                non_null_count = dfs[arr[num][i]]["correct"].notnull().sum()
                # 计算值为 True 的行数
                true_count = (dfs[arr[num][i]]["correct"] == True).sum()
                # 计算每个实验的准确率
                accuracy = true_count / non_null_count
                if j == 0:
                    if "2" in file_name:
                        df_recall_2.insert(
                            df_recall_2.shape[1],
                            file_name + "_rt_" + arr[num][i],
                            pd.Series(dfs[arr[num][i]]["rt"].mean()),
                        )
                        df_recall_2.insert(
                            df_recall_2.shape[1],
                            file_name + "_accuracy_" + arr[num][i],
                            pd.Series(accuracy),
                        )
                    if "4" in file_name:
                        df_recall_4.insert(
                            df_recall_4.shape[1],
                            file_name + "_rt_" + arr[num][i],
                            pd.Series(dfs[arr[num][i]]["rt"].mean()),
                        )
                        df_recall_4.insert(
                            df_recall_4.shape[1],
                            file_name + "_accuracy_" + arr[num][i],
                            pd.Series(accuracy),
                        )
                    if "6" in file_name:
                        df_recall_6.insert(
                            df_recall_6.shape[1],
                            file_name + "_rt_" + arr[num][i],
                            pd.Series(dfs[arr[num][i]]["rt"].mean()),
                        )
                        df_recall_6.insert(
                            df_recall_6.shape[1],
                            file_name + "_accuracy_" + arr[num][i],
                            pd.Series(accuracy),
                        )
                else:
                    if "2" in file_name:
                        df_recognition_2.insert(
                            df_recognition_2.shape[1],
                            file_name + "_rt_" + arr[num][i],
                            pd.Series(dfs[arr[num][i]]["rt"].mean()),
                        )
                        df_recognition_2.insert(
                            df_recognition_2.shape[1],
                            file_name + "_accuracy_" + arr[num][i],
                            pd.Series(accuracy),
                        )
                    if "4" in file_name:
                        df_recognition_4.insert(
                            df_recognition_4.shape[1],
                            file_name + "_rt_" + arr[num][i],
                            pd.Series(dfs[arr[num][i]]["rt"].mean()),
                        )
                        df_recognition_4.insert(
                            df_recognition_4.shape[1],
                            file_name + "_accuracy_" + arr[num][i],
                            pd.Series(accuracy),
                        )
                    if "6" in file_name:
                        df_recognition_6.insert(
                            df_recognition_6.shape[1],
                            file_name + "_rt_" + arr[num][i],
                            pd.Series(dfs[arr[num][i]]["rt"].mean()),
                        )
                        df_recognition_6.insert(
                            df_recognition_6.shape[1],
                            file_name + "_accuracy_" + arr[num][i],
                            pd.Series(accuracy),
                        )
            print(df_recall_2, df_recognition_2)

    df_topo = [[], []]
    colors = ["green", "orange", "blue", "purple", "red", "cyan"]
    linestyle = ["-", "--"]
    col = [stimtype + "_500", stimtype + "_1000", stimtype + "_1500"]
    # 绘制每个子图的实线和虚线折线图
    for k, dfs in enumerate(
        [
            [df_recall_2, df_recognition_2],
            [df_recall_4, df_recognition_4],
            [df_recall_6, df_recognition_6],
        ]
    ):
        for m, assessment in enumerate(["rt", "accuracy"]):
            #  创建画布
            fig, ax = plt.subplots()
            plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
            for i, df in enumerate(dfs):
                nums = [int(re.findall(r"_\d+_(\d+)", col)[0]) for col in df.columns]
                sorted_col_name = [
                    df.columns[i]
                    for i in sorted(range(len(nums)), key=lambda k: nums[k])
                ]
                for j in range(len(arr[f"{2 * (k + 1)}"])):
                    df_topo[i].append(
                        [
                            col
                            for col in sorted_col_name
                            if arr[f"{2 * (k + 1)}"][j] in col
                            and str(assessment) in col
                        ]
                    )
            print(df_topo)
            for i, df in enumerate(dfs):
                print(df_topo[i])
                for j in range(len(arr[f"{2 * (k + 1)}"])):
                    ax.plot(
                        col,
                        df[df_topo[i][j]].values[0],
                        label=arr[f"{2 * (k + 1)}"][j]
                        + f"{'_recall' if i == 0 else '_recognition'}",
                        linestyle=linestyle[i],
                        color=colors[j],
                    )
            df_topo = [[], []]
            # 添加图例和横纵轴标签
            # 设置中文字体
            ax.legend(loc="upper right")
            ax.set_xlabel("ISI")
            ax.set_ylabel(assessment)
            # 添加整个图形的标题
            fig.suptitle("实验一_" + f"{2 * (k + 1)}" + "_recall_" + assessment)
            # 显示图形
            plt.show()
            plt.savefig(
                r"E:\数据汇总\实验一\汇总\\"
                + f"{2 * (k + 1)}"
                + "_recall_color"
                + assessment
                + ".png"
            )


# SumData3("color")


# dynamic 4
def drawCompares(urlpath, Type):
    path_color = urlpath + "\data.csv"
    path_shape = urlpath + "\shape_data.csv"
    data_color = pd.read_csv(
        path_color, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_shape = pd.read_csv(
        path_shape, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    df_color_box = pd.DataFrame()
    df_shape_box = pd.DataFrame()
    df_color = pd.DataFrame()
    df_shape = pd.DataFrame()
    # 箱线图
    for i, df in enumerate([data_color, data_shape]):
        for j, col in enumerate(["motion_E", "topo_E", "none_E", "motion", "topo"]):
            dfs = {}
            dfs[col] = df[df["Target"] == col].reset_index(drop=True)
            dfs[col] = dfs[col].loc[:, ["rt", "correct"]]
            # 处理准确率
            # 计算非空行数
            non_null_count = dfs[col]["correct"].notnull().sum()
            # 计算值为 True 的行数
            true_count = (dfs[col]["correct"] == True).sum()
            # 计算每个实验的准确率
            accuracy = true_count / non_null_count
            if i == 0:
                df_color_box = pd.concat([df_color_box, dfs[col]["rt"]], axis=1)
                df_color.insert(
                    df_color.shape[1], col + "_accuracy", pd.Series(accuracy)
                )
            else:
                df_shape_box = pd.concat([df_shape_box, dfs[col]["rt"]], axis=1)
                df_shape.insert(
                    df_shape.shape[1], col + "_accuracy", pd.Series(accuracy)
                )

    df_color_box.columns = [
        "motion_rt",
        "topo_rt",
        "none_rt",
        "motion_E_rt",
        "topo_E_rt",
    ]
    df_shape_box.columns = [
        "motion_rt",
        "topo_rt",
        "none_rt",
        "motion_E_rt",
        "topo_E_rt",
    ]
    col = ["motion", "topo", "none", "motion_E", "topo_E"]

    if Type == "color":
        i = 0
        dfs = [df_color_box, df_color]
    elif Type == "shape":
        i = 1
        dfs = [df_shape_box, df_shape]

    # print(dfs[0].columns, dfs[1])
    # 创建画布和子图
    fig, ax1 = plt.subplots(figsize=(5, 4), sharex="all")
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.xticks(fontname="Times New Roman")
    plt.yticks(fontname="Times New Roman")
    # 绘制箱线图
    dfs[0].plot(
        kind="box", ax=ax1, positions=[1, 2, 3, 4, 5], color="#0e606b"
    )  # 这个写法能过滤NaN值
    # 创建第二个轴
    ax2 = ax1.twinx()
    # 绘制折线图
    ax2.plot([1, 2, 3, 4, 5], dfs[1].iloc[0], color="#f66f69", label="Accuracy")
    # 设置左轴标签和标题
    ax1.set_ylabel("RT", fontname="Times New Roman")
    ax1.set_xticks([1, 2, 3, 4, 5])
    ax1.set_xticklabels(col)
    ax1.set_title(
        "color_RT & Accuracy" if i == 0 else "shape_RT & Accuracy",
        fontname="Times New Roman",
    )
    # 设置右轴标签
    ax2.set_ylabel("Accuracy", fontname="Times New Roman")
    ax2.set_ylim(0.65, 1)  # 根据需要设置合适的范围
    # 在图例中添加折线图的标签
    lines, labels = ax2.get_legend_handles_labels()
    ax2.legend(lines, labels)

    # 调整子图之间的间距
    fig.tight_layout()
    # 显示图形

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode("utf-8")
    return image_data
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\动态A\\"
    #     + f"{'color' if i == 0 else 'shape'}"
    #     + "compare_data.jpg",
    #     format="jpg",
    #     dpi=1000,
    # )

    # # plt.savefig(r'E:\数据汇总\dynamic\\' + f"{'color' if i == 0 else 'shape'}" + 'compare_data.svg', format='svg')
    # plt.show()


# drawCompares()


def drawCompares1():
    path = r"E:\数据汇总\dynamic\汇总\data.csv"
    data = pd.read_csv(path, encoding="utf-8", engine="python", on_bad_lines="warn")
    data_c = data[(data["NUM"] == 4) & (data["TYPE"] == "color")]
    data_c["Target"] = data_c["Target"].apply(lambda x: x + "_E")
    data_s = data[(data["NUM"] == 4) & (data["TYPE"] == "shape")]
    data_s["Target"] = data_s["Target"].apply(lambda x: x + "_E")
    path_color = r"E:\数据汇总\dynamic\4\汇总\data.csv"
    path_shape = r"E:\数据汇总\dynamic\4\汇总\shape_data.csv"
    data_color = pd.read_csv(
        path_color, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_shape = pd.read_csv(
        path_shape, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_shape = pd.concat([data_shape, data_s], axis=0)
    data_color = pd.concat([data_color, data_c], axis=0)
    md = smf.mixedlm("rt ~ Target", data_color, groups=data_color["name"])
    mdf = md.fit()
    # 查看模型结果
    print(mdf.summary())
    # 获取系数估计值和p值

    md_correct = smf.mixedlm("correct ~ Target", data_color, groups=data_color["name"])
    mdf = md_correct.fit()
    # 查看模型结果
    print(mdf.summary())
    md = smf.mixedlm("rt ~ Target", data_shape, groups=data_shape["name"])
    mdf = md.fit()
    # 查看模型结果
    print(mdf.summary())
    # 获取系数估计值和p值

    md_correct = smf.mixedlm("correct ~ Target", data_shape, groups=data_shape["name"])
    mdf = md_correct.fit()
    # 查看模型结果
    print(mdf.summary())

    # df_color_box = pd.DataFrame()
    # df_shape_box = pd.DataFrame()
    # df_color = pd.DataFrame()
    # df_shape = pd.DataFrame()
    # # 箱线图
    # for i, df in enumerate([data_color, data_shape]):
    #     for j, col in enumerate(["motion", "topo", "motion_E", "topo_E", "topo_2", "topo_3"]):
    #         dfs = {}
    #         dfs[col] = df[df["Target"] == col].reset_index(drop=True)
    #         dfs[col] = dfs[col].loc[:, ['rt', 'correct']]
    #         # 处理准确率
    #         # 计算非空行数
    #         non_null_count = dfs[col]['correct'].notnull().sum()
    #         # 计算值为 True 的行数
    #         true_count = (dfs[col]['correct'] == True).sum()
    #         # 计算每个实验的准确率
    #         accuracy = true_count / non_null_count
    #         if i == 0:
    #             df_color_box = pd.concat([df_color_box, dfs[col]['rt']], axis=1)
    #             df_color.insert(df_color.shape[1], col + "_accuracy", pd.Series(accuracy))
    #         else:
    #             df_shape_box = pd.concat([df_shape_box, dfs[col]['rt']], axis=1)
    #             df_shape.insert(df_shape.shape[1], col + "_accuracy", pd.Series(accuracy))
    #
    # df_color_box.columns = ["motion_rt", "topo_rt", "motion_E_rt", "topo_E_rt", "topo_2_rt", "topo_3_rt"]
    # df_shape_box.columns = ["motion_rt", "topo_rt", "motion_E_rt", "topo_E_rt", "topo_2_rt", "topo_3_rt"]
    # col = ["D_motion", "D_topo", "D_motion_E", "D_topo_E", "S_topo_C", "S_topo_E"]
    #
    # for i, dfs in enumerate([[df_color_box, df_color], [df_shape_box, df_shape]]):
    #     print(dfs[0].columns, dfs[1])
    #     # 创建画布和子图
    #     fig, ax1 = plt.subplots(figsize=(6, 4), sharex="all")
    #     plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
    #     # 绘制箱线图
    #     dfs[0].plot(kind='box', ax=ax1, positions=[1, 2, 3, 4, 5, 6], color='#0e606b',widths=0.5)  # 这个写法能过滤NaN值
    #     # 创建第二个轴
    #     ax2 = ax1.twinx()
    #     # 绘制折线图
    #     ax2.plot([1, 2, 3, 4, 5, 6], dfs[1].iloc[0], color='#f66f69', label='Accuracy',marker='o')
    #     # 设置左轴标签和标题
    #     ax1.set_ylabel("RT")
    #     ax1.set_xticks([1, 2, 3, 4, 5, 6])
    #     ax1.set_xticklabels(col)
    #     ax1.set_title("color_RT & Accuracy" if i == 0 else "shape_RT & Accuracy")
    #     # 设置右轴标签
    #     ax2.set_ylabel('Accuracy')
    #     ax2.set_ylim(0.65, 1)  # 根据需要设置合适的范围
    #     # 在图例中添加折线图的标签
    #     lines, labels = ax2.get_legend_handles_labels()
    #     ax2.legend(lines, labels)
    #
    #     # 调整子图之间的间距
    #     fig.tight_layout()
    #     # 显示图形
    #     plt.savefig(r'E:\数据汇总\\' + f"{'color' if i == 0 else 'shape'}" + 'compare_data.svg', format='svg')
    #     plt.show()


# drawCompares1()
