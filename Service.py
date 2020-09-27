# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import requests
import json
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='testsubmit.log', level=logging.INFO, format=LOG_FORMAT)

class Service(object):
    papernum=0  #试卷数
    havesub_papernum=0 #已经提交的试卷数
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
            logging.info(response.text)
            logininfo=json.loads(response.text)
            if logininfo is not None:
                if logininfo['code']==100:
                    response=self.session.get(self.logined_url,headers=self.headers)
                    if response.status_code==200:
                        logging.info(str(login_name)+"登录成功！")
                        self.inserttolog('用户'+str(login_name)+"登录成功！")
                        return logininfo
                else:
                    self.inserttolog('用户' + str(login_name) + "登录失败！")


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
            logging.info(response.text)
            self.inserttolog('获取学生选课信息成功！')
            #print(response.text)
            eleactivedata=json.loads(response.text)
            if eleactivedata is not None:
                courselist=eleactivedata['pager']['datas']
                for course in courselist:
                    semeId=course['semeId']
                    courseId = course['courseId']
                    self.getstudentcursework(semeId=semeId,courseId=courseId)


    def getstudentcursework(self,semeId,courseId):
        #作业列表URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_list'
        post_data={
            'semeId':semeId,
            'courseId':courseId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            logging.info(response.text)
            paperdata=json.loads(response.text)
            if paperdata is not None:
                self.papernum=len(paperdata)
                self.show_singstudent_proc(maximum=self.papernum,value=self.havesub_papernum)
                self.inserttolog('获取学生试卷信息成功！共'+str(self.papernum)+'套试卷')
                for paper in paperdata:
                    self.getstudentpaper(paper['paperId'])
                    self.havesub_papernum+=1
                    self.inserttolog('自动完成第' + str(self.havesub_papernum) + '套试卷')
                    self.show_singstudent_proc(maximum=self.papernum, value=self.havesub_papernum)



    def getstudentpaper(self,paperId):
        #试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/paper'
        paperId=998
        post_data={
            'paperId':paperId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            paperinfo=json.loads(response.text)
            print(len(paperinfo))
            for queitem in paperinfo:
                queitem['quelib']['okFlag']=queitem['quelib']['ok1']
                #print(json.dumps(queitem,ensure_ascii=False))
            subpaper=json.dumps(paperinfo,ensure_ascii=False)
            self.submitpaper(subpaper)

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
    def submitpaper(self,subpaper):
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/submit_work?paperId=998&workId=1103'
        post_data={
            'sub':subpaper
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print('submit paper---'+response.text)
            self.inserttolog('自动提交试卷：' + response.text)

    # 显示单个学生的测试进度
    def show_singstudent_proc(self,maximum,value):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.show_procbar_process(maximum,value)

    def inserttolog(self,str):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.insertToLog(str)


if __name__=='__main__':
    service=Service()
    service.login(login_name='202020121200',login_psw='1qaz2wsx')
    service.geteleactive(semeId='40',studentNo='202020121200')