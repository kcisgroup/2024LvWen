import os
import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.sandbox.stats.multicomp import MultiComparison
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.formula.api as smf
from static.pythonfiles.datafunc import process_data, namefun
from static.pythonfiles.drawsns import drawCompares


def param_test1(scvpath):
    data_res = []
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选识别和回忆文件
    # 创建一个空字典
    dfs = {"shape": {"2": {}, "4": {}, "6": {}}, "color": {"2": {}, "4": {}, "6": {}}}

    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)
        num = re.findall(r"_(\d+)_", file_name)[0]
        if num == "2":
            arr = ["topo", "motion"]
        else:
            arr = ["topo", "motion", "none"]
        dt_rt, df = process_data(scvpath + "\\" + f)
        mask_topo = df["target"].str.contains("_").fillna(False)
        mask_motion = (df["motion"] == 1.0) & (df["topo"] == 0.0)
        mask_none = (df["motion"] == 0.0) & (df["topo"] == 0.0)
        df = namefun(df)
        df["name"].fillna(method="ffill", inplace=True)
        for m, col in enumerate(arr):
            if "shape" in file_name:
                dfs["shape"][num][col] = df[
                    (df["answer"].notna())
                    & (mask_topo if m == 0 else mask_motion if m == 1 else mask_none)
                ].reset_index(drop=True)
                dfs["shape"][num][col] = dfs["shape"][num][col].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange"]
                ]
            else:
                dfs["color"][num][col] = df[
                    (df["answer"].notna())
                    & (mask_topo if m == 0 else mask_motion if m == 1 else mask_none)
                ].reset_index(drop=True)
                dfs["color"][num][col] = dfs["color"][num][col].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange"]
                ]

    # print(dfs)
    #
    # # 将原始数据集转换为长格式
    #
    for n, arr in enumerate(["shape", "color"]):
        for i, num in enumerate(["2", "4", "6"]):
            dfs[arr][num] = pd.concat(
                [v.assign(Target=k) for k, v in dfs[arr][num].items()]
            )

        dfs[arr] = pd.concat([v.assign(NUM=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(TYPE=k) for k, v in dfs.items()])
    data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
    # print(data_long)
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    # data_long.to_csv(scvpath + "\\汇总\\data.csv", index=False, encoding='utf-8')
    # data_long = pd.read_csv(
    #     scvpath + "\\汇总\\data.csv",
    #     encoding="utf-8",
    #     engine="python",
    #     on_bad_lines="warn",
    # )
    # 混合线性效应模型
    # data = data_long[(data_long["NUM"] == 4) & (data_long["TYPE"] == "shape")]
    # print(data)
    data = data_long
    md = smf.mixedlm("rt ~ Target*NUM*TYPE", data, groups=data["name"])
    mdf = md.fit()
    # 查看模型结果
    data_res.append({"rt": mdf.summary()})
    # print(mdf.summary())
    # 获取系数估计值和p值

    md_correct = smf.mixedlm("correct ~ Target*NUM*TYPE", data, groups=data["name"])
    mdf = md_correct.fit()
    # 查看模型结果
    data_res.append({"correct": mdf.summary()})
    # print(mdf.summary())
    # # 建立混合线性效应模型
    # data = data_long[(data_long['TYPE'] == "color") & (data_long['NUM'] == 6) & (data_long['Target'] == "motion")]
    # print(data)
    # md = smf.mixedlm("rt ~ mchange", data, groups=data["name"])
    # mdf = md.fit()
    # # 查看模型结果
    # print(mdf.summary())
    # # 获取系数估计值和p值
    #
    # md_correct = smf.mixedlm("correct ~ mchange", data, groups=data["name"])
    # mdf = md_correct.fit()
    # # 查看模型结果
    # print(mdf.summary())
    #
    # data = data_long[(data_long['TYPE'] == "color") & (data_long['NUM'] == 6) & (data_long['Target'] == "topo")]
    # print(data)
    # md = smf.mixedlm("rt ~ tchange", data, groups=data["name"])
    # mdf = md.fit()
    # # 查看模型结果
    # print(mdf.summary())
    # # 获取系数估计值和p值
    #
    # md_correct = smf.mixedlm("correct ~ tchange", data, groups=data["name"])
    # mdf = md_correct.fit()
    # # 查看模型结果
    # print(mdf.summary())
    return data_res


path = r"E:\数据汇总\dynamic"


# param_test1(path)


def draw_dynamic(scvpath):
    data = pd.read_csv(scvpath, encoding="utf-8", engine="python", on_bad_lines="warn")
    for j, type in enumerate(["shape", "color"]):
        df = data[data["TYPE"] == type]
        df_topo_rt = pd.DataFrame()
        df_motion_rt = pd.DataFrame()
        df_none_rt = pd.DataFrame()
        df_topo_accuracy = pd.DataFrame()
        df_motion_accuracy = pd.DataFrame()
        df_none_accuracy = pd.DataFrame()
        for i, num in enumerate([2, 4, 6]):
            dfs = df[df["NUM"] == num]
            print(dfs[dfs["Target"] == "topo"]["rt"].reset_index(drop=True))
            df_topo_rt.insert(
                df_topo_rt.shape[1],
                num,
                pd.Series(dfs[dfs["Target"] == "topo"]["rt"].mean()),
            )
            # df_topo_rt = pd.concat([df_topo_rt, dfs[dfs["Target"] == "topo"].reset_index(drop=True)['rt']], axis=1)
            # 处理准确率
            df_topo_accuracy.insert(
                df_topo_accuracy.shape[1],
                num,
                pd.Series(
                    (dfs[dfs["Target"] == "topo"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "topo"]["correct"].notnull().sum()
                ),
            )
            df_motion_rt.insert(
                df_motion_rt.shape[1],
                num,
                pd.Series(dfs[dfs["Target"] == "motion"]["rt"].mean()),
            )
            # df_motion_rt = pd.concat([df_motion_rt, dfs[dfs["Target"] == "motion"].reset_index(drop=True)['rt']], axis=1)
            # 处理准确率
            df_motion_accuracy.insert(
                df_motion_accuracy.shape[1],
                num,
                pd.Series(
                    (dfs[dfs["Target"] == "motion"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "motion"]["correct"].notnull().sum()
                ),
            )
            if num != 2:
                df_none_rt.insert(
                    df_none_rt.shape[1],
                    num,
                    pd.Series(dfs[dfs["Target"] == "none"]["rt"].mean()),
                )
                # df_none_rt = pd.concat([df_none_rt, dfs[dfs["Target"] == "none"].reset_index(drop=True)['rt']], axis=1)
                # 处理准确率
                df_none_accuracy.insert(
                    df_none_accuracy.shape[1],
                    num,
                    pd.Series(
                        (dfs[dfs["Target"] == "none"]["correct"] == True).sum()
                        / dfs[dfs["Target"] == "none"]["correct"].notnull().sum()
                    ),
                )

        print(df_topo_accuracy, df_motion_accuracy, df_none_accuracy)
        col = [type + "_2", type + "_4", type + "_6"]
        colors = ["#f66f69", "#1597a5", "#0e606b"]
        for i, dfss in enumerate(
            [[df_topo_rt, df_motion_rt], [df_topo_accuracy, df_motion_accuracy]]
        ):
            #  创建画布
            fig, ax = plt.subplots()
            plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
            for m, df in enumerate(dfss):
                ax.plot(
                    [1, 2, 3],
                    df.values[0],
                    marker="o",
                    label=f"{'Topo' if m == 0 else 'Motion'}",
                    color=colors[m],
                )
            if i == 0:
                ax.plot(
                    [2, 3],
                    df_none_rt.values[0],
                    marker="o",
                    label="NTNM",
                    color=colors[2],
                )
            else:
                ax.plot(
                    [2, 3],
                    df_none_accuracy.values[0],
                    marker="o",
                    label="NTNM",
                    color=colors[2],
                )
            ax.set_xticks([1, 2, 3])
            ax.set_xticklabels(col)
            lines, labels = ax.get_legend_handles_labels()
            ax.set_title(type + "_RT" if i == 0 else type + "_Accuracy")
            ax.legend(lines, labels)

            plt.savefig(
                r"E:\数据汇总\dynamic\汇总\\"
                + type
                + f"{'_RT_' if i == 0 else '_Accuracy_'}"
                + "compare_data.svg",
                format="svg",
            )
            plt.show()


scvpath = r"E:\数据汇总\dynamic\\汇总\\data.csv"


# draw_dynamic(scvpath)


# dy
def param_testdy(scvpath, Type):
    data_res = []
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选识别和回忆文件
    # 创建一个空字典
    dfs_topo = {"shape": {}, "color": {}}
    dfs_motion = {"shape": {}, "color": {}}
    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)
        dt_rt, df = process_data(scvpath + "\\" + f)
        df = namefun(df)
        df["name"].fillna(method="ffill", inplace=True)
        if "shape" in file_name:
            if "topo" in file_name:
                dfs_topo["shape"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_topo["shape"] = dfs_topo["shape"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]
            if "motion" in file_name:
                dfs_motion["shape"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_motion["shape"] = dfs_motion["shape"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]

        else:
            if "topo" in file_name:
                dfs_topo["color"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_topo["color"] = dfs_topo["color"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]
            if "motion" in file_name:
                dfs_motion["color"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_motion["color"] = dfs_motion["color"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]

    print(dfs_motion, dfs_topo)
    dfs = {"topo": dfs_topo, "motion": dfs_motion}
    # 将原始数据集转换为长格式

    for n, arr in enumerate(["topo", "motion"]):
        dfs[arr] = pd.concat([v.assign(TYPE=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(Target=k) for k, v in dfs.items()])
    data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
    # print(data_long)
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    data_long.to_csv(scvpath + "/汇总/data_4.csv", index=False, encoding="utf-8")
    # data_long = pd.read_csv(
    #     scvpath + "\汇总\data_4.csv",
    #     encoding="utf-8",
    #     engine="python",
    #     on_bad_lines="warn",
    # )
    # # 实验二
    # data_long_2 = pd.read_csv(
    #     "E:\数据汇总\data2.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    # )
    # data_long_2 = data_long_2[
    #     (data_long_2["ISI"] == 1000)
    #     & (data_long_2["NUM"] == 4)
    #     & (data_long_2["Examtype"] == "recall")
    #     & (data_long_2["Target"] == "topo")
    #     & (data_long_2["TYPE"] == "color")
    # ].reset_index(drop=True)
    # data_long_2["Target"] = "topo_2"
    # # 实验三
    # data_long_3 = pd.read_csv(
    #     "E:\数据汇总\data3.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    # )
    # data_long_3 = data_long_3[
    #     (data_long_3["ISI"] == 1000)
    #     & (data_long_3["NUM"] == 4)
    #     & (data_long_3["Examtype"] == "recall")
    #     & (data_long_3["Target"] == "topo")
    #     & (data_long_3["TYPE"] == "color")
    # ].reset_index(drop=True)
    # data_long_3["Target"] = "topo_3"
    # # 动态Main
    # data_long_4 = pd.read_csv(
    #     r"E:\数据汇总\dynamic\\汇总\\data.csv",
    #     encoding="utf-8",
    #     engine="python",
    #     on_bad_lines="warn",
    # )
    # data_long_41 = (
    #     data_long_4[
    #         (data_long_4["NUM"] == 4)
    #         & (data_long_4["Target"] == "topo")
    #         & (data_long_4["TYPE"] == "color")
    #     ]
    #     .reset_index(drop=True)
    #     .copy()
    # )
    # data_long_41.loc[:, "Target"] = "topo_E"
    # data_long_42 = (
    #     data_long_4[
    #         (data_long_4["NUM"] == 4)
    #         & (data_long_4["Target"] == "motion")
    #         & (data_long_4["TYPE"] == "color")
    #     ]
    #     .reset_index(drop=True)
    #     .copy()
    # )
    # data_long_42.loc[:, "Target"] = "motion_E"
    # data_long_43 = (
    #     data_long_4[
    #         (data_long_4["NUM"] == 4)
    #         & (data_long_4["Target"] == "none")
    #         & (data_long_4["TYPE"] == "color")
    #     ]
    #     .reset_index(drop=True)
    #     .copy()
    # )
    # data_long_43.loc[:, "Target"] = "none_E"
    # # print(data_long_3)
    # 混合线性效应模型
    # # 建立混合线性效应模型
    # data = data_long[(data_long["TYPE"] == "color") & (data_long["T"] == 1)]
    # data = pd.concat(
    #     [data, data_long_2, data_long_3, data_long_41, data_long_42, data_long_43],
    #     axis=0,
    # )
    # data.to_csv(scvpath + "\\data.csv", index=False, encoding="utf-8")
    # print(data)
    data_long = data_long[(data_long["TYPE"] == Type) & (data_long["T"] == 1)]
    md = smf.mixedlm("rt ~ Target*TYPE", data_long, groups=data_long["name"])
    mdf = md.fit()
    # 查看模型结果
    print(mdf.summary())
    data_res.append({"rt": mdf.summary()})
    # 获取系数估计值和p值

    md_correct = smf.mixedlm(
        "correct ~ Target*TYPE", data_long, groups=data_long["name"]
    )
    mdf = md_correct.fit()
    # 查看模型结果
    print(mdf.summary())
    data_res.append({"correct": mdf.summary()})
    return data_res


path1 = r"E:\数据汇总\dynamic\4"

# param_testdy(path1)


# drawCompares()


def param_testdy1(scvpath, scvpath1, scvpath2, scvpath3):
    data_res = []
    data_long = pd.read_csv(
        scvpath2, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_long_2 = pd.read_csv(
        scvpath, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_long_2 = data_long_2[
        (data_long_2["ISI"] == 1000)
        & (data_long_2["Examtype"] == "recall")
        & (data_long_2["Target"] == "topo")
        & (data_long_2["TYPE"] == "shape")
    ].reset_index(drop=True)
    data_long_2["Target"] = "topo_2"
    data_long_3 = pd.read_csv(
        scvpath1, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_long_3 = data_long_3[
        (data_long_3["ISI"] == 1000)
        & (data_long_3["Examtype"] == "recall")
        & (data_long_3["Target"] == "topo")
        & (data_long_3["TYPE"] == "shape")
    ]
    data_long_3["Target"] = "topo_3"
    data_long4 = pd.read_csv(
        scvpath3,
        encoding="utf-8",
        engine="python",
        on_bad_lines="warn",
    )
    data_long41 = data_long4[
        (data_long4["TYPE"] == "shape")
        & (data_long4["T"] == 1)
        & (data_long4["Target"] == "topo")
    ].copy()
    data_long42 = data_long4[
        (data_long4["TYPE"] == "shape")
        & (data_long4["T"] == 1)
        & (data_long4["Target"] == "motion")
    ].copy()
    data_long41.loc[:, "Target"] = "topo_E"
    data_long42.loc[:, "Target"] = "motion_E"
    # 混合线性效应模型
    # 建立混合线性效应模型
    data = data_long[(data_long["TYPE"] == "shape")]
    data = pd.concat([data_long_2, data_long_3, data], axis=0)
    data = data[data["NUM"] == 4]
    data = pd.concat([data_long_2, data_long_3, data, data_long41, data_long42], axis=0)
    # 将"Target"变量转换为虚拟变量，以"topo_2"作为基准组
    dummy_vars = pd.get_dummies(data["Target"], prefix="Target")
    dummy_vars = dummy_vars.drop(
        "Target_topo", axis=1
    )  # 删除"Target_topo_2"列，保留其他虚拟变量

    # 将虚拟变量与其他变量合并为一个新的数据框
    new_data = pd.concat([data[["name", "rt", "correct"]], dummy_vars], axis=1)

    md = smf.mixedlm(
        "rt ~ Target_topo_2+Target_motion +Target_none+ Target_topo_3+Target_topo_E+Target_motion_E",
        new_data,
        groups=new_data["name"],
    )
    mdf = md.fit()
    # 查看模型结果
    data_res.append({"rt": mdf.summary()})
    # print(mdf.summary())
    # 获取系数估计值和p值

    md_correct = smf.mixedlm(
        "correct ~ Target_topo_2+Target_motion +Target_none+ Target_topo_3+Target_topo_E+Target_motion_E",
        new_data,
        groups=new_data["name"],
    )
    mdf = md_correct.fit()
    data_res.append({"correct": mdf.summary()})
    # 查看模型结果
    # print(mdf.summary())
    return data_res


path2 = r"E:\数据汇总\dynamic\\汇总\\data.csv"


# param_testdy1(path2)


def param_testTorM(scvpath):
    data_res = []
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选识别和回忆文件
    # 创建一个空字典
    dfs_topo = {"shape": {}, "color": {}}
    dfs_motion = {"shape": {}, "color": {}}
    for f in csv_files:
        file_name, file_ext = os.path.splitext(f)
        dt_rt, df = process_data(scvpath + "\\" + f)
        df = namefun(df)
        df["name"].fillna(method="ffill", inplace=True)
        if "shape" in file_name:
            if "topo" in file_name:
                dfs_topo["shape"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_topo["shape"] = dfs_topo["shape"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]
            if "motion" in file_name:
                dfs_motion["shape"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_motion["shape"] = dfs_motion["shape"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]

        else:
            if "topo" in file_name:
                dfs_topo["color"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_topo["color"] = dfs_topo["color"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]
            if "motion" in file_name:
                dfs_motion["color"] = df[(df["answer"].notna())].reset_index(drop=True)
                dfs_motion["color"] = dfs_motion["color"].loc[
                    :, ["name", "rt", "target", "correct", "mchange", "tchange", "T"]
                ]

    print(dfs_motion, dfs_topo)
    dfs = {"topo": dfs_topo, "motion": dfs_motion}
    # 将原始数据集转换为长格式

    for n, arr in enumerate(["topo", "motion"]):
        dfs[arr] = pd.concat([v.assign(TYPE=k) for k, v in dfs[arr].items()])
    data_long = pd.concat([v.assign(Target=k) for k, v in dfs.items()])
    data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
    # print(data_long)
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    # data_long = pd.read_csv(
    #     scvpath + "\\data_4.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    # )

    data = data_long[
        (data_long["TYPE"] == "color")
        & (data_long["T"] == 1)
        & (data_long["Target"] == "topo")
    ]
    # print(data)
    md = smf.mixedlm("rt ~ tchange", data, groups=data["name"])
    mdf = md.fit()
    # 查看模型结果
    print(mdf.summary())
    # 获取系数估计值和p值

    md_correct = smf.mixedlm("correct ~ tchange", data, groups=data["name"])
    mdf = md_correct.fit()
    # 查看模型结果
    print(mdf.summary())

    data1 = data_long[
        (data_long["TYPE"] == "color")
        & (data_long["T"] == 1)
        & (data_long["Target"] == "motion")
    ]
    print(data)
    md = smf.mixedlm("rt ~ mchange", data1, groups=data1["name"])
    mdf = md.fit()
    data_res.append({"rt": mdf.summary()})
    # 查看模型结果
    print(mdf.summary())
    # 获取系数估计值和p值

    md_correct = smf.mixedlm("correct ~ mchange", data1, groups=data1["name"])
    mdf = md_correct.fit()
    data_res.append({"correct": mdf.summary()})
    # 查看模型结果
    print(mdf.summary())
    return data_res


path2 = r"E:\数据汇总\dynamic\4\汇总"


# param_testTorM(path2, "color")


def param_testTorM1(scvpath, type):
    data_long1 = pd.read_csv(
        scvpath + "\\data.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    for i, num in enumerate([2, 4, 6]):
        data_long = data_long1[data_long1["NUM"] == num]
        data = data_long[(data_long["TYPE"] == type) & (data_long["Target"] == "topo")]

        md = smf.mixedlm("rt ~ mchange", data, groups=data["name"])
        mdf = md.fit()
        # 查看模型结果
        print(mdf.summary())
        # 获取系数估计值和p值

        md_correct = smf.mixedlm("correct ~ mchange", data, groups=data["name"])
        mdf = md_correct.fit()
        print(mdf.summary())

        data1 = data_long[
            (data_long["TYPE"] == type) & (data_long["Target"] == "motion")
        ]
        print(data)
        md = smf.mixedlm("rt ~ tchange", data1, groups=data1["name"])
        mdf = md.fit()
        print(mdf.summary())

        md_correct = smf.mixedlm("correct ~ tchange", data1, groups=data1["name"])
        mdf = md_correct.fit()
        print(mdf.summary())


path3 = r"E:\数据汇总\dynamic\汇总"


# param_testTorM1(path3, "color")


def draw_dynamic1(scvpath):
    data = pd.read_csv(scvpath, encoding="utf-8", engine="python", on_bad_lines="warn")
    data_topo1 = pd.read_csv(
        r"E:\数据汇总\data2.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_topo_E1 = pd.read_csv(
        r"E:\数据汇总\data3.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    for j, type in enumerate(["shape", "color"]):
        df = data[data["TYPE"] == type]
        data_topo = data_topo1[data_topo1["TYPE"] == type]
        data_topo_E = data_topo_E1[data_topo_E1["TYPE"] == type]
        df_topo_rt = pd.DataFrame()
        df_topo_rt_S = pd.DataFrame()
        df_topo_rt_E = pd.DataFrame()
        df_motion_rt = pd.DataFrame()
        df_none_rt = pd.DataFrame()
        df_topo_accuracy_S = pd.DataFrame()
        df_topo_accuracy_E = pd.DataFrame()
        df_topo_accuracy = pd.DataFrame()
        df_motion_accuracy = pd.DataFrame()
        df_none_accuracy = pd.DataFrame()
        for i, num in enumerate([2, 4, 6]):
            dfs = df[df["NUM"] == num]
            # print(dfs[dfs["Target"] == "topo"]['rt'].reset_index(drop=True))
            # 静态
            df_topo_rt_S.insert(
                df_topo_rt_S.shape[1],
                num,
                pd.Series(
                    data_topo[
                        (data_topo["Target"] == "topo")
                        & (data_topo["NUM"] == num)
                        & (data_topo["ISI"] == 1000)
                        & (data_topo["Examtype"] == "recall")
                    ]["rt"].mean()
                ),
            )
            df_topo_rt_E.insert(
                df_topo_rt_E.shape[1],
                num,
                pd.Series(
                    data_topo_E[
                        (data_topo_E["Target"] == "topo")
                        & (data_topo_E["NUM"] == num)
                        & (data_topo_E["ISI"] == 1000)
                        & (data_topo_E["Examtype"] == "recall")
                    ]["rt"].mean()
                ),
            )
            df_topo_accuracy_S.insert(
                df_topo_accuracy_S.shape[1],
                num,
                pd.Series(
                    (
                        data_topo[
                            (data_topo["Target"] == "topo")
                            & (data_topo["NUM"] == num)
                            & (data_topo["ISI"] == 1000)
                            & (data_topo["Examtype"] == "recall")
                        ]["correct"]
                        == 1
                    ).sum()
                    / data_topo[
                        (data_topo["Target"] == "topo")
                        & (data_topo["NUM"] == num)
                        & (data_topo["ISI"] == 1000)
                        & (data_topo["Examtype"] == "recall")
                    ]["correct"]
                    .notnull()
                    .sum()
                ),
            )
            df_topo_accuracy_E.insert(
                df_topo_accuracy_E.shape[1],
                num,
                pd.Series(
                    (
                        data_topo_E[
                            (data_topo_E["Target"] == "topo")
                            & (data_topo_E["NUM"] == num)
                            & (data_topo_E["ISI"] == 1000)
                            & (data_topo_E["Examtype"] == "recall")
                        ]["correct"]
                        == 1
                    ).sum()
                    / data_topo_E[
                        (data_topo_E["Target"] == "topo")
                        & (data_topo_E["NUM"] == num)
                        & (data_topo_E["ISI"] == 1000)
                        & (data_topo_E["Examtype"] == "recall")
                    ]["correct"]
                    .notnull()
                    .sum()
                ),
            )
            # 动态
            df_topo_rt.insert(
                df_topo_rt.shape[1],
                num,
                pd.Series(dfs[dfs["Target"] == "topo"]["rt"].mean()),
            )
            # 处理准确率
            df_topo_accuracy.insert(
                df_topo_accuracy.shape[1],
                num,
                pd.Series(
                    (dfs[dfs["Target"] == "topo"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "topo"]["correct"].notnull().sum()
                ),
            )
            df_motion_rt.insert(
                df_motion_rt.shape[1],
                num,
                pd.Series(dfs[dfs["Target"] == "motion"]["rt"].mean()),
            )
            # 处理准确率
            df_motion_accuracy.insert(
                df_motion_accuracy.shape[1],
                num,
                pd.Series(
                    (dfs[dfs["Target"] == "motion"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "motion"]["correct"].notnull().sum()
                ),
            )
            if num != 2:
                df_none_rt.insert(
                    df_none_rt.shape[1],
                    num,
                    pd.Series(dfs[dfs["Target"] == "none"]["rt"].mean()),
                )
                # df_none_rt = pd.concat([df_none_rt, dfs[dfs["Target"] == "none"].reset_index(drop=True)['rt']], axis=1)
                # 处理准确率
                df_none_accuracy.insert(
                    df_none_accuracy.shape[1],
                    num,
                    pd.Series(
                        (dfs[dfs["Target"] == "none"]["correct"] == True).sum()
                        / dfs[dfs["Target"] == "none"]["correct"].notnull().sum()
                    ),
                )

        col = [type + "_2", type + "_4", type + "_6"]
        colors = ["#f66f69", "#1597a5", "#0e606b", "#ffc24b", "#81b8df"]
        for i, dfss in enumerate(
            [
                [df_topo_rt, df_motion_rt, df_topo_rt_S, df_topo_rt_E],
                [
                    df_topo_accuracy,
                    df_motion_accuracy,
                    df_topo_accuracy_S,
                    df_topo_accuracy_E,
                ],
            ]
        ):
            #  创建画布
            fig, ax = plt.subplots()
            plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
            for m, df in enumerate(dfss):
                ax.plot(
                    [1, 2, 3],
                    df.values[0],
                    marker=f"{'v' if m == 2 or m == 3 else 'o'}",
                    linestyle=f"{'--' if m == 2 or m == 3 else '-'}",
                    label=f"{'Topo' if m == 0 else 'Motion' if m == 1 else 'Topo_S' if m == 2 else 'Topo_E'}",
                    color=colors[m],
                )
            if i == 0:
                ax.plot(
                    [2, 3],
                    df_none_rt.values[0],
                    marker="o",
                    label="NTNM",
                    color=colors[4],
                )
            else:
                ax.plot(
                    [2, 3],
                    df_none_accuracy.values[0],
                    marker="o",
                    label="NTNM",
                    color=colors[4],
                )
            ax.set_xticks([1, 2, 3])
            ax.set_xticklabels(col)
            lines, labels = ax.get_legend_handles_labels()
            ax.set_title(type + "_RT" if i == 0 else type + "_Accuracy")
            ax.legend(lines, labels)

            # plt.savefig(r'E:\数据汇总\dynamic\汇总\\' + type + f"{'_RT_' if i == 0 else '_Accuracy_'}" + 'compare_data.svg',
            #             format='svg')
            plt.show()


scvpath1 = r"E:\数据汇总\dynamic\\汇总\\data.csv"
# draw_dynamic1(scvpath1)
