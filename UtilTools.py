# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='worksubmit.log', level=logging.INFO, format=LOG_FORMAT)
logging.basicConfig(filename='worksubmit_error.log', level=logging.ERROR, format=LOG_FORMAT)

class UtilTools(object):
    testSubmitGUI = None

    def init_procbar(self):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.init_proc()

    def show_procbar_proc(self, maximum, value):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.show_procbar_process(maximum, value)

    # 显示具体的进度信息
    def inserttolog(self, str):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.insertToLog(str)

    # 记日志
    def log(self, logstr, islog=False):
        self.inserttolog(logstr)
        if islog:
            logging.info(logstr)

    # 设置状态栏的状态信息
    def set_status_bar(self, str):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.set_status_bar(str)
        else:
            print(str)