import json
import os
import re

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro


# recall
def dfSave(df_save, new_df, new_df1):
    nrows_before = new_df.shape[0]
    # 使用布尔索引选择符合条件的行
    # 删除rt为空的这些行
    index_names = new_df1[(new_df1["rt"].isna())].index
    new_df.drop(index_names, axis=0, inplace=True)
    new_df1.drop(index_names, axis=0, inplace=True)
    # 1、响应时间小于100ms 2、超出3s的响应时间范围的
    # 将 "NaN" 替换为 np.nan
    new_df1["rt"] = new_df1["rt"].replace("NaN", np.nan)
    # 将数据转换为 int 类型
    new_df1["rt"] = new_df1["rt"].astype(int)
    index_names = new_df1[
        (new_df1["rt"] <= 100)
        | (new_df1["stimulus"].notna() & new_df1["response"].isna())
    ].index
    # 删除这些行
    new_df.drop(index_names, axis=0, inplace=True)
    new_df1.drop(index_names, axis=0, inplace=True)
    nrows_after = new_df.shape[0]
    # 计算删除的行数
    delete_rows = nrows_before - nrows_after

    # 将需要的数据整合并保存至新的csv文件
    df_save = pd.concat(
        [
            df_save,
            pd.DataFrame(
                {
                    "rt": new_df1.loc[:, "rt"],
                    "response": new_df1.loc[:, "response"],
                    "answer": new_df1.loc[:, "response_answer"],
                    "stimulus": new_df.loc[:, "stimulus"],
                    "target": new_df1.loc[:, "response_target"],
                    "correct": new_df1.loc[:, "correct"],
                    "webgazer_data": new_df.loc[:, "webgazer_data"],
                    "webgazer_targets_data": new_df.loc[:, "webgazer_targets_data"],
                    "canvas_data": new_df.loc[:, "webgazer_targets"],
                }
            ),
        ],
        ignore_index=True,
    )
    return df_save


# recognition
def dfSave1(df_save, new_df):
    nrows_before = new_df.shape[0]
    # 使用布尔索引选择符合条件的行
    # 删除rt为空的这些行
    index_names = new_df[(new_df["rt"].isna())].index
    new_df.drop(index_names, axis=0, inplace=True)
    # 1、响应时间小于100ms 2、超出3s的响应时间范围的
    # 将 "NaN" 替换为 np.nan
    new_df["rt"] = new_df["rt"].replace("NaN", np.nan)
    # 将数据转换为 int 类型
    new_df["rt"] = new_df["rt"].astype(int)
    index_names = new_df[
        (new_df["rt"] <= 100) | (new_df["stimulus"].notna() & new_df["response"].isna())
    ].index
    # 删除这些行
    new_df.drop(index_names, axis=0, inplace=True)
    nrows_after = new_df.shape[0]
    # 计算删除的行数
    delete_rows = nrows_before - nrows_after

    # 将需要的数据整合并保存至新的csv文件
    df_save = pd.concat(
        [
            df_save,
            pd.DataFrame(
                {
                    "rt": new_df.loc[:, "rt"],
                    "response": new_df.loc[:, "response"],
                    "answer": new_df.loc[:, "response_answer"],
                    "stimulus": new_df.loc[:, "stimulus"],
                    "target": new_df.loc[:, "target"],
                    "correct": new_df.loc[:, "correct"],
                    "webgazer_data": new_df.loc[:, "webgazer_data"],
                    "webgazer_targets_data": new_df.loc[:, "webgazer_targets_data"],
                    "canvas_data": new_df.loc[:, "webgazer_targets"],
                }
            ),
        ],
        ignore_index=True,
    )
    return df_save


def merge_non_nan(x):
    unique_values = x.unique()
    non_nan_values = [str(val) for val in unique_values if pd.notnull(val)]
    return ", ".join(non_nan_values)


