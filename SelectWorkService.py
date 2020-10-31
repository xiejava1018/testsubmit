# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import sqlite3
import xlrd
import os

dbname='wsdb.db'
class SelectWorkService(object):
    utiltools = None
    def __init__(self):
        # 初始化服务
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS DOWORK
               (STU_NO       VARCHAR(20)   NOT NULL,
                STU_DOWORK       VARCHAR(50)    NOT NULL);''')
        print("Table created successfully")
        conn.commit()
        conn.close()


    # 初始化数据（从excel里读入初始化数据）
    def initdata(self,filepath=None):
        self.init_procbar()
        self.log('开始初始化自定义用户作业数据....')
        # 从Excel里读入数据
        if filepath:
            datapath=filepath
        else:
            root_dir = os.path.abspath(os.curdir)
            datapath = os.path.join(root_dir, "dowork.xlsx")
        try:
            book = xlrd.open_workbook(datapath)
            sheet1 = book.sheets()[0]
            nrows = sheet1.nrows
            conn = sqlite3.connect(dbname)
            delectSQL='delete from DOWORK'
            conn.execute(delectSQL)
            conn.commit()
            i = 0
            maximum = nrows
            for row in range(nrows):
                i = i + 1
                self.show_dowork_proc(maximum, i)
                row_values = sheet1.row_values(row)
                if row>0:
                    std_no = row_values[1]
                    std_dowork = row_values[2]
                    insertSQL='insert into DOWORK(STU_NO,STU_DOWORK) values (\''+std_no+'\',\''+std_dowork+'\')'
                    self.log(insertSQL)
                    conn.execute(insertSQL)
                    conn.commit()
            conn.close()
            self.init_procbar()
            self.log('初始化自定义用户作业数据成功！')
            self.set_status('初始化自定义用户作业数据成功！')
        except :
            self.init_procbar()
            self.log('初始化自定义用户作业数据失败，请检查导入的文件格式！')
            self.set_status('初始化数据失败！')
            exit()


    # 判断是否选做了该课程或作业
    def isdowork(self,stu_no,stu_dowork):
        do=False
        conn = sqlite3.connect(dbname)
        selectSQL = 'select STU_DOWORK from DOWORK where STU_NO=\'' + stu_no+'\' and STU_DOWORK=\''+stu_dowork+'\''
        cursor = conn.execute(selectSQL)
        if cursor.fetchone():
            do=True
        conn.close
        return do

    # 判断是否是选做作业
    def isselectdo(self,stu_no):
        selectdo=False
        conn = sqlite3.connect(dbname)
        selectSQL = 'select STU_DOWORK from DOWORK where STU_NO=' + stu_no
        cursor = conn.execute(selectSQL)
        if cursor.fetchone():
            selectdo=True
        conn.close
        return selectdo



    def init_procbar(self):
        if self.utiltools is not None:
            self.utiltools.init_procbar()


    def show_dowork_proc(self,maximum,value):
        if self.utiltools is not None:
            self.utiltools.show_procbar_proc(maximum,value)

    # 记日志
    def log(self,logstr,islog=False):
        if self.utiltools is not None:
            self.utiltools.log(logstr,islog)
        else:
            print(logstr)

    # 设置状态栏的状态信息
    def set_status(self,str):
        if self.utiltools is not None:
            self.utiltools.set_status_bar(str)
        else:
            print(str)

if __name__=='__main__':
    wsDBconn=SelectWorkService()
    wsDBconn.getdoworkbystuno('202020121200')