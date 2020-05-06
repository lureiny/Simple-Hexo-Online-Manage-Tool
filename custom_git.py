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

    def push(self, files_to_push):
        """
        推送更新
        """
        try:
            if files_to_push:
                self.__message = ", ".join(files_to_push)
                self.index.add(list(files_to_push))
                self.index.commit(self.__message)
                self.remote.push()
                logger.info("文件\"{}\"更新到远程仓库".format(self.__message))
                return True
            logger.info("本地git版本为最新版本")
        except Exception as error:
            logger.error("push出现错误: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False
