# server/app.py
from flask import Flask, send_file, render_template, request, jsonify, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from urllib.parse import unquote
import os
import sys
import json
import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from werkzeug.utils import secure_filename
from static.pythonfiles.data import datapro_recall
from static.pythonfiles.data_recognition import datapro_recognition
from static.pythonfiles.data_dynamic import datapro_dynamic
from static.pythonfiles.data_dynamic1 import datapro_dynamic1
from static.pythonfiles.data_test import param_test, param_testto
from static.pythonfiles.drawsns import SumData1, SumData2, drawCompares
from static.pythonfiles.compareRecallAndRecog import Comparison2and3
from static.pythonfiles.draw_dynamic import draw_dynamic1, draw_dynamic2
from static.pythonfiles.eyeDataProcess import eyeData, eyeDataProcess1
from static.pythonfiles.eyedatapro import (
    eyeData1,
    eyeDataProcessSAVE,
    eyeDataProcessStatic,
    draw,
    analy,
)
from static.pythonfiles.eyeData_dynamic import (
    eyeDatady,
    eyeDataAnalysis,
    eyeDataAnalysis1,
    eyeDataAnalysisTandM,
    eyeDataAnalysisTM,
)
from static.pythonfiles.eyedata_dypro import (
    eyeDataProcessdy,
    eyeDataProcessdyp,
    eyeDatadyp,
)
from static.pythonfiles.datatest_dynamic import (
    param_test1,
    param_testTorM,
    param_testdy,
    param_testdy1,
)
from static.pythonfiles.gazeheatplot import fun
from static.pythonfiles.dataSurvey import drawsurvey
from datetime import datetime

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost:3306/pos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = "784fsrsryyfyft"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)


class Examinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(255), nullable=False)
    exam_comment = db.Column(db.String(255), nullable=False)
    designerid = db.Column(db.Integer, primary_key=True)
    designer = db.Column(db.String(255), nullable=False)
    generation_date = db.Column(db.Date, nullable=False)


class Web_Attention_Memory_Exam(db.Model):
    __tablename__ = "Web_Attention_Memory_Exam"
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(255), nullable=False)
    designerid = db.Column(db.Integer, primary_key=True)
    designer = db.Column(db.String(255), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    studytype = db.Column(db.String(255), nullable=False)
    Num = db.Column(db.String(255), nullable=False)
    ISI = db.Column(db.String(255), nullable=False)
    generation_date = db.Column(db.Date, nullable=False)


class Web_Deployment_Exam(db.Model):
    __tablename__ = "Web_Deployment_Exam"
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(255), nullable=False)
    designerid = db.Column(db.Integer, primary_key=True)
    designer = db.Column(db.String(255), nullable=False)
    generation_date = db.Column(db.Date, nullable=False)


# 系统注册操作
@app.route("/register", methods=["POST"])
def system_register():
    data = request.json  # 获取前端发送的 JSON 数据
    provided_userrole = data.get("userRole")  # 用户身份
    provided_username = data.get("userName")
    provided_password = data.get("password")
    provided_name = data.get("name")
    provided_gender = data.get("gender")
    provided_birthdate = data.get("birthdate")
    provided_phoneNumber = data.get("phoneNumber")
    # 查询数据库以检查该身份的用户是否存在
    exist_user = User.query.filter_by(
        username=provided_username, role=provided_userrole, name=provided_name
    ).first()
    if exist_user:
        return jsonify({"message": "该用户已存在"})
    # 在这里执行数据库插入操作
    new_user = User(
        username=provided_username,
        password=provided_password,
        role=provided_userrole,
        name=provided_name,
        gender=provided_gender,
        birthday=provided_birthdate,
        phone_number=provided_phoneNumber,
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})


# 系统登录操作
@app.route("/login", methods=["POST"])
def system_login():
    data = request.json  # 获取前端发送的 JSON 数据
    provided_userrole = data.get("userRole")  # 用户身份
    provided_username = data.get("userName")
    provided_password = data.get("password")
    # 查询数据库以检查该身份的用户是否存在
    user = User.query.filter_by(
        username=provided_username, role=provided_userrole
    ).first()
    if user and user.password == provided_password:
        # 用户存在，密码匹配，可以视为登录成功
        # 将用户名和身份权限保存在会话中
        session["username"] = provided_username
        session["user_role"] = provided_userrole
        print(session)
        return jsonify({"message": "Login successful"})
    else:
        # 用户不存在，密码不匹配，登录失败
        return jsonify({"message": "Invalid username, user role, or password"})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()  # 清除 session
    return jsonify({"message": "Logout successful"}), 200


