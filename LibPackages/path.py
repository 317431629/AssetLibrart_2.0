# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import liberConfig


class Path(object):
    def __init__(self, path):
        self.path = path

    def isExist(self):
        """
        :return: bool
        """
        return os.path.exists(self.path)

    def isFolder(self):
        """
        :return: bool
        """
        return os.path.isdir(self.path)

    def isFile(self):
        """
        :return: bool
        """
        return os.path.isfile(self.path)

    def create(self):
        """
        :return: None
        """
        if os.path.isdir(self.path):
            return
        os.makedirs(self.path)

    def remove(self):
        """
        :return: None
        """
        if self.isFolder():
            try:
                shutil.rmtree(self.path)
            except:
                cmd = "rd /s /q \"%s\"" % self.path
                subprocess.Popen(cmd, shell=True)
        elif self.isFile():
            os.remove(self.path)

    def dirname(self):
        """
        :return: str
        """
        return os.path.dirname(self.path)

    def children(self):
        """
        :return: list
        """
        paths = list()
        if self.isFolder():
            all_children = os.listdir(self.path)
            for i in liberConfig.IGNORE_LIST:
                try:
                    all_children.remove(i)
                except:pass
            for each in all_children:
                paths.append("{0}/{1}".format(self.path, each).replace("\\", "/"))
        return paths

    def listdir(self):
        if self.isFolder():
            return os.listdir(self.path)
        return []

    def hasChildren(self):
        """
        :return:bool
        """
        if self.isFolder():
            return True if os.listdir(self.path) else False
        return False

    def rename(self, name):
        """
        :param name: str
        :return: bool
        """
        if self.isExist():
            os.rename(self.path, name)
            return True
        return False

    def basename(self):
        return os.path.basename(self.path)

    def join(self, name):
        path = os.path.abspath(os.path.join(self.path, name))
        path = path.replace("\\", "/")
        return path

    def isValid(self):
        if self.isFolder():
            if not self.hasChildren():
                return True
            else:
                children = self.listdir()
                if "thumbnail.png" in children and "info.json" in children:
                    return False
                if self.basename() in liberConfig.IGNORE_LIST:
                    return False
            return True
        return False

    def ext(self):
        return os.path.splitext(self.path)[-1]


if __name__ == "__main__":
    Path("D:/test/kakakakaak").remove()
