from flask import Flask, flash, request, request, jsonify, render_template, send_from_directory
import json
from schedul import Schedule
import threading
import pathlib
import re
import os
import hmac, hashlib
import logging
import traceback
import time
from hashlib import md5
from manage import Manage
import sys
import importlib


WEBHOOK = importlib.import_module("webhook")

# 允许的文件后缀
ALLOWED_EXTENSIONS = {'md', 'markdown'}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.templates_auto_reload = True

# 读取配置信息
with open("config.json", encoding="utf-8") as file:
    data = json.load(file)
    POST_PATH = pathlib.Path(data["post_path"])
    DEPLOY_CMD = data["deploy_cmd"]
    FRONT_MATTERS = set(data["front_matters"])
    LOCAL_GIT_PATH = pathlib.Path(data["local_git_path"])
    REMOTE_GIT = data["remote_git"]
    # 标记是否自动运行，如果true，则此时当git pull无更新时自动舍弃本次更新
    AUTO_GIT = data["auto_git"]
    TIMER = data["timer"]
    WEBHOOK_USED = data["webhook_used"]
    WEBHOOK_SECRET = data["webhook_secret"]
    REQUEST_LOG = pathlib.Path(data["request_log"])
    CUSTOM_LOG = pathlib.Path(data["custom_log"])
    SYSTEM_LOG = pathlib.Path(data["system_log"])
    EXTENDS = data["extends"]
    MARKDOWN_FILE_CLASS = data["markdown_file_class"]
    TOKEN = md5(data["token"].encode("utf-8")).hexdigest()
    BIND = data["bind"]
    PORT = data["port"]
    BLOG_URL = data["blog_url"]
    GIT = data["git"] if data["git"] in ["gitee", "github"] else "github"


# flask请求日志
request_logger = logging.getLogger("werkzeug")
request_logger.setLevel(logging.DEBUG)
request_file_handler = logging.FileHandler(REQUEST_LOG, encoding="utf-8")
request_logger.addHandler(request_file_handler)
os.sys.stdout = open(REQUEST_LOG, "a", encoding="utf-8")


# 自定义的输出
logger = logging.getLogger('custom')
logger.setLevel(logging.DEBUG)
custom_file_handler = logging.FileHandler(CUSTOM_LOG, encoding="utf-8")                     # 创建文件句柄
log_format = logging.Formatter(f"%(asctime)s [%(levelname)s] : %(message)s")                # 指定格式
custom_file_handler.setFormatter(log_format)
logger.addHandler(custom_file_handler)


# 定义系统调用输出日志，git和hexo输出日志
system_logger = logging.getLogger('system_hexo')
system_logger.setLevel(logging.DEBUG)
system_logger_handler = logging.FileHandler(SYSTEM_LOG, encoding="utf-8")
system_logger_handler.setFormatter(log_format)
system_logger.addHandler(system_logger_handler)


if WEBHOOK_USED is False:
    logger.info("执行定时调度任务")
    s = Schedule(local_git_path=LOCAL_GIT_PATH, remote_git=REMOTE_GIT, auto_git=AUTO_GIT, post_path=POST_PATH, front_matters=FRONT_MATTER, deploy_cmd=DEPLOY_CMD, timer=TIMER, extends=EXTENDS, markdown_file_class=MARKDOWN_FILE_CLASS)
    s.schedul_start()


# 判断文件是否为
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 更新部署Hexo，重新生成静态文件
def deploy():
    result = os.popen(DEPLOY_CMD)
    system_logger.info(result.buffer.read().decode("utf-8"))


def token_verify(token: str):
    return True if md5(token.encode('utf-8')).hexdigest() == TOKEN else False

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", blog=BLOG_URL)

# 上传主程序
@app.route("/upload", methods=["POST"])
def upload():
    status = {"status": "Error", "msg": "文件上传出现错误"}
    status_code = 400
    token = request.form.get("token")
    if not token_verify(token):
        status["msg"] = "无效token！"
        status_code = 401
        return  jsonify(status), status_code
    try:
        if 'file' not in request.files:
            return jsonify(status), status_code
        file = request.files['file']
        if file.filename == "":
            return jsonify(status), status_code
        data = request.get_json()
        file.filename = re.sub(r"\"*$", "", file.filename)
        if file and allowed_file(file.filename):
            schedul = Schedule(local_git_path=LOCAL_GIT_PATH, remote_git=REMOTE_GIT, auto_git=AUTO_GIT, post_path=POST_PATH, front_matters=FRONT_MATTERS, deploy_cmd=DEPLOY_CMD, timer=TIMER, extends=EXTENDS, markdown_file_class=MARKDOWN_FILE_CLASS)
            if schedul.upload_schedul(file_name=file.filename, data=file.read().decode("utf-8")) is False:
                return jsonify(status), status_code
            status["f"] = file.filename
            status["msg"] = "文件上传成功：{}".format(file.filename)
            status["status"] = "Success"
            status_code = 200
            return jsonify(status), status_code
        status["msg"] = "不支持的文件格式: {}".format(file.filename)
        return jsonify(status), status_code
    except Exception as error:
        logger.error("Flask主程序出现问题：{}".format(str(error)))
        exc_type, exc_value, exc_tb = sys.exc_info()
        format_tb_info = traceback.format_exception()
        logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
        status_code = 500
        return jsonify(status), status_code 