# 获取用户角色
@app.route("/get_user_role", methods=["POST"])
def get_user_role():
    username = session.get("username")
    user_role = session.get("user_role")
    if username:
        return jsonify({"role": user_role, "username": username})
    else:  # 用户不存在
        return jsonify({"role": " "})


# 获取用户信息
@app.route("/get_user_data", methods=["POST"])
def get_user_data():
    # 从会话中获取用户名和身份权限
    username = session.get("username")
    user_role = session.get("user_role")
    # print(session)
    # 查询数据库以检查该身份的用户是否存在
    user = User.query.filter_by(username=username, role=user_role).first()
    if user:  # 用户存在
        return jsonify(
            {
                "userName": user.username,
                "name": user.name,
                "gender": user.gender,
                "birthdate": user.birthday.strftime("%Y-%m-%d"),
                "phoneNumber": user.phone_number,
                "role": user.role,
                "registration_date": user.registration_date,
            }
        )
    else:  # 用户不存在
        return jsonify({"message": "User not found"})


# 获取所有参与者信息（管理员权限）
@app.route("/get_all_participants_info", methods=["POST"])
def get_all_participants_info():
    if session.get("user_role") == "admin":
        participants_info = User.query.all()
        # 根据需要将查询到的信息转换为适当的格式
        data = [
            {
                "username": user.username,
                "role": user.role,
                "gender": user.gender,
                "name": user.name,
                "phone_number": user.phone_number,
                "birthday": user.birthday.strftime("%Y-%m-%d"),
            }
            for user in participants_info
        ]
        return jsonify(data)
    if session.get("user_role") == "designer":
        # print("qqq")
        participants_info = User.query.filter_by(role="participant").all()
        # 根据需要将查询到的信息转换为适当的格式
        data = [
            {
                "username": user.username,
                "role": user.role,
                "gender": user.gender,
                "name": user.name,
                "phone_number": user.phone_number,
                "birthday": user.birthday.strftime("%Y-%m-%d"),
            }
            for user in participants_info
        ]
        return jsonify(data)
    else:
        return jsonify({"message": "Permission denied"})


# 获取所有实验信息（管理员权限）
@app.route("/get_all_exam_info", methods=["POST"])
def get_all_exam_info():
    if session.get("user_role") == "admin":
        exam_info = Examinfo.query.all()
        # 根据需要将查询到的信息转换为适当的格式
        data = [
            {
                "exam_name": ExamInfo.exam_name,
                "exam_comment": ExamInfo.exam_comment,
                "designer": ExamInfo.designer,
                "generation_date": ExamInfo.generation_date.strftime("%Y-%m-%d"),
            }
            for ExamInfo in exam_info
        ]
        return jsonify(data)
    if session.get("user_role") == "designer":
        print("qqq")
        exam_info = Examinfo.query.filter_by(designer=session.get("username")).all()
        # 根据需要将查询到的信息转换为适当的格式
        data = [
            {
                "exam_name": ExamInfo.exam_name,
                "exam_comment": ExamInfo.exam_comment,
                "designer": ExamInfo.designer,
                "generation_date": ExamInfo.generation_date.strftime("%Y-%m-%d"),
            }
            for ExamInfo in exam_info
        ]
        return jsonify(data)
    else:
        return jsonify({"message": "Permission denied"})


# 获取具体实验信息
@app.route("/get_detail_exam_info", methods=["POST"])
def get_detail_exam_info():
    data = request.json  # 获取前端发送的 JSON 数据
    examName = data.get("examName")  #
    examid = data.get("id")
    if examid == 2:
        exam_info = Web_Deployment_Exam.query().all()
        print(exam_info)
        # 根据需要将查询到的信息转换为适当的格式
        data = [
            {
                "exam_name": ExamInfo.exam_name,
                "designer": ExamInfo.designer,
                "generation_date": ExamInfo.generation_date.strftime("%Y-%m-%d"),
            }
            for ExamInfo in exam_info
        ]
        return jsonify(data)
    if examid == 1:
        exam_info = Web_Attention_Memory_Exam.query.all()
        # 根据需要将查询到的信息转换为适当的格式
        data = [
            {
                "exam_name": ExamInfo.exam_name,
                "designer": ExamInfo.designer,
                "task": ExamInfo.task,
                "studytype": ExamInfo.studytype,
                "Num": ExamInfo.Num,
                "ISI": ExamInfo.ISI,
                "generation_date": ExamInfo.generation_date.strftime("%Y-%m-%d"),
            }
            for ExamInfo in exam_info
        ]
        return jsonify(data)
    else:
        return jsonify({"message": "Permission denied"})


