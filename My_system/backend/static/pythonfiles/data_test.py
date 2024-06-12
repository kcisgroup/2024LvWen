import os
import re

import numpy as np
import pandas as pd

# import pingouin as pg
import statsmodels.api as sm
from scipy.stats import shapiro, friedmanchisquare, kruskal, f_oneway
from statsmodels.formula.api import ols
from statsmodels.regression.mixed_linear_model import MixedLMResults
from statsmodels.sandbox.stats.multicomp import MultiComparison
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

from static.pythonfiles.datafunc import process_data, namefun

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


# 参数检验
def param_test11(scvpath, num, stimtype, ISI):
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选包含数字num的文件名
    selected_files = [f for f in csv_files if num in f and stimtype in f and ISI in f]
    recall_file = [f for f in selected_files if "recall" in f]
    recognition_file = [f for f in selected_files if "recognition" in f]
    recall_rt, df_recall = process_data(scvpath + "\\" + recall_file[0])
    recognition_rt, df_recognition = process_data(scvpath + "\\" + recognition_file[0])
    df_recall = namefun(df_recall)
    df_recognition = namefun(df_recognition)
    df_recall["name"].fillna(method="ffill", inplace=True)
    df_recognition["name"].fillna(method="ffill", inplace=True)
    # print(df_recall, df_recognition)
    # df_recall.to_csv(path + "\\_c.csv", index=False, encoding='utf-8')
    if stimtype == "shape":
        arr = arr_shape
    else:
        arr = arr_color
    # 创建一个空字典
    dfs_recall = {}
    dfs_recognition = {}
    for col in recall_rt.columns:
        dfs_recall[col] = df_recall[
            (df_recall["answer"].notna())
            & (df_recall["answer"] != 5)
            & (df_recall["name"] == col)
        ].reset_index(drop=True)
        dfs_recall[col] = dfs_recall[col].loc[:, ["rt", "target", "correct"]]

    for col in recognition_rt.columns:
        dfs_recognition[col] = df_recognition[
            (df_recognition["answer"].notna())
            & (df_recognition["answer"] != 5)
            & (df_recognition["name"] == col)
        ].reset_index(drop=True)
        dfs_recognition[col] = dfs_recognition[col].loc[:, ["rt", "target", "correct"]]

    for j in range(2):
        dfs = dfs_recall if j == 0 else dfs_recognition
        # 将原始数据集转换为长格式
        data_long = pd.concat([v.assign(key=k) for k, v in dfs.items()])
        data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
        print(data_long)

        # # 参数检验
        # # 进行单因素方差分析，并计算p值
        # f, p = f_oneway(data_long[data_long['target'] == 'circle']['rt'],
        #                 data_long[data_long['target'] == 'hexagram']['rt'],
        #                 data_long[data_long['target'] == 'rect']['rt'],
        #                 data_long[data_long['target'] == 'star']['rt'],
        #                 data_long[data_long['target'] == 'triangle']['rt'])
        # # f, p = f_oneway(data_long[data_long['target'] == 'red']['rt'],
        # #                 data_long[data_long['target'] == 'green']['rt'],
        # #                 data_long[data_long['target'] == 'blue']['rt'],
        # #                 data_long[data_long['target'] == 'purple']['rt'],
        # #                 data_long[data_long['target'] == 'yellow']['rt'])
        # print("One-way ANOVA F-value(rt): {:.4f}".format(f))
        # print("One-way ANOVA p-value(rt): {:.4f}".format(p))
        # f, p = f_oneway(data_long[data_long['target'] == 'circle']['correct'],
        #                 data_long[data_long['target'] == 'hexagram']['correct'],
        #                 data_long[data_long['target'] == 'rect']['correct'],
        #                 data_long[data_long['target'] == 'star']['correct'],
        #                 data_long[data_long['target'] == 'triangle']['correct'])
        # # f, p = f_oneway(data_long[data_long['target'] == 'red']['correct'],
        # #                 data_long[data_long['target'] == 'green']['correct'],
        # #                 data_long[data_long['target'] == 'blue']['correct'],
        # #                 data_long[data_long['target'] == 'purple']['correct'],
        # #                 data_long[data_long['target'] == 'yellow']['correct'])
        # print("One-way ANOVA F-value(correct): {:.4f}".format(f))
        # print("One-way ANOVA p-value(correct): {:.4f}".format(p))

        # 进行重复测量方差分析
        # 使用 np.mean 聚合函数对数据进行聚合
        data_long_agg = data_long.groupby(["key", "target"], as_index=False).agg(
            {"log_rt": np.mean}
        )
        aov_rt = AnovaRM(
            data_long_agg, depvar="log_rt", subject="key", within=["target"]
        )
        result = aov_rt.fit()
        print(result.summary())
        # aov_correct = AnovaRM(data_long_agg, depvar='correct', subject='key', within=['target'])
        # result = aov_correct.fit()
        # print(result.summary())

        # # 使用OLS模型进行重复测量方差分析
        # rm = ols("rt ~ C(target) + C(key) + C(target):C(key)",data=data_long).fit()
        # table = sm.stats.anova_lm(rm, typ=2)
        # print(table)
        # # 创建虚拟变量
        data = pd.get_dummies(data_long, columns=["target"], drop_first=True)
        # # 定义自变量和因变量
        # X = data[['rt', 'target_hexagram', 'target_rect', 'target_star', 'target_triangle']]
        # y = data['correct'].replace({True: 1, False: 0})
        # # 添加常量列并创建模型
        # X = sm.add_constant(X)
        # model = sm.OLS(y, X).fit()
        # # 输出模型的回归结果
        # print(model.summary())

        # # tukey hsd
        # mc = MultiComparison(data_long['rt'], data_long['target'])
        # result = mc.tukeyhsd()
        # print(result)
        #
        # # 进行多重比较并使用Bonferroni校正
        # comp = pairwise_tukeyhsd(data_long['rt'], data_long['target'])
        # print(comp)
        # comp_bonf = pairwise_tukeyhsd(data_long['rt'], data_long['target'], alpha=0.05 / int(num))
        # print(comp_bonf)

        # # 回归模型
        # # 构建模型，这里假设只考虑形状对反应时间的影响，使用圆形作为基准水平
        data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
        # model = sm.formula.ols('rt ~ C(target, Treatment("circle"))', data=data_long).fit()  # 最小二乘回归模型
        # model_correct = sm.formula.ols('correct ~ C(target, Treatment("circle"))', data=data_long).fit()  # 最小二乘回归模型
        # # 查看模型摘要
        # print(model.summary())
        # print(model_correct.summary())

        # 混合线性效应模型
        # 建立混合线性效应模型
        md = smf.mixedlm("rt ~ target", data_long, groups=data_long["key"])
        mdf = md.fit()
        # 查看模型结果
        print(mdf.summary())

        md_correct = smf.mixedlm("correct ~ target", data_long, groups=data["key"])
        mdf = md_correct.fit()
        # 查看模型结果
        print(mdf.summary())


