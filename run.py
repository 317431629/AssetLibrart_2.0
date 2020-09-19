# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import sys
PYTHON_PATH = "//10.168.30.2/LocalShare/py27/Lib/site-packages"
TOOL_PATH = "//10.168.30.2/LocalShare/library"
sys.path.append(PYTHON_PATH)
sys.path.append(TOOL_PATH)

from Core import library

tool = library.LibraryTool()
tool.show()