# 更新用户信息
@app.route("/update_user_data", methods=["PUT"])
def update_user_data():
    # 从会话中获取用户名和身份权限
    username = session.get("username")
    user_role = session.get("user_role")
    user = User.query.filter_by(username=username, role=user_role).first()
    if user:
        data = request.json
        user.username = data.get("userName")
        user.gender = data.get("gender")
        user.birthday = data.get("birthdate")
        user.phone_number = data.get("phoneNumber")

        # 如果前端提供了新密码，则更新密码
        new_password = data.get("password")
        if new_password:
            user.password = new_password
        # print(user.birthdate)
        db.session.commit()
        print("success")
        return jsonify({"message": "User data updated successfully"})
    else:
        return jsonify({"message": "User not found"})


# 静态文件中间件，指定静态资源目录
@app.route("/memory_exam1")
def open_memory_exam():
    ISI = request.args.get("ISI")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    TaskType = request.args.get("TaskType")
    return render_template(
        "memory_exam1.html",
        ISI=ISI,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        TaskType=TaskType,
    )


@app.route("/memory_exam2")
def open_memory_exam_2():
    ISI = request.args.get("ISI")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    TaskType = request.args.get("TaskType")
    return render_template(
        "memory_exam2.html",
        ISI=ISI,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        TaskType=TaskType,
    )


@app.route("/memory_exam2_pro")
def open_memory_exam_2_pro():
    ISI = request.args.get("ISI")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    TaskType = request.args.get("TaskType")
    return render_template(
        "memory_exam2_pro.html",
        ISI=ISI,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        TaskType=TaskType,
    )


@app.route("/memory_exam4")
def open_memory_exam_4():
    ISI = request.args.get("ISI")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    TaskType = request.args.get("TaskType")
    return render_template(
        "memory_exam4.html",
        ISI=ISI,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        TaskType=TaskType,
    )


@app.route("/memory_exam4_pro")
def open_memory_exam_4_pro():
    ISI = request.args.get("ISI")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    TaskType = request.args.get("TaskType")
    return render_template(
        "memory_exam4_pro.html",
        ISI=ISI,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        TaskType=TaskType,
    )


@app.route("/memory_exam6")
def open_memory_exam_6():
    ISI = request.args.get("ISI")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    TaskType = request.args.get("TaskType")
    return render_template(
        "memory_exam6.html",
        ISI=ISI,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        TaskType=TaskType,
    )


@app.route("/memory_exam6_pro")
def open_memory_exam_6_pro():
    ISI = request.args.get("ISI")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    TaskType = request.args.get("TaskType")
    return render_template(
        "memory_exam6_pro.html",
        ISI=ISI,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        TaskType=TaskType,
    )


@app.route("/dynamic")
def open_dynamic():
    Exam_Type = request.args.get("Exam_Type")
    StimNumber = request.args.get("StimNumber")
    StudyAttribute = unquote(request.args.get("StudyAttribute"))
    ChangeType = request.args.get("ChangeType")
    return render_template(
        "dynamic.html",
        Exam_Type=Exam_Type,
        Stimnumber=StimNumber,
        StudyAttribute=StudyAttribute,
        ChangeType=ChangeType,
    )


@app.route("/exployment")
def open_exployment():
    Exam_url = request.args.get("Exam_url")
    if "survey" in Exam_url:
        url = "survey.html"
    else:
        url = "index.html"
    return render_template(url, Exam_url=Exam_url)


@app.route("/get_qian_html")
def get_qian_html():
    content = render_template("qian.html")
    return content


# 设置上传文件保存的目录
UPLOAD_FOLDER = "D:/VScode/My_system/file"
# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = {"csv"}  # 可根据实际需求添加文件类型


