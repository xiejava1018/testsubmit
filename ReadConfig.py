# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""

import configparser
import os

class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            root_dir = os.path.abspath(os.curdir)
            configpath = os.path.join(root_dir, "config.ini")
            print(configpath)
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def get_configvalue(self,option,item):
        values=None
        if self.cf.has_option(option,item):
            values=self.cf.get(option,item)
        return values


if __name__ == '__main__':
    test = ReadConfig()
    t = test.get_configvalue("delay-time",'workdelay')
    print(t)
