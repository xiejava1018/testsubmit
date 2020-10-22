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
import logging

dbname='wsdb.db'
class SelectWorkService(object):
    def __init__(self):
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
    def initdata(self):
        # 从Excel里读入数据
        root_dir = os.path.abspath(os.curdir)
        datapath = os.path.join(root_dir, "dowork.xlsx")
        book = xlrd.open_workbook(datapath)
        sheet1 = book.sheets()[0]
        nrows = sheet1.nrows
        conn = sqlite3.connect(dbname)
        delectSQL='delete from DOWORK'
        conn.execute(delectSQL)
        conn.commit()
        for row in range(nrows):
            row_values = sheet1.row_values(row)
            if row>0:
                std_no = row_values[1]
                std_dowork = row_values[2]
                insertSQL='insert into DOWORK(STU_NO,STU_DOWORK) values (\''+std_no+'\',\''+std_dowork+'\')'
                print(insertSQL)
                conn.execute(insertSQL)
                conn.commit()
        conn.close()

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

if __name__=='__main__':
    wsDBconn=SelectWorkService()
    wsDBconn.getdoworkbystuno('202020121200')