@app.route("/performSearch")
def performSearch():
    data = []
    Etype = request.args.get("Etype")
    Examtype = request.args.get("Examtype")
    StimNum = request.args.get("StimNum")
    ISI = request.args.get("ISI")
    Ttype = request.args.get("Ttype")
    if Examtype == "Auxiliary":
        Ttype = Ttype + "_pro"
    url = UPLOAD_FOLDER + "/" + Etype + "/" + Ttype + "/"
    if Etype == "动态":
        url = url + StimNum
    else:
        url = url + ISI + "/" + StimNum
    print(url)
    # 获取该文件夹下所有csv文件
    files = os.listdir(url)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    for idx, f in enumerate(csv_files, start=1):
        StudyAttribute = ""
        if "color" in f and "shape" in f:
            StudyAttribute = "颜色&形状"
        elif "color" in f:
            StudyAttribute = "颜色"
        elif "shape" in f:
            StudyAttribute = "形状"
        file_data = {
            "id": idx,
            "TaskType": Ttype,
            "StudyAttribute": StudyAttribute,
            "StimNumber": StimNum,
            "FileName": f,
            "ISI": ISI,
            "Exam_Type": " " if Examtype == "Main" or Examtype == "" else "pro",
        }
        data.append(file_data)
    # print(data)
    return data


@app.route("/download")
def download_files():
    folder_path = "static/pythonfiles"
    file1_path = f"{folder_path}/data.py"
    file2_path = f"{folder_path}/datafunc.py"
    # 创建一个 BytesIO 对象，用于在内存中创建 Zip 文件
    # 记录当前工作目录
    current_directory = os.getcwd()
    try:
        # 更改工作目录到 Flask 应用的根目录
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # 创建一个 BytesIO 对象，用于在内存中创建 Zip 文件
        zip_buffer = BytesIO()
        # 使用 zipfile 将两个文件压缩到 Zip 文件中
        with ZipFile(zip_buffer, "w") as zip_file:
            zip_file.write(file1_path, os.path.basename(file1_path))
            zip_file.write(file2_path, os.path.basename(file2_path))
        # 将 BytesIO 对象的内容发送给用户
        zip_buffer.seek(0)
        return send_file(
            zip_buffer, download_name="data_process(示例).zip", as_attachment=True
        )
    finally:
        # 恢复原始的工作目录
        os.chdir(current_directory)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_files():
    # 路径参数
    Etype = request.form.get("Etype")
    Examtype = request.form.get("Examtype")
    StimNum = request.form.get("StimNum")
    ISI = request.form.get("ISI")
    Ttype = request.form.get("Ttype")
    if Examtype == "Auxiliary":
        Ttype = Ttype + "_pro"
    # 文件
    uploaded_files = request.files.getlist("files[]")
    uploaded_filenames = []
    # 路径配置
    url = UPLOAD_FOLDER + "/" + Etype + "/" + Ttype + "/"
    if Etype == "动态":
        url = url + str(StimNum)
    else:
        url = url + str(ISI) + "/" + StimNum
    # 文件存储
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(url, filename))
            uploaded_filenames.append(filename)
    return jsonify({"uploaded_filenames": uploaded_filenames})


@app.route("/SelectToProcess", methods=["POST"])
def SelectToProcess():
    data = request.json
    url_save = UPLOAD_FOLDER + "/process"
    selected_rows = data.get("selectedRows", [])
    # 路径参数
    Etype = data.get("Etype")
    Examtype = data.get("Examtype")
    StimNum = data.get("StimNum")
    ISI = data.get("ISI")
    Ttype = data.get("Ttype")
    url_save = url_save + "/" + Etype
    if Examtype == "Auxiliary":
        Ttype = Ttype + "_pro"
        url_save = url_save + "/pro"
    url = UPLOAD_FOLDER + "/" + Etype + "/" + Ttype + "/"
    if Etype == "动态":
        if Examtype == "Main":
            url = url + str(StimNum)
    else:
        url = url + str(ISI) + "/" + str(StimNum)
    if Etype != "动态":
        if "recall" in Ttype:
            datapro_recall(str(ISI), str(StimNum), url, url_save)
        if "recognition" in Ttype:
            datapro_recognition(str(ISI), str(StimNum), url, url_save)
    else:
        if "pro" in Ttype:
            datapro_dynamic1(str(StimNum), url, url_save)
        else:
            datapro_dynamic(str(StimNum), url, url_save)
    # 文件

    return jsonify({"uploaded_filenames": 4})