path = r"E:\数据汇总\实验一"


# param_test(path, "2", "color", "_500")


# 参数检验
def param_test_topo(scvpath, num, stimtype, ISI):
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选包含数字num的文件名
    selected_files = [f for f in csv_files if num in f and stimtype in f and ISI in f]
    recall_file = [f for f in selected_files if "recall" in f]
    recognition_file = [f for f in selected_files if "recognition" in f]
    recall_rt, df_recall = process_data(scvpath + "\\" + recall_file[0])
    recognition_rt, df_recognition = process_data(scvpath + "\\" + recognition_file[0])
    df_recall = namefun(df_recall)
    df_recognition = namefun(df_recognition)
    df_recall["name"].fillna(method="ffill", inplace=True)
    df_recognition["name"].fillna(method="ffill", inplace=True)
    # print(df_recall, df_recognition)
    # df_recall.to_csv(path + "\\_c.csv", index=False, encoding='utf-8')
    if stimtype == "shape":
        arr = arr_shape
    else:
        arr = arr_color
    # 创建一个空字典
    dfs_recall = {"2": {}, "4": {}, "6": {}}
    dfs_recognition = {"2": {}, "4": {}, "6": {}}

    mask_recall = df_recall["target"].str.contains("_1").fillna(False)
    mask_recognition = df_recognition["target"].str.contains("_1").fillna(False)
    for i, col in enumerate(["topo", "no_topo"]):
        dfs_recall[col] = df_recall[
            (df_recall["answer"].notna())
            & (df_recall["answer"] != 5)
            & (mask_recall if i == 0 else ~mask_recall)
        ].reset_index(drop=True)
        dfs_recall[col] = dfs_recall[col].loc[:, ["name", "rt", "target", "correct"]]
        dfs_recognition[col] = df_recognition[
            (df_recognition["answer"].notna())
            & (df_recognition["answer"] != 5)
            & (mask_recognition if i == 0 else ~mask_recognition)
        ].reset_index(drop=True)
        dfs_recognition[col] = dfs_recognition[col].loc[
            :, ["name", "rt", "target", "correct"]
        ]

    for j in range(2):
        dfs = dfs_recall if j == 0 else dfs_recognition
        # 将原始数据集转换为长格式
        data_long = pd.concat([v.assign(key=k) for k, v in dfs.items()])
        data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
        print(data_long)
        data = pd.get_dummies(data_long, columns=["key"], drop_first=True)
        data_long["correct"] = data["correct"].replace({True: 1, False: 0})
        # 进行重复测量方差分析
        # 使用 np.mean 聚合函数对数据进行聚合
        # data_long_agg = data_long.groupby(['name', 'key'], as_index=False).agg({'log_rt': np.mean})
        # aov_rt = AnovaRM(data_long_agg, depvar='log_rt', subject='name', within=['key'])
        # result = aov_rt.fit()
        # print(result.summary())
        #
        # aov_correct = AnovaRM(data_long_agg, depvar='correct', subject='name', within=['key'])
        # result = aov_correct.fit()
        # print(result.summary())

        # # 使用OLS模型进行重复测量方差分析
        # rm = ols("rt ~ C(target) + C(key) + C(target):C(key)",data=data_long).fit()
        # table = sm.stats.anova_lm(rm, typ=2)
        # print(table)
        # # 创建虚拟变量

        # # 定义自变量和因变量
        # X = data[['rt', 'target_hexagram', 'target_rect', 'target_star', 'target_triangle']]
        # y = data['correct'].replace({True: 1, False: 0})
        # # 添加常量列并创建模型
        # X = sm.add_constant(X)
        # model = sm.OLS(y, X).fit()
        # # 输出模型的回归结果
        # print(model.summary())

        # tukey hsd
        mc = MultiComparison(data_long["rt"], data_long["key"])
        result = mc.tukeyhsd()
        print(result)
        # tukey hsd
        mc = MultiComparison(data_long["correct"], data_long["key"])
        result = mc.tukeyhsd()
        print(result)
        print(" ------------====------------  ")
        # 进行多重比较并使用Bonferroni校正
        comp = pairwise_tukeyhsd(data_long["rt"], data_long["key"])
        print(comp)
        comp_bonf = pairwise_tukeyhsd(data_long["rt"], data_long["key"], alpha=0.05 / 2)
        print(comp_bonf)
        comp = pairwise_tukeyhsd(data_long["correct"], data_long["key"])
        print(comp)
        comp_bonf = pairwise_tukeyhsd(
            data_long["correct"], data_long["key"], alpha=0.05 / 2
        )
        print(comp_bonf)
        # # 回归模型
        # # 构建模型，这里假设只考虑形状对反应时间的影响，使用圆形作为基准水平

        # model = sm.formula.ols('rt ~ C(target, Treatment("circle"))', data=data_long).fit()  # 最小二乘回归模型
        # model_correct = sm.formula.ols('correct ~ C(target, Treatment("circle"))', data=data_long).fit()  # 最小二乘回归模型
        # # 查看模型摘要
        # print(model.summary())
        # print(model_correct.summary())

        # 混合线性效应模型
        # 建立混合线性效应模型
        md = smf.mixedlm("rt ~ key", data_long, groups=data["name"])
        mdf = md.fit()
        # 查看模型结果
        print(mdf.summary())

        md_correct = smf.mixedlm("correct ~ key", data_long, groups=data["name"])
        mdf = md_correct.fit()
        # 查看模型结果
        print(mdf.summary())


