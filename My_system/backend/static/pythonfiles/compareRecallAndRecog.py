import os
import random
import re
import io
import base64
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from static.pythonfiles.datafunc import process_data


def Comparison(number, stim_num, assessment):
    path_recall = (
        r"E:\数据汇总\实验"
        + number
        + "\汇总\\recall_"
        + stim_num
        + "_"
        + assessment
        + ".csv"
    )
    path_recognition = (
        r"E:\数据汇总\实验"
        + number
        + "\汇总\\recognition_"
        + stim_num
        + "_"
        + assessment
        + ".csv"
    )
    # 读取文件
    df_recall = pd.read_csv(
        path_recall, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    df_recognition = pd.read_csv(
        path_recognition, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    last_low_recall = df_recall.iloc[-1]
    last_low_recognition = df_recognition.iloc[-1]
    fig, ax = plt.subplots()
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
    df_shape = []
    df_color = []
    colors = ["purple", "blue"]
    # 绘制每个子图的实线和虚线折线图
    for i, df in enumerate([df_recall, df_recognition]):
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
    col = ["500", "1000", "1500"]
    for i, df in enumerate([last_low_recall, last_low_recognition]):
        ax.plot(
            col,
            df[df_shape[i]],
            label=f"{'recall' if i == 0 else 'recognition'}_shape",
            linestyle="-",
            color=colors[i],
        )
    for i, df in enumerate([last_low_recall, last_low_recognition]):
        ax.plot(
            col,
            df[df_color[i]],
            label=f"{'recall' if i == 0 else 'recognition'}_color",
            linestyle="--",
            color=colors[i],
        )
    # 添加图例和横纵轴标签
    # 设置中文字体
    ax.legend(loc="upper right")
    ax.set_xlabel("ISI")
    ax.set_ylabel(assessment)
    # 添加整个图形的标题
    fig.suptitle("实验" + number + "_" + stim_num + "_" + assessment)
    # 显示图形
    plt.show()
    plt.savefig(
        r"E:\数据汇总\实验" + number + "\汇总\\" + stim_num + "_" + assessment + ".svg",
        format="svg",
    )


# Comparison("一", "2", "rt")


def Comparison2and3(urlpath, num, assessment, examtype):
    path_all = urlpath + "/data3.csv"
    if assessment == "accuracy":
        assessment = "correct"
    df = pd.read_csv(path_all, encoding="utf-8", engine="python", on_bad_lines="warn")
    for i, numb in enumerate([2, 4, 6]):
        df_n = df[
            (df["NUM"] == numb)
            & (df["Target"] == "topo")
            & (df["Examtype"] == examtype)
        ]
        df_rt_sum = pd.DataFrame()
        dt_correct = pd.DataFrame()
        for j, type in enumerate(["shape", "color"]):
            df_e = df_n[df_n["TYPE"] == type]
            for m, isi in enumerate([500, 1000, 1500]):
                df_i = df_e[df_e["ISI"] == isi]
                # 处理准确率
                # 计算非空行数
                non_null_count = df_i["correct"].notnull().sum()
                # 计算值为 True 的行数
                true_count = (df_i["correct"] == 1).sum()
                # 计算每个实验的准确率
                accuracy = true_count / non_null_count
                dt_correct.insert(
                    dt_correct.shape[1],
                    examtype + "_" + type + "_" + str(numb) + "_" + str(isi),
                    pd.Series(accuracy),
                )
                # 处理rt
                # 计算均值和标准差
                mean = pd.DataFrame(
                    [df_i["rt"].mean()],
                    columns=[
                        examtype
                        + "_"
                        + type
                        + "_"
                        + str(numb)
                        + "_"
                        + str(isi)
                        + "_mean"
                    ],
                )
                std = pd.DataFrame(
                    [df_i["rt"].std()],
                    columns=[
                        examtype
                        + "_"
                        + type
                        + "_"
                        + str(numb)
                        + "_"
                        + str(isi)
                        + "_std"
                    ],
                )
                # 将对应的“rt”列单独提取，以样本名作为列名，生成一个新的dt
                df_rt_sum = pd.concat([df_rt_sum, mean], axis=1)
                # 根据列(即ISI间隔不同)计算该列的整体均值以及方差，插入最后一行
                df_rt_sum = pd.concat([df_rt_sum, std], axis=1)
        # 将数据保存
        df_rt_sum.to_csv(
            urlpath + "/" + examtype + "_" + str(numb) + "_topo_rt.csv",
            index=False,
            encoding="utf-8",
        )
        dt_correct.to_csv(
            urlpath + "/" + examtype + "_" + str(numb) + "_topo_correct.csv",
            index=False,
            encoding="utf-8",
        )

    path1 = urlpath + "/" + examtype + "_2_topo_" + assessment + ".csv"
    path2 = urlpath + "/" + examtype + "_4_topo_" + assessment + ".csv"
    path3 = urlpath + "/" + examtype + "_6_topo_" + assessment + ".csv"
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
        if assessment == "correct":
            df_shape.append([col for col in sorted_col_name if "shape" in col])
            df_color.append([col for col in sorted_col_name if "color" in col])
    print(df_shape)
    col = [examtype + "_500", examtype + "_1000", examtype + "_1500"]
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
    ax.set_ylabel("accuracy", fontname="Times New Roman")
    # 添加整个图形的标题
    fig.suptitle("Static-T-E-Experiments")
    # 显示图形
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    # Convert the image buffer to base64 encoding
    image_data = base64.b64encode(buffer.read()).decode("utf-8")
    # plt.show()
    # # plt.savefig(r'E:\数据汇总\实验' + num + '\汇总\\' + examtype + "_" + assessment + '.svg', format='svg')
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\静态F\\" + examtype + "_" + assessment + ".jpg",
    #     format="jpg",
    #     dpi=1000,
    # )
    return image_data


# Comparison2and3("三", "correct", "recall")


# 刺激数量作为x轴,实验一
def Comparison2(stimtype):
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
    df_recall_500 = pd.DataFrame()
    df_recall_1000 = pd.DataFrame()
    df_recall_1500 = pd.DataFrame()
    df_recognition_500 = pd.DataFrame()
    df_recognition_1000 = pd.DataFrame()
    df_recognition_1500 = pd.DataFrame()
    for j, fs in enumerate([selected_file_recall, selected_file_recognition]):
        for f in fs:
            # 获取文件名和后缀
            file_name, file_ext = os.path.splitext(f)
            num = re.findall(r"_(\d+)_\d+", file_name)[0]
            dt_rt, df = process_data(path_csv + "\\" + f)
            dfs = {}
            dfs[num] = df[(df["answer"].notna()) & (df["answer"] != 5)].reset_index(
                drop=True
            )
            dfs[num] = dfs[num].loc[:, ["rt", "correct"]]
            # 处理准确率
            # 计算非空行数
            non_null_count = dfs[num]["correct"].notnull().sum()
            # 计算值为 True 的行数
            true_count = (dfs[num]["correct"] == True).sum()
            # 计算每个实验的准确率
            accuracy = true_count / non_null_count
            if j == 0:
                if "_500" in file_name:
                    df_recall_500.insert(
                        df_recall_500.shape[1],
                        file_name + "_rt",
                        pd.Series(dfs[num]["rt"].mean()),
                    )
                    df_recall_500.insert(
                        df_recall_500.shape[1],
                        file_name + "_accuracy",
                        pd.Series(accuracy),
                    )
                if "_1000" in file_name:
                    df_recall_1000.insert(
                        df_recall_1000.shape[1],
                        file_name + "_rt",
                        pd.Series(dfs[num]["rt"].mean()),
                    )
                    df_recall_1000.insert(
                        df_recall_1000.shape[1],
                        file_name + "_accuracy",
                        pd.Series(accuracy),
                    )
                if "_1500" in file_name:
                    df_recall_1500.insert(
                        df_recall_1500.shape[1],
                        file_name + "_rt",
                        pd.Series(dfs[num]["rt"].mean()),
                    )
                    df_recall_1500.insert(
                        df_recall_1500.shape[1],
                        file_name + "_accuracy",
                        pd.Series(accuracy),
                    )
            else:
                if "_500" in file_name:
                    df_recognition_500.insert(
                        df_recognition_500.shape[1],
                        file_name + "_rt",
                        pd.Series(dfs[num]["rt"].mean()),
                    )
                    df_recognition_500.insert(
                        df_recognition_500.shape[1],
                        file_name + "_accuracy",
                        pd.Series(accuracy),
                    )
                if "_1000" in file_name:
                    df_recognition_1000.insert(
                        df_recognition_1000.shape[1],
                        file_name + "_rt",
                        pd.Series(dfs[num]["rt"].mean()),
                    )
                    df_recognition_1000.insert(
                        df_recognition_1000.shape[1],
                        file_name + "_accuracy",
                        pd.Series(accuracy),
                    )
                if "_1500" in file_name:
                    df_recognition_1500.insert(
                        df_recognition_1500.shape[1],
                        file_name + "_rt",
                        pd.Series(dfs[num]["rt"].mean()),
                    )
                    df_recognition_1500.insert(
                        df_recognition_1500.shape[1],
                        file_name + "_accuracy",
                        pd.Series(accuracy),
                    )
        print(df_recall_500, df_recognition_500)

    df_colum = []
    colors = ["red", "blue", "green"]
    linestyle = ["-", "--"]
    col = [stimtype + "_2", stimtype + "_4", stimtype + "_6"]
    # 绘制每个子图的实线和虚线折线图
    for m, assessment in enumerate(["rt", "accuracy"]):
        #  创建画布
        fig, ax = plt.subplots()
        plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
        for k, dfs in enumerate(
            [
                [df_recall_500, df_recall_1000, df_recall_1500],
                [df_recognition_500, df_recognition_1000, df_recognition_1500],
            ]
        ):
            for i, df in enumerate(dfs):
                nums = [int(re.findall(r"_(\d+)_\d+", col)[0]) for col in df.columns]
                sorted_col_name = [
                    df.columns[i]
                    for i in sorted(range(len(nums)), key=lambda k: nums[k])
                ]
                df_colum.append(
                    [col for col in sorted_col_name if str(assessment) in col]
                )
            print(df_colum)
            for i, df in enumerate(dfs):
                print(df_colum[i])
                ax.plot(
                    col,
                    df[df_colum[i]].values[0],
                    label=f"{500 * (i + 1)}"
                    + f"{'_recall' if k == 0 else '_recognition'}",
                    linestyle=linestyle[k],
                    color=colors[i],
                )
            df_colum = []
            # 添加图例和横纵轴标签
            # 设置中文字体
            ax.legend(loc="upper right")
            ax.set_xlabel("ISI")
            ax.set_ylabel(assessment)
            # 添加整个图形的标题
            fig.suptitle("实验一_shape_" + assessment)
            # 显示图形
            plt.show()
            plt.savefig(
                r"E:\数据汇总\实验一\汇总\\"
                + f"{2 * (k + 1)}"
                + "_recall_"
                + assessment
                + ".png"
            )


# Comparison2("color")