# 数据分析下的功能
@app.route("/performSearchItems")
def performSearchItems():
    data = []
    Etype = request.args.get("Etype")
    Examtype = request.args.get("Examtype")
    Ttype = request.args.get("Ttype")
    url = UPLOAD_FOLDER + "/" + "process/" + Etype
    if Examtype == "Auxiliary":
        url = url + "/pro"
    print(Examtype)
    # 获取该文件夹下所有csv文件
    files = os.listdir(url)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    for idx, f in enumerate(csv_files, start=1):
        StudyAttribute = ""
        if "color" in f:
            StudyAttribute = "颜色"
        elif "shape" in f:
            StudyAttribute = "形状"
        if Etype != "动态":
            if Ttype in f:
                file_data = {
                    "id": idx,
                    "TaskType": Ttype,
                    "StudyAttribute": StudyAttribute,
                    "FileName": f,
                    "Exam_Type": " " if Examtype == "Main" or Examtype == "" else "pro",
                }
                data.append(file_data)
        else:
            file_data = {
                "id": idx,
                "TaskType": Ttype,
                "StudyAttribute": StudyAttribute,
                "FileName": f,
                "Exam_Type": " " if Examtype == "Main" else "pro",
            }
            data.append(file_data)
    return data


# 显著性分析
@app.route("/SignificantInformation", methods=["POST"])
def significantInformation():
    data = []
    request_data = request.json
    Etype = request_data.get("Etype")
    Examtype = request_data.get("Examtype")
    Ttype = request_data.get("Ttype")
    Type = request_data.get("Type")
    urlpath = UPLOAD_FOLDER + "/" + "process/" + Etype
    if Examtype == "Auxiliary":
        urlpath = urlpath + "/" + "pro"
    if Etype == "预实验":
        data = param_test(urlpath, Ttype)
    elif Etype == "静态":
        data = param_testto(urlpath, Ttype)
    elif Etype == "动态":
        if Examtype == "Main":
            data = param_test1(urlpath)
        else:
            data = param_testdy(urlpath, Type)

    # 提取混合线性效应模型的rt和correct结果
    rt_result = data[0]["rt"].as_html()  # 获取rt结果的表格
    correct_result = data[1]["correct"].as_html()  # 获取correct结果的表格

    # 将结果格式化为JSON
    json_data = {"rt_result": rt_result, "correct_result": correct_result}
    # print("qqqq", json_data)
    return jsonify(json_data)


@app.route("/FigureInformation", methods=["POST"])
def figureInformation():
    data = []
    request_data = request.json
    Etype = request_data.get("Etype")
    Examtype = request_data.get("Examtype")
    Ttype = request_data.get("Ttype")
    Factor = request_data.get("Factor")
    Type = request_data.get("Type")
    urlpath = UPLOAD_FOLDER + "/" + "process/" + Etype
    if Etype == "预实验":
        urlpath = urlpath + "/汇总"
        data = SumData1(urlpath, "", Factor, Ttype)
    elif Etype == "静态":
        if Examtype == "Main":
            data = SumData2(urlpath, "", Factor, Ttype, Type)
        else:
            urlpath = urlpath + "/pro/汇总"
            data = Comparison2and3(urlpath, "", Factor, Ttype)
    elif Etype == "动态":
        if Examtype == "Main":
            urlpath = urlpath + "/汇总"
            data = draw_dynamic1(urlpath, Factor)
        if Examtype == "Auxiliary":
            urlpath = urlpath + "/pro/汇总"
            data = drawCompares(urlpath, Type)

    json_data = {"imagedata": data}
    return json_data


# 综合显著性分析
@app.route("/ComprehensiveSignificantInformation", methods=["POST"])
def ComprehensivesignificantInformation():
    data = []
    urlpath1 = UPLOAD_FOLDER + "/process/静态/汇总/data2.csv"
    urlpath2 = UPLOAD_FOLDER + "/process/静态/pro/汇总/data3.csv"
    urlpath3 = UPLOAD_FOLDER + "/process/动态/汇总/data.csv"
    urlpath4 = UPLOAD_FOLDER + "/process/动态/pro/汇总/data_4.csv"
    data = param_testdy1(urlpath1, urlpath2, urlpath3, urlpath4)
    # 提取混合线性效应模型的rt和correct结果
    rt_result = data[0]["rt"].as_html()  # 获取rt结果的表格
    correct_result = data[1]["correct"].as_html()  # 获取correct结果的表格
    # 将结果格式化为JSON
    json_data = {"rt_result": rt_result, "correct_result": correct_result}
    return jsonify(json_data)