path1 = r"E:\数据汇总\实验二"


# param_test_topo(path1, "2", "shape", "_500")


# 实验二topo和非topo
def param_testto(scvpath, Examtype):
    data_res = []
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选识别和回忆文件
    recall_files = [f for f in csv_files if "recall" in f]
    recognition_files = [f for f in csv_files if "recognition" in f]
    # rfiles = [f for f in csv_files if Examtype in f]
    # 创建一个空字典
    dfs_recall = {
        "shape": {
            "2": {"topo": {}, "no_topo": {}},
            "4": {"topo": {}, "no_topo": {}},
            "6": {"topo": {}, "no_topo": {}},
        },
        "color": {
            "2": {"topo": {}, "no_topo": {}},
            "4": {"topo": {}, "no_topo": {}},
            "6": {"topo": {}, "no_topo": {}},
        },
    }
    dfs_recognition = {
        "shape": {
            "2": {"topo": {}, "no_topo": {}},
            "4": {"topo": {}, "no_topo": {}},
            "6": {"topo": {}, "no_topo": {}},
        },
        "color": {
            "2": {"topo": {}, "no_topo": {}},
            "4": {"topo": {}, "no_topo": {}},
            "6": {"topo": {}, "no_topo": {}},
        },
    }

    for i, fs in enumerate([recall_files, recognition_files]):
        for f in fs:
            file_name, file_ext = os.path.splitext(f)
            ISI = re.findall(r"_\d+_(\d+)", file_name)[0]
            num = re.findall(r"_(\d+)_\d+", file_name)[0]
            dt_rt, df = process_data(scvpath + "\\" + f)
            mask_recall = df["target"].str.contains("_1").fillna(False)
            mask_recognition = df["target"].str.contains("_1").fillna(False)
            df = namefun(df)
            df["name"].fillna(method="ffill", inplace=True)
            for m, col in enumerate(["topo", "no_topo"]):
                if "shape" in file_name:
                    if i == 0:
                        dfs_recall["shape"][num][col][ISI] = df[
                            (df["answer"].notna())
                            & (df["answer"] != 5)
                            & (mask_recall if m == 0 else ~mask_recall)
                        ].reset_index(drop=True)
                        dfs_recall["shape"][num][col][ISI] = dfs_recall["shape"][num][
                            col
                        ][ISI].loc[:, ["name", "rt", "target", "correct"]]
                    else:
                        dfs_recognition["shape"][num][col][ISI] = df[
                            (df["answer"].notna())
                            & (df["answer"] != 5)
                            & (mask_recognition if m == 0 else ~mask_recognition)
                        ].reset_index(drop=True)
                        dfs_recognition["shape"][num][col][ISI] = dfs_recognition[
                            "shape"
                        ][num][col][ISI].loc[:, ["name", "rt", "target", "correct"]]
                else:
                    if i == 0:
                        dfs_recall["color"][num][col][ISI] = df[
                            (df["answer"].notna())
                            & (df["answer"] != 5)
                            & (mask_recall if m == 0 else ~mask_recall)
                        ].reset_index(drop=True)
                        dfs_recall["color"][num][col][ISI] = dfs_recall["color"][num][
                            col
                        ][ISI].loc[:, ["name", "rt", "target", "correct"]]
                    else:
                        dfs_recognition["color"][num][col][ISI] = df[
                            (df["answer"].notna())
                            & (df["answer"] != 5)
                            & (mask_recognition if m == 0 else ~mask_recognition)
                        ].reset_index(drop=True)
                        dfs_recognition["color"][num][col][ISI] = dfs_recognition[
                            "color"
                        ][num][col][ISI].loc[:, ["name", "rt", "target", "correct"]]
    # print(dfs_recall)

    dfs = {"recall": dfs_recall, "recognition": dfs_recognition}
    # 将原始数据集转换为长格式
    for m, type in enumerate(["recall", "recognition"]):
        for n, arr in enumerate(["shape", "color"]):
            for i, num in enumerate(["2", "4", "6"]):
                for k, target in enumerate(["topo", "no_topo"]):
                    dfs[type][arr][num][target] = pd.concat(
                        [
                            v.assign(ISI=k)
                            for k, v in dfs[type][arr][num][target].items()
                        ]
                    )
                dfs[type][arr][num] = pd.concat(
                    [v.assign(Target=k) for k, v in dfs[type][arr][num].items()]
                )
            dfs[type][arr] = pd.concat(
                [v.assign(NUM=k) for k, v in dfs[type][arr].items()]
            )
        dfs[type] = pd.concat([v.assign(TYPE=k) for k, v in dfs[type].items()])
    data_long = pd.concat([v.assign(Examtype=k) for k, v in dfs.items()])
    data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
    # print(data_long)
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    # data_long.to_csv(scvpath + "\\汇总\\data.csv", index=False, encoding="utf-8")
    # # 检测共线性
    # variables = ['ISI', 'NUM', 'TYPE', 'Examtype']
    # mapping1 = {'recall': 1, 'recognition': 2}
    # mapping2 = {'shape': 1, 'color': 2}
    # mapping3 = {'500': 500, '1000': 1000, '1500': 1500}
    # mapping4 = {'2': 2, '4': 4, '6': 6}
    # X = data_long[variables]
    # X['TYPE'] = X['TYPE'].map(mapping2)
    # X['Examtype'] = X['Examtype'].map(mapping1)
    # X['NUM'] = X['NUM'].map(mapping4)
    # X['ISI'] = X['ISI'].map(mapping3)
    # print(X)
    # X = sm.add_constant(X)
    # vif = pd.DataFrame()
    # vif["Variable"] = X.columns
    # vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    # print(vif)

    # 混合线性效应模型
    # 建立混合线性效应模型
    data = data_long[(data_long["Examtype"] == Examtype)]
    # print(data)
    md = smf.mixedlm("rt ~Target*NUM*ISI*TYPE", data, groups=data["name"])
    mdf = md.fit()
    # print(mdf.summary())
    data_res.append({"rt": mdf.summary()})
    # 查看模型结果
    # print(mdf.summary())
    # md = smf.mixedlm("rt ~ TYPE+ISI+NUM+Examtype", data_long, groups=data_long["name"])
    # mdf = md.fit()
    # # 查看模型结果
    # print(mdf.summary())
    md_correct = smf.mixedlm("correct ~ Target*NUM*ISI*TYPE", data, groups=data["name"])
    mdf = md_correct.fit()
    # 查看模型结果
    # print(mdf.summary())
    data_res.append({"correct": mdf.summary()})
    # md_correct = smf.mixedlm("correct ~ Target+NUM+Examtype+TYPE", data, groups=data["name"])
    # mdf = md_correct.fit()
    # # 查看模型结果
    # print(mdf.summary())
    return data_res


