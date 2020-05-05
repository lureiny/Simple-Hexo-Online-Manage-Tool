import time
import re
from collections import defaultdict
import os, sys
import pathlib
import random
import logging
import traceback

logger = logging.getLogger('custom')
system_logger = logging.getLogger("system_hexo")

class Markdown_File:
    def __init__(self, **kwargs):
        """
        初始化实体信息
        """
        # front_matters表示文件中哪些词可以作为front_matter
        if  {'data', 'filename', 'front_matters', 'post_path'}.difference(set(kwargs.keys())):
            raise KeyError("缺少以下参数: '{}'".format(", ".join({'data', 'filename', 'front_matters', 'post_path'}.difference(set(kwargs.keys())))))
        self.filename = kwargs["filename"]
        # 用来解析成title
        self.filenames = self._filename_format()
        self.filename = "_".join(self.filenames) + ".md"
        self.new_file_data = kwargs["data"].replace("\r", "")
        self.post_path = kwargs["post_path"]
        self.front_matters = kwargs["front_matters"]
        self._updated = self._file_exist()
        self.front_matters_compile = re.compile(r"^([#]? *(?:{})) *".format("|".join(self.front_matters)))
        self.new_file_heads = dict()
        self.new_file_bodys = list()
        self.old_file_heads = dict()
        self.old_file_bodys = list()
        

    def check(self) -> bool:
        try:
            if self._updated:
                self.old_file_heads, self.old_file_bodys = self._parse_file(self._read_file(self.post_path / self.filename))
            else:
                self.old_file_heads = self._generate_front_matter()
            self.new_file_heads, self.new_file_bodys = self._parse_file(self.new_file_data)
            if self._updated and self.old_file_bodys == self.new_file_bodys and self.new_file_heads == self.old_file_heads:
                return None
            self._merge_head()
            return True
        except Exception as error:
            logger.error("检查未通过: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False

    def _file_exist(self):
        """
        判断操作是否为更新,True表示为更新
        """
        if self.filename in os.listdir(self.post_path):
            return True
        return False

    def upgrade(self):
        """
        更新文件方法
        """
        try:
            self._save_file()
            return True
        except Exception as error:
            logger.error("文件写入失败: {}".format(str(error)))
            exc_type, exc_value, exc_tb = sys.exc_info()
            format_tb_info = traceback.format_exception()
            logger.error("{} {}".format(format_tb_info[-2].replace("\n"), format_tb_info[-1].replace("\n")))
            return False

    def _parse_file(self, filedata: str) -> list:
        """
        获取文件Format-matter信息和body信息
        """
        filedatas = filedata.split("\n")
        while filedatas and filedatas[0] == "":
            filedatas.pop(0)
        if not filedatas:
            return list([dict({}), [""]])
        if filedatas[0] != "---":
            return list([dict({}), filedatas])
        else:
            heads = defaultdict(list)
            key = ""
            for head in filedatas[1:filedatas[1:].index("---")+1]:
                head = re.sub(r"^ *", "", head)
                matched = re.match(self.front_matters_compile, head)
                if matched:
                    key = re.sub(r"^ *", "", matched.group(1))
                    head = re.sub(r"^{}".format(key), "", head)
                    head = re.split(r"^.*?[:：] *", head)[1:]
                    if head[0]:
                        heads[key].append(head[0])
                elif head[0] == "-":
                    heads[key].append(head)
                    heads[key].append("")
            return list([heads, filedatas[filedatas[1:].index("---")+2:]])

    def _generate_front_matter(self):
        """
        生成基础front-matter信息
        """
        return {"date": [time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), ],
                "title": [" ".join(self.filenames), ]
            }

    def _read_file(self, path:pathlib.Path) -> str:
        """
        返回文件内容
        """
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
        return data.replace("\r", "")

    def _filename_format(self):
        """
        格式化文件名
        """
        return re.sub(r"\.(md|markdown)$", "", self.filename).split(" ")

    def _merge_head(self):
        """
        合并新旧文件head
        """
        if "date" in self.new_file_heads and "date" in self.old_file_heads:
            del self.new_file_heads["date"]
        for key in self.new_file_heads.keys():
            key = re.sub(r"^ *", "", key)
            if key[0] == "#" and re.sub(r"^# *", "", key) in self.old_file_heads:
                del self.old_file_heads[re.sub(r"^# *", "", key)]
            else:
                self.old_file_heads[key] = self.new_file_heads[key]
        self.new_file_heads = self.old_file_heads

    def _save_file(self):
        """
        存储文件
        """
        logger.info("开始写入文件: {}".format(self.filename))
        with open(self.post_path / self.filename, "w", encoding="utf-8") as file:
            file.write("---\n")
            for head in self.new_file_heads:
                file.write("{}: ".format(head))
                if len(self.new_file_heads[head]) > 1:
                    file.write("\n")
                    for subhead in self.new_file_heads[head]:
                        if subhead:
                            file.write("  {}\n".format(subhead))
                else:
                    file.write("".join(self.new_file_heads[head]))
                    file.write("\n")
            file.write("---\n")
            file.write("\n".join(self.new_file_bodys))


class Markdown_File_ButterFly(Markdown_File):
    def __init__(self, **kwargs):
        """
        初始化实体信息
        filename: str, post_path: pathlib.Path, data: str, front_matters: set, imgs_path: pathlib.Path, img_path: str
        """
        if  {'data', 'filename', 'front_matters', 'img_path', 'imgs_path', 'post_path'}.difference(set(kwargs.keys())):
            raise KeyError("缺少以下参数: '{}'".format(", ".join({'data', 'filename', 'front_matters', 'img_path', 'imgs_path', 'post_path'}.difference(set(kwargs.keys())))))
        super().__init__(**kwargs)
        self.imgs_path = kwargs["imgs_path"]
        self.img_path = kwargs["img_path"]

    def _random_get_img(self):
        """
        随机选择一张图片库中的图片
        """
        return random.choice(os.listdir(self.imgs_path))

    def _generate_front_matter(self):
        """
        生成基础front-matter信息
        """
        img = self._random_get_img()
        return {"date": [time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), ],
                "title": [" ".join(self.filenames), ],
                "top_img": ["{}/{}".format(self.img_path, img), ],
                "cover": ["{}/{}".format(self.img_path, img), ]
            }

