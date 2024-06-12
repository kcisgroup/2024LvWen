import csv

input_path = r"E:\数据2\1\combine_data.csv"
B_AOI = {
    "AOI1": [[417, 1982], [10, 108]],
    "AOI2": [[417, 1982], [174, 442]],
    "AOI3": [[417, 1982], [453, 750]],
    "AOI4": [[417, 1982], [765, 1203]],
    "AOI5": [[417, 1982], [1217, 1530]],
    "AOI6": [[417, 1982], [1534, 1956]],
    "AOI7": [[417, 1982], [1960, 2288]],
    "AOI8": [[417, 1982], [2307, 2691]],
    "AOI9": [[417, 1982], [2692, 2902]],
    "AOI10": [[417, 1982], [2905, 3179]],
    "AOI11": [[417, 1982], [3200, 3498]],
    "AOI12": [[417, 1982], [3515, 4163]],
    "AOI13": [[417, 1982], [4163, 4497]],
    "AOI14": [[417, 1982], [4534, 4874]],
    "AOI15": [[417, 1982], [4878, 5548]],
}
T_AOI = {
    "AOI1": [[538, 1862], [0, 171]],  # 导航栏
    "AOI2": [[538, 1308], [171, 606]],  # 酒店预定
    "AOI3": [[1308, 2015], [171, 610]],
    "AOI4": [[538, 1531], [624, 1958]],  # 境内外
    "AOI5": [[1532, 1833], [628, 1132]],
    "AOI6": [[1532, 1833], [1132, 1633]],  # 排行
    "AOI7": [[538, 1532], [1975, 3115]],  # 自助、周边、自驾
    "AOI8": [[538, 1532], [3136, 3404]],  # 酒店
    "AOI9": [[538, 1532], [3412, 4089]],
    "AOI10": [[538, 1532], [4118, 4365]],
    "AOI11": [[538, 1532], [4391, 4809]],  # 笔记
    "AOI12": [[499, 1893], [4827, 5542]],
    "AOI13": [[538, 1862], [5564, 5964]],  # 页脚
}


def process(inputpath):
    with open(inputpath) as f:
        reader = csv.reader(f)
        raws = list(reader)
    return raws