@app.route("/webhook", methods=["POST"])
def webhook():
    if WEBHOOK_USED is False:
        return jsonify({"status": "Error", "message": "Not activated webhook"})
    git = getattr(WEBHOOK, GIT)
    sign, status, status_code = git(request=request, key=WEBHOOK_SECRET)
    if sign:
        logger.info("有新的push请求")
        schedul = Schedule(local_git_path=LOCAL_GIT_PATH, remote_git=REMOTE_GIT, auto_git=AUTO_GIT, post_path=POST_PATH, front_matters=FRONT_MATTERS, deploy_cmd=DEPLOY_CMD, timer=TIMER, extends=EXTENDS, markdown_file_class=MARKDOWN_FILE_CLASS)
        schedul.webhook()
        return jsonify(status), status_code
    return jsonify(status), status_code


@app.route("/getfiles", methods=["POST"])
def get_files():
    data = request.get_json()
    status = {"status": "Error", "files": [], "msg": "未知错误"}
    status_code = 500
    if data and token_verify(data["token"]):
        status["status"] = "Success"
        status_code = 200
        m = Manage(POST_PATH)
        status["files"] = m.all_file_info()
        del status["msg"]
        return jsonify(status), status_code
    return jsonify(status), status_code


@app.route("/download", methods=["POST"])
def download():
    status = {"status": "Error", "msg": "未知错误"}
    status_code = 500
    data = dict(request.form)
    try:
        data["filename"] = data["filename"][0] if type(data["filename"]) == list else data["filename"]
        data["token"] = data["token"][0] if type(data["token"]) == list else data["token"]
    except KeyError:
        logger.error("参数错误: {}".format(str(error)))
        exc_type, exc_value, exc_tb = sys.exc_info()
        format_tb_info = traceback.format_exception()
        logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
        status["msg"] = "参数错误"
        status_code = 400
    if not (POST_PATH / data["filename"]).exists():
        status["msg"] = "文件不存在，请刷新文件列表"
        status_code = 404
    elif not token_verify(data["token"]):
        status["msg"] = "无效token"
        status_code = 401
    else:
        return send_from_directory(POST_PATH, filename=data["filename"], as_attachment=True)
    return jsonify(status), status_code
    

@app.route('/delete', methods=["POST"])
def delete():
    data = request.get_json()
    status = {"status": "Error", "msg": "未知错误"}
    status_code = 500
    if data is None:
        status["msg"] = "参数错误"
        status_code = 400
    elif {"token", "filename"}.difference(set(data.keys())):
        status["msg"] = "缺少以下参数：{}".format(", ".join({"token", "filename"}.difference(set(data.keys()))))
        status_code = 400
    elif not token_verify(data["token"]):
        status["msg"] = "无效token"
        status_code = 401
    else:
        m = Manage(POST_PATH)
        s, msg = m.del_file(filename=data["filename"], local_git_path=LOCAL_GIT_PATH)
        threading.Thread(target=deploy, args=[]).start()
        if s:
            status["status"] = "Success"
            status["msg"] = msg
            status_code = 200
    logger.info(status["msg"])
    return jsonify(status), status_code


@app.route("/flush", methods=["POST"])
def flush():
    data = request.get_json()
    status = {"status": "Error", "msg": "未知错误"}
    status_code = 500
    if data is None:
        status["msg"] = "参数错误"
        status_code = 400
    elif {"token", }.difference(set(data.keys())):
        status["msg"] = "缺少以下参数：{}".format(", ".join({"token", }.difference(set(data.keys()))))
        status_code = 400
    elif not token_verify(data["token"]):
        status["msg"] = "无效token"
        status_code = 400
    else:
        threading.Thread(target=deploy, args=()).start()
        status["status"] = "Success"
        status["msg"] = "重新生成静态文件中，请稍后刷新Blog页面"
        status_code = 200
    return jsonify(status), status_code


request_logger.info("[{}]: 程序启动".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
app.run(host=BIND, port=PORT)