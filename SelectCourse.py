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
class SelectCourseService(object):

    utiltools = None
    def __init__(self):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS WS_COURSE
               (SPEC_NAME       VARCHAR(20)   NOT NULL,
                LEVEL_NAME      VARCHAR(20)   NOT NULL,
                COUSE_TERM      VARCHAR(20)   NOT NULL,
                COUSE_NO        VARCHAR(20)   NOT NULL,
                COUSE_NAME      VARCHAR(50)   NOT NULL,
                COUSE_TYPE      VARCHAR(50)   NOT NULL,
                COUSE_CREDIT    NUMBER (2)    NOT NULL,
                COUSE_TESTTYPE  VARCHAR(10)   NOT NULL,
                COUSE_ID        VARCHAR(20)   NOT NULL,
                COUSE_RECOMMEND NUMBER(1)     default 0);''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    # 初始化数据（从excel里读入初始化数据）
    def initdata(self,filepath=None):
        self.init_procbar()
        # 从Excel里读入数据
        if filepath:
            datapath = filepath
        else:
            root_dir = os.path.abspath(os.curdir)
            datapath = os.path.join(root_dir, "推荐选课.xlsx")
        try:
            delectSQL = 'delete from WS_COURSE'
            book = xlrd.open_workbook(datapath)
            conn = sqlite3.connect(dbname)
            conn.execute(delectSQL)
            conn.commit()
            i=0
            maximum=len(book.sheets())
            self.show_dowork_proc(maximum,i)
            self.log('正在初始化推荐选课数据...')
            self.set_status('正在初始化推荐选课数据...')
            for sheet in book.sheets():
                spacename=sheet.name
                print(spacename)
                i = i + 1
                self.show_dowork_proc(maximum, i)
                if '科目代码' == spacename:
                    break
                spacename_str=spacename.split('-')
                spacename=spacename_str[0]
                levelname=spacename_str[1]
                nrows = sheet.nrows
                for row in range(nrows):
                    row_values = sheet.row_values(row)
                    if row == 1:
                        courseid_index = row_values.index('新科目代码')
                        coursename_index = row_values.index('课程名')
                        courseno_index = 1
                        coursecredit_index = row_values.index('学分')
                        coursectesttype_index=row_values.index('考试形式')
                        courserecomm_index = row_values.index('推荐选课')
                    if row>1:
                        print(row_values)
                        if '学分合计'==row_values[0]:
                            break
                        if len(row_values[0])>0:
                            courseterm=row_values[0][1:2]
                        courseno=str(int(row_values[courseno_index]))
                        coursename=(row_values[coursename_index])
                        if len(row_values[3])>0:
                            coursetype=row_values[3]
                        elif len(row_values[4])>0:
                            coursetype=row_values[4]
                        coursecredit=str(int(row_values[coursecredit_index]))
                        coursetesttype=row_values[coursectesttype_index]
                        courserecommend='0'
                        if '是'==row_values[courserecomm_index]:
                            courserecommend='1'
                        courseid = str(int(row_values[courseid_index]))
                        insertSQL='insert into WS_COURSE(SPEC_NAME,LEVEL_NAME,COUSE_TERM,COUSE_NO,COUSE_NAME,COUSE_TYPE,COUSE_CREDIT,COUSE_TESTTYPE,COUSE_ID,COUSE_RECOMMEND) ' \
                                  'values (\''+spacename+'\',\''+levelname+'\',\''+courseterm+'\',\''+courseno+'\',\''+coursename+'\',\''+coursetype+'\',\''+coursecredit+'\'' \
                                  ',\''+coursetesttype+'\',\''+courseid+'\',\''+courserecommend+'\')'
                        #self.log(insertSQL)
                        conn.execute(insertSQL)
                        conn.commit()
            conn.close()
            self.init_procbar()
            self.log('初始化推荐选课数据成功！')
            self.set_status('初始化推荐选课数据成功！')
        except:
            self.init_procbar()
            self.log('初始化推荐选课数据失败，请检查导入的文件格式！')
            self.set_status('初始化数据失败！')
            exit()

    # 判断是否是推荐课程
    def isRecommedCourse(self,spacename,levelname,courseterm,courseid):
        isRecommed=False
        conn = sqlite3.connect(dbname)
        selectSQL = 'select * from WS_COURSE where SPEC_NAME=\'' + spacename+'\' and LEVEL_NAME=\''+levelname+'\' and COUSE_TERM=\''+str(courseterm)+'\' and COUSE_ID=\''+str(courseid)+'\' and COUSE_RECOMMEND=1'
        cursor = conn.execute(selectSQL)
        print(selectSQL)
        if cursor.fetchone():
            isRecommed=True
        conn.close
        return isRecommed


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
    wsDBconn=SelectCourseService()
    wsDBconn.initdata()