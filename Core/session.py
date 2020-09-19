# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang
import requests


class LibrarySession(object):
    def __init__(self):
        self.session = requests.post()

    def request_data(self):
        pass