path5 = r"E:\数据汇总\实验三"
# param_testto(path5)


# 检测刺激数目的显著性
def param_test_num(scvpath, stimtype, ISI):
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选包含数字num的文件名
    selected_files = [f for f in csv_files if stimtype in f and ISI in f]  # 2,4,6
    recall_files = [f for f in selected_files if "recall" in f]
    recognition_files = [f for f in selected_files if "recognition" in f]
    # 创建一个空字典
    dfs_recall = {}
    dfs_recognition = {}
    for i, fs in enumerate([recall_files, recognition_files]):
        for f in fs:
            file_name, file_ext = os.path.splitext(f)
            num = re.findall(r"_(\d+)_\d+", file_name)[0]
            dt_rt, df = process_data(scvpath + "\\" + f)
            df = namefun(df)
            df["name"].fillna(method="ffill", inplace=True)
            if i == 0:
                dfs_recall[num] = df[
                    (df["answer"].notna()) & (df["answer"] != 5)
                ].reset_index(drop=True)
                dfs_recall[num] = dfs_recall[num].loc[:, ["name", "rt", "correct"]]
            else:
                dfs_recognition[num] = df[
                    (df["answer"].notna()) & (df["answer"] != 5)
                ].reset_index(drop=True)
                dfs_recognition[num] = dfs_recognition[num].loc[
                    :, ["name", "rt", "correct"]
                ]

    print(dfs_recall, dfs_recognition)
    for j in range(2):
        dfs = dfs_recall if j == 0 else dfs_recognition
        # 将原始数据集转换为长格式
        data_long = pd.concat([v.assign(key=k) for k, v in dfs.items()])
        data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
        print(data_long)
        data = pd.get_dummies(data_long, columns=["key"], drop_first=True)
        data_long["correct"] = data["correct"].replace({True: 1, False: 0})
        # # 进行重复测量方差分析
        # # 使用 np.mean 聚合函数对数据进行聚合
        # data_long_agg = data_long.groupby(['name', 'key'], as_index=False).agg({'log_rt': np.mean})
        # aov_rt = AnovaRM(data_long_agg, depvar='log_rt', subject='name', within=['key'])
        # result = aov_rt.fit()
        # print(result.summary())
        #
        # aov_correct = AnovaRM(data_long_agg, depvar='correct', subject='name', within=['key'])
        # result = aov_correct.fit()
        # print(result.summary())

        # tukey hsd
        mc = MultiComparison(data_long["rt"], data_long["key"])
        result = mc.tukeyhsd()
        print(result)
        # tukey hsd
        mc = MultiComparison(data_long["correct"], data_long["key"])
        result = mc.tukeyhsd()
        print(result)
        print(" ------------====------------  ")
        # 进行多重比较并使用Bonferroni校正
        comp = pairwise_tukeyhsd(data_long["rt"], data_long["key"])
        print(comp)
        comp_bonf = pairwise_tukeyhsd(data_long["rt"], data_long["key"], alpha=0.05 / 2)
        print(comp_bonf)
        comp = pairwise_tukeyhsd(data_long["correct"], data_long["key"])
        print(comp)
        comp_bonf = pairwise_tukeyhsd(
            data_long["correct"], data_long["key"], alpha=0.05 / 2
        )
        print(comp_bonf)

        # 混合线性效应模型
        # 建立混合线性效应模型
        md = smf.mixedlm("rt ~ key", data_long, groups=data["name"])
        mdf = md.fit()
        # 查看模型结果
        print(mdf.summary())

        md_correct = smf.mixedlm("correct ~ key", data_long, groups=data["name"])
        mdf = md_correct.fit()
        # 查看模型结果
        print(mdf.summary())