# 综合图表分析
@app.route("/ComprehensiveFigureInformation", methods=["POST"])
def ComprehensiveFigureInformation():
    data = []
    urlpath1 = UPLOAD_FOLDER + "/process/静态/汇总/data2.csv"
    urlpath2 = UPLOAD_FOLDER + "/process/静态/pro/汇总/data3.csv"
    urlpath3 = UPLOAD_FOLDER + "/process/动态/汇总/data.csv"
    urlpath4 = UPLOAD_FOLDER + "/process/动态/pro/汇总/data_4.csv"
    urlpath5 = UPLOAD_FOLDER + "/process/预实验/汇总/data.csv"
    data = draw_dynamic2(urlpath1, urlpath2, urlpath3, urlpath4, urlpath5)
    # 提取混合线性效应模型的rt和correct结果
    rt_result = data[0]["RT"]  # 获取rt结果的表格
    correct_result = data[1]["Accuracy"]  # 获取correct结果的表格
    # 将结果格式化为JSON
    json_data = {"rt_result": rt_result, "correct_result": correct_result}
    return jsonify(json_data)


# 眼动数据处理
@app.route("/EyedataProcess", methods=["POST"])
def EyedataProcess():
    request_data = request.json
    Eye_proType = request_data.get("Eye_proType")
    Etype = request_data.get("Etype")
    Examtype = request_data.get("Examtype")
    url = UPLOAD_FOLDER + "/process/" + Etype
    if Examtype == "Auxiliary":
        url = url + "/pro"
    if Eye_proType == "眼动轨迹":
        eyeData(url)
    elif Eye_proType == "注视点的数量":
        if Etype == "预实验" or Etype == "静态":
            eyeData1(url)
        elif Etype == "动态":
            if Examtype == "Main":
                eyeDatady(url)
            elif Examtype == "Auxiliary":
                eyeDatadyp(url)
    return jsonify({"uploaded_filenames": 4})


