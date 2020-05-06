import sys
import pathlib
import logging
import traceback
import time
from git import Repo


logger = logging.getLogger('custom')
system_logger = logging.getLogger("system_hexo")


class Git:
    def __init__(self, local_path: pathlib.Path, **kwargs):
        self.local_path = local_path
        self.__message = ""
        self.repo = Repo(local_path)
        self.index = self.repo.index
        self.remote = self.repo.remote()
        self.files_to_del = set()
        self.files_to_add_or_modified = set()

    def pull(self):
        """
        pull数据库
        """
        try:
            self.remote.pull()
        except Exception as error:
            logger.error("pull出现错误：{}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False

    def push(self):
        """
        推送更新
        """
        try:
            if self.files_to_add_or_modified | self.files_to_del:
                if self.files_to_del:
                    self.__message += "删除文件：\n{}\n".format("\n".join(self.files_to_del))
                    self.index.remove(list(self.files_to_del))
                if self.files_to_add_or_modified:
                    self.__message += "新增或更新的文件：\n{}\n".format("\n".join(self.files_to_add_or_modified))
                    self.index.add(list(self.files_to_add_or_modified))    
                self.index.commit(self.__message)
                self.remote.push()
                logger.info("提交信息:{}\n".format(self.__message))
                return True
            logger.info("本地git版本为最新版本")
        except Exception as error:
            logger.error("push出现错误: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False