path2 = r"E:\数据汇总\实验一"


# param_test_num(path2, "color", "_500")


# 检测ISI的显著性
def param_test_ISI(scvpath, stimtype, num):
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选包含数字num的文件名
    selected_files = [
        f for f in csv_files if stimtype in f and num in f
    ]  # 500,1000,1500
    recall_files = [f for f in selected_files if "recall" in f]
    recognition_files = [f for f in selected_files if "recognition" in f]
    # 创建一个空字典
    dfs_recall = {}
    dfs_recognition = {}
    for i, fs in enumerate([recall_files, recognition_files]):
        for f in fs:
            file_name, file_ext = os.path.splitext(f)
            ISI = re.findall(r"_\d+_(\d+)", file_name)[0]
            dt_rt, df = process_data(scvpath + "\\" + f)
            df = namefun(df)
            df["name"].fillna(method="ffill", inplace=True)
            if i == 0:
                dfs_recall[ISI] = df[
                    (df["answer"].notna()) & (df["answer"] != 5)
                ].reset_index(drop=True)
                dfs_recall[ISI] = dfs_recall[ISI].loc[:, ["name", "rt", "correct"]]
            else:
                dfs_recognition[ISI] = df[
                    (df["answer"].notna()) & (df["answer"] != 5)
                ].reset_index(drop=True)
                dfs_recognition[ISI] = dfs_recognition[ISI].loc[
                    :, ["name", "rt", "correct"]
                ]

    print(dfs_recall, dfs_recognition)
    for j in range(2):
        dfs = dfs_recall if j == 0 else dfs_recognition
        # 将原始数据集转换为长格式
        data_long = pd.concat([v.assign(key=k) for k, v in dfs.items()])
        data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
        print(data_long)
        data = pd.get_dummies(data_long, columns=["key"], drop_first=True)
        data_long["correct"] = data["correct"].replace({True: 1, False: 0})

        # tukey hsd
        mc = MultiComparison(data_long["rt"], data_long["key"])
        result = mc.tukeyhsd()
        print(result)
        # tukey hsd
        mc = MultiComparison(data_long["correct"], data_long["key"])
        result = mc.tukeyhsd()
        print(result)
        print(" ------------====------------  ")
        # 进行多重比较并使用Bonferroni校正
        comp = pairwise_tukeyhsd(data_long["rt"], data_long["key"])
        print(comp)
        comp_bonf = pairwise_tukeyhsd(data_long["rt"], data_long["key"], alpha=0.05 / 2)
        print(comp_bonf)
        comp = pairwise_tukeyhsd(data_long["correct"], data_long["key"])
        print(comp)
        comp_bonf = pairwise_tukeyhsd(
            data_long["correct"], data_long["key"], alpha=0.05 / 2
        )
        print(comp_bonf)

        # 混合线性效应模型
        # 建立混合线性效应模型
        md = smf.mixedlm("rt ~ key", data_long, groups=data["name"])
        mdf = md.fit()
        # 查看模型结果
        print(mdf.summary())

        md_correct = smf.mixedlm("correct ~ key", data_long, groups=data["name"])
        mdf = md_correct.fit()
        # 查看模型结果
        print(mdf.summary())