# 检查 eyedata 文件夹是否为空的端点
@app.route("/checkEyedataFolder", methods=["POST"])
def check_eyedata_folder():
    request_data = request.json
    Eye_proType = request_data.get("Eye_proType")
    Etype = request_data.get("Etype")
    Examtype = request_data.get("Examtype")
    urlpath = UPLOAD_FOLDER + "/process/" + Etype
    if Examtype == "Auxiliary":
        urlpath = urlpath + "/pro"
    urlpath = urlpath + "/eyedata"
    if Eye_proType == "注视点的数量":
        urlpath = urlpath + "/num"
    try:
        # 使用 os.listdir 获取文件夹内容
        files = os.listdir(urlpath)
        # 检查文件夹是否为空
        is_eyedata_folder_empty = len(files) == 0
        return jsonify({"isEyedataFolderEmpty": is_eyedata_folder_empty})
    except Exception as e:
        print(f"Error checking eyedata folder: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


# 计算目标眼动命中率
@app.route("/performHitRate", methods=["POST"])
def PerformHitRate():
    request_data = request.json
    Eye_proType = request_data.get("Eye_proType")
    Etype = request_data.get("Etype")
    Examtype = request_data.get("Examtype")
    urlpath = UPLOAD_FOLDER + "/process/" + Etype
    if Examtype == "Auxiliary":
        urlpath = urlpath + "/pro"
    urlpath = urlpath + "/eyedata"
    if Eye_proType == "注视点的数量":
        urlpath = urlpath + "/num"
    # eyeDataProcessSAVE(paths)
    if Etype == "预实验" or Etype == "静态":
        res = eyeDataProcessStatic(urlpath, Etype)
    elif Etype == "动态":
        if Examtype == "Main":
            res = eyeDataProcessdy(urlpath)
        elif Examtype == "Auxiliary":
            res = eyeDataProcessdyp(urlpath)
    return jsonify(res)


# 眼动数据显著性分析
@app.route("/EyeSignificantInformation", methods=["POST"])
def EyesignificantInformation():
    data = []
    request_data = request.json
    Factor = request_data.get("Factor")
    Eye_proType = request_data.get("Eye_proType")  # 数据处理方式
    Etype = request_data.get("Etype")
    Examtype = request_data.get("Examtype")
    Ttype = request_data.get("Ttype")
    Type = request_data.get("Type")
    urlpath = UPLOAD_FOLDER + "/" + "process/" + Etype
    if Examtype == "Auxiliary":
        urlpath = urlpath + "/" + "pro"
    urlpath = urlpath + "/eyedata"
    if Etype == "预实验":
        urlpath = urlpath + "/num/data.csv"
        data_long = pd.read_csv(
            urlpath, encoding="utf-8", engine="python", on_bad_lines="warn"
        )
        data = analy(data_long)
    elif Etype == "静态":
        data = eyeDataProcess1(urlpath, Factor, 0)
    elif Etype == "动态":
        urlpath = urlpath + "/eyedata.csv"
        if Examtype == "Main":
            for m, arr in enumerate(["shape", "color"]):
                data1 = []
                for i, num in enumerate([2, 4, 6]):
                    data_res = eyeDataAnalysis(urlpath, num, arr, "", 0)
                    data1.append({num: data_res})
                data.append({arr: data1})
            data_res = eyeDataAnalysisTM(urlpath)
            data.append({"Further": data_res})
        else:
            for m, arr in enumerate(["shape", "color"]):
                data_res = eyeDataAnalysis1(urlpath, arr, 0)
                data.append({arr: data_res})
            data_res = eyeDataAnalysisTandM(urlpath, "", 0)
            data.append({"Further": data_res})
    print(data)
    if Etype == "动态" and Examtype == "Main":
        eyedata_result_2_s = data[0]["shape"][0][2].as_html()
        eyedata_result_4_s = data[0]["shape"][1][4].as_html()
        eyedata_result_6_s = data[0]["shape"][2][6].as_html()
        eyedata_result_2_c = data[1]["color"][0][2].as_html()
        eyedata_result_4_c = data[1]["color"][1][4].as_html()
        eyedata_result_6_c = data[1]["color"][2][6].as_html()
        eyedata_result_f = data[2]["Further"].as_html()
        # 将结果格式化为JSON
        json_data = {
            "eyedata_result_2_s": eyedata_result_2_s,
            "eyedata_result_4_s": eyedata_result_4_s,
            "eyedata_result_6_s": eyedata_result_6_s,
            "eyedata_result_2_c": eyedata_result_2_c,
            "eyedata_result_4_c": eyedata_result_4_c,
            "eyedata_result_6_c": eyedata_result_6_c,
            "eyedata_result_f": eyedata_result_f,
        }
    elif Etype == "动态" and Examtype == "Auxiliary":
        eyedata_result_s = data[0]["shape"].as_html()
        eyedata_result_c = data[1]["color"].as_html()
        eyedata_result_f = data[2]["Further"].as_html()
        json_data = {
            "eyedata_result_s": eyedata_result_s,
            "eyedata_result_c": eyedata_result_c,
            "eyedata_result_f": eyedata_result_f,
        }
    else:
        # 提取混合线性效应模型的结果
        eyedata_result_2 = data[0][2].as_html()
        eyedata_result_4 = data[1][4].as_html()
        eyedata_result_6 = data[2][6].as_html()
        # 将结果格式化为JSON
        json_data = {
            "eyedata_result_2": eyedata_result_2,
            "eyedata_result_4": eyedata_result_4,
            "eyedata_result_6": eyedata_result_6,
        }
    return jsonify(json_data)


@app.route("/EyeFigureInformation", methods=["POST"])
def EyefigureInformation():
    data = []
    request_data = request.json
    Etype = request_data.get("Etype")
    Examtype = request_data.get("Examtype")
    Factor = request_data.get("Factor")
    Type = request_data.get("Type")
    urlpath = UPLOAD_FOLDER + "/" + "process/" + Etype
    if Examtype == "Auxiliary":
        urlpath = urlpath + "/" + "pro"
    urlpath = urlpath + "/eyedata"
    if Etype == "预实验":
        urlpath = urlpath + "/num/data.csv"
        data_long = pd.read_csv(
            urlpath, encoding="utf-8", engine="python", on_bad_lines="warn"
        )
        data = draw(
            data_long[(data_long["first_dot"] == data_long["target"])],
            data_long[(data_long["first_dot"] != data_long["target"])],
            Factor,
        )
    elif Etype == "静态":
        data = eyeDataProcess1(urlpath, Factor, 1)
    elif Etype == "动态":
        urlpath = urlpath + "/eyedata.csv"
        if Examtype == "Main":
            data = eyeDataAnalysis(urlpath, "", "", Factor, 1)
        if Examtype == "Auxiliary":
            if Type == "综合":
                data = eyeDataAnalysis1(urlpath, "", 1)
            else:
                data = eyeDataAnalysisTandM(urlpath, Type, 1)
    json_data = {"imagedata": data}
    return json_data


# 网页使用数据处理
@app.route("/deploydataProcess", methods=["POST"])
def DeploydataProcess():
    request_data = request.json
    Webpage = request_data.get("Webpage")
    url = UPLOAD_FOLDER + "/实际部署/" + Webpage
    url1 = UPLOAD_FOLDER + "/process/实际部署/"
    combine_data = pd.DataFrame()
    for file in os.listdir(url):
        if file.endswith(".csv") and "webgazer" in file and "(1)" not in file:
            file_path = os.path.join(url, file)
            data = pd.read_csv(file_path, header=None)  # 无列名拼接
            combine_data = pd.concat([combine_data, data], ignore_index=True)
    # 删除合并后数据中的第一行
    combined_data = combine_data.iloc[1:]
    combine_data.to_csv(url1 + "/" + Webpage + "_combine_data.csv", index=False)
    return jsonify({"uploaded_filenames": "success"})


# 热图数据处理
@app.route("/Gazeheat", methods=["POST"])
def Gazeheat():
    url = UPLOAD_FOLDER + "/process/实际部署/booking_combine_data.csv"
    url1 = UPLOAD_FOLDER + "/process/实际部署/tuniu_combine_data.csv"
    b_path = UPLOAD_FOLDER + "/img/b.png"
    t_path = UPLOAD_FOLDER + "/img/tt.png"
    data = fun(url, b_path)
    data1 = fun(url1, t_path)
    json_data = {"booking_result": data, "tuniu_result": data1}
    return jsonify(json_data)


@app.route("/performDeployItems", methods=["POST"])
def performDeployItems():
    data = []
    request_data = request.json
    Webpage = request_data.get("Webpage")
    url = UPLOAD_FOLDER + "/实际部署/" + Webpage
    # 获取该文件夹下所有csv文件
    files = os.listdir(url)
    # 过滤出所有以 .csv 结尾的文件
    csv_files = [file for file in files if file.endswith(".csv")]
    for idx, f in enumerate(csv_files, start=1):
        file_data = {
            "id": idx,
            "FileName": f,
        }
        data.append(file_data)
    print(data)
    return data


# 眼动数据显著性分析
@app.route("/SurveyFigureInformation", methods=["POST"])
def SurveyFigureInformation():
    data_b = pd.DataFrame(columns=["name", "response"])
    data_t = pd.DataFrame(columns=["name", "response"])
    url = UPLOAD_FOLDER + "/实际部署/survey"
    for file in os.listdir(url):
        filepath = os.path.join(url, file)
        df = pd.read_csv(filepath)
        name = json.loads(df[df["trial_index"] == 1]["response"].values[0])
        value1 = df[df["trial_index"] == 5]["response"]
        value2 = df[df["trial_index"] == 7]["response"]
        # 从data中选择name和response列并添加到data_b
        data_b = pd.concat(
            [data_b, pd.DataFrame({"name": [name["name"]], "response": value1[5]})],
            ignore_index=True,
        )
        data_t = pd.concat(
            [data_t, pd.DataFrame({"name": [name["name"]], "response": value2[7]})],
            ignore_index=True,
        )
    data = drawsurvey(data_b, data_t)
    json_data = {"image_data": data}
    return jsonify(json_data)


@app.route("/webpagefileupload", methods=["POST"])
def Webpagefileupload():
    # 路径参数
    Webpage = request.form.get("Webpage")
    # 文件
    uploaded_files = request.files.getlist("files[]")
    uploaded_filenames = []
    # 路径配置
    url = UPLOAD_FOLDER + "/实际部署/" + Webpage + "/"
    # 文件存储
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(url, filename))
            uploaded_filenames.append(filename)
    return jsonify({"uploaded_filenames": uploaded_filenames})


# 启动服务器
if __name__ == "__main__":
    app.run(debug=True, port=8080)