# 处理newdf
def processdf(new_df):
    # 按照每四行进行分组
    grouped_df = new_df.groupby(new_df.index // 4)
    # 对每个分组应用聚合函数，将相同列的数据合并
    merged_df = grouped_df.agg(merge_non_nan)
    # 重置索引
    merged_df.reset_index(drop=True, inplace=True)
    # print(merged_df)
    return merged_df


def processdf2(new_df1, new_df):
    global result
    if new_df1.shape[0] == new_df.shape[0]:
        for index, row in new_df1.iterrows():
            if row["motion"] == 1.0 and row["topo"] == 0.0:
                s = json.loads(new_df.loc[index, "stimulus"])
                # 判断数列中的值是否包含指定字符串
                for elem in s:
                    if "_1" in elem:
                        result = "single"
                        break
                    elif "_2" in elem:
                        result = "double"
                        break
                    else:
                        result = ""
                new_df1.loc[index, "tchange"] = result
            if row["motion"] == 0.0 and row["topo"] == 1.0:
                target = row["response_target"]
                if "_1" in target:
                    result = "single"
                elif "_2" in target:
                    result = "double"
                new_df1.loc[index, "tchange"] = result
    # print(new_df1)
    return new_df1


def processdf3(new_df1, new_df):
    global result
    if new_df1.shape[0] == new_df.shape[0]:
        for index, row in new_df1.iterrows():
            if row["motion"] == 1.0 and row["topo"] == 0.0:
                new_df1.loc[index, "tchange"] = ""
            if row["motion"] == 0.0 and row["topo"] == 1.0:
                target = row["response_target"]
                if "_1" in target:
                    result = "single"
                    new_df1.loc[index, "T"] = 1
                elif "_2" in target:
                    result = "double"
                    new_df1.loc[index, "T"] = 1
                else:
                    result = ""
                    new_df1.loc[index, "T"] = 0
                new_df1.loc[index, "tchange"] = result
                new_df1.loc[index, "mchange"] = ""
    # print(new_df1)
    return new_df1


# dynamic
def dfSave2(df_save, new_df, new_df1):
    nrows_before = new_df1.shape[0]
    new_df = processdf(new_df)
    new_df1 = processdf2(new_df1, new_df)
    # 使用布尔索引选择符合条件的行
    # 删除rt为空的这些行
    index_names = new_df1[(new_df1["rt"].isna())].index
    new_df1.drop(index_names, axis=0, inplace=True)
    new_df.drop(index_names, axis=0, inplace=True)

    # 1、响应时间小于100ms 2、超出3s的响应时间范围的
    # 将 "NaN" 替换为 np.nan
    new_df1["rt"] = new_df1["rt"].replace("NaN", np.nan)
    # 将数据转换为 int 类型
    new_df1["rt"] = new_df1["rt"].astype(int)
    index_names = new_df1[
        (new_df1["rt"] <= 100)
        | (new_df1["stimulus"].notna() & new_df1["response"].isna())
    ].index
    # 删除这些行
    new_df.drop(index_names, axis=0, inplace=True)
    new_df1.drop(index_names, axis=0, inplace=True)
    nrows_after = new_df.shape[0]
    # 计算删除的行数
    delete_rows = nrows_before - nrows_after

    # 将需要的数据整合并保存至新的csv文件
    df_save = pd.concat(
        [
            df_save,
            pd.DataFrame(
                {
                    "rt": new_df1.loc[:, "rt"],
                    "response": new_df1.loc[:, "response"],
                    "answer": new_df1.loc[:, "response_answer"],
                    "stimulus": new_df.loc[:, "stimulus"],
                    "target": new_df1.loc[:, "response_target"],
                    "correct": new_df1.loc[:, "correct"],
                    "webgazer_data": new_df.loc[:, "webgazer_data"],
                    "webgazer_targets_data": new_df.loc[:, "webgazer_targets_data"],
                    "canvas_data": new_df.loc[:, "webgazer_targets"],
                    "motion": new_df1.loc[:, "motion"],
                    "topo": new_df1.loc[:, "topo"],
                    "mchange": new_df1.loc[:, "mchange"],
                    "tchange": new_df1.loc[:, "tchange"],
                }
            ),
        ],
        ignore_index=True,
    )
    return df_save


def dfSave3(df_save, new_df, new_df1):
    nrows_before = new_df1.shape[0]
    new_df = processdf(new_df)
    new_df1 = processdf3(new_df1, new_df)
    # 使用布尔索引选择符合条件的行
    # 删除rt为空的这些行
    index_names = new_df1[(new_df1["rt"].isna())].index
    new_df1.drop(index_names, axis=0, inplace=True)
    new_df.drop(index_names, axis=0, inplace=True)

    # 1、响应时间小于100ms 2、超出3s的响应时间范围的
    # 将 "NaN" 替换为 np.nan
    new_df1["rt"] = new_df1["rt"].replace("NaN", np.nan)
    # 将数据转换为 int 类型
    new_df1["rt"] = new_df1["rt"].astype(int)
    index_names = new_df1[
        (new_df1["rt"] <= 100)
        | (new_df1["stimulus"].notna() & new_df1["response"].isna())
    ].index
    # 删除这些行
    new_df.drop(index_names, axis=0, inplace=True)
    new_df1.drop(index_names, axis=0, inplace=True)
    nrows_after = new_df.shape[0]
    # 计算删除的行数
    delete_rows = nrows_before - nrows_after
    merged_df = new_df1.combine_first(new_df)
    # print(merged_df)
    merged_df = merged_df[(merged_df["motion"] == 0.0) & (merged_df["topo"] == 1.0)]

    # 将需要的数据整合并保存至新的csv文件
    df_save = pd.concat(
        [
            df_save,
            pd.DataFrame(
                {
                    "rt": merged_df.loc[:, "rt"],
                    "response": merged_df.loc[:, "response"],
                    "answer": merged_df.loc[:, "response_answer"],
                    "stimulus": merged_df.loc[:, "stimulus"],
                    "target": merged_df.loc[:, "response_target"],
                    "correct": merged_df.loc[:, "correct"],
                    "webgazer_data": merged_df.loc[:, "webgazer_data"],
                    "webgazer_targets_data": merged_df.loc[:, "webgazer_targets_data"],
                    "canvas_data": merged_df.loc[:, "webgazer_targets"],
                    "motion": merged_df.loc[:, "motion"],
                    "topo": merged_df.loc[:, "topo"],
                    "mchange": merged_df.loc[:, "mchange"],
                    "tchange": merged_df.loc[:, "tchange"],
                    "T": merged_df.loc[:, "T"],
                }
            ),
        ],
        ignore_index=True,
    )
    return df_save


# 定义预处理函数
def preprocess_value(s):
    if isinstance(s, float):
        return s  # 如果是 float 类型，直接返回原值
    elif isinstance(s, str) and s.endswith("_1"):
        return s[:-2]  # 去掉 '_1'
    elif isinstance(s, str) and s.endswith("_2"):
        return s[:-2]  # 去掉 '_2'
    else:
        return s  # 不需要处理的值，直接返回原值


# 进一步处理异常值(单个文件)
def process_data(path):
    # 获取文件名和后缀
    file_name, file_ext = os.path.splitext(os.path.basename(path))
    # 读取文件
    df = pd.read_csv(path, encoding="utf-8", engine="python", on_bad_lines="warn")
    # print(df)
    # 获取样本数量，以样本名作为标签
    df_name = df[df["name"].notna()].loc[:, "name"].tolist()
    # print(df_name)
    # 为相同样本名的值后面添加后缀
    count_dict = {}
    name_result = []
    for item in df_name:
        if item in count_dict:
            count_dict[item] += 1
            name_result.append(str(item) + "_" + str(count_dict[item]))
        else:
            count_dict[item] = 0
            name_result.append(str(item) + "_0")
    # print(name_result)
    # 根据姓名提取对应的"rt"列
    dt_rt = pd.DataFrame()
    # 获取两个样本名对应行之间的rt
    for i in range(len(name_result) - 1):
        name, name_index = name_result[i].split("_")
        name1, name_index1 = name_result[i + 1].split("_")
        row_index0 = df.loc[df["name"] == name].index[int(name_index)]
        row_index1 = df.loc[df["name"] == name1].index[int(name_index1)]
        # print(row_index0, row_index1)
        # 将对应的“rt”列单独提取，以样本名作为列名，生成一个新的dt
        new_col = pd.Series(
            df.loc[row_index0 + 1 : row_index1 - 1, "rt"].tolist(), dtype="float64"
        )
        dt_rt.insert(i, name_result[i], new_col)
    # 将最后一个样本的rt写入dt_rt
    name, name_index = name_result[len(df_name) - 1].split("_")
    row_index0 = df.loc[df["name"] == name].index[int(name_index)]
    new_col = pd.Series(df.loc[row_index0 + 1 :, "rt"].tolist(), dtype="float64")
    dt_rt.insert(len(df_name) - 1, name_result[len(df_name) - 1], new_col)
    # print(df)

    # 计算异常值，前三行若存在异常值，则将其删除，其原因可能是未能及时反应实验要求造成的
    for col in dt_rt.columns:
        # 计算每一列的上下四分位数，得出dt_rt中异常值的行
        q1, q3 = np.percentile(dt_rt[col].dropna(), [25, 75])
        outliers = dt_rt[
            (dt_rt[col] < q1 - 1.5 * (q3 - q1)) | (dt_rt[col] > q3 + 1.5 * (q3 - q1))
        ][col]
        # 异常值不为空时
        if len(outliers) > 0:
            # print(f"Column {col} has {len(outliers)} outliers:\n{outliers}")
            for i in range(len(outliers)):
                if 0 <= outliers.index[i] <= 2:
                    # 将dt_rt中的异常值置为nan
                    dt_rt.loc[outliers.index[i], col] = np.nan
                    # 从df中删除异常值所对应的行
                    name, name_index = col.split("_")
                    row = (
                        df.loc[df["name"] == name].index[int(name_index)]
                        + outliers.index[i]
                        + 1
                    )
                    df.drop(row, axis=0, inplace=True)
                    # print(df.loc[df.loc[df['name'] == name].index[int(name_index)]:, "rt"])
    return dt_rt, df


def namefun(df):
    name_col = df[df["name"].notna()]
    # 初始化一个计数器
    counter = {}
    # 遍历 name_col 中的每个值
    for i, val in enumerate(name_col["name"]):
        index = df[df["name"] == val].index[0]
        # print(index)
        # 如果当前值是一个新值，则将其加入计数器
        if val not in counter:
            counter[val] = 0
        else:
            # 将计数器值加 1
            counter[val] += 1
        # 在 name_col 中将当前位置的值替换成 "原始值_计数器值"
        df.loc[index, "name"] = str(val) + "_" + str(counter[val])
    # print(df[df['name'].notna()])
    return df


# 绘制箱线图
def drawboxplot(dt, df, file_name):
    # 计算均值和标准差
    mean = dt.mean()
    std = dt.std()
    # 图1
    # 创建子图，共享x轴，y轴
    fig, axs = plt.subplots(ncols=dt.shape[1], figsize=(8, 6), sharey=True, sharex=True)
    # 显示均值和标准差
    for i, col in enumerate(dt.columns):
        # 判断样本是否符合正态分布
        data = dt[col].dropna().to_numpy()
        # 进行Shapiro-Wilk检验
        stat, p = shapiro(data)
        # 输出检验结果
        print("Shapiro-Wilk Test:")
        print(f"Statistics = {stat:.3f}, p-value = {p:.3f}")
        if p > 0.05:
            print(col + "样本数据符合正态分布")
        else:
            print(col + "样本数据不符合正态分布")

        # 绘制箱线图
        sns.boxplot(data=dt[col], ax=axs[i], color="white")
        # 添加均值和方差
        axs[i].axhline(mean[i], color="r", linestyle="--")
        axs[i].axhspan(mean[i] - std[i], mean[i] + std[i], facecolor="r", alpha=0.2)
        # 设置x轴标签，字体为黑体
        axs[i].set_xlabel(col, fontname="SimHei", fontsize=10)
    # 设置y轴标签
    axs[0].set_ylabel("rt")
    # 调整布局
    plt.tight_layout()
    fig.suptitle(file_name)
    plt.show()

    # 判断样本整体是否符合正态分布
    # 忽略空值，将列数据提取出来并转换为numpy数组
    data = df["rt"].dropna().to_numpy()
    # 进行Shapiro-Wilk检验
    stat, p = shapiro(data)
    # 输出检验结果
    print("Shapiro-Wilk Test:")
    print(f"Statistics = {stat:.3f}, p-value = {p:.3f}")
    if p > 0.05:
        print("样本数据符合正态分布")
    else:
        print("样本数据不符合正态分布")
    return mean, std


def drawSumboxplot(df, df_col_mean, df_col_std, type0, type, path_all, num):
    path = path_all + "\\汇总\\" + type + "_" + type0 + "_" + num + ".png"
    # 创建子图，共享x轴，y轴
    fig, axs = plt.subplots(ncols=3, figsize=(8, 6), sharey=True)
    for i in range(len(df_col_mean)):
        mean = df[df_col_mean[i]].iloc[-1]
        std = df[df_col_std[i]].iloc[-1]
        # 处理列名
        last_underscore_index = df_col_mean[i].rfind("_")
        result = df_col_mean[i][:last_underscore_index]
        # 绘制箱线图
        sns.boxplot(data=df[df_col_mean[i]].iloc[:-1], ax=axs[i], color="white")
        # 添加均值和方差
        axs[i].axhline(mean, color="r", linestyle="--")
        axs[i].axhspan(mean - std, mean + std, facecolor="r", alpha=0.2)
        # 设置x轴标签，字体为黑体
        axs[i].set_xlabel(result, fontname="SimHei", fontsize=10)
    # 设置y轴标签
    axs[0].set_ylabel("rt")
    # 调整布局
    plt.tight_layout()
    plt.xlabel(re.sub(r"(_[^_]+){2}$", "", df_col_mean[1]))
    plt.show()
    plt.savefig(path)


def drawSumplot(df, shape_cols, color_cols, num, type, lable, path_all):
    path = path_all + "\\汇总\\" + type + "_plot_" + num + "_" + lable + ".png"
    last_row = df.iloc[-1, :]
    col = [
        type + "_" + num + "_500",
        type + "_" + num + "_1000",
        type + "_" + num + "_1500",
    ]
    # 绘制折线图
    # 创建一个新的图形对象
    fig = plt.figure()
    plt.plot(col, last_row[shape_cols], label="Shape")
    plt.plot(col, last_row[color_cols], label="Color")
    # 设置图例和横坐标标签
    plt.legend()
    plt.ylabel(lable)
    plt.xlabel(type + "_" + num + "_" + lable)
    # 显示图形
    plt.show()
    plt.savefig(path)