path3 = r"E:\数据汇总\实验一"


# param_test_ISI(path3, "color", "2")


# 检测完整的显著性
def param_test(scvpath, Examtype):
    data = []
    files = os.listdir(scvpath)
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
    for i, fs in enumerate([recall_files, recognition_files]):
        for f in fs:
            file_name, file_ext = os.path.splitext(f)
            ISI = re.findall(r"_\d+_(\d+)", file_name)[0]
            num = re.findall(r"_(\d+)_\d+", file_name)[0]
            dt_rt, df = process_data(scvpath + "\\" + f)
            df = namefun(df)
            df["name"].fillna(method="ffill", inplace=True)
            if "shape" in file_name:
                if i == 0:
                    dfs_recall["shape"][num][ISI] = df[
                        (df["answer"].notna()) & (df["answer"] != 5)
                    ].reset_index(drop=True)
                    dfs_recall["shape"][num][ISI] = dfs_recall["shape"][num][ISI].loc[
                        :, ["name", "rt", "correct"]
                    ]
                else:
                    dfs_recognition["shape"][num][ISI] = df[
                        (df["answer"].notna()) & (df["answer"] != 5)
                    ].reset_index(drop=True)
                    dfs_recognition["shape"][num][ISI] = dfs_recognition["shape"][num][
                        ISI
                    ].loc[:, ["name", "rt", "correct"]]
            else:
                if i == 0:
                    dfs_recall["color"][num][ISI] = df[
                        (df["answer"].notna()) & (df["answer"] != 5)
                    ].reset_index(drop=True)
                    dfs_recall["color"][num][ISI] = dfs_recall["color"][num][ISI].loc[
                        :, ["name", "rt", "correct"]
                    ]
                else:
                    dfs_recognition["color"][num][ISI] = df[
                        (df["answer"].notna()) & (df["answer"] != 5)
                    ].reset_index(drop=True)
                    dfs_recognition["color"][num][ISI] = dfs_recognition["color"][num][
                        ISI
                    ].loc[:, ["name", "rt", "correct"]]
    # print(dfs_recall)
    # for j in range(2):
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
    data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
    # print(data_long)
    data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
    # print(data_long.info())
    # print(data_long.head())

    # # 检测共线性
    # variables = ['ISI', 'NUM', 'TYPE', 'Examtype']
    # mapping1 = {'recall': 1, 'recognition': 2}
    # mapping2 = {'shape': 1, 'color': 2}
    # mapping3 = {'500': 500, '1000': 1000, '1500': 1500}
    # mapping4 = {'2': 2, '4': 4, '6': 6}
    # X = data_long[variables]
    # X['TYPE'] = X['TYPE'].map(mapping2)
    # X['Examtype'] = X['Examtype'].map(mapping1)
    # X['NUM'] = X['NUM'].map(mapping4)
    # X['ISI'] = X['ISI'].map(mapping3)
    # print(X)
    # X = sm.add_constant(X)
    # vif = pd.DataFrame()
    # vif["Variable"] = X.columns
    # vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    # print(vif)

    # 混合线性效应模型
    # 建立混合线性效应模型
    data_long = data_long[(data_long["Examtype"] == Examtype)]
    md = smf.mixedlm("rt ~ ISI*NUM*TYPE", data_long, groups=data_long["name"])
    mdf = md.fit()
    data.append({"rt": mdf.summary()})
    # 查看模型结果
    # print(mdf.summary())
    # md = smf.mixedlm("rt ~ TYPE+ISI+NUM+Examtype", data_long, groups=data_long["name"])
    # mdf = md.fit()
    # # 查看模型结果
    # print(mdf.summary())

    md_correct = smf.mixedlm(
        "correct ~ ISI*NUM*TYPE", data_long, groups=data_long["name"]
    )
    mdf = md_correct.fit()
    data.append({"correct": mdf.summary()})
    # 查看模型结果
    # print(mdf.summary())
    # md_correct = smf.mixedlm("correct ~ TYPE+ISI+NUM+Examtype", data_long, groups=data_long["name"])
    # mdf = md_correct.fit()
    # # 查看模型结果
    # print("aaa", mdf.summary())
    return data


