# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
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
class RecomCourseService(object):
    def __init__(self):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS WS_RECOMM_COURSE
               (COUSE_ID        VARCHAR(20)   NOT NULL,
                COUSE_NAME      VARCHAR(50)   NOT NULL,
                COUSE_RECOMMEND NUMBER(1)     default 0);''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    # 初始化数据（从excel里读入初始化数据）
    def initdata(self):
        # 从Excel里读入数据
        root_dir = os.path.abspath(os.curdir)
        datapath = os.path.join(root_dir, "推荐选课.xlsx")
        delectSQL = 'delete from WS_RECOMM_COURSE'
        book = xlrd.open_workbook(datapath)
        conn = sqlite3.connect(dbname)
        conn.execute(delectSQL)
        conn.commit()
        for sheet in book.sheets():
            spacename=sheet.name
            print(spacename)
            if '科目代码'==spacename:
                break
            nrows = sheet.nrows
            for row in range(nrows):
                row_values = sheet.row_values(row)
                if row==0:
                    levelname=row_values[0]
                if row==1:
                    courseid_index=row_values.index('新科目代码')
                    coursename_index=row_values.index('课程名')
                    courserecomm_index=row_values.index('推荐选课')
                if row>1:
                    print(row_values)
                    if '学分合计'==row_values[0]:
                        break
                    if len(row_values[0])>0:
                        courseterm=row_values[0]
                    courseno=str(int(row_values[1]))
                    coursename=(row_values[coursename_index])
                    if len(row_values[3])>0:
                        coursetype=row_values[3]
                    elif len(row_values[4])>0:
                        coursetype=row_values[4]
                    coursecredit=str(int(row_values[5]))
                    coursetesttype=row_values[6]
                    courserecommend='0'
                    if '是'==row_values[courserecomm_index]:
                        courserecommend='1'
                    courseid=str(int(row_values[courseid_index]))
                    insertSQL='insert into WS_RECOMM_COURSE(COUSE_ID,COUSE_NAME,COUSE_RECOMMEND) ' \
                              'values (\''+courseid+'\',\''+coursename+'\',\''+courserecommend+'\')'
                    print(insertSQL)
                    conn.execute(insertSQL)
                    conn.commit()
        conn.close()

    def checktable(self,tablename):
        ifexist=False
        conn = sqlite3.connect(dbname)
        selectSQL='SELECT count(*) FROM sqlite_master WHERE type = \'table\' AND name =\''+tablename+'\''
        cursor = conn.execute(selectSQL)
        data=cursor.fetchone()
        if data[0]>0:
            ifexist=True
        return ifexist

if __name__=='__main__':
    wsDBconn=RecomCourseService()
    wsDBconn.initdata()
    wsDBconn.checktable('WS_RECOMM_COURSE')