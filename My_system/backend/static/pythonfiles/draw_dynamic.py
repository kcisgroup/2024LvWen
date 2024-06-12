import pandas as pd
from matplotlib import pyplot as plt
import os
import io
import base64


def draw_dynamic1(scvpath, Factor):
    # 动态汇总
    data = pd.read_csv(
        scvpath + "/data.csv", encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    # 获取上一级路径
    parent_path = os.path.dirname(scvpath)  # 动态
    parent_path = os.path.dirname(parent_path)  # process
    # 进入上一级路径的预实验文件夹
    pre_experiment_folder = os.path.join(parent_path, "静态")  # process/静态
    # 进入 "汇总文件夹"
    summary_folder = os.path.join(pre_experiment_folder, "汇总")  # process/静态/汇总
    data_topo1 = pd.read_csv(
        summary_folder + "/data2.csv",
        encoding="utf-8",
        engine="python",
        on_bad_lines="warn",
    )
    parent_path = os.path.dirname(summary_folder)  # process/静态
    summary_folder = os.path.join(parent_path, "pro")  # process/静态/汇总
    summary_folder = os.path.join(summary_folder, "汇总")  # process/静态/汇总
    data_topo_E1 = pd.read_csv(
        summary_folder + "/data3.csv",
        encoding="utf-8",
        engine="python",
        on_bad_lines="warn",
    )
    fig, ax = plt.subplots()
    fig1, ax1 = plt.subplots()
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.xticks(fontname="Times New Roman")
    plt.yticks(fontname="Times New Roman")
    col = ["S_topo", "S_topo_E", "D_topo", "D_motion", "D_NTNM"]
    colors = ["#f66f69", "#1597a5", "#0e606b", "#ffc24b", "#81b8df"]
    for j, type in enumerate(["shape", "color"]):
        df = data[data["TYPE"] == type]
        data_topo2 = data_topo1[data_topo1["TYPE"] == type]
        data_topo_E2 = data_topo_E1[data_topo_E1["TYPE"] == type]
        for i, num in enumerate([2, 4, 6]):
            df_rt = pd.DataFrame()
            df_accuracy = pd.DataFrame()
            dfs = df[df["NUM"] == num]
            data_topo = data_topo2[
                (data_topo2["NUM"] == num)
                & (data_topo2["ISI"] == 1000)
                & (data_topo2["Examtype"] == "recall")
            ]
            data_topo_E = data_topo_E2[
                (data_topo_E2["NUM"] == num)
                & (data_topo_E2["ISI"] == 1000)
                & (data_topo_E2["Examtype"] == "recall")
            ]

            # 静态
            df_rt.insert(
                df_rt.shape[1],
                "S_topo",
                pd.Series(data_topo[(data_topo["Target"] == "topo")]["rt"].mean()),
            )
            df_rt.insert(
                df_rt.shape[1],
                "S_topo_E",
                pd.Series(data_topo_E[(data_topo_E["Target"] == "topo")]["rt"].mean()),
            )
            df_accuracy.insert(
                df_accuracy.shape[1],
                "S_topo",
                pd.Series(
                    (data_topo[(data_topo["Target"] == "topo")]["correct"] == 1).sum()
                    / data_topo[(data_topo["Target"] == "topo")]["correct"]
                    .notnull()
                    .sum()
                ),
            )
            df_accuracy.insert(
                df_accuracy.shape[1],
                "S_topo_E",
                pd.Series(
                    (
                        data_topo_E[(data_topo_E["Target"] == "topo")]["correct"] == 1
                    ).sum()
                    / data_topo_E[(data_topo_E["Target"] == "topo")]["correct"]
                    .notnull()
                    .sum()
                ),
            )
            # 动态
            df_rt.insert(
                df_rt.shape[1],
                "D_topo",
                pd.Series(dfs[dfs["Target"] == "topo"]["rt"].mean()),
            )
            df_rt.insert(
                df_rt.shape[1],
                "D_motion",
                pd.Series(dfs[dfs["Target"] == "motion"]["rt"].mean()),
            )
            # 处理准确率
            df_accuracy.insert(
                df_accuracy.shape[1],
                "D_topo",
                pd.Series(
                    (dfs[dfs["Target"] == "topo"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "topo"]["correct"].notnull().sum()
                ),
            )
            df_accuracy.insert(
                df_accuracy.shape[1],
                "D_motion",
                pd.Series(
                    (dfs[dfs["Target"] == "motion"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "motion"]["correct"].notnull().sum()
                ),
            )
            if num != 2:
                df_rt.insert(
                    df_rt.shape[1],
                    "D_NTNM",
                    pd.Series(dfs[dfs["Target"] == "none"]["rt"].mean()),
                )
                # 处理准确率
                df_accuracy.insert(
                    df_accuracy.shape[1],
                    "D_NTNM",
                    pd.Series(
                        (dfs[dfs["Target"] == "none"]["correct"] == True).sum()
                        / dfs[dfs["Target"] == "none"]["correct"].notnull().sum()
                    ),
                )
            # print(df_rt)

            if num == 2:
                ax.plot(
                    [1, 2, 3, 4],
                    df_rt.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
                ax1.plot(
                    [1, 2, 3, 4],
                    df_accuracy.values[0],
                    marker=f"{'v' if j == 0 else 'o' }",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
            else:
                ax.plot(
                    [1, 2, 3, 4, 5],
                    df_rt.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
                ax1.plot(
                    [1, 2, 3, 4, 5],
                    df_accuracy.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
    if Factor == "rt":
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(col)
        lines, labels = ax.get_legend_handles_labels()
        ax.set_title("RT", fontname="Times New Roman")
        ax.legend(lines, labels)
        # plt.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=1000)
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode("utf-8")
    elif Factor == "accuracy":
        ax1.set_xticks([1, 2, 3, 4, 5])
        ax1.set_xticklabels(col)
        lines, labels = ax1.get_legend_handles_labels()
        ax1.set_title("Accuracy", fontname="Times New Roman")
        ax1.legend(lines, labels)
        # plt.tight_layout()
        buffer = io.BytesIO()
        fig1.savefig(buffer, format="png", dpi=1000)
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode("utf-8")

    # # plt.savefig(r'E:\数据汇总\dynamic\汇总\\' + 'Accuracy_compare_data.svg',
    # #             format='svg')
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\动态F\\" + "RT_compare_data.jpg",
    #     format="jpg",
    #     dpi=1000,
    # )

    # plt.show()
    return image_data


scvpath1 = r"E:\数据汇总\dynamic\\汇总\\data.csv"
# draw_dynamic1(scvpath1)


# 全部进行对比
def draw_dynamic2(urlpath1, urlpath2, urlpath3, urlpath4, urlpath5):
    res = []
    data1 = pd.read_csv(
        urlpath5, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data = pd.read_csv(urlpath3, encoding="utf-8", engine="python", on_bad_lines="warn")
    data_E = pd.read_csv(
        urlpath4,
        encoding="utf-8",
        engine="python",
        on_bad_lines="warn",
    )
    data_topo1 = pd.read_csv(
        urlpath1, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    data_topo_E1 = pd.read_csv(
        urlpath2, encoding="utf-8", engine="python", on_bad_lines="warn"
    )
    fig, ax = plt.subplots()
    fig1, ax1 = plt.subplots()
    col = [
        "S_pre",
        "S_topo",
        "S_topo_E",
        "D_topo",
        "D_motion",
        "D_NTNM",
        "D_topo_E",
        "D_motion_E",
    ]
    colors = ["#f66f69", "#1597a5", "#0e606b", "#ffc24b", "#81b8df"]
    for j, type in enumerate(["shape", "color"]):
        df_pre = data1[data1["TYPE"] == type]
        df = data[data["TYPE"] == type]
        df1 = data_E[(data_E["TYPE"] == type) & (data_E["T"] == 1)]
        data_topo2 = data_topo1[data_topo1["TYPE"] == type]
        data_topo_E2 = data_topo_E1[data_topo_E1["TYPE"] == type]
        for i, num in enumerate([2, 4, 6]):
            df_pres = df_pre[
                (df_pre["NUM"] == num)
                & (df_pre["ISI"] == 1000)
                & (df_pre["Examtype"] == "recall")
            ]
            df_rt = pd.DataFrame()
            df_accuracy = pd.DataFrame()
            dfs = df[df["NUM"] == num]
            data_topo = data_topo2[
                (data_topo2["NUM"] == num)
                & (data_topo2["ISI"] == 1000)
                & (data_topo2["Examtype"] == "recall")
            ]
            data_topo_E = data_topo_E2[
                (data_topo_E2["NUM"] == num)
                & (data_topo_E2["ISI"] == 1000)
                & (data_topo_E2["Examtype"] == "recall")
            ]

            # 静态
            df_rt.insert(df_rt.shape[1], "S_pre", pd.Series(df_pres["rt"].mean()))
            df_rt.insert(
                df_rt.shape[1],
                "S_topo",
                pd.Series(data_topo[(data_topo["Target"] == "topo")]["rt"].mean()),
            )
            df_rt.insert(
                df_rt.shape[1],
                "S_topo_E",
                pd.Series(data_topo_E[(data_topo_E["Target"] == "topo")]["rt"].mean()),
            )
            df_accuracy.insert(
                df_accuracy.shape[1],
                "S_pre",
                pd.Series(
                    (df_pres["correct"] == 1).sum() / df_pres["correct"].notnull().sum()
                ),
            )
            df_accuracy.insert(
                df_accuracy.shape[1],
                "S_topo",
                pd.Series(
                    (data_topo[(data_topo["Target"] == "topo")]["correct"] == 1).sum()
                    / data_topo[(data_topo["Target"] == "topo")]["correct"]
                    .notnull()
                    .sum()
                ),
            )
            df_accuracy.insert(
                df_accuracy.shape[1],
                "S_topo_E",
                pd.Series(
                    (
                        data_topo_E[(data_topo_E["Target"] == "topo")]["correct"] == 1
                    ).sum()
                    / data_topo_E[(data_topo_E["Target"] == "topo")]["correct"]
                    .notnull()
                    .sum()
                ),
            )
            # 动态
            df_rt.insert(
                df_rt.shape[1],
                "D_topo",
                pd.Series(dfs[dfs["Target"] == "topo"]["rt"].mean()),
            )
            df_rt.insert(
                df_rt.shape[1],
                "D_motion",
                pd.Series(dfs[dfs["Target"] == "motion"]["rt"].mean()),
            )
            # 处理准确率
            df_accuracy.insert(
                df_accuracy.shape[1],
                "D_topo",
                pd.Series(
                    (dfs[dfs["Target"] == "topo"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "topo"]["correct"].notnull().sum()
                ),
            )
            df_accuracy.insert(
                df_accuracy.shape[1],
                "D_motion",
                pd.Series(
                    (dfs[dfs["Target"] == "motion"]["correct"] == True).sum()
                    / dfs[dfs["Target"] == "motion"]["correct"].notnull().sum()
                ),
            )
            if num != 2:
                df_rt.insert(
                    df_rt.shape[1],
                    "D_NTNM",
                    pd.Series(dfs[dfs["Target"] == "none"]["rt"].mean()),
                )
                # 处理准确率
                df_accuracy.insert(
                    df_accuracy.shape[1],
                    "D_NTNM",
                    pd.Series(
                        (dfs[dfs["Target"] == "none"]["correct"] == True).sum()
                        / dfs[dfs["Target"] == "none"]["correct"].notnull().sum()
                    ),
                )
                if num == 4:
                    df_rt.insert(
                        df_rt.shape[1],
                        "D_topo_E",
                        pd.Series(df1[df1["Target"] == "topo"]["rt"].mean()),
                    )
                    df_rt.insert(
                        df_rt.shape[1],
                        "D_motion_E",
                        pd.Series(df1[df1["Target"] == "motion"]["rt"].mean()),
                    )
                    # 处理准确率
                    df_accuracy.insert(
                        df_accuracy.shape[1],
                        "D_topo_E",
                        pd.Series(
                            (df1[df1["Target"] == "topo"]["correct"] == True).sum()
                            / df1[df1["Target"] == "topo"]["correct"].notnull().sum()
                        ),
                    )
                    df_accuracy.insert(
                        df_accuracy.shape[1],
                        "D_motion_E",
                        pd.Series(
                            (df1[df1["Target"] == "motion"]["correct"] == True).sum()
                            / df1[df1["Target"] == "motion"]["correct"].notnull().sum()
                        ),
                    )

            # print(df_rt)
            # Set the font to Times New Roman
            plt.rcParams["font.family"] = "serif"
            plt.rcParams["font.serif"] = ["Times New Roman"]
            plt.xticks(fontname="Times New Roman")
            plt.yticks(fontname="Times New Roman")
            if num == 2:
                ax.plot(
                    [1, 2, 3, 4, 5],
                    df_rt.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
                ax1.plot(
                    [1, 2, 3, 4, 5],
                    df_accuracy.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
            if num == 6:
                ax.plot(
                    [1, 2, 3, 4, 5, 6],
                    df_rt.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
                ax1.plot(
                    [1, 2, 3, 4, 5, 6],
                    df_accuracy.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
            if num == 4:
                ax.plot(
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    df_rt.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
                ax1.plot(
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    df_accuracy.values[0],
                    marker=f"{'v' if j == 0 else 'o'}",
                    label=f"{'2' if i == 0 else '4' if i == 1 else '6'}{'_shape' if j == 0 else '_color'}",
                    linestyle=f"{'--' if j == 1 else '-'}",
                    color=colors[i],
                )
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax1.set_xticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_xticklabels(col)
    ax1.set_xticklabels(col)
    lines, labels = ax.get_legend_handles_labels()
    ax.set_title("RT", fontname="Times New Roman")
    ax.legend(lines, labels)

    lines, labels = ax1.get_legend_handles_labels()
    ax1.set_title("Accuracy", fontname="Times New Roman")
    ax1.legend(lines, labels)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    res.append({"RT": base64.b64encode(buffer.read()).decode("utf-8")})
    buffer = io.BytesIO()
    fig1.savefig(buffer, format="png", dpi=1000)
    buffer.seek(0)
    res.append({"Accuracy": base64.b64encode(buffer.read()).decode("utf-8")})
    # plt.savefig(r'E:\数据汇总\\' + 'RT_compare_data_1.svg',
    #             format='svg')
    # plt.savefig(
    #     r"E:\小论文\小论文图\数据图\动态F\\" + "Accuracy_compare_data_1.jpg",
    #     format="jpg",
    #     dpi=1000,
    # )
    # # plt.savefig(r'E:\数据汇总\\' + 'RT_compare_data_1.tiff',
    # #             format='tiff', dpi=500)
    # plt.show()
    return res


scvpath2 = r"E:\数据汇总\dynamic\\汇总\\data.csv"
# draw_dynamic2(scvpath2)