path4 = r"E:\数据汇总\实验一"


# param_test(path4, "recall")


# 参数检验
def param_test_detail(scvpath, num, stimtype):
    files = os.listdir(scvpath)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 筛选包含数字num的文件名
    selected_files = [f for f in csv_files if num in f and stimtype in f]
    recall_files = [f for f in selected_files if "recall" in f]
    recognition_files = [f for f in selected_files if "recognition" in f]
    dfs_recall = pd.DataFrame()
    dfs_recognition = pd.DataFrame()
    if stimtype == "shape":
        arr = arr_shape
    else:
        arr = arr_color
    for i, fs in enumerate([recall_files, recognition_files]):
        for f in fs:
            file_name, file_ext = os.path.splitext(f)
            # ISI = re.findall(r'_\d+_(\d+)', file_name)[0]
            dt_rt, df = process_data(scvpath + "\\" + f)
            df = namefun(df)
            print(arr[num])
            df["name"].fillna(method="ffill", inplace=True)
            # for j in range(len(arr[num])):
            if i == 0:
                dfs_recall = df[
                    (df["answer"].notna())
                    & (df["answer"] != 5)
                    & (df["target"].notna())
                ].reset_index(drop=True)
                dfs_recall = dfs_recall.loc[:, ["name", "target", "rt", "correct"]]
            else:
                dfs_recognition = df[
                    (df["answer"].notna())
                    & (df["answer"] != 5)
                    & (df["target"].notna())
                ].reset_index(drop=True)
                dfs_recognition = dfs_recognition.loc[
                    :, ["name", "target", "rt", "correct"]
                ]
    print(dfs_recall, dfs_recognition)
    for j in range(2):
        dfs = dfs_recall if j == 0 else dfs_recognition
        # 将原始数据集转换为长格式
        # for n, ISI in enumerate(["500", "1000", "1500"]):
        #     dfs[ISI] = pd.concat([v.assign(Target=k) for k, v in dfs[ISI].items()])
        # data_long = pd.concat([v.assign(Target=k) for k, v in dfs.items()])
        data_long = dfs
        data_long["log_rt"] = np.log(data_long["rt"])  # 对数变换
        # 将原始数据集转换为长格式
        data_long["correct"] = data_long["correct"].replace({True: 1, False: 0})
        print(data_long)
        # 混合线性效应模型
        # 建立混合线性效应模型
        md = smf.mixedlm("rt ~ target", data_long, groups=data_long["name"])
        mdf = md.fit()
        # 查看模型结果
        print(mdf.summary())

        md_correct = smf.mixedlm(
            "correct ~ target", data_long, groups=data_long["name"]
        )
        mdf = md_correct.fit()
        # 查看模型结果
        print(mdf.summary())


paths = r"E:\数据汇总\实验一"
# param_test_detail(paths, "2", "color")
