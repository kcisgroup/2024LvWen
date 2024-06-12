# coding=utf-8
import os
import pandas as pd
import json

from static.pythonfiles.datafunc import preprocess_value, dfSave1

types = ["shape", "color"]
exam_type = ["recognition", "recall"]
arr_shape = ["rect", "triangle", "circle", "star", "hexagram", "diamond"]
arr_color = ["green", "yellow", "blue", "purple", "red", "cyan"]


def datapro_recognition(ISI, SIZE, PATH, PATH_SAVE):
    path = PATH
    path_save = PATH_SAVE
    path_participant = r"E:\实验人员.csv"
    name_response = {}
    df_save_shape = pd.DataFrame()
    df_save_color = pd.DataFrame()
    files = os.listdir(path)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    # 打开实验人员CSV文件并读取数据
    df_names = pd.read_csv(
        path_participant, encoding="utf-8", engine="python", on_bad_lines="warn"
    )

    for f in csv_files:
        df = pd.read_csv(
            path + "\\" + f, encoding="utf-8", engine="python", on_bad_lines="warn"
        )
        # 将实验人员信息提取出来
        name_response.update(json.loads(df["response"][2]))
        name_response.update(json.loads(df["response"][3]))
        name_response_df = pd.DataFrame([name_response], index=["index_name"])

        # 将人员信息写入,去除重复行
        df_names = pd.concat(
            [df_names, name_response_df], ignore_index=True
        ).drop_duplicates()
        df_names.to_csv(path_participant, index=False)

        # 将 NaN 值替换为字符串 "NaN"
        df["target"] = df["target"].fillna("NaN")
        # 使用 apply 方法对列 'target' 的值进行预处理
        processed_series = df["target"].apply(preprocess_value)
        # 替换字符串 "ring" 为 "circle"
        processed_series = processed_series.str.replace("ring", "circle")

        # 查找shape和color的起始行
        if not df[processed_series.isin(arr_shape)].empty:
            shape_index_0 = df[processed_series.isin(arr_shape)].index[0]
            shape_index_1 = df[processed_series.isin(arr_shape)].index[-1]
        else:
            shape_index_0 = None
            shape_index_1 = None
        # color不需要处理
        if not df["target"][df["target"].isin(arr_color)].empty:
            color_index_0 = df["target"][df["target"].isin(arr_color)].index[0]
            color_index_1 = df["target"][df["target"].isin(arr_color)].index[-1]
        else:
            color_index_0 = None
            color_index_1 = None

        if (shape_index_0 is not None) & (color_index_0 is not None):
            print(shape_index_0, shape_index_1, color_index_0, color_index_1)
            # 创建布尔掩码，获取“webgazer_data”列非空的行，并重新排序
            new_df_shape = (
                df[(df["webgazer_data"].notna())]
                .loc[shape_index_0:shape_index_1]
                .reset_index(drop=True)
            )
            new_df_color = (
                df[(df["webgazer_data"].notna())]
                .loc[color_index_0:color_index_1]
                .reset_index(drop=True)
            )
            print(name_response_df)
            # shape
            df_save_shape = pd.concat(
                [df_save_shape, name_response_df], ignore_index=True
            )
            df_save_shape = dfSave1(df_save_shape, new_df_shape)
            # color
            df_save_color = pd.concat(
                [df_save_color, name_response_df], ignore_index=True
            )
            df_save_color = dfSave1(df_save_color, new_df_color)
        elif (shape_index_0 is not None) & (color_index_0 is None):
            print(shape_index_0, shape_index_1)
            # 创建布尔掩码，获取“webgazer_data”列非空的行
            new_df_shape = (
                df[df["webgazer_data"].notna()]
                .loc[shape_index_0:shape_index_1]
                .reset_index(drop=True)
            )
            print(name_response_df)
            df_save_shape = pd.concat(
                [df_save_shape, name_response_df], ignore_index=True
            )
            df_save_shape = dfSave1(df_save_shape, new_df_shape)
        elif (shape_index_0 is None) & (color_index_0 is not None):
            print(color_index_0, color_index_1)
            # 创建布尔掩码，获取“webgazer_data”列非空的行
            new_df_color = (
                df[df["webgazer_data"].notna()]
                .loc[color_index_0:color_index_1]
                .reset_index(drop=True)
            )
            print(name_response_df)
            df_save_color = pd.concat(
                [df_save_color, name_response_df], ignore_index=True
            )
            df_save_color = dfSave1(df_save_color, new_df_color)
    df_save_shape.to_csv(
        path_save
        + "\\"
        + exam_type[0]
        + "_"
        + types[0]
        + "_"
        + SIZE
        + "_"
        + ISI
        + ".csv",
        index=False,
        encoding="utf-8",
    )
    df_save_color.to_csv(
        path_save
        + "\\"
        + exam_type[0]
        + "_"
        + types[1]
        + "_"
        + SIZE
        + "_"
        + ISI
        + ".csv",
        index=False,
        encoding="utf-8",
    )
