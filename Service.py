# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import time
import requests
import json
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='worksubmit.log', level=logging.INFO, format=LOG_FORMAT)

delaytime1=1 #等待时间
delaytime2=2 #等待时间

class Service(object):
    #papernum=0  #试卷数
    #havesub_papernum=0 #已经提交的试卷数
    testSubmitGUI=None
    def __init__(self):
        self.headers={
            'Referer':'https://jxjyxb.bucm.edu.cn/stu.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Host':'jxjyxb.bucm.edu.cn'
        }
        self.login_url='https://jxjyxb.bucm.edu.cn/stu.html#/login'
        self.post_url='https://jxjyxb.bucm.edu.cn/api/v1/student/main/login'
        self.logined_url='https://jxjyxb.bucm.edu.cn/stu.html#/xuexi/benxueqi'
        self.session=requests.Session()

    def login(self,login_name,login_psw):
        post_data={
            'student.studentNo':login_name,
            'student.pwd':login_psw
        }
        response=self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.status_code==200:
            userlogininfo=response.text
            print(userlogininfo)
            #logging.info(response.text)
            logininfo=json.loads(response.text)
            if logininfo is not None:
                if logininfo['code']==100:
                    # 学生名字
                    student_name=logininfo['stu']['name']
                    response=self.session.get(self.logined_url,headers=self.headers)
                    if response.status_code==200:
                        logstr='用户'+str(login_name)+'登录成功,学生姓名：'+student_name
                        self.log(logstr)
                        return logininfo
                else:
                    self.log('用户' + str(login_name) + "登录失败！")


    #获取学员选课信息
    def geteleactive(self,semeId,studentNo):
        #选课信息URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/eleactive/list'
        post_data={
            'page': '1',
            'pageSize': '100',
            'eleactive.semeId': semeId,
            'eleactive.studentNo': studentNo
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            #logging.info(response.text)
            self.log('获取学生选课信息成功！')
            #print(response.text)
            eleactivedata=json.loads(response.text)
            if eleactivedata is not None:
                courselist=eleactivedata['pager']['datas']
                for course in courselist:
                    semeId=course['semeId']
                    courseId = course['courseId']
                    courseName = course['courseD']
                    self.log('获取学生'+str(studentNo)+'选课'+courseName+'成功！')
                    courseplanid =''
                    if 'coursePlanId' in course:
                        courseplanid=course['coursePlanId']
                    if self.getstudentlearninfo(courseplanid):
                        self.log('获取学生'+str(studentNo)+'选课'+courseName+'学习计划'+str(courseplanid)+'成功')
                        self.getstudentcursework(semeId=semeId,courseId=courseId,courseName=courseName)
                    else:
                        self.log('获取学生' + str(studentNo) + '选课' + courseName + '学习计划' + str(courseplanid) + '失败')

    # 获取学生学习计划
    def getstudentlearninfo(self,coursePlanId):
        iflearn=False
        # 作业列表URL
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/courseplan/learninfo?coursePlanId='+str(coursePlanId)
        response = self.session.get(request_url,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            if response.text is not None and response.text!='':
                result_data = json.loads(response.text)
                if result_data is not None:
                    if result_data['code']==100:
                        iflearn=True
        return iflearn

    # 获取学生作业
    def getstudentcursework(self,semeId,courseId,courseName):
        #作业列表URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_list'
        post_data={
            'semeId':semeId,
            'courseId':courseId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            #logging.info(response.text)
            paperdata=json.loads(response.text)
            if paperdata is not None:
                papernum=len(paperdata)
                havesub_papernum=0
                self.show_singstudent_proc(maximum=papernum,value=havesub_papernum)
                self.log('获取学生'+courseName+'作业信息成功！共'+str(papernum)+'套作业')
                for paper in paperdata:
                    workId=paper['id']
                    paperId=paper['paperId']
                    paperName=paper['name']
                    havesub_papernum += 1
                    if 'courseWorkStu' in paper:
                        createTime=paper['courseWorkStu']['createTime']
                        print(createTime)
                        timeArray= time.localtime(createTime/1000)
                        workTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        self.log('第' + str(havesub_papernum) + '套作业-试卷编号：' + str(paperId) + '-' + paperName+'在'+workTime+'提交过！')
                        self.show_singstudent_proc(maximum=papernum, value=havesub_papernum)
                    else:
                        self.getstudentpaper(paperId,workId)
                        self.log('自动完成第' + str(havesub_papernum) + '套作业-试卷编号：'+str(paperId)+'-'+paperName)
                        self.show_singstudent_proc(maximum=papernum, value=havesub_papernum)
                    time.sleep(delaytime2)


    # 获取试卷
    def getstudentpaper(self,paperId,workId):
        #试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/paper'
        paperId=paperId
        post_data={
            'paperId':paperId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            paperinfo=json.loads(response.text)
            self.log('试卷'+str(paperId)+'共'+str(len(paperinfo))+'道题目')
            for queitem in paperinfo:
                print(queitem['id'])
                if 'quelib' in queitem:
                    type=queitem['quelib']['type'] #
                    if type==0 or type==2:
                        queitem['quelib']['okFlag']=queitem['quelib']['ok1']
                    if type==1:
                        queitem['quelib']['okFlag'] = queitem['quelib']['ok1']
                        for num in range(2,10):
                            ok = 'ok'+str(num)
                            if ok in queitem['quelib']:
                                okflag='okFlag'+str(num)
                                queitem['quelib'][okflag] = queitem['quelib'][ok]
                    if type==3:
                        print('问答题')
                time.sleep(delaytime1)
            subpaper=json.dumps(paperinfo,ensure_ascii=False)
            print(subpaper)
            #提交试卷
            time.sleep(delaytime1)
            self.submitpaper(paperId,workId,subpaper)

    def getstudentworktest(self,paperId):
        # 试卷URL
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_test'
        post_data = {
            'paperId': paperId
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print('test---'+response.text)

    # 提交试卷
    def submitpaper(self,paperId,workId,subpaper):
        # 提交试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/submit_work?paperId='+str(paperId)+'&workId='+str(workId)
        post_data={
            'sub':subpaper
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print('submit paper---'+response.text)
            self.log('自动提交试卷：' + response.text)

    # 显示单个学生的测试进度
    def show_singstudent_proc(self,maximum,value):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.show_procbar_process(maximum,value)

    def inserttolog(self,str):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.insertToLog(str)

    def log(self,logstr):
        logging.info(logstr)
        self.inserttolog(logstr)


if __name__=='__main__':
    service=Service()
    service.login(login_name='202020121200',login_psw='1qaz2wsx')
    #service.geteleactive(semeId='40',studentNo='202020121200')
    #service.getstudentpaper(1002,1107)
    print(service.getstudentlearninfo('46903'))