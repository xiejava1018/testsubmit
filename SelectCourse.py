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
                COURSE_TERM      VARCHAR(20)   NOT NULL,
                COURSE_NO        VARCHAR(20)   NOT NULL,
                COURSE_NAME      VARCHAR(50)   NOT NULL,
                COURSE_TYPE      VARCHAR(10)   NOT NULL,
                COURSE_CREDIT    NUMBER (2)    NOT NULL,
                COURSE_TESTTYPE  VARCHAR(10)   NOT NULL,
                COURSE_ID        VARCHAR(20)   NOT NULL,
                COURSE_RECOMMEND NUMBER(1)     default 0);''')
        print("Table WS_COURSE created successfully")
        c.execute('''CREATE TABLE IF NOT EXISTS WS_TOSELECT_COURSE
               (COURSE_STU_NO        VARCHAR(20)   NOT NULL,
                COURSE_CENGCI        VARCHAR(20)   NOT NULL,
                COURSE_COURSED       VARCHAR(50)   NOT NULL,
                COURSE_COURSEID      VARCHAR(20)   NOT NULL,
                COURSE_EXAMSCOREPE   VARCHAR(20)   NOT NULL,
                COURSE_EXAMTYPE      VARCHAR(20)   NOT NULL,
                COURSE_ID            VARCHAR(20)   NOT NULL,
                COURSE_LEARNHOUR     VARCHAR(20)   NOT NULL,
                COURSE_LEARNSCORE    VARCHAR(20)   NOT NULL,
                COURSE_MAINFLAG      VARCHAR(20)   NOT NULL,
                COURSE_PLANID        VARCHAR(20)   NOT NULL,
                COURSE_RECOMFLAG     VARCHAR(20)   NOT NULL,
                COURSE_SEMENUM       VARCHAR(20)   NOT NULL,
                COURSE_SPEC          VARCHAR(20)   NOT NULL,
                COURSE_SPECID        VARCHAR(20)   NOT NULL,
                COURSE_TEACHTYPE     VARCHAR(10)   NOT NULL, 
                COURSE_TYPE          VARCHAR(10)   NOT NULL, 
                COURSE_WORKSCOREPE   VARCHAR(20)   NOT NULL);''')
        print("Table WS_TOSELECT_COURSE created successfully")
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
                if len(spacename_str)>=2:
                    spacename=spacename_str[0]
                    levelname=spacename_str[1]
                    nrows = sheet.nrows
                    indexrow_values = sheet.row_values(1)
                    if '新科目代码' in indexrow_values and '课程名' in indexrow_values and '学分' in indexrow_values and '考试形式' in indexrow_values and '推荐选课' in indexrow_values :
                        courseid_index = indexrow_values.index('新科目代码')
                        coursename_index = indexrow_values.index('课程名')
                        courseno_index = 1
                        coursecredit_index = indexrow_values.index('学分')
                        coursectesttype_index=indexrow_values.index('考试形式')
                        courserecomm_index = indexrow_values.index('推荐选课')
                        for row in range(nrows):
                            row_values = sheet.row_values(row)
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
                                insertSQL='insert into WS_COURSE(SPEC_NAME,LEVEL_NAME,COURSE_TERM,COURSE_NO,COURSE_NAME,COURSE_TYPE,COURSE_CREDIT,COURSE_TESTTYPE,COURSE_ID,COURSE_RECOMMEND) ' \
                                          'values (\''+spacename+'\',\''+levelname+'\',\''+courseterm+'\',\''+courseno+'\',\''+coursename+'\',\''+coursetype+'\',\''+coursecredit+'\'' \
                                          ',\''+coursetesttype+'\',\''+courseid+'\',\''+courserecommend+'\')'
                                #self.log(insertSQL)
                                conn.execute(insertSQL)
                                conn.commit()
                    else:
                        conn.close()
                        self.log('初始化推荐选课数据失败，无法获取课程信息，请检查选课文件格式！当前sheet页'+sheet.name)
                        self.set_status('初始化数据失败！')
                        return
                else:
                    conn.close()
                    self.log('初始化推荐选课数据失败，无法获取专业和层次信息，请检查文件格式！当前sheet页'+sheet.name+'sheet页名称应为 专业-层次 ')
                    self.set_status('初始化数据失败！')
                    return
            conn.close()
            self.init_procbar()
            self.log('初始化推荐选课数据成功！')
            self.set_status('初始化推荐选课数据成功！')
        except:
            self.init_procbar()
            self.log('初始化推荐选课数据失败，请重新运行该程序！')
            self.set_status('初始化数据失败！')
            exit()

    def get_recommend_courselist(self,stu_no,course_type=None):
        # course_type=0 必修，course_type=1 选修
        conn=sqlite3.connect(dbname)
        if course_type!=None:
            selectSQL = 'select a.* from WS_TOSELECT_COURSE a,WS_COURSE b where b.SPEC_NAME=a.COURSE_SPEC and b.LEVEL_NAME=a.COURSE_CENGCI ' \
                        'and b.COURSE_TERM=a.COURSE_SEMENUM and b.COURSE_ID=a.COURSE_COURSEID and b.COURSE_RECOMMEND=1 and a.COURSE_STU_NO=\''+str(stu_no)+'\' and a.COURSE_TYPE=\''+str(course_type)+'\' order by a.COURSE_SEMENUM desc,a.COURSE_TYPE '
            print(selectSQL)
            cursor = conn.execute(selectSQL)
        else:
            selectSQL='''select a.* from WS_TOSELECT_COURSE a,WS_COURSE b where b.SPEC_NAME=a.COURSE_SPEC and b.LEVEL_NAME=a.COURSE_CENGCI and b.COURSE_TERM=a.COURSE_SEMENUM
                                                       and b.COURSE_ID=a.COURSE_COURSEID and b.COURSE_RECOMMEND=1 and a.COURSE_STU_NO=? order by a.COURSE_SEMENUM desc,a.COURSE_TYPE,a.COURSE_LEARNSCORE desc '''
            cursor = conn.execute(selectSQL,tuple({stu_no,}))
        recommend_course_list =[]
        for course_row in cursor.fetchall():
            course={'cengci': str(course_row[1]),
                    'courseD': str(course_row[2]),
                    'courseId':str(course_row[3]),
                    'examScorePe':str(course_row[4]),
                    'examtype':str(course_row[5]),
                    'id': str(course_row[6]),
                    'learnHour': str(course_row[7]),
                    'learnScore':str(course_row[8]),
                    'mainFlag':str(course_row[9]),
                    'planId':str(course_row[10]),
                    'recomFlag':str(course_row[11]),
                    'semenum':str(course_row[12]),
                    'spec':str(course_row[13]),
                    'specId':str(course_row[14]),
                    'teachType':str(course_row[15]),
                    'type':str(course_row[16]),
                    'workScorePe':str(course_row[17])}
            recommend_course_list.append(course)
        conn.close()
        return recommend_course_list

    # 根据学生学号插入学生选课信息
    def insert_tobeslectcourselist(self,stu_no,tobeselectcourses):
        for selectcourse in tobeselectcourses:
            self.insert_selctcourse(stu_no,selectcourse)

    # 插入选课数据到选课表
    def insert_selctcourse(self,stu_no,selectcourse):
        conn = sqlite3.connect(dbname)
        '''{'cengci': '高起专', 'courseD': '生理学Z', 'courseId': 63, 'examScorePe': 60, 'examtype': 0, 'id': 46463,
         'learnHour': 72, 'learnScore': 4, 'mainFlag': 0, 'planId': 755, 'recomFlag': 0, 'semenum': 2, 'spec': '中药学',
         'specId': 2, 'teachType': 1, 'type': 1, 'workScorePe': 40}'''
        recomflag='0'
        if 'recomFlag' in selectcourse:
            recomflag=selectcourse['recomFlag']
        spec=''
        if 'spec' in selectcourse:
            spec=selectcourse['spec']
        table='WS_TOSELECT_COURSE'
        data = {
            'COURSE_STU_NO': stu_no,
            'COURSE_CENGCI': selectcourse['cengci'],
            'COURSE_COURSED': selectcourse['courseD'],
            'COURSE_COURSEID': selectcourse['courseId'],
            'COURSE_EXAMSCOREPE': selectcourse['examScorePe'],
            'COURSE_EXAMTYPE': selectcourse['examtype'],
            'COURSE_ID': selectcourse['id'],
            'COURSE_LEARNHOUR': selectcourse['learnHour'],
            'COURSE_LEARNSCORE': selectcourse['learnScore'],
            'COURSE_MAINFLAG': selectcourse['mainFlag'],
            'COURSE_PLANID': selectcourse['planId'],
            'COURSE_RECOMFLAG': recomflag,
            'COURSE_SEMENUM': selectcourse['semenum'],
            'COURSE_SPEC': spec,
            'COURSE_SPECID': selectcourse['specId'],
            'COURSE_TEACHTYPE': selectcourse['teachType'],
            'COURSE_TYPE': selectcourse['type'],
            'COURSE_WORKSCOREPE': selectcourse['workScorePe'],
        }
        keys = ','.join(data.keys())
        values = ','.join(['?'] * len(data))
        #keys=tuple(data.keys())
        #values =tuple(data.values())
        insertSQL='INSERT INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        print(insertSQL)
        print(tuple(data.values()))
        conn.execute(insertSQL,tuple(data.values()))
        conn.commit()
        conn.close()

    # 删除学生选课记录
    def delete_selctcourse(self,stu_no):
        conn = sqlite3.connect(dbname)
        deleteSQL = 'delete from WS_TOSELECT_COURSE where COURSE_STU_NO=?'
        conn.execute(deleteSQL, tuple({stu_no,}))
        conn.commit()
        conn.close()

    # 判断是否是推荐课程
    def isRecommedCourse(self,spacename,levelname,courseterm,courseid):
        isRecommed=False
        conn = sqlite3.connect(dbname)
        selectSQL = 'select * from WS_COURSE where SPEC_NAME=\'' + spacename+'\' and LEVEL_NAME=\''+levelname+'\' and COURSE_TERM=\''+str(courseterm)+'\' and COURSE_ID=\''+str(courseid)+'\' and COURSE_RECOMMEND=1'
        cursor = conn.execute(selectSQL)
        print(selectSQL)
        if cursor.fetchone():
            isRecommed=True
        conn.close
        return isRecommed

    # 判断是否有初始化数据
    def ishaveinitdata(self):
        havedata=False
        conn = sqlite3.connect(dbname)
        selectSQL = 'select * from WS_COURSE'
        cursor = conn.execute(selectSQL)
        if cursor.fetchone():
            havedata=True
        conn.close
        return havedata


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
    wsDBconn.get_recommend_course('201820112006')
