from git import Git
from hashlib import md5
import shutil
import os
import pathlib
import threading
from markdown import Markdown_File
import logging
import traceback
import time, re
import importlib

logger = logging.getLogger('custom')
system_logger = logging.getLogger("system_hexo")


class Schedule:
    def __init__(self, extends=dict({}), **kwargs):
        if {'auto_git', 'deploy_cmd', 'front_matters', 'local_git_path', 'post_path', 'remote_git', 'timer', 'markdown_file_class'}.difference(set(kwargs.keys())):
            raise KeyError("缺少以下参数: '{}'".format(", ".join({'auto_git', 'deploy_cmd', 'front_matters', 'local_git_path', 'post_path', 'remote_git', 'timer', 'markdown_file_class'}.difference(set(kwargs.keys())))))
        self.extends = extends
        self.local_git_path = kwargs["local_git_path"]
        self.remote_git = kwargs["remote_git"]
        self.auto_git = kwargs["auto_git"] 
        self.post_path = kwargs["post_path"]
        self.front_matters = kwargs["front_matters"]
        self.deploy_cmd = kwargs["deploy_cmd"]
        self.timer = kwargs["timer"]
        moudle = importlib.import_module(".", "markdown")
        self.markdown_file_class = getattr(moudle, kwargs["markdown_file_class"])


    # 生成文件夹内文件的的md5s
    def __calc_md5s(self, path: pathlib.Path) -> dict:
        temp = dict()
        for f in os.listdir(path):
            if (f.endswith(".md") or f.endswith(".markdown")) and f != "README.md":
                temp[self.__calc_md5(path / f)] = f
        return temp

    @staticmethod
    def __calc_md5(file_path: pathlib.Path) -> str:
        with open(file_path, "rb") as file:
            return md5(file.read()).hexdigest()

    # 更新删除处理
    def __del_operate(self, file_to_del: set):
        logger.info("删除文件：{}".format("、".join(file_to_del)))
        for f in file_to_del:
            if (self.post_path / f).exists():
                os.remove(self.post_path / f)

    # 更新或者新增加的文件处理后增加到hexo目录后需要重新上传到github上
    def __cp_file(self, files_to_cp: list):
        for f in files_to_cp:
            os.remove(self.local_git_path / f[1])
            shutil.copy2(self.post_path / f[0], self.local_git_path / f[0])

    # 单次调度版删除
    def __cp_file_once(self, files_to_cp: list):
        for f in files_to_cp:
            shutil.copy2(self.post_path / f, self.local_git_path / f)
        
    def __deploy(self):
        logger.info("开始部署")
        result = os.popen(self.deploy_cmd)
        result = result.buffer.read().decode("utf-8")
        system_logger.info(result)
        return result

    # 调度任务
    def __schedul(self):
        git = Git(local_path=self.local_git_path, remote_git=self.remote_git)
        if self.auto_git and git.pull() is None:
            logger.info("remote_git无更新,放弃本次更新部署")
        else:
            old_md5 = self.__calc_md5s(self.post_path)
            new_md5 = self.__calc_md5s(self.local_git_path)
            self.__del_operate(set(old_md5.values()).difference(set(new_md5.values())))
            old_md5 = self.__calc_md5s(self.post_path)
            file_to_push_list = list()
            for new in set(new_md5.keys()).difference(set(old_md5.keys())):
                with open(self.local_git_path / new_md5[new], "r", encoding="utf-8") as file:
                    new_data = file.read()
                md_file = self.markdown_file_class(filename=new_md5[new], post_path=self.post_path, data=new_data, front_matters=self.front_matters, **self.extends)
                if md_file.check() is False:
                    continue
                if md_file.upgrade() is False:
                    continue
                file_to_push_list.append((md_file.filename, new_md5[new]))
            threading.Thread(target=self.__deploy, args=()).start()
            self.__cp_file(files_to_cp=file_to_push_list)
            add_files = {x[0] for x in file_to_push_list}
            del_files = {x[1] for x in file_to_push_list}
            if git.push(add_files | del_files) is None:
                logger.info("git无文件更新，舍弃本次push")

    def __filename_format(self, file_name: str):
        """
        格式化文件名
        """
        return re.sub(r"\.(md|markdown)$", "", file_name).split(" ")

    # 通过网络接口上传文件的同步，同步到git
    def __upload_schedul(self, file_name: str, data: str):
        md_file = self.markdown_file_class(filename=file_name, post_path=self.post_path, data=data, front_matters=self.front_matters, **self.extends)
        if md_file.check() is False:
            return False
        if md_file.upgrade() is False:
            return False
        threading.Thread(target=self.__deploy, args=()).start()
        file_name = "_".join(self.__filename_format(file_name)) + ".md"
        git = Git(local_path=self.local_git_path, remote_git=self.remote_git)
        git.pull()
        post_file_md5 = self.__calc_md5(self.post_path / file_name)
        git_file_md5 = None
        if (self.local_git_path / file_name).exists():
            logger.info("文件\"{}\"存在，开始检查是否版本相同".format(file_name))
            git_file_md5 = self.__calc_md5(self.local_git_path / file_name)
        if git_file_md5 and git_file_md5 == post_file_md5:
            logger.info("本次通过网络接口上传的文件已经存在且版本相同，不需要更新")
            git.push([file_name, ])
            return
        logger.info("开始复制文件\"{}\"到git_path".format(file_name))
        self.__cp_file_once([file_name, ])
        if git.push([file_name, ]) is None:
            logger.info("git无文件更新，舍弃本次push")
        else:
            logger.info("文件\"{}\"更新到github".format(file_name))
        return True

    # 开始执行任务
    def schedul_start(self):
        try:
            self.__schedul()
        except Exception as error:
            logger.error("定时调度任务出现问题: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
        finally:
            threading.Timer(self.timer, self.schedul_start).start()

    def webhook(self):
        try:
            logger.info("执行单次调度")
            self.__schedul()
        except Exception as error:
            logger.error("单次调度任务出现问题: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))

    def upload_schedul(self, file_name: str, data: str):
        try:
            return self.__upload_schedul(file_name=file_name, data=data)
        except Exception as error:
            logger.error("网络接口上传文件同步到git时出现问题: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
