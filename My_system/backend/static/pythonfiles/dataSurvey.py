import json
import os
import textwrap
import io
import base64
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # 设置后端为Agg
from matplotlib import pyplot as plt


# data_b = pd.DataFrame(columns=["name", "response"])
# data_t = pd.DataFrame(columns=["name", "response"])
# path = r"E:/数据2/3"
# for file in os.listdir(path):
#     filepath = os.path.join(path, file)
#     df = pd.read_csv(filepath)
#     name = json.loads(df[df["trial_index"] == 1]["response"].values[0])
#     value1 = df[df["trial_index"] == 5]["response"]
#     value2 = df[df["trial_index"] == 7]["response"]
#     # 从data中选择name和response列并添加到data_b
#     data_b = pd.concat(
#         [data_b, pd.DataFrame({"name": [name["name"]], "response": value1[5]})],
#         ignore_index=True,
#     )
#     data_t = pd.concat(
#         [data_t, pd.DataFrame({"name": [name["name"]], "response": value2[7]})],
#         ignore_index=True,
#     )


def caculSum(data_df):
    responses = data_df["response"]
    all_response = [json.loads(response) for response in responses]
    all_values = [list(d.values()) for d in all_response]
    # print(all_values)
    # 计算每个子列表的总分
    totals = [sum(sublist) for sublist in all_values]
    # 计算总分的平均分
    average_score = sum(totals) / len(all_values)
    # print("总分平均分:", average_score)


# caculSum(data_b)
# caculSum(data_t)


def caculate(data_df):
    responses = data_df["response"]
    all_response = [json.loads(response) for response in responses]
    all_values = [list(d.values()) for d in all_response]

    # 计算每个键的平均值
    average_values = [
        sum(vals) / len(vals) for vals in zip(*all_values)
    ]  # zip(*矩阵的转置)
    # 创建包含键名和平均值的DataFrame
    key = [
        "网站的整体外观和布局：",
        "网站的颜色和图像选择：",
        "信息的呈现方式和清晰度：",
        "网站的导航菜单和链接的可见性和易用性：",
        "对网站的整体印象：",
        "是否愿意使用这个网站进行门票预定：",
    ]
    # key = ["Website's overall appearance and layout:",
    #        "Website's color and image selection:",
    #        "Presentation style and clarity of information:",
    #        "Visibility and usability of the website's navigation menu and links:",
    #        "Overall impression of the website:",
    #        "Willingness to use this website for ticket reservations:"]
    average_response_df = pd.DataFrame({"key": key, "average_value": average_values})
    # print(average_response_df)
    return average_response_df


def drawsurvey(d_b, d_t):
    average_response_df1 = caculate(d_b)
    average_response_df2 = caculate(d_t)
    y = average_response_df1["key"]
    x1 = average_response_df1["average_value"]
    x2 = average_response_df2["average_value"]
    # 绘制条形图
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]  # 用来正常显示中文标签SimHei
    plt.rcParams["axes.unicode_minus"] = (
        False  # 用来正常显示负号 #有中文出现的情况，需要u'内容'
    )
    ax.barh(
        y,
        x1,
        color="#0e606b",
        align="center",
        label="booking.com",
        height=0.6,
        alpha=0.7,
    )
    ax.barh(y, x2, color="#0e606b", align="center", label="tuniu.com", height=0.6)
    ax.set_xlabel("平均值", fontsize=13)
    ax.set_ylabel("问题", fontsize=13)
    ax.set_title("李克里量表平均值", fontsize=13)
    plt.xlim(2, 4)
    plt.xticks([2, 2.5, 3, 3.5, 4], fontsize=13)
    plt.yticks(y, fontsize=13)
    plt.gca().invert_yaxis()  # y轴逆序
    plt.subplots_adjust(left=0.25, right=0.95, top=0.8, bottom=0.1)
    # 自动换行并设置宽度
    wrap_width = 9  # 设置标签的宽度
    wrapped_labels = [textwrap.fill(label, wrap_width) for label in y]
    plt.yticks(y, wrapped_labels, ha="left")
    yax = ax.get_yaxis()
    pad = max(T.label.get_window_extent().width for T in yax.majorTicks)
    yax.set_tick_params(pad=pad - 30)
    plt.legend(fontsize=13)
    plt.tight_layout()  # 解决Y轴显示不完全的问题
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    res = base64.b64encode(buffer.read()).decode("utf-8")
    return res


# drawsurvey()
