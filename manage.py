import pathlib
import os, sys
import re
import time
from custom_git import Git
import threading

class Manage:
    def __init__(self, path: pathlib.Path):
        self.path = path

    def _all_file(self):
        return os.listdir(self.path)

    def _get_tile_date(self, data: str):
        data = data.split("\n")
        temp = dict({"title": "", "date": ""})
        if data[0] != "---":
            return temp
        for d in data[1:]:
            if d == "---":
                break
            if re.split(r":", d, 1)[0] == "title":
                temp["title"] = re.sub(r"^ *", "", re.split(r":", d, 1)[1])
            elif re.split(r":", d, 1)[0] == "date":
                temp["date"] = re.sub(r"^ *", "", re.split(r":", d, 1)[1])
        return temp

    def all_file_info(self):
        all_info = list()
        for f in self._all_file():
            if (self.path / f).is_file() and (self.path / f).suffix in ".md.markdown":
                with open(self.path / f, "r", encoding="utf-8") as file:
                    data = file.read()
                    t = self._get_tile_date(data)
                    all_info.append([f, t["title"], t["date"] if t["date"] else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(self.path / f))), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(self.path / f)))])
        return all_info

    def del_file(self, filename: str, local_git_path: pathlib.Path):
        git = Git(local_git_path)
        info = [True, "删除成功"]
        if git.pull() is False:
            info[0] = False
            info[1] = "Pull出现错误"
        if (local_git_path / filename).exists():
            git.files_to_del.add(filename)
            os.remove(local_git_path / filename)
        if (self.path / filename).exists():
            os.remove(self.path / filename)
        else:
            info[0] = False
            info[1] += "文件不存在，请刷新文件列表"
        threading.Thread(target=git.push).start()
        return info

