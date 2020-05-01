import os
import pathlib
import logging
import traceback
import time

logger = logging.getLogger('custom')
system_logger = logging.getLogger("system_hexo")


class Git:
    def __init__(self, local_path: pathlib.Path, **kwargs):
        self.local_path = local_path
        self.__message = ""

    def pull(self):
        """
        pull数据库
        """
        try:
            os.chdir(self.local_path)
            result = os.popen("git pull")
            result = result.buffer.read().decode("utf-8")
            system_logger.info(result)
            if "Already up to date." in result:
                logger.info("Already up to date.")
                return None
            return True
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
            os.chdir(self.local_path)
            if self.__add(filenames=files_to_push):
                if self.__commit() is None:
                    return None
                result = os.popen("git push")
                result = result.buffer.read().decode("utf-8")
                system_logger.info(result)
                return True
            return False
        except Exception as error:
            logger.error("push出现错误: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False

    def __commit(self):
        try:
            result = os.popen("git commit -m \"{}\"".format(self.__message))
            result = result.buffer.read().decode("utf-8")
            system_logger.info(result)
            if "nothing to commit, working tree clean" in result:
                logger.info("nothing to commit, working tree clean")
                return None
            return True
        except Exception as error:
            logger.error("commit出现错误: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False


    def __add(self, filenames):
        """
        添加文件到缓冲区
        """
        try:
            for f in filenames:
                os.system("git add \"{}\"".format(f))
                self.__message += "{} ".format(f)
            return True
        except Exception as error:
            logger.error("添加缓冲区出现错误: